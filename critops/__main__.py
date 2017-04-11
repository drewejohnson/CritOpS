"""
   ______     _ __  ____       _____      _   _________       ________
  / ____/____(_) /_/ __ \____ / ___/     / | / / ____/ |     / /_  __/
 / /   / ___/ / __/ / / / __ \\__ \_____/  |/ / __/  | | /| / / / /
/ /___/ /  / / /_/ /_/ / /_/ /__/ /____/ /|  / /___  | |/ |/ / / /
\____/_/  /_/\__/\____/ .___/____/    /_/ |_/_____/  |__/|__/ /_/
                     /_/


                        CritOpS
A Critical Optimization Search tool for NEWT[1]
A. Johnson

Objective: Iteratively update a parameter in a template NEWT file in
order to obtain a critical system.

[1]: M. D. DeHart, and S. Bowman, "Reactor Physics Methods and Analysis
    Capabilities in SCALE," Nuclear Technology, Technical Paper
    vol. 174, no.2, pp. 196-213, 2011.
"""

import argparse
import os
import sys

from critops import utils
from critops.constants import header, default_params
from critops.iterator import itermain
from critops.outputs import output_landing
from critops.readinputs import readmain

# Input parameters
parser = argparse.ArgumentParser(description=header, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('inp_file', type=str, help='template SCALE input file')
parser.add_argument('param_file', type=str, help='file containing parameters for operation')
parser.add_argument('-v', '--verbose', help='reveal more of the mystery behind the operation', action='store_true')
parser.add_argument('-o', '--output', help="write status to output file", type=str)

if __name__ == '__main__':

    if int(sys.version_info[0]) < 3:
        raise SystemError('Need python 3 >')

    kwargs = {}
    for key in default_params:
        kwargs[key] = default_params[key]

    args = vars(parser.parse_args())
    kwargs['verbose'] = args.pop('verbose')
    kwargs['output'] = args.pop('output')

    if kwargs['output'] is None:
        print(header)
    else:
        with open(kwargs['output'], 'w') as outobj:
            outobj.write(header)

    # Update files to be absolute references
    for file in ('inp_file', 'param_file'):
        args[file] = os.path.join(os.getcwd(), args[file])
        if not os.path.exists(args[file]):
            utils.error('File {} does not exist'.format(args[file]), 'CritOps __main__', args)

    # Read the input files
    template, iter_vars = readmain(args['inp_file'], args['param_file'], kwargs)

    # Start the iteration
    iter_vecs, k_vec, conv_type = itermain(template, args['inp_file'], iter_vars, kwargs)

    # Output
    output_landing(iter_vecs, k_vec, conv_type, **kwargs)
