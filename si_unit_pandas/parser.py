#!/usr/bin/env python3
#
#  parser.py
#
#  Copyright (c) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Based on cyberpandas
#  https://github.com/ContinuumIO/cyberpandas
#  Copyright (c) 2018, Anaconda, Inc.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are met:
#
#  * Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
#  * Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
#  * Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#  SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#  OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

# stdlib
from typing import Sequence, Union

# 3rd party
import numpy as np  # type: ignore
from pandas.api.types import is_list_like  # type: ignore

# this package
from si_unit_pandas.base import Celsius, Fahrenheit
from si_unit_pandas.temperature_array import CelsiusType, TemperatureArray

__all__ = ["to_temperature"]

_to_temp_types = Union[float, str, Sequence[Union[float, str]]]


def to_temperature(values: _to_temp_types) -> TemperatureArray:
	"""
	Convert values to a TemperatureArray

	:param values: int, float, str, Celsius or Fahrenheit, or sequence of those

	:return:
	"""

	if is_list_like(values):
		return TemperatureArray(_to_temperature_array(values))
	else:
		return TemperatureArray(_to_temperature_array([values]))


def _to_temperature_array(
		values: Union[TemperatureArray, np.ndarray, Sequence[Union[str, float]]]
		) -> np.ndarray:  # : Union[TemperatureArray, np.ndarray]
	"""

	:param values:

	:return:
	"""

	if isinstance(values, TemperatureArray):
		return values.data

	if (isinstance(values, np.ndarray) and values.ndim == 1 and np.issubdtype(values.dtype, np.integer)):
		values = values.astype(float)
		values = np.asarray(values, dtype=CelsiusType._record_type)

	elif not (isinstance(values, np.ndarray) and values.dtype == CelsiusType._record_type):
		values = _to_int_pairs(values)

	return np.atleast_1d(np.asarray(values, dtype=CelsiusType._record_type))


def _to_int_pairs(values: _to_temp_types):
	"""

	:param values:

	:return:
	"""

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
				new_values.append(float(v))

		values = [float(v) for v in new_values]
	return values
