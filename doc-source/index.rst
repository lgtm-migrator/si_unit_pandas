===========================
si_unit_pandas
===========================

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
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Activity
	  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy| |pre_commit_ci|
	* - Other
	  - |license| |language| |requires|

.. |docs| rtfd-shield::
	:project: si_unit_pandas
	:alt: Documentation Build Status

.. |docs_check| actions-shield::
	:workflow: Docs Check
	:alt: Docs Check Status

.. |actions_linux| actions-shield::
	:workflow: Linux
	:alt: Linux Test Status

.. |actions_windows| actions-shield::
	:workflow: Windows
	:alt: Windows Test Status

.. |actions_macos| actions-shield::
	:workflow: macOS
	:alt: macOS Test Status

.. |actions_flake8| actions-shield::
	:workflow: Flake8
	:alt: Flake8 Status

.. |actions_mypy| actions-shield::
	:workflow: mypy
	:alt: mypy status

.. |requires| requires-io-shield::
	:alt: Requirements Status

.. |coveralls| coveralls-shield::
	:alt: Coverage

.. |codefactor| codefactor-shield::
	:alt: CodeFactor Grade

.. |pypi-version| pypi-shield::
	:project: si_unit_pandas
	:version:
	:alt: PyPI - Package Version

.. |supported-versions| pypi-shield::
	:project: si_unit_pandas
	:py-versions:
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| pypi-shield::
	:project: si_unit_pandas
	:implementations:
	:alt: PyPI - Supported Implementations

.. |wheel| pypi-shield::
	:project: si_unit_pandas
	:wheel:
	:alt: PyPI - Wheel

.. |license| github-shield::
	:license:
	:alt: License

.. |language| github-shield::
	:top-language:
	:alt: GitHub top language

.. |commits-since| github-shield::
	:commits-since: v0.0.1
	:alt: GitHub commits since tagged version

.. |commits-latest| github-shield::
	:last-commit:
	:alt: GitHub last commit

.. |maintained| maintained-shield:: 2021
	:alt: Maintenance

.. |pypi-downloads| pypi-shield::
	:project: si_unit_pandas
	:downloads: month
	:alt: PyPI - Downloads

.. |pre_commit_ci| pre-commit-ci-shield::
	:alt: pre-commit.ci status

.. end shields


.. start installation

.. installation:: si_unit_pandas
	:pypi:
	:github:

.. end installation

Key Concepts
============

``CelsiusType``
----------------

This is a data type (like ``numpy.dtype('int64')`` or
``pandas.api.types.CategoricalDtype()``. For the most part, you won't interact
with ``CelsiusType`` directly. It will be the value of the ``.dtype`` attribute on
your arrays.

Example
------------

.. code-block:: python

	from si_unit_pandas import TemperatureArray
	import pandas as pd

	TemperatureArray([10, 20, 30, 40, 50])


.. toctree::
	:hidden:

	Home<self>

.. toctree::
	:maxdepth: 3
	:caption: Documentation

	usage
	API Reference<docs>
	contributing
	Source

.. start links

View the :ref:`Function Index <genindex>` or browse the `Source Code <_modules/index.html>`__.

`Browse the GitHub Repository <https://github.com/domdfcoding/si_unit_pandas>`__

.. end links
