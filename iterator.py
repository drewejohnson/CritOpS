"""

NRE6401 - Molten Salt Reactor
msr-refl-iter
A. Johnson

iterator

Objective: Main file for controlling the iteration scheme

Functions:
    iter_main: Landing function that drives the iteration

Classes:

"""
import subprocess

import globalparams as gp
import utils
from outputs import parse_scale_out_eig, output_landing


def makefile(_tfile, _iter):
    """
    Write the new output file using the value from iteration _iter
    :param _tfile: Template output file with variables to be replaced
    :param _iter: Iteration number
    :return: Name of input file
    """
    _ofile = _tfile.name[:_tfile.name.rfind('.')] + "_" + str(_iter).zfill(len(str(gp.iter_lim))) + ".inp"

    with open(_ofile, 'w') as _outObj:
        for _line in gp.template_file:
            if gp.var_char not in _line:
                _outObj.write(_line)
            else:
                _var = _line[_line.index(gp.var_char):].split()[0][1:]
                # assumes that iteration variable will be followed by a space
                _outObj.write(_line.replace(gp.var_char + _var, "{:7.5f}".format(gp.iter_vecs[_var][-1])))

    return _ofile


def update_itervar():
    """
    Simple function to adjust the updating of the iteration variables

    Operates according to the following logic:
    An increase in a reflector parameter (thickness) will introduce more reflectance, increasing the eigenvalue
    Therefore, if the current eigenvalue is larger than the desired value, decrease the reflector thickness
    z_{n+1} = z_n \frac{k_{target}}{k_n}

    :return: status
        status = 0 if the updated value is inside the intended range
        status = 1 if the desired updated value is greater than the specified maximum of the parameter
            and the max value is used as the updated value
        status = -1 if the desired updated value is less than the specified maximum of the parameter
            and the minimum value is used as the updated value
    """

    # Assumes only one iteration variable for now
    _var = list(gp.iter_vars.keys())[0]
    _des = gp.iter_vecs[_var][-1] * gp.k_target / gp.k_vec[-1]
    # may square the ratio of k for small convergence

    if _des > gp.iter_vars[_var][2]:
        gp.iter_vecs[_var].append(gp.iter_vars[_var][2])
        return 1
    elif _des < gp.iter_vars[_var][1]:
        gp.iter_vecs[_var].append(gp.iter_vars[_var][1])
        return -1
    else:
        gp.iter_vecs[_var].append(_des)
        return 0


def itermain():
    """Main function for controlling the iteration"""

    for _var in gp.iter_vars.keys():
        gp.iter_vecs[_var] = [gp.iter_vars[_var][0], ]

    gp.k_vec.append(gp.k_guess)

    utils.vprint("Starting the iteration procedure....\n")

    conv_flag = False
    conv_type = None
    _n = 0
    while _n < gp.iter_lim:
        _n += 1
        _iter_file = makefile(gp.args.inp_file, _n)
        utils.vprint('Running SCALE iteration number {}...'.format(_n))
        # todo: Add try/except for errors
        subprocess.run([gp.exe_str, _iter_file])
        utils.vprint('  done')
        stat, _k = parse_scale_out_eig(_iter_file.replace('.inp', '.out'))
        if stat:  # successful operation
            utils.vprint("  {0:<3}: {1}".format(_n, _k))
            gp.k_vec.append(_k)
        else:
            utils.error('Could not find value of k-eff for iteration file {0}.inp\n'
                        'Check {0}.out for error message'.format(_iter_file.split('.')[0]),
                        'itermain() of iteration {}'.format(_n))
            # todo: Parse through output and find cause of error

        # check for convergance based on updated eigenvalue, and then a termination based on exceeding the specified
        # input range from the parameter file
        if abs(_k - gp.k_target) < gp.eps_k:
            conv_type = 0
            break
        stat = update_itervar()
        if stat == 0:
            conv_flag = False
        else:
            conv_type = stat
            if conv_flag:
                break

    if _n == gp.iter_lim and conv_type is None:
        conv_type = 2

    output_landing(conv_type)
