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

[1]: M. D. DeHart, and S. Bowman, "Reactor Physics Methods and Analysis Capabilities in SCALE," Nuclear Technology, Technical Paper
vol. 174, no.2, pp. 196-213, 2011.

ASCII Art generated from [http://patorjk.com/software/taag](http://patorjk.com/software/taag/#p=display&f=Slant&t=CritOpS-NEWT)

## Input Syntax
```
python3 CritOpS.py [-h] [-v] [-o OUTPUT] inp_file param_file

positional arguments:
  inp_file              template SCALE input file
  param_file            file containing parameters for operation

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         reveal more of the mystery behind the operation
  -o OUTPUT, --output OUTPUT
                        write status to output file
```

