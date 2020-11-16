# 3rd party
import pytest

# this package
from si_unit_pandas import parser
from si_unit_pandas.temperature_array import TemperatureArray


@pytest.mark.parametrize("values", [62, "62", "62.0"])
def test_to_temperature(values):
	result = parser.to_temperature(values)
	expected = TemperatureArray([62.0])
	assert result.equals(expected)


def test_to_temperature_edge():
	ip_int = 2**64
	result = parser.to_temperature([ip_int])[0]
	assert int(result) == ip_int


def test_to_temperature_scalar():
	result = parser.to_temperature(1)
	expected = parser.to_temperature([1])
	assert len(result) == 1
	assert all(result == expected)
