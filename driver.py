import subprocess
import os
from staticfg import CFGBuilder
import normal_flow
import ast

# Get all the paths
paths = []
for filename in os.listdir('evalscripts'):
    paths.append(os.path.join('evalscripts/', filename))

# Go through all these files and build the CFG, run dataflow analysis, and write out warnings
# We also want total number of bugs and total time taken
total_time = 0
total_bugs = 0
for path in paths:
    cfg = CFGBuilder().build_from_file('cfg', path)
    name = os.path.basename(path).split('.')[0]
    if os.path.exists(f'warnings/{name}.txt'):
        os.remove(f'warnings/{name}.txt')
    with open(path, 'r') as file:
        code = file.read()
    with open(f'warnings/{name}_ast.txt', 'w') as file:
        tree = ast.parse(code)
        ast_rep = ast.dump(tree, indent=4)
        file.write(ast_rep)
    warning_time = normal_flow.do_dataflow_analysis(cfg)
    total_time += warning_time[1]
    total_bugs += len(warning_time[0])
    normal_flow.raise_warnings(f'warnings/{name}.txt', warning_time[0], warning_time[1])

print(f'That took {str(total_time)} seconds.\n')
print(f'We found {total_bugs} bugs.')




