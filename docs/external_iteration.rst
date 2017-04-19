==========================
Importing CritOps Iterator
==========================

.. _external:

External Usage
--------------

The :file:`CritOpS` module can easily be imported into external processing scripts.
Presented here is an example of executing the iteration routine as a standalone process.
::

    from critops.iterator import itermain
    from critops.utils import oprint
    from critops.outputs import output_landing


    critArgs = {
        'k-target': 9.98515E-01,
         'eps_k': 1E-8,
        'verbose': False,
        'output': None,
        'iter_lim': 15,
        'exe_str': 'C:\\Scale-6.2.1\\bin\\scalerte.exe',
        'k-id': 'Input buckling',
        'k-col': 9,
        'stalequit': False,
    }

    iter_var = {'buck': (1.2E-03, 1.00E-03, 5.00E-3)}

    bFile = 'intHX5_buck.inp'

    oprint('\nStarting buckling iteration\n', **critArgs)

    iter_vec, k_vec, conv_type = itermain(bFile, iter_var,

    output_landing(iter_vec, k_vec, conv_type, **critArgs)

.. _defaults:

Default Arguments
-----------------

============= ================================== ==========================================
**Parameter** **Default**                        **Note**
============= ================================== ==========================================
``eps_k``     1E-4                               Tightness on `k` convergence
``k_target``  1.0                                Desired `k-eff`
``iter_lim``  50                                 Maximum number of iterations
``tiny``      1E-16                              Numerical zero
``var_char``  ``'$'``                            Character to identify iteration variables
``k-id``      ``'k-eff = '``                     String to identify line containing `k-eff`
``k-col``     2                                  Location of `k-eff` in ``line.split()``
``stalequit`` ``True``                           Terminate if `k-eff` hasn't changed
``exe_str``   C:\\SCALE-6.2.1\\bin\\scalerte.exe Absolute path to ``SCALE`` executable
============= ================================== ==========================================