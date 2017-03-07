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
import globalparams as gp
import utils


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
                _outObj.write(_line.replace(gp.var_char + _var, "{:7.5f}".format(gp.iter_vars[_var][_iter])))

    return _ofile


def itermain():
    """Main function for controlling the iteration"""

    for _var in gp.iter_vars.keys():
        gp.iter_vecs[_var] = [gp.iter_vars[_var][0]]

    gp.k_vec.append(gp.k_guess)

    utils.vprint("Starting the iteration procedure....")

    for _n in range(gp.iter_lim):
        makefile(gp.args.inp_file, _n)
