from staticfg import CFGBuilder
import ast 
import graphviz as gv
from enum import Enum
import os
import copy
import time
from tabulate import tabulate
# Initialization:
# 	Set everything to bottom
# 	Set the first line (incoming start of method) to top 

# We are looking at node N:
# 	Look at all of the incoming (incident) edges that have N as their destination
# 	Take the lub (the conversative approximation) of all of those
# 	That’s your incoming dataflow fact for X
# 	Look up in your set of rules, and apply the right rule to compute the outgoing info for X
# 	Change the the outgoing edge labels for edges that start in N and have another destination based on that

# Lists of sanitizers
normalizers = ['boxcox', 'yeojohnson']
normal_tests = ['shapiro', 'normaltest']

# List of sinks
sinks = ['ttest_ind', 'ttest_1samp', 'ttest_rel', 'pearsonr', 'f_oneway']

class LatticeElement(Enum):
    BOTTOM = "bottom"
    SAFE = "sanitized"
    TOP = "potentially unsanitized"
    
def join(elt1, elt2):
    if elt1 == LatticeElement.BOTTOM:
        return elt2
    elif elt2 == LatticeElement.BOTTOM:
        return elt1
    elif elt1 == elt2:
        # SS or TT
        return elt1
    else:
        # ST or TS
        return LatticeElement.TOP

# All edges will have a list of dataflow facts. 
# When we've gone through all edges and the facts haven't changed, we've reached a fixpoint and stop analysis.
facts_of_edges = {}

def get_fact_of_variable(facts, var):
    # if var is not in facts, return bottom because we haven't seen it yet
    if var in facts: return facts[var]
    else: return LatticeElement.BOTTOM

def get_facts_of_edge(edge):
    if edge in facts_of_edges: return facts_of_edges[edge]
    else: return {}

def merge(sigma1, sigma2):
    # Sigmas are dicts of facts for variables.
    # Put keys into a setlike object, and merge over that.
    all_vars = set(sigma1.keys()).union(set(sigma2.keys()))
    merged_dict = {}
    for var in all_vars:
        elt1 = get_fact_of_variable(sigma1, var)
        elt2 = get_fact_of_variable(sigma2, var)
        joined_elt = join(elt1, elt2)
        merged_dict[var] = joined_elt
    return merged_dict

# Incoming edges to each node will have a set of facts that we need to merge.
# First, we get the incoming facts for all links.
# Then, we merge all incoming facts and return the result.
def get_incoming_facts(node):
    # Get predecessor links
    pred_links = node.predecessors
    # Look up their facts to put in a list of dicts 
    pred_facts = []
    for link in pred_links:
        edge = (link.source.id, node.id)
        facts = get_facts_of_edge(edge)
        facts_copy = facts.copy()
        pred_facts.append(facts_copy)
    # Merge over all incoming facts
    if not pred_facts: # pred_facts is empty because this is the first node
        return {}
    else:
        incoming_facts = pred_facts[0]
    for i in range(1, len(pred_facts)):
        incoming_facts = merge(incoming_facts, pred_facts[i])
    return incoming_facts

def sink_update(call, facts, warnings):
    if isinstance(call, ast.Call): # e.g., results.append(...)
        if isinstance(call.func, ast.Attribute):
            if call.func.attr in sinks:
                # check func args in facts
                for arg in call.args:
                    if isinstance(arg, ast.Name):
                        if get_fact_of_variable(facts, arg.id) == LatticeElement.TOP:
                            warnings.add((call.func.attr, call.lineno, arg.id))
        for arg in call.args:
            sink_update(arg, facts, warnings)

def normal_update(call, facts):
    # Nuance: normalizer within a call that is not assigned will be flagged as a warning
    # The programmer may think that further usages of the data will be normal, but this is not the case
    if isinstance(call, ast.Call): # e.g., print(...)
        if isinstance(call.func, ast.Attribute):
            if call.func.attr in normal_tests:
                # update facts
                for arg in call.args:
                    if isinstance(arg, ast.Name):
                        facts[arg.id] = LatticeElement.SAFE

