"""

NRE6401 - Molten Salt Reactor
CritOpS
A. Johnson

utils.py

Objective: Utilities for error messages, variable type checking

Functions:
    warning: produce a non-fatal warning message
    error: produce a fatal error message
    show_license: print the license
    vprint: verbose print shortcut
    oprint: Print to screen or append to file, depending on verbosity
    check_defaults: Update any missing keys from parameter dictionary
Classes:

"""
from critops.constants import lineBreakShort, default_params


def check_defaults(params: dict):
    """Update missing keys with default values"""
    for key in default_params:
        if key not in params:
            params[key] = default_params[key]


def oprint(_msg, **kwargs):
    """
    Print message to stdout if output argument not chosen.
    Else, append message to output file"
    """
    if 'output' not in kwargs or kwargs['output'] is None:
        print(_msg)
    else:
        with open(kwargs['output'], 'a') as outobj:
            outobj.write(_msg)


def warning(_msg, _loc=None, **kwargs):
    """Produce a non-fatal warning message"""
    oprint(lineBreakShort + _msg)
    if _loc is not None:
        oprint(" in " + _loc, **kwargs)
    oprint(lineBreakShort[::-1], **kwargs)


def error(_msg, _loc, **kwargs):
    """Produce a fatal error message"""
    oprint(lineBreakShort + "Fatal error: " + _msg + "\nin " + _loc, **kwargs)
    raise SystemExit


def vprint(_msg, **kwargs):
    """Print a chatty message"""
    if 'verbose' in kwargs and kwargs['verbose']:
        oprint(_msg, **kwargs)
