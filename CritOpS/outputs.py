"""

NRE6401 - Molten Salt Reactor
CritOpS
A. Johnson

outputs

Objective: Functions for reading SCALE output files and writing output files

Functions:
    parse_scale_output: Parse through the SCALE output file and return status


"""
import pandas as pd

import CritOpS.utils as utils


def output_landing(iter_vecs: dict, k_vec: (list, tuple), _outtype: int, **kwargs):
    """
    Write the output file according to the type of output
    :param iter_vecs: Dictionary with iteration variables and their values through the procedure
    :param k_vec: Vector of eigenvalues
    :param _outtype: Flag indicating the reason the program terminated
        0: Nothing went wrong
        1: Desired update value for iteration parameter twice exceeded the maximum value from the parameter file
       -1: Desired update value for iteration parameter twice exceeded the minimum value from the parameter file
        2: Exceeded the total number of iterations allotted
    :return:
    """
    utils.check_defaults(kwargs)
    out_messages = {0: " Completed successfullly",
                    1: "Terminated due to iteration parameter {} twice exceeding max value {}".format(
                        list(iter_vecs.keys())[0], iter_vecs[list(iter_vecs.keys())[0]][2]),
                    -1: "Terminated due to iteration parameter {} twice exceeding minimum value {}".format(
                        list(iter_vecs.keys())[0], iter_vecs[list(iter_vecs.keys())[0]][1]),
                    2: "Terminated due to exceeding the iteration limit {}".format(kwargs['iter_lim'])
                    }
    utils.oprint('End of operation. Status: {}'.format(out_messages[_outtype]))
    var_df = pd.DataFrame({_var: iter_vecs[_var] for _var in iter_vecs})
    var_df['k-eff'] = k_vec
    utils.oprint(var_df.to_string())
