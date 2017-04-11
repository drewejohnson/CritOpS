"""

NRE6401 - Molten Salt Reactor
CritOps
A. Johnson

readinputs

Objective: Read the inputs, update global variables, and check for proper variable usage

Functions:
    check_inputs: make sure values in global_parameters are good for running
    read_param: Read the parameter file and update values in globalparams
    readMain: Main driver for reading and processing the input files

"""
import os.path

import critops.utils as utils
from critops import constants

iter_ints = ('iter_lim',)
iter_floats = ('eps_k', 'inf', 'tiny', "k_target")


def read_param(_pfile, **kwargs):
    """
    Read the parameter file and update values in globalparams
    :param _pfile: Parameter file
    :return: iter_vars: Dictionary of iteration variables and their starting, minima, and maximum values
    """

    iter_vars = {}

    utils.vprint('Reading from parameter file {}'.format(_pfile), **kwargs)
    with open(_pfile, 'r') as pobj:
        _line = pobj.readline()
        _count = 1
        _locStr = 'read_param() for parameter file {}  - line {}'

        while _line != "":
            _lSplit = _line.split()
            if _lSplit[0] == 'iter_var':
                if len(_lSplit) == 5:
                    iter_vars[_lSplit[1]] = [float(_v) for _v in _lSplit[2:]]
                else:
                    utils.error('Need starting, minimum, and maximum value for parameter {}'.format(_lSplit[1]),
                                _locStr.format(_pfile.name, _count), **kwargs)
            elif _lSplit[0] == 'var_char':
                if _lSplit[1] in constants.supVarChars:
                    kwargs['var_char'] = _lSplit[1]
                else:
                    utils.error('Variable character {} not supported at this moment.'.format(_lSplit[1]),
                                _locStr.format(_pfile.name, _count), **kwargs)
            elif _lSplit[0] in iter_floats:
                kwargs[_lSplit[0]] = float(_lSplit[1])
            elif _lSplit[0] in iter_ints:
                kwargs[_lSplit[0]] = int(_lSplit[1])
            elif _lSplit[0] == 'exe_str':
                kwargs['exe_str'] = _lSplit[1]
            _line = pobj.readline()
            _count += 1
    utils.vprint('  done', **kwargs)
    return iter_vars


def check_inputs(temp_lines: list, iter_vars: dict, **kwargs):
    """Run over the inputs and make sure things are good for operation"""
    utils.vprint('Checking run parameters', **kwargs)
    for _int in iter_ints:
        try:
            assert kwargs[_int] % 1 == 0
        except AssertionError:
            utils.error('Variable {} must be integer, not {}'.format(_int, kwargs[_int]),
                        'check_inputs()', **kwargs)
        try:
            assert kwargs[_int] > 0
        except AssertionError:
            utils.error('Variable {} must be positive, not {}'.format(_int, kwargs[_int]),
                        'check_inputs()', **kwargs)
    for _flt in iter_floats:
        try:
            assert kwargs[_flt] > 0
        except AssertionError:
            utils.error('Variable {} must be positive, not {}'.format(_flt, kwargs[_flt]),
                        'check_inputs()', **kwargs)

    if len(iter_vars) > 1:
        utils.error('Only one value can be modified as iter_var at this moment. Variables indicated:\n' +
                    "\n".join(iter_vars.keys()), "check_inputs()", **kwargs)
    elif len(iter_vars) == 0:
        utils.error('No iteration variable to update. Use the following syntax in input file:\n'
                    'iter_var <var> <start> <min> <max>', 'check_inputs()', **kwargs)

    l_count = 1
    _instance_count = 0
    for _line in temp_lines:
        if kwargs['var_char'] in _line:
            if _line.split(kwargs['var_char'])[1].split()[0] in iter_vars:
                _instance_count += 1
                utils.vprint('  {} at line {} in input file'.
                             format(_line.split(kwargs['var_char'])[1].split()[0], l_count), **kwargs)
        l_count += 1

    if _instance_count == 0:
        utils.error('No instances of iteration variables {} found in input file'.format(', '.join(iter_vars.keys())),
                    'check_inputs()', **kwargs)

    if not os.path.isfile(kwargs['exe_str']):
        utils.error('Execution file {} does not exist'.format(kwargs['exe_str']), 'check_inputs()', **kwargs)

    utils.vprint('  done', **kwargs)


def readmain(tmp_file, param_file, kwargs: dict):
    """Main driver for reading and processing input files.    
    :param tmp_file: Template input file
    :param param_file: Parameter file
    :param kwargs: Additional arguments
        - verbose (True) - status updates
        - output (None) - print to screen
        Plus additional iteration parameters
    :return List of valid template file lines and dictionary of interation variables
        Updates kwargs based on values in param_file
    """
    utils.check_defaults(kwargs)
    utils.vprint('Reading from input file {}'.format(tmp_file), **kwargs)
    with open(tmp_file, 'r') as file:
        tmp_lines = file.readlines()
    utils.vprint('  done', **kwargs)
    iter_vars = read_param(param_file, **kwargs)
    check_inputs(tmp_lines, iter_vars, **kwargs)

    return tmp_lines, iter_vars
