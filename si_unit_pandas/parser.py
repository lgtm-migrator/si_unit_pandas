import numpy as np
from pandas.api.types import is_list_like

from .base import Celsius, Fahrenheit


def to_temperature(values):
	"""Convert values to TemperatureArray

	Parameters
	----------
	values : int, float, str, Celsius or Farenheit, or sequence of those

	Returns
	-------
	addresses : TemperatureArray

	Examples
	--------
	Parse strings
	>>> to_temperature([Celsius(24), 25, 26.3, 27])
	TemperatureArray([24.0 ℃, 25.0 ℃, 26.3 ℃, 27.0 ℃])

	# TODO:
	Or integers
	>>> to_temperature([3232235777,
					  42540766452641154071740215577757643572])
	<TemperatureArray(['192.168.1.1', '0:8a2e:370:7334:2001:db8:85a3:0'])>

	Or packed binary representations
	>>> to_temperature([b'\xc0\xa8\x01\x01',
					  b' \x01\r\xb8\x85\xa3\x00\x00\x00\x00\x8a.\x03ps4'])
	<TemperatureArray(['192.168.1.1', '0:8a2e:370:7334:2001:db8:85a3:0'])>
	"""
	from . import TemperatureArray

	if not is_list_like(values):
		values = [values]

	return TemperatureArray(_to_temperature_array(values))


def _to_temperature_array(values):
	from .temperature_array import CelsiusType, TemperatureArray

	if isinstance(values, TemperatureArray):
		return values.data

	if (
			isinstance(values, np.ndarray)
			and values.ndim == 1
			and np.issubdtype(values.dtype, np.integer)
		):
		values = values.astype(float)
		values = np.asarray(values, dtype=CelsiusType._record_type)

	elif not (
			isinstance(values, np.ndarray)
			and values.dtype == CelsiusType._record_type
		):
		values = _to_int_pairs(values)

	return np.atleast_1d(np.asarray(values, dtype=CelsiusType._record_type))


def _to_int_pairs(values):
	if isinstance(values, (str, int, float, Celsius)):
		if isinstance(values, Fahrenheit):
			values = (values - 32) * (5 / 9)

		return float(values)

	elif isinstance(values, np.ndarray) and values.dtype != object:
		if values.ndim != 2:
			raise ValueError("'values' should be a 2-D when passing a NumPy array.")

	else:
		new_values = []
		for v in values:
			if isinstance(v, Fahrenheit):
				new_values.append((v - 32) * (5 / 9))
			else:
				new_values.append(v)

		values = [float(v) for v in new_values]
	return values
