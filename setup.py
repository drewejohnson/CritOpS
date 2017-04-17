"""

Setup
    - Properly install CritOpS

A. Johnson

Install with python setup.py install

"""

from setuptools import setup

shortDesc = 'A Critical Optimization Search Tool for NEWT'
longDesc = r"""
   ______     _ __  ____       _____      _   _________       ________
  / ____/____(_) /_/ __ \____ / ___/     / | / / ____/ |     / /_  __/
 / /   / ___/ / __/ / / / __ \\__ \_____/  |/ / __/  | | /| / / / /
/ /___/ /  / / /_/ /_/ / /_/ /__/ /____/ /|  / /___  | |/ |/ / / /
\____/_/  /_/\__/\____/ .___/____/    /_/ |_/_____/  |__/|__/ /_/
                     /_/

""" + """
                        critops
A Critical Optimization Search tool for NEWT[1]
A. Johnson

Objective: Iteratively update a parameter in a template NEWT file in
order to obtain a critical system.

[1]: M. D. DeHart, and S. Bowman, "Reactor Physics Methods and Analysis
\tCapabilities in SCALE," Nuclear Technology, Technical Paper
\tvol. 174, no.2, pp. 196-213, 2011."""

vRelease = 2
vMacro = 1
vMicro = 0

vDevel = 'dev'
vDevelMicro = '1'

if vDevel:
    version = "{}.{}.{}.{}{}".format(vRelease, vMacro, vMicro, vDevel, vDevelMicro)
else:
    version = "{}.{}.{}".format(vRelease, vMacro, vMicro)

installReqs = ['pandas>=0.19']

if __name__ == '__main__':
    setup(
        name='critops',
        version=version,
        description=shortDesc,
        long_description=longDesc,
        maintainer='A. Johnson',
        maintainer_email='1drew.e.johnson [at] gmail.com',
        url='https://github.com/drewejohnson/critops',
        install_requires=installReqs,
        python_requires='>=3.4',
        packages=['critops'],
        license='MIT License'
    )
