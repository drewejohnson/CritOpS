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

line_break = '-' * 10 + '\n'


def warning(_msg, _loc=None):
    """Produce a non-fatal warning message"""
    print(line_break + _msg, end="")
    if _loc is not None:
        print(" in " + _loc, end="")
    print(line_break[::-1])


def error(_msg, _loc):
    """Produce a fatal error message"""
    raise SystemExit(line_break + _msg + "\nin " + _loc)


def show_license():
    """Print the contents of LICENSE to stdout"""
    with("LICENSE", 'r') as _license:
        print(_license.read())
    raise SystemExit


def vprint(_msg):
    """Print a chatty message"""
    if gp.args.verbose:
        print(_msg)
