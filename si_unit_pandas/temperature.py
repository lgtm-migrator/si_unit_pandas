#!/usr/bin/env python3
#
#  temperature.py
"""
Temperature-specific functionality.
"""
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
import abc
import operator
import re
from typing import Any, Sequence, Type, TypeVar, Union

# 3rd party
import numpy  # type: ignore
import pandas  # type: ignore
from domdf_python_tools import doctools
from pandas.api.extensions import ExtensionDtype  # type: ignore
from pandas.core.dtypes.inference import is_list_like  # type: ignore

# this package
from si_unit_pandas.base import BaseArray, UserFloat

__all__ = [
		"Celsius",
		"CelsiusType",
		"Fahrenheit",
		"TemperatureArray",
		"TemperatureBase",
		"is_temperature_type",
		"to_temperature"
		]

_to_temp_types = Union[float, str, Sequence[Union[float, str]]]

# -----------------------------------------------------------------------------
# Extension Type
# -----------------------------------------------------------------------------


class TemperatureBase(metaclass=abc.ABCMeta):
	"""
	Metaclass providing a common base class for Temperatures.
	"""


@doctools.append_docstring_from(float)
class Celsius(UserFloat):
	"""
	:class:`float` subclass representing a temperature in Celsius.
	"""

	def __init__(self, value):
		if isinstance(value, str):
			value = re.split("[ ℃°C]", value)[0]

		super().__init__(value)

	def __str__(self) -> str:
		"""
		Return the temperature as a string.
		"""

		return f"{float(self)}\u205F\u2103"

	def __repr__(self) -> str:
		"""
		Return a string representation of the temperature.
		"""

		return str(self)


@doctools.append_docstring_from(float)
class Fahrenheit(UserFloat):
	"""
	:class:`float` subclass representing a temperature in Fahrenheit.
	"""

	def __str__(self) -> str:
		"""
		Return the temperature as a string.
		"""

		return f"{float(self)}\u205F\u2109"

	def __repr__(self) -> str:
		"""
		Return a string representation of the temperature.
		"""

		return str(self)


TemperatureBase.register(Celsius)
TemperatureBase.register(Fahrenheit)


@pandas.api.extensions.register_extension_dtype
class CelsiusType(ExtensionDtype):
	"""
	Numpy dtype representing a temperature in degrees Celsius.
	"""

	name: str = "celsius"
	type: Type = TemperatureBase  # noqa: A003  # pylint: disable=redefined-builtin
	kind: str = 'O'
	_record_type: Type = numpy.float

	@classmethod
	def construct_from_string(cls, string):
		"""
		Construct a :class:`~.CelsiusType` from a string.

		:param string:
		"""

		if string == cls.name:
			return cls()
		else:
			raise TypeError(f"Cannot construct a '{cls.__name__}' from '{string}'")

	@classmethod
	def construct_array_type(cls) -> Type["TemperatureArray"]:  # noqa: D102
		return TemperatureArray

	@property
	def _is_numeric(self) -> bool:
		"""
		Whether columns with this dtype should be considered numeric.

		By default ExtensionDtypes are assumed to be non-numeric.
		They'll be excluded from operations that exclude non-numeric
		columns, like (groupby) reductions, plotting, etc.
		"""

		return True

	@property
	def _is_boolean(self) -> bool:
		"""
		Whether this dtype should be considered boolean.

		By default, ExtensionDtypes are assumed to be non-numeric.
		Setting this to True will affect the behavior of several places,
		e.g.

		* is_bool
		* boolean indexing
		"""

		return True


# -----------------------------------------------------------------------------
# Extension Container
# -----------------------------------------------------------------------------

_A = TypeVar("_A")


