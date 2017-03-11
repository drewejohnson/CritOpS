"""

NRE6401 - Molten Salt Reactor
msr-refl-iter
A. Johnson

readinputs

Objective: Read the inputs, update global variables, and check for proper variable usage

Functions:
    check_inputs: make sure values in global_parameters are good for running
    read_param: Read the parameter file and update values in globalparams
    readMain: Main driver for reading and processing the input files

Classes:

"""
import globalparams as gp
import utils


def read_param(_pfile):
    """
    Read the parameter file and update values in globalparams
    :param _pfile: Parameter file
    :return: None
    """
    utils.vprint('Reading from parameter file {}'.format(_pfile.name))
    _rLine = _pfile.readline
    _line = _rLine()
    _count = 1
    _locStr = 'read_param() for parameter file {}  - line {}'

    while _line != "":
        _lSplit = _line.split()
        if _lSplit[0] == 'iter_var':
            if len(_lSplit) == 5:
                gp.iter_vars[_lSplit[1]] = [float(_v) for _v in _lSplit[2:]]
            else:
                utils.error('Need starting, minimum, and maximum value for parameter {}'.format(_lSplit[1]),
                            _locStr.format(_pfile.name, _count))
        elif _lSplit[0] == 'var_char':
            if _lSplit[1] in gp.supVarChars:
                gp.var_char = _lSplit[1]
            else:
                utils.error('Variable character {} not supported at this moment.'.format(_lSplit[1]),
                            _locStr.format(_pfile.name, _count))
        elif _lSplit[0] in gp.iter_floats:
            gp.__dict__[_lSplit[0]] = float(_lSplit[1])
        elif _lSplit[0] in gp.iter_ints:
            gp.__dict__[_lSplit[0]] = int(_lSplit[1])
        elif _lSplit[0] == 'exe_str':
            gp.exe_str = _lSplit[1]
        _line = _rLine()
        _count += 1
    utils.vprint('  done')


def check_inputs():
    """Run over the inputs and make sure things are good for operation"""
    utils.vprint('Checking run parameters')
    for _int in gp.iter_ints:
        try:
            assert gp.__dict__[_int] % 1 == 0
        except AssertionError:
            utils.error('Variable {} must be integer, not {}'.format(_int, gp.__dict__[_int]),
                        'check_inputs()')
        try:
            assert gp.__dict__[_int] > 0
        except AssertionError:
            utils.error('Variable {} must be positive, not {}'.format(_int, gp.__dict__[_int]),
                        'check_inputs()')
    for _flt in gp.iter_floats:
        try:
            assert gp.__dict__[_flt] > 0
        except AssertionError:
            utils.error('Variable {} must be positive, not {}'.format(_flt, gp.__dict__[_flt]),
                        'check_inputs()')

    if len(gp.iter_vars) > 1:
        utils.error('Only one value can be modified as iter_var at this moment. Variables indicated:\n' +
                    "\n".join(gp.iter_vars.keys()), "check_inputs()")
    elif len(gp.iter_vars) == 0:
        utils.error('No iteration variable to update. Use the following syntax in input file:\n'
                    'iter_var var start min max', 'check_inputs()')

    l_count = 1
    _instance_count = 0
    for _line in gp.template_file:
        if gp.var_char in _line:
            if _line.split(gp.var_char)[1].split()[0] in gp.iter_vars:
                _instance_count += 1
                utils.vprint('  {} at line {} in input file'.
                             format(_line.split(gp.var_char)[1].split()[0], l_count))
        l_count += 1

    if _instance_count == 0:
        utils.error('No instances of iteration variable {} found in input file {}'.format(gp.iter_vars.keys(),
                                                                                          gp.args.inp_file.name),
                    'check_inputs()')

    utils.vprint('  done')


def readmain():
    """Main driver for reading and processing input files"""
    utils.vprint('Reading from input file {}'.format(gp.args.inp_file.name))
    gp.template_file = gp.args.inp_file.readlines()
    utils.vprint('  done')
    gp.args.inp_file.close()
    read_param(gp.args.param_file)
    check_inputs()
