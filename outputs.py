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

import utils


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
