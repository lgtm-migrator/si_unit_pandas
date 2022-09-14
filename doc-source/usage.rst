=====
Usage
=====

This document describes how to use the methods and classes provided by ``si_unit_pandas``.

We'll assume that the following imports have been performed.

.. code-block:: python

   # 3rd party
   import pandas as pd

   # this package
   from si_unit_pandas import TemperatureArray, to_temperature

Parsing
-------

First, you'll need some temperature data. Much like pandas'
:func:`pandas.to_datetime`, ``si_unit_pandas`` provides :func:`to_temperature` for
converting sequences of anything to a specialized array, :class:`TemperatureArray` in
this case.

From Strings
""""""""""""

:func:`to_temperature` can parse a sequence strings where each element represents a temperature.

.. code-block:: python

   to_temperature(["10", "20", "30", "40", "50"])

From Numbers
"""""""""""""

:func:`to_temperature` can also parse a sequence of numbers.

.. code-block:: python

   to_temperature([10, 20, 30.0, 40.5, 50])


Pandas Integration
------------------

``TemperatureArray`` satisfies pandas extension array interface, which means that it can safely be stored inside pandas' Series and DataFrame.

.. code-block:: python

   values = to_temperature([10, 20, 30.0, 40.5, 50])

   ser = pd.Series(values)

   df = pd.DataFrame({"temperatures": values})


Most pandas methods that make sense should work.
