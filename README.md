```   
   ______     _ __  ____       _____      _   _________       ________
  / ____/____(_) /_/ __ \____ / ___/     / | / / ____/ |     / /_  __/
 / /   / ___/ / __/ / / / __ \\__ \_____/  |/ / __/  | | /| / / / /
/ /___/ /  / / /_/ /_/ / /_/ /__/ /____/ /|  / /___  | |/ |/ / / /
\____/_/  /_/\__/\____/ .___/____/    /_/ |_/_____/  |__/|__/ /_/
                     /_/
```                     
# CritOpS-NEWT
A Critical Optimization Search tool for NEWT[1]

A. Johnson

**Objective**: Iteratively update a parameter in a template NEWT file in
order to obtain a critical system.
## Setup
```
git clone https://github.com/drewejohnson/CritOpS.git
cd CritOpS
python setup.py install
```
The code currently requires `python3` due to some formatting calls, and `pandas` for some better data output.

## Input Syntax
```
python3 CritOpS.py inp_file param_file [-v] [-o OUTPUT]

positional arguments:
  inp_file              template SCALE input file
  param_file            file containing parameters for operation

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         reveal more of the mystery behind the operation
  -o OUTPUT, --output OUTPUT
                        write status to output file
```
The parameter file controls iteration procedure and `SCALE` execution.
Parameters that can be updated with the parameter file include
1. `k_target`: Desired value of k-eff to be obtained from the `SCALE` runs
1. `eps_k`: Acceptable accuracy between `k_target` and each value of k-eff
1. `iter_lim`: Maximum number of times to run `SCALE`
1. `exe_str`: Absolute path to your `SCALE` executable. 
1. `var_char`: Whatever character you want to use as a designator for the variables

Currently, `CritOpS` only supports one iteration variable, which is declared in the parameter file with 
```
iter_var <var> <start> <min> <max>
```

The input file should be a valid `NEWT` input file, with some minor modifications.
There should exist certain values defined as variables preceeded by the `var_char`,
```
cuboid 20 5   0  0 -$del_z
```

Given some input and parameter files, the code will create and execute successive input files, 
parse the outputs for the update k-eff, and then update the iteration variables.

## Caveats/Future Work
This code was designed to optimize the thickness of a reflector, and assumes that each parameter
has a positive effect on criticality.
Increasing the value of an iteration variable is assumed to increase the criticality.
Technically this code could work on any `SCALE` input file, and so long as the output file contains the k-eff string, the iteration procedure should work.
This was not the intent, nor has this been tested.

Future work will include 
1. The ability to specify positive/negative feedbacks
1. The ability to specify and iterate upon multiple variables
1. The ability to define some variables as functions of iteration variables

## License
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

## References
[1]: M. D. DeHart, and S. Bowman, "Reactor Physics Methods and Analysis Capabilities in SCALE," Nuclear Technology, Technical Paper
vol. 174, no.2, pp. 196-213, 2011. http://dx.doi.org/10.13182/NT174-196

ASCII Art generated from [http://patorjk.com/software/taag](http://patorjk.com/software/taag/#p=display&f=Slant&t=CritOpS-NEWT)