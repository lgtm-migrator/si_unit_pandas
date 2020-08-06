# 3rd party
import numpy  # type: ignore
import pytest

# this package
from si_unit_pandas import CelsiusType
from si_unit_pandas.temperature_array import TemperatureArray, TemperatureBase


def test_celsius_type():
	# https://pandas.pydata.org/docs/reference/api/pandas.api.extensions.ExtensionDtype.html
	assert CelsiusType.name == "celsius"
	assert CelsiusType.type is TemperatureBase
	assert CelsiusType.kind == "O"

	obj = CelsiusType()
	assert obj.name == "celsius"
	assert obj.type is TemperatureBase
	assert obj.kind == "O"
	assert obj.na_value is numpy.nan
	assert obj.names is None

	assert obj.construct_array_type() is TemperatureArray
	assert CelsiusType.construct_array_type() is TemperatureArray
	assert isinstance(obj.construct_from_string("celsius"), CelsiusType)
	assert isinstance(CelsiusType.construct_from_string("celsius"), CelsiusType)

	with pytest.raises(TypeError):
		obj.construct_from_string("foo")

	assert obj.is_dtype(CelsiusType())
	assert CelsiusType.is_dtype(CelsiusType())

	assert not CelsiusType.is_dtype(float)
	assert not CelsiusType.is_dtype(int)
	assert not CelsiusType.is_dtype(str)
	assert not CelsiusType.is_dtype(tuple)
	assert not CelsiusType.is_dtype(list)
	assert not CelsiusType.is_dtype(dict)
	assert not CelsiusType.is_dtype(set)

	assert obj._is_numeric
	assert obj._is_boolean
