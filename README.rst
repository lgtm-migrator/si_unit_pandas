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
	  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
	* - Activity
	  - |commits-latest| |commits-since| |maintained|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy| |pre_commit_ci|
	* - Other
	  - |license| |language| |requires|

.. |docs| image:: https://img.shields.io/readthedocs/si_unit_pandas/latest?logo=read-the-docs
	:target: https://si_unit_pandas.readthedocs.io/en/latest
	:alt: Documentation Build Status

.. |docs_check| image:: https://github.com/domdfcoding/si_unit_pandas/workflows/Docs%20Check/badge.svg
	:target: https://github.com/domdfcoding/si_unit_pandas/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |actions_linux| image:: https://github.com/domdfcoding/si_unit_pandas/workflows/Linux/badge.svg
	:target: https://github.com/domdfcoding/si_unit_pandas/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/domdfcoding/si_unit_pandas/workflows/Windows/badge.svg
	:target: https://github.com/domdfcoding/si_unit_pandas/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/domdfcoding/si_unit_pandas/workflows/macOS/badge.svg
	:target: https://github.com/domdfcoding/si_unit_pandas/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/domdfcoding/si_unit_pandas/workflows/Flake8/badge.svg
	:target: https://github.com/domdfcoding/si_unit_pandas/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/domdfcoding/si_unit_pandas/workflows/mypy/badge.svg
	:target: https://github.com/domdfcoding/si_unit_pandas/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://requires.io/github/domdfcoding/si_unit_pandas/requirements.svg?branch=master
	:target: https://requires.io/github/domdfcoding/si_unit_pandas/requirements/?branch=master
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/domdfcoding/si_unit_pandas/master?logo=coveralls
	:target: https://coveralls.io/github/domdfcoding/si_unit_pandas?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/domdfcoding/si_unit_pandas?logo=codefactor
	:target: https://www.codefactor.io/repository/github/domdfcoding/si_unit_pandas
	:alt: CodeFactor Grade

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

.. |maintained| image:: https://img.shields.io/maintenance/yes/2021
	:alt: Maintenance

.. |pre_commit_ci| image:: https://results.pre-commit.ci/badge/github/domdfcoding/si_unit_pandas/master.svg
	:target: https://results.pre-commit.ci/latest/github/domdfcoding/si_unit_pandas/master
	:alt: pre-commit.ci status

.. end shields

|

Installation
--------------

.. start installation

``si_unit_pandas`` can be installed from GitHub.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install git+https://github.com/domdfcoding/si_unit_pandas

.. end installation

Example
------------

.. code-block:: python

	from si_unit_pandas import TemperatureArray
	import pandas as pd

	TemperatureArray([10, 20, 30, 40, 50])
