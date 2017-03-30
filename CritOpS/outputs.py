"""

NRE6401 - Molten Salt Reactor
msr-refl-iter
A. Johnson

outputs

Objective: Functions for reading SCALE output files and writing output files

Functions:
    parse_scale_output: Parse through the SCALE output file and return status

Classes:

"""
import pandas as pd
import CritOpS.utils as utils

from CritOpS import globalparams as gp


def parse_scale_out_eig(_ofile):
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
        utils.error("SCALE output file {} not found".format(_ofile), 'parse_scale_out_eig()')

    _rK = None
    _stat = False
    utils.vprint('\n Parsing output file {}'.format(_ofile))
    with open(_ofile, 'r') as _outObj:
        _line = _outObj.readline()
        while _line != "":
            if "k-eff = " in _line:
                _rK = float(_line.split()[-1])
                _stat = True
                break
            _line = _outObj.readline()
    utils.vprint('  done')
    return _stat, _rK


def output_landing(_out_type):
    """
    Write the output file according to the type of output
    :param _out_type: Flag indicating the reason the program terminated
        0: Nothing went wrong
        1: Desired update value for iteration parameter twice exceeded the maximum value from the parameter file
       -1: Desired update value for iteration parameter twice exceeded the minimum value from the parameter file
        2: Exceeded the total number of iterations allotted
    :return:
    """
    out_messages = {0: " Completed successfullly",
                    1: "Terminated due to iteration parameter {} twice exceeding max value {}".format(
                        list(gp.iter_vars.keys())[0], gp.iter_vars[list(gp.iter_vars.keys())[0]][2]),
                    -1: "Terminated due to iteration parameter {} twice exceeding minimum value {}".format(
                        list(gp.iter_vars.keys())[0], gp.iter_vars[list(gp.iter_vars.keys())[0]][2], ),
                    2: "Terminated due to exceeding the iteration limit {}".format(gp.iter_lim)
                    }
    utils.oprint('End of operation. Status: {}'.format(out_messages[_out_type]))
    var_df = pd.DataFrame({_var: gp.iter_vecs[_var] for _var in gp.iter_vars})
    var_df['k-eff'] = gp.k_vec
    utils.oprint(var_df.to_string())
