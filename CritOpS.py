"""

NRE6401 - Molten Salt Reactor
msr-refl-iter
A. Johnson

refl_iter

Objective: Main file for reading the input, and driving control of the operation

Functions:

Classes:

"""
import globalparams as gp
from iterator import itermain
from readinputs import readmain

gp.args = gp.parser.parse_args()
if gp.args.output is None:
    print(gp.header)
else:
    with open(gp.args.output, 'w') as outobj:
        outobj.write(gp.header)

# Read the input files
readmain()

# Start the iteration
itermain()
