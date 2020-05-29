===========================
si_unit_pandas
===========================

.. start short_desc

**Custom Pandas dtypes for values with SI units.**

.. end short_desc

.. start shields 

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs|
	* - Tests
	  - |travis| |requires| |coveralls| |codefactor|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Other
	  - |license| |language| |commits-since| |commits-latest| |maintained| 

.. |docs| image:: https://readthedocs.org/projects/si_unit_pandas/badge/?version=latest
	:target: https://si_unit_pandas.readthedocs.io/en/latest/?badge=latest
	:alt: Documentation Status

.. |travis| image:: https://img.shields.io/travis/com/domdfcoding/si_unit_pandas/master?logo=travis
	:target: https://travis-ci.com/domdfcoding/si_unit_pandas
	:alt: Travis Build Status

.. |requires| image:: https://requires.io/github/domdfcoding/si_unit_pandas/requirements.svg?branch=master
	:target: https://requires.io/github/domdfcoding/si_unit_pandas/requirements/?branch=master
	:alt: Requirements Status

.. |coveralls| image:: https://coveralls.io/repos/github/domdfcoding/si_unit_pandas/badge.svg?branch=master
	:target: https://coveralls.io/github/domdfcoding/si_unit_pandas?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/domdfcoding/si_unit_pandas
	:target: https://www.codefactor.io/repository/github/domdfcoding/si_unit_pandas
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/si_unit_pandas.svg
	:target: https://pypi.org/project/si_unit_pandas/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/si_unit_pandas.svg
	:target: https://pypi.org/project/si_unit_pandas/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/si_unit_pandas
	:target: https://pypi.org/project/si_unit_pandas/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/si_unit_pandas
	:target: https://pypi.org/project/si_unit_pandas/
	:alt: PyPI - Wheel

.. |license| image:: https://img.shields.io/github/license/domdfcoding/si_unit_pandas
	:alt: License
	:target: https://github.com/domdfcoding/si_unit_pandas/blob/master/LICENSE

.. |language| image:: https://img.shields.io/github/languages/top/domdfcoding/si_unit_pandas
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/domdfcoding/si_unit_pandas/v0.0.1
	:target: https://github.com/domdfcoding/si_unit_pandas/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/domdfcoding/si_unit_pandas
	:target: https://github.com/domdfcoding/si_unit_pandas/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2020
	:alt: Maintenance

.. end shields


.. start installation

.. tabs::

	.. tab:: from PyPI

		.. prompt:: bash

			pip install si_unit_pandas


	.. tab:: from GitHub

		.. prompt:: bash

			pip install git+https://github.com//si_unit_pandas@master

.. end installation

Key Concepts
============

``CelsiusType``
----------------

This is a data type (like ``numpy.dtype('int64')`` or
``pandas.api.types.CategoricalDtype()``. For the most part, you won't interact
with ``CelsiusType`` directly. It will be the value of the ``.dtype`` attribute on
your arrays.

``TemperatureArray``
---------------------

This is the container for your IPAddress data.

Usage
-----

.. code-block:: python

	from si_unit_pandas import TemperatureArray
	import pandas as pd

	TemperatureArray([10, 20, 30, 40, 50])

``TemperatureArray`` is a container for temperatures.
It can in turn be stored in pandas' containers:

.. code-block:: python

	pd.Series(arr)
	pd.DataFrame({"addresses": arr})

See :ref:`usage` for more.



.. toctree::
	:hidden:

	Home<self>

.. toctree::
	:maxdepth: 3
	:caption: Documentation

	usage
	API Reference<docs>
	Source
	Building

.. start links

View the :ref:`Function Index <genindex>` or browse the `Source Code <_modules/index.html>`__.

`Browse the GitHub Repository <https://github.com/domdfcoding/si_unit_pandas>`__

.. end links