def do_dataflow_analysis(cfg):
    start_time = time.time()
    warnings_to_raise = set()
    fixpoint = False
    while not fixpoint:
        fixpoint = True # Until proven otherwise below
        for node in cfg:
            # Try to update edge facts
            facts_to_update = get_incoming_facts(node)
            for s in node.statements:
                if isinstance(s, ast.Assign):
                    for lhs in s.targets:
                        if isinstance(lhs, ast.Name): # x = 
                            if isinstance(s.value, ast.Name): # x = y
                                # Pass dataflow facts from y to x
                                facts_to_update[lhs.id] = get_fact_of_variable(facts_to_update, s.value.id)
                            elif isinstance(s.value, ast.Call): # x = func()
                                if isinstance(s.value.func, ast.Attribute): 
                                    # if this attribute is one of our normalizers, update fact of left target to be safe
                                    if (s.value.func.attr in normalizers):
                                        facts_to_update[lhs.id] = LatticeElement.SAFE
                                    elif (s.value.func.attr in normal_tests):
                                        # parameter is safe
                                        for arg in s.value.args:
                                            if isinstance(arg, ast.Name):
                                                facts_to_update[arg.id] = LatticeElement.SAFE
                                    elif (s.value.func.attr in sinks):
                                        # add to warnings if calling on non-normal data
                                        for arg in s.value.args:
                                            if isinstance(arg, ast.Name):
                                                if get_fact_of_variable(facts_to_update, arg.id) == LatticeElement.TOP:
                                                    warnings_to_raise.add((s.value.func.attr, s.lineno, arg.id))
                                    else: # x = some unknown thing
                                        facts_to_update[lhs.id] = LatticeElement.TOP
                            else: # x = some unknown thing
                                facts_to_update[lhs.id] = LatticeElement.TOP
                        elif isinstance(lhs, ast.Tuple): # x, y ... =
                            if isinstance(s.value, ast.Name): # x, y ... = z
                                for i in range(len(lhs.elts)):
                                    facts_to_update[lhs.elts[i].id] = get_fact_of_variable(facts_to_update, s.value.id)
                            elif isinstance(s.value, ast.Call): # x, y ... = func()
                                # func is either a Name (for simple calls) or an Attribute (for our library calls)
                                if isinstance(s.value.func, ast.Attribute):
                                    # if this attribute is one of our normalizers, update fact of left target to be safe
                                    if (s.value.func.attr in normalizers):
                                        facts_to_update[lhs.elts[0].id] = LatticeElement.SAFE
                                    elif (s.value.func.attr in normal_tests):
                                        # Argument is presumed safe (e.g., stats.shapiro(x) makes x assumed normal)
                                        for arg in s.value.args:
                                            if isinstance(arg, ast.Name):
                                                facts_to_update[arg.id] = LatticeElement.SAFE
                                    elif (s.value.func.attr in sinks):
                                        # We've reached a sink. Check if one of the parameters is TOP
                                        # If so, there exists a path where one of the parameters is not sanitized
                                        for arg in s.value.args:
                                            if isinstance(arg, ast.Name):
                                                if get_fact_of_variable(facts_to_update, arg.id) == LatticeElement.TOP:
                                                    # Raise alarm
                                                    warnings_to_raise.add((s.value.func.attr, s.lineno, arg.id))
                            else:
                                # x, y = some unknown thing
                                for i in range(len(lhs.elts)):
                                   facts_to_update[lhs.elts[i].id] = LatticeElement.TOP
                elif isinstance(s, ast.Expr):
                    if isinstance(s.value, ast.Call):
                        # Someone might be appending the result of a sink to a list
                        sink_update(s.value, facts_to_update, warnings_to_raise)
                        # or printing the result of a normal test
                        normal_update(s.value, facts_to_update)
            # Check to see if any of the edge facts from this node changed. if not, stop looping
            for edge in node.exits:
                facts_to_update_copy = copy.deepcopy(facts_to_update)
                old_facts = get_facts_of_edge((node.id, edge.target.id))
                if facts_to_update != old_facts:
                    # Update global edge facts
                    facts_of_edges[(node.id, edge.target.id)] = facts_to_update_copy
                    fixpoint = False
    end_time = time.time()
    return (warnings_to_raise, (end_time - start_time))

def raise_warnings(file_name, warnings_to_raise, time):
    # Sort warnings_to_raise by lineno for readability
    warnings_to_raise = list(warnings_to_raise)
    warnings_to_raise = sorted(warnings_to_raise, key=lambda x: x[1])
    with open(file_name, 'a') as file:
        time_string = str(time)
        if (time < 1):
            time_string = "< 1"
        file.write(f'Found {len(warnings_to_raise)} potential normality-related bug(s) in {time_string} seconds.\n')
        file.write(f"""The table below shows statistical tests which require normally-distributed data that 
may be called in your script without checking the data for normality. 
Consider checking the data for normality using a test like scipy.stats.shapiro before 
the line number given.\n""")
        headers = ["Statistical Test", "Line", "Potentially Non-Normal Data"]
        table_data = []
        for warning in warnings_to_raise:
            table_data.append([warning[0], warning[1], warning[2]])
        table = tabulate(table_data, headers=headers, tablefmt="grid")
        file.write(table + "\n")

