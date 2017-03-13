"""

NRE6401 - Molten Salt Reactor
msr-refl-iter
A. Johnson

globalparams

Objective: Contain the default parameters for operation, and be common place to refer to global variables

Functions:

Classes:

"""

import argparse

# Header
lineBreakLong = "*" * 70 + '\n'
pName = "CritOpS-NEWT"
asciiHeader = r"""
   ______     _ __  ____       _____      _   _________       ________
  / ____/____(_) /_/ __ \____ / ___/     / | / / ____/ |     / /_  __/
 / /   / ___/ / __/ / / / __ \\__ \_____/  |/ / __/  | | /| / / / /
/ /___/ /  / / /_/ /_/ / /_/ /__/ /____/ /|  / /___  | |/ |/ / / /
\____/_/  /_/\__/\____/ .___/____/    /_/ |_/_____/  |__/|__/ /_/
                     /_/
"""  # http://patorjk.com/software/taag/#p=display&f=Slant&t=CritOpS-NEWT

header = lineBreakLong + asciiHeader + pName.center(len(lineBreakLong)) + """
A Critical Optimization Search tool for NEWT[1]
A. Johnson

Objective: Iteratively update a parameter in a template NEWT file in
order to obtain a critical system.

[1]: M. D. DeHart, and S. Bowman, "Reactor Physics Methods and Analysis
\tCapabilities in SCALE," Nuclear Technology, Technical Paper
vol. 174, no.2, pp. 196-213, 2011.

""" + lineBreakLong

# Input parameters
parser = argparse.ArgumentParser(description=header, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('inp_file', type=argparse.FileType('r'), help='template SCALE input file')
parser.add_argument('param_file', type=argparse.FileType('r'),
                    help='file containing parameters for operation')
parser.add_argument('-v', '--verbose', help='reveal more of the mystery behind the operation',
                    action='store_true')
parser.add_argument('-o', '--output', help="write status to output file", type=str)
args = None
supVarChars = ('$',)  # will add more later

# Iteration parameters
iter_vars = {}  # syntax: iter_vars['param'] =  [initial_value, minimum_value, maximium_value]
eps_k = 1E-6
k_target = 1.0
inf = 1E30
tiny = 1E-16
iter_lim = 50
iter_ints = ('iter_lim',)
iter_floats = ('eps_k', 'inf', 'tiny', "k_target")
iter_vecs = {}
k_vec = []

# SCALE parameters
var_char = '$'
exe_str = r'C:\SCALE-6.2.1\bin\scalerte'
template_file = None

# Outputs
