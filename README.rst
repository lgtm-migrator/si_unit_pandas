****************
si_unit_pandas
****************

.. start short_desc

**Custom Pandas dtypes for values with SI units.**

.. end short_desc

``si_unit_pandas`` provides support for storing temperatures inside a pandas DataFrame using pandas' `Extension Array Interface <https://pandas.pydata.org/docs/reference/api/pandas.api.extensions.ExtensionArray.html#pandas.api.extensions.ExtensionArray>`_

.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs| |docs_check|
	* - Tests
	  - |travis| |actions_windows| |actions_macos| |coveralls| |codefactor| |pre_commit_ci|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Activity
	  - |commits-latest| |commits-since| |maintained|
	* - Other
	  - |license| |language| |requires| |pre_commit|

.. |docs| image:: https://img.shields.io/readthedocs/si_unit_pandas/latest?logo=read-the-docs
	:target: https://si_unit_pandas.readthedocs.io/en/latest/?badge=latest
	:alt: Documentation Build Status

.. |docs_check| image:: https://github.com/domdfcoding/si_unit_pandas/workflows/Docs%20Check/badge.svg
	:target: https://github.com/domdfcoding/si_unit_pandas/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |travis| image:: https://github.com/domdfcoding/si_unit_pandas/workflows/Linux%20Tests/badge.svg
	:target: https://github.com/domdfcoding/si_unit_pandas/actions?query=workflow%3A%22Linux+Tests%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/domdfcoding/si_unit_pandas/workflows/Windows%20Tests/badge.svg
	:target: https://github.com/domdfcoding/si_unit_pandas/actions?query=workflow%3A%22Windows+Tests%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/domdfcoding/si_unit_pandas/workflows/macOS%20Tests/badge.svg
	:target: https://github.com/domdfcoding/si_unit_pandas/actions?query=workflow%3A%22macOS+Tests%22
	:alt: macOS Test Status

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

.. |pre_commit_ci| image:: https://results.pre-commit.ci/badge/github/domdfcoding/si_unit_pandas/master.svg
	:target: https://results.pre-commit.ci/latest/github/domdfcoding/si_unit_pandas/master
	:alt: pre-commit.ci status

.. end shields

|

Installation
--------------

.. start installation

``si_unit_pandas`` can be installed from PyPI.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install si_unit_pandas

.. end installation

Example
------------

.. code-block:: python

	from si_unit_pandas import TemperatureArray
	import pandas as pd

	TemperatureArray([10, 20, 30, 40, 50])