class TemperatureArray(BaseArray):
	"""
	Holder for Temperatures.

	TemperatureArray is a container for Temperatures. It satisfies pandas'
	extension array interface, and so can be stored inside
	:class:`pandas.Series` and :class:`pandas.DataFrame`.
	"""

	__array_priority__: int = 1000
	_dtype = CelsiusType()
	_itemsize: int = 16
	can_hold_na: bool = True

	def __init__(self, data, dtype=None, copy: bool = False):

		# The dtype is always CelsiusType
		data = _to_temperature_array(data)  # TODO: avoid potential copy

		if copy:
			data = data.copy()

		self.data = data

	def __getitem__(self, item: Union[int, slice, numpy.ndarray]) -> Any:
		"""
		Select a subset of self.

		:param item:
			* int: The position in 'self' to get.

			* slice: A slice object, where 'start', 'stop', and 'step' are integers or None.

			* ndarray: A 1-d boolean NumPy ndarray the same length as 'self'

		:rtype: scalar or ExtensionArray

		.. note::

			For scalar ``item``, return a scalar value suitable for the array's
			type. This should be an instance of ``self.dtype.type``.

			For slice ``key``, return an instance of ``ExtensionArray``, even
			if the slice is length 0 or 1.

			For a boolean mask, return an instance of ``ExtensionArray``, filtered
			to the values where ``item`` is True.
		"""

		result = operator.getitem(self.data, item)

		if result.ndim == 0:
			return Celsius(result.item())
		else:
			return type(self)(result)

	def _format_values(self):
		formatted = []

		# TODO: perf

		for i in range(len(self)):
			formatted.append(Celsius(self.data[i]))

		return formatted

	@property
	def _parser(self):
		return to_temperature

	def append(self, value: _to_temp_types) -> None:
		"""
		Append a value to this TemperatureArray.

		:param value:
		"""

		super().append(value)

	def astype(self, dtype, copy=True):
		"""
		Returns the array with its values as the given dtype.

		:param dtype:
		:param copy: If :py:obj:`True`, returns a copy of the array.
		"""

		if isinstance(dtype, CelsiusType):
			if copy:
				self = self.copy()
			return self
		return super().astype(dtype)

	def isin(self, other: _to_temp_types) -> numpy.ndarray:
		"""
		Check whether elements of `self` are in `other`.

		Comparison is done elementwise.

		:param other:

		:return: A 1-D boolean ndarray with the same length as self.
		"""

		if isinstance(other, (str, float)) or not isinstance(other, (self.__class__, Sequence)):
			other = [other]  # type: ignore

		temperatures = []

		if not isinstance(other, self.__class__):
			for net in other:
				net = Celsius(net)
				temperatures.append(net)
		else:
			temperatures = other

		temperatures = self.__class__(temperatures)

		mask = numpy.zeros(len(self), dtype="bool")
		for network in temperatures:
			mask |= self == network

		mask |= self == temperatures
		return mask


def is_temperature_type(obj) -> bool:
	"""
	Returns whether ``obj`` is a temperature type.

	:param obj:
	"""

	t = getattr(obj, "dtype", obj)

	try:
		return isinstance(t, CelsiusType) or issubclass(t, CelsiusType)
	except Exception:
		return False


def to_temperature(values: _to_temp_types) -> TemperatureArray:
	"""
	Convert values to a :class:`~.TemperatureArray`.

	:param values:
	"""

	if is_list_like(values):
		return TemperatureArray(_to_temperature_array(values))
	else:
		return TemperatureArray(_to_temperature_array([values]))


def _to_temperature_array(
		values: Union[TemperatureArray, numpy.ndarray, Sequence[Union[str, float]]]
		) -> numpy.ndarray:  # : Union[TemperatureArray, np.ndarray]
	"""
	Convert the values to a temperature array.

	:param values:
	"""

	if isinstance(values, TemperatureArray):
		return values.data

	if isinstance(values, numpy.ndarray) and values.ndim == 1 and numpy.issubdtype(values.dtype, numpy.integer):
		values = values.astype(float)
		values = numpy.asarray(values, dtype=CelsiusType._record_type)

	elif not (isinstance(values, numpy.ndarray) and values.dtype == CelsiusType._record_type):
		values = _to_int_pairs(values)

	return numpy.atleast_1d(numpy.asarray(values, dtype=CelsiusType._record_type))


def _to_int_pairs(values: _to_temp_types):

	if isinstance(values, (str, int, float, Celsius)):
		if isinstance(values, Fahrenheit):
			values = (values - 32) * (5 / 9)

		return float(values)

	elif isinstance(values, numpy.ndarray) and values.dtype != object:
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
