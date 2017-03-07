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

from utils import show_license

# Input parameters
parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('inp_file', type=argparse.FileType('r'), help='template SCALE input file')
parser.add_argument('param_file', type=argparse.FileType('r'),
                    help='file containing parameters for operation')
parser.add_argument('-v', '--verbose', help='reveal more of the mystery behind the operation',
                    action='store_true')
parser.add_argument('-l', '--license', help='show license information', type=show_license)
# todo: make the -l command work without input files
# todo: Add formattable execution statement i.e. -x "C:\SCALE-6.2.1\bin\scalerte {} > z{}.out"
args = None
supVarChars = ('$',)  # will add more later

# Iteration parameters
iter_vars = {}  # syntax: iter_vars['param'] =  [initial_value, minimum_value, maximium_value]
eps_k = 1E-6
k_guess = 1.0
inf = 1E30
tiny = 1E-16
iter_lim = 50
iter_ints = ('iter_lim',)
iter_floats = ('eps_k', 'inf', 'tiny', 'k_guess')
iter_vecs = {}
k_vec = []

# SCALE parameters
var_char = '$'
exe_str = r'C:\SCALE-6.2.1\bin\scalerte'
template_file = None
