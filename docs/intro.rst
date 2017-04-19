=====
Intro
=====

This is the documentation for CritOpS, a Critical Optimization Search tool for use with NEWT[1].
CritOpS is designed to iteratively modify inputs for NEWT to obtain a desired eigenvalue.
More documentation will be added before the final release of this code, including examples and validation testing.

.. _setup:

Setup
-----
::

    git clone https://github.com/drewejohnson/CritOpS.git
    cd CritOpS
    python setup.py install

The code currently requires `python3` due to some formatting calls, and `pandas` for some better data output.

.. _usage:

Usage
-----

CritOpS can be run from the terminal while in the directory outside the critops folder with the command ::

    $ python critops <mainfile> <paramfile>

Where <mainfile> is a valid NEWT input file with some variables in place of valid values and <paramfile> is the
file that contains limits on iteration parameters, desired k-eff, and indicates the variable to be iterated upon.
See :file:`testing/iter_tester.inp` and :file:`testing/param_tester.txt` for one example case.

::

    python3 CritOpS.py inp_file param_file [-v] [-o OUTPUT]

    positional arguments:
      inp_file              template SCALE input file
      param_file            file containing parameters for operation

    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         reveal more of the mystery behind the operation
      -o OUTPUT, --output OUTPUT
                            write status to output file

The parameter file controls iteration procedure and `SCALE` execution.
Parameters that can be updated with the parameter file include

    #. `k_target`: Desired value of k-eff to be obtained from the `SCALE` runs
    #. `eps_k`: Acceptable accuracy between `k_target` and each value of k-eff
    #. `iter_lim`: Maximum number of times to run `SCALE`
    #. `exe_str`: Absolute path to your `SCALE` executable.
    #. `var_char`: Whatever character you want to use as a designator for the variables

Currently, `CritOpS` only supports one iteration variable, which is declared in the parameter file with::

    iter_var <var> <start> <min> <max>

The input file should be a valid `NEWT` input file, with some minor modifications.
There should exist certain values defined as variables preceeded by the `var_char`, ::

    cuboid 20 5   0  0 -$del_z

Given some input and parameter files, the code will create and execute successive input files,
parse the outputs for the update k-eff, and then update the iteration variables.

.. _license:

License
-------

MIT License

Copyright (c) 2017 Andrew Johnson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

References
----------

[1]: M. D. DeHart, and S. Bowman, "Reactor Physics Methods and Analysis Capabilities in SCALE," Nuclear Technology, Technical Paper vol. 174, no.2, pp. 196-213, 2011.
