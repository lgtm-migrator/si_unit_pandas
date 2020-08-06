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
	  - |docs| |docs_check|
	* - Tests
	  - |travis| |actions_windows| |actions_macos| |coveralls| |codefactor|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Activity
	  - |commits-latest| |commits-since| |maintained|
	* - Other
	  - |license| |language| |requires| |pre_commit|

.. |docs| image:: https://img.shields.io/readthedocs/si_unit_pandas/latest?logo=read-the-docs
	:target: https://si_unit_pandas.readthedocs.io/en/latest/?badge=latest
	:alt: Documentation Status

.. |docs_check| image:: https://github.com/domdfcoding/si_unit_pandas/workflows/Docs%20Check/badge.svg
	:target: https://github.com/domdfcoding/si_unit_pandas/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |travis| image:: https://img.shields.io/travis/com/domdfcoding/si_unit_pandas/master?logo=travis
	:target: https://travis-ci.com/domdfcoding/si_unit_pandas
	:alt: Travis Build Status

.. |actions_windows| image:: https://github.com/domdfcoding/si_unit_pandas/workflows/Windows%20Tests/badge.svg
	:target: https://github.com/domdfcoding/si_unit_pandas/actions?query=workflow%3A%22Windows+Tests%22
	:alt: Windows Tests Status

.. |actions_macos| image:: https://github.com/domdfcoding/si_unit_pandas/workflows/macOS%20Tests/badge.svg
	:target: https://github.com/domdfcoding/si_unit_pandas/actions?query=workflow%3A%22macOS+Tests%22
	:alt: macOS Tests Status

.. |requires| image:: https://requires.io/github/domdfcoding/si_unit_pandas/requirements.svg?branch=master
	:target: https://requires.io/github/domdfcoding/si_unit_pandas/requirements/?branch=master
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/domdfcoding/si_unit_pandas/master?logo=coveralls
	:target: https://coveralls.io/github/domdfcoding/si_unit_pandas?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/domdfcoding/si_unit_pandas?logo=codefactor
	:target: https://www.codefactor.io/repository/github/domdfcoding/si_unit_pandas
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/si_unit_pandas
	:target: https://pypi.org/project/si_unit_pandas/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/si_unit_pandas?logo=python&logoColor=white
	:target: https://pypi.org/project/si_unit_pandas/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/si_unit_pandas
	:target: https://pypi.org/project/si_unit_pandas/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/si_unit_pandas
	:target: https://pypi.org/project/si_unit_pandas/
	:alt: PyPI - Wheel

.. |license| image:: https://img.shields.io/github/license/domdfcoding/si_unit_pandas
	:target: https://github.com/domdfcoding/si_unit_pandas/blob/master/LICENSE
	:alt: License

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

.. |pre_commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
	:target: https://github.com/pre-commit/pre-commit
	:alt: pre-commit

.. end shields


.. start installation

.. tabs::

	.. tab:: from PyPI

		.. prompt:: bash

			python3 -m pip install si_unit_pandas --user


	.. tab:: from GitHub

		.. prompt:: bash

			python3 -m pip install git+https://github.com/domdfcoding/si_unit_pandas@master --user

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
