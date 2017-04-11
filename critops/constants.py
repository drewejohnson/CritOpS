"""

NRE6401 - Molten Salt Reactor
CritOpS
A. Johnson

constants

Objective: Header file for some useful constants

"""
lineBreakShort = '-' * 10 + '\n'
lineBreakLong = "*" * 70 + '\n'

default_params = {
    'eps_k': 1E-4, 'k_target': 1.0, 'iter_lim': 50,
    'inf': 1E30, 'tiny': 1E-16, 'var_char': '$', 'exe_str': 'C:\\SCALE-6.2.1\\bin\\scalerte.exe'
}

pName = "CritOpS-NEWT  v2.0.0dev5"
asciiHeader = r"""
   ______     _ __  ____       _____      _   _________       ________
  / ____/____(_) /_/ __ \____ / ___/     / | / / ____/ |     / /_  __/
 / /   / ___/ / __/ / / / __ \\__ \_____/  |/ / __/  | | /| / / / /
/ /___/ /  / / /_/ /_/ / /_/ /__/ /____/ /|  / /___  | |/ |/ / / /
\____/_/  /_/\__/\____/ .___/____/    /_/ |_/_____/  |__/|__/ /_/
                     /_/
"""  # http://patorjk.com/software/taag/#p=display&f=Slant&t=CritOpS-NEWT

header = lineBreakLong + asciiHeader + pName.center(len(lineBreakLong)) + """
A Critical Optimization Search tool for NEWT[1]
A. Johnson

Objective: Iteratively update a parameter in a template NEWT file in
order to obtain a critical system.

[1]: M. D. DeHart, and S. Bowman, "Reactor Physics Methods and Analysis
\tCapabilities in SCALE," Nuclear Technology, Technical Paper
\tvol. 174, no.2, pp. 196-213, 2011.

""" + lineBreakLong

supVarChars = ('$',)
