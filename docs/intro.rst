=====
Intro
=====

This is the documentation for *CritOpS*, a Critical Optimization Search tool for use with `NEWT`[1].
*CritOpS* is designed to iteratively modify inputs for `NEWT` to obtain a desired eigenvalue.
More documentation will be added before the final release of this code, including examples and validation testing.

Usage
-----

*CritOpS* can be run from the terminal while in the directory outside the `critops` folder with the command ::

    $ python critops <mainfile> <paramfile>

Where `<mainfile>` is a valid `NEWT` input file with some variables in place of valid values and `<paramfile>` is the
file that contains limits on iteration parameters, desired k-eff, and indicates the variable to be iterated upon.
See :file:`testing/iter_tester.inp` and :file:`testing/param_tester.txt` for one example case.

References
----------
[1]: M. D. DeHart, and S. Bowman, "Reactor Physics Methods and Analysis Capabilities in SCALE," Nuclear Technology, Technical Paper vol. 174, no.2, pp. 196-213, 2011.
