"""

NRE6401 - Molten Salt Reactor

CritOpS

A. Johnson

Objective: Main file for controlling the iteration scheme

Functions:

    iter_main: Landing function that drives the iteration
    
    makefile: Write the new output file using the value from iteration _iter
    
    update_itervar: Simple function to update the iteration variables.    
    
    parse_scale_out_eig: Read through the SCALE output file specified by _ofile and return status and eigenvalue (if present)

"""
import subprocess

import critops.utils as utils


def makefile(_tfile: (list, tuple), _name: str, _iter: int, _varchar: str, _vars: dict):
    """
    Write the new output file using the value from iteration _iter
    
    :param _tfile: Template output file with variables to be replaced
    :param _name: Name of original file
    :param _iter: Iteration number
    :param _varchar: Variable character to update with new_val
    :param _vars: Dictionary with iteration variables as keys and their new values as keys
        i.e. {del_z: 10.21, del_r: 3.4}
    
    :return: Name of input file
    """
    _ofile = _name[:_name.rfind('.')] + "_" + str(_iter) + ".inp"

    with open(_ofile, 'w') as _outObj:
        for _line in _tfile:
            if _varchar not in _line:
                _outObj.write(_line)
            else:
                _var = _line[_line.index(_varchar):].split()[0][1:]
                # assumes that iteration variable will be followed by a space
                _outObj.write(_line.replace(_varchar + _var, "{:7.5f}".format(_vars[_var])))

    return _ofile


def update_itervar(iter_vars: dict, iter_vec: dict, kvec: (list, tuple), ktarg: float):
    """Simple function to update the iteration variables.
    Currently set up for a positive feedback on the variables.
    I.e. increasing each iteration variable will increase k
    
    :param iter_vars: Dictionary of iteration variables and their minima/maxima
    :param iter_vec: Dictionary of iteration variables and their values through the iteratio procedure
    :param kvec: Vector of eigenvalues
    :param ktarg: Target eigenvalue
    
    :return: status
        status = 0 if the updated value is inside the intended range
        status = 1 if the desired updated value is greater than the specified maximum of the parameter
        and the max value is used as the updated value
        status = -1 if the desired updated value is less than the specified maximum of the parameter
        and the minimum value is used as the updated value
    """

    # Assumes only one iteration variable for now
    _var = list(iter_vars.keys())[0]
    _delk = [ktarg - kv for kv in kvec]

    if len(kvec) <= 1:
        _des = iter_vec[_var][-1] * (ktarg / kvec[-1]) ** 2
    else:
        _des = iter_vec[_var][-1] - _delk[-1] * (iter_vec[_var][-2] - iter_vec[_var][-1]) / (_delk[-2] - _delk[-1])

    if _des > iter_vars[_var][2]:
        iter_vec[_var].append(iter_vars[_var][2])
        return 1
    elif _des < iter_vars[_var][1]:
        iter_vec[_var].append(iter_vars[_var][1])
        return -1
    else:
        iter_vec[_var].append(_des)
        return 0


def parse_scale_out_eig(_ofile: str, **kwargs):
    """
    Read through the SCALE output file specified by _ofile and return status and eigenvalue (if present)
    
    :param _ofile: SCALE .out file
    
    :return: Status, eigenvalue
    
        status = True if output file exists and eigenvalue was extracted
        status = False if output file exists but no eigenvalue was found (possible error in input file syntax)
        exit operation if no output file found
    """
    try:
        open(_ofile, 'r').close()
    except IOError:
        utils.error("SCALE output file {} not found\n".format(_ofile), 'parse_scale_out_eig()\n', **kwargs)

    _rK = None
    _stat = False
    utils.vprint('\n Parsing output file {}\n'.format(_ofile), **kwargs)
    with open(_ofile, 'r') as _outObj:
        _line = _outObj.readline()
        while _line != "":
            if "k-eff = " in _line:
                _rK = float(_line.split()[-1])
                _stat = True
                break
            _line = _outObj.readline()
    utils.vprint('  done\n', **kwargs)
    return _stat, _rK


def itermain(tmp_list: (list, tuple), file_name: str, iter_vars: dict, kwargs: dict):
    """Main function for controlling the iteration
    
    :param tmp_list: List of lines from template file
    :param file_name: Name of template file
    :param iter_vars: Dictionary of iteration variables and their starting, minima, and maximum values
    :param kwargs: Additional keyword arguments
    
    :return: k_vec: List of progression of eigenvalue through iteration procedure
    :return: iter_vecs: Dictionary of iteration and their values through iteration procedure
    :return: conv_type - reason for exiting iter_main
    
        0: Accurately converged to target eigenvalue in specified iterations
    
        1: iter_var exceeded specified maximum twice
    
        -1: iter_var exceeded specified minimum twice
    
        2: Reached iteration limit without reaching target eigenvalue
    
        -2: Previous two k are close to similar 
       
    """
    # Make sure all the required keywords are present. If not, set to defaults from constants.py
    utils.check_defaults(kwargs)

    iter_vecs = {}

    for _var in iter_vars:
        iter_vecs[_var] = [iter_vars[_var][0], ]

    utils.oprint("Starting the iteration procedure....\n", **kwargs)

    conv_flag = False
    conv_type = None
    _n = 0
    k_vec = []

    while _n < kwargs['iter_lim']:
        _n += 1
        _iterfile = makefile(tmp_list, file_name, _n, kwargs['var_char'],
                             {_var: iter_vecs[_var][-1] for _var in iter_vars})
        utils.vprint('\nRunning SCALE iteration number {}...\n'.format(_n), **kwargs)
        subprocess.call([kwargs['exe_str'], _iterfile])
        utils.vprint('  done\n', **kwargs)
        stat, _k = parse_scale_out_eig(_iterfile.replace('.inp', '.out'), **kwargs)
        if stat:  # successful operation
            utils.oprint("  {0:<3}: {1}\n".format(_n, _k), **kwargs)
            k_vec.insert(_n - 1, _k)
        else:
            utils.error('Could not find value of k-eff for iteration file {0}.inp\n'
                        'Check {0}.out for error message\n'.format(file_name),
                        'itermain() of iteration {}\n'.format(_n), **kwargs)

        # check for convergance based on updated eigenvalue, and then a termination based on exceeding the specified
        # input range from the parameter file
        if abs(_k - kwargs['k_target']) < kwargs['eps_k']:
            utils.oprint('  done\n', **kwargs)
            return iter_vecs, k_vec, 0
        if len(k_vec) > 2 and abs(_k - k_vec[-2]) < kwargs['eps_k']:
            utils.oprint('  done\n', **kwargs)
            return iter_vecs, k_vec, -2
        stat = update_itervar(iter_vars, iter_vecs, k_vec, kwargs['k_target'])
        if stat == 0:
            conv_flag = False
        else:
            conv_type = stat
            if conv_flag:
                utils.oprint('  done\n', **kwargs)
                for var in iter_vecs:
                    iter_vecs[var].pop()
                return iter_vecs, k_vec, conv_type
            conv_flag = True

    if _n == kwargs['iter_lim'] and conv_type is None:
        conv_type = 2

    utils.oprint('  done\n', **kwargs)
    return iter_vecs, k_vec, conv_type
