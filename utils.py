"""

NRE6401 - Molten Salt Reactor
msr-refl-iter
A. Johnson

utils.py

Objective: Utilities for error messages, variable type checking

Functions:
    warning: produce a non-fatal warning message
    error: produce a fatal error message
    show_license: print the license
    vprint: verbose print shortcut
Classes:

"""
import globalparams as gp

lineBreakShort = '-' * 10 + '\n'


def oprint(_msg):
    """
    Print message to stdout if output argument not chosen.
    Else, append message to output file"
    """
    if gp.args.output is None:
        print(_msg)
    else:
        with open(gp.args.output, 'a') as outobj:
            outobj.write(_msg + '\n')


def warning(_msg, _loc=None):
    """Produce a non-fatal warning message"""
    oprint(lineBreakShort + _msg)
    if _loc is not None:
        oprint(" in " + _loc)
    oprint(lineBreakShort[::-1])


def error(_msg, _loc):
    """Produce a fatal error message"""
    oprint(lineBreakShort + "Fatal error: " + _msg + "\nin " + _loc)
    raise SystemExit


def show_license():
    """Print the contents of LICENSE to stdout"""
    with("LICENSE", 'r') as _license:
        print(_license.read())
    raise SystemExit


def vprint(_msg):
    """Print a chatty message"""
    if gp.args.verbose:
        oprint(_msg)
