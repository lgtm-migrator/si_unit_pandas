#!/usr/bin/env python3
#
#  temperature_array.py
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
#  _isstringslice based on awkward-array
#  https://github.com/scikit-hep/awkward-array
#  Copyright (c) 2018-2019, Jim Pivarski
#  Licensed under the BSD 3-Clause License

# stdlib
import abc
import collections
from typing import Sequence, Type, Union

# 3rd party
import numpy  # type: ignore
import pandas  # type: ignore
import six
from pandas.api.extensions import ExtensionDtype  # type: ignore

# this package
from .base import Celsius, Fahrenheit, NumPyBackedExtensionArrayMixin

__all__ = ["CelsiusType", "TemperatureArray", "TemperatureBase", "is_temperature_type"]

_to_temp_types = Union[float, str, Sequence[Union[float, str]]]

# -----------------------------------------------------------------------------
# Extension Type
# -----------------------------------------------------------------------------


class TemperatureBase(metaclass=abc.ABCMeta):
	"""
	Metaclass providing a common base class for Temperatures.
	"""


TemperatureBase.register(Celsius)
TemperatureBase.register(Fahrenheit)


@pandas.api.extensions.register_extension_dtype
class CelsiusType(ExtensionDtype):
	name: str = "celsius"
	type: Type = TemperatureBase
	kind: str = 'O'
	_record_type: Type = numpy.float

	@classmethod
	def construct_from_string(cls, string):
		if string == cls.name:
			return cls()
		else:
			raise TypeError(f"Cannot construct a '{cls.__name__}' from '{string}'")

	@classmethod
	def construct_array_type(cls) -> Type["TemperatureArray"]:
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


class TemperatureArray(numpy.lib.mixins.NDArrayOperatorsMixin, NumPyBackedExtensionArrayMixin):
	"""
	Holder for Temperatures.

	TemperatureArray is a container for Temperatures. It satisfies pandas'
	extension array interface, and so can be stored inside
	:class:`pandas.Series` and :class:`pandas.DataFrame`.
	"""

	__array_priority__: int = 1000
	_dtype = CelsiusType()
	_itemsize: int = 16
	ndim: int = 1
	can_hold_na: bool = True

	def __init__(self, data, dtype=None, copy: bool = False):
		# this package
		from .parser import _to_temperature_array

		# The dtype is always CelsiusType

		data = _to_temperature_array(data)  # TODO: avoid potential copy

		if copy:
			data = data.copy()

		self.data = data

	@classmethod
	def _from_ndarray(cls, data: numpy.ndarray, copy: bool = False) -> "TemperatureArray":
		"""
		Zero-copy construction of a TemperatureArray from an ndarray.

		:param data: This should have CelsiusType._record_type dtype
		:param copy: Whether to copy the data.

		:return:
		"""

		if copy:
			data = data.copy()

		new = TemperatureArray([])
		new.data = data

		return new

	# -------------------------------------------------------------------------
	# Properties
	# -------------------------------------------------------------------------
	@property
	def na_value(self):
		"""
		The missing value

		**Examples**

		>>> TemperatureArray([]).na_value
		``numpy.nan``
		"""

		return self.dtype.na_value

	def take(self, indices, allow_fill: bool = False, fill_value=None):
		# Can't use pandas' take yet
		# 1. axis
		# 2. I don't know how to do the reshaping correctly.

		indices = numpy.asarray(indices, dtype="int")

		if allow_fill and fill_value is None:
			fill_value = self.na_value
		elif allow_fill and not isinstance(fill_value, tuple):
			if not numpy.isnan(fill_value):
				fill_value = int(fill_value)

		if allow_fill:
			mask = (indices == -1)
			if not len(self):
				if not (indices == -1).all():
					msg = "Invalid take for empty array. Must be all -1."
					raise IndexError(msg)
				else:
					# all NA take from and empty array
					took = (
							numpy.full(
									(len(indices), 2),
									fill_value,
									dtype=">u8",
									).reshape(-1).astype(self.dtype._record_type)
							)
					return self._from_ndarray(took)
			if (indices < -1).any():
				msg = "Invalid value in 'indicies'. Must be all >= -1 for 'allow_fill=True'"
				raise ValueError(msg)

		took = self.data.take(indices)
		if allow_fill:
			took[mask] = fill_value

		return self._from_ndarray(took)

	# -------------------------------------------------------------------------
	# Interfaces
	# -------------------------------------------------------------------------

	def __repr__(self) -> str:
		formatted = self._format_values()
		return f"TemperatureArray({formatted!r})"

	def _format_values(self):
		formatted = []

		# TODO: perf

		for i in range(len(self)):
			formatted.append(Celsius(self.data[i]))

		return formatted

	@property
	def _parser(self):
		# this package
		from .parser import to_temperature

		return to_temperature

	def append(self, value: _to_temp_types):
		"""
		Append a value to this TemperatureArray.

		:param value:
		:type value:

		:return:
		:rtype:
		"""

		# this package
		from .parser import to_temperature

		self.data = numpy.append(self.data, to_temperature(value).data)

	def __setitem__(self, key, value):
		# this package
		from .parser import to_temperature

		value = to_temperature(value).data
		self.data[key] = value

	def __delitem__(self, where):
		if isinstance(where, str):
			del self.data[where]
		elif _isstringslice(where):
			for x in where:
				del self.data[x]
		else:
			raise TypeError(f"invalid index for removing column from Table: {where}")

	def astype(self, dtype, copy=True):
		if isinstance(dtype, CelsiusType):
			if copy:
				self = self.copy()
			return self
		return super().astype(dtype)

	# ------------------------------------------------------------------------
	# Ops
	# ------------------------------------------------------------------------

	def isna(self):
		"""
		Indicator for whether each element is missing.
		"""

		if numpy.isnan(self.na_value):
			return numpy.isnan(self.data)
		else:
			return self.data == self.na_value

	def isin(self, other) -> numpy.ndarray:
		"""
		Check whether elements of `self` are in `other`.

		Comparison is done elementwise.

		:param other:
		:type other: str or sequences

		:return: A 1-D boolean ndarray with the same length as self.
		"""

		if (isinstance(other, (str, float)) or not isinstance(other, (TemperatureArray, collections.Sequence))):
			other = [other]

		temperatures = []

		if not isinstance(other, TemperatureArray):
			for net in other:
				net = Celsius(net)
				temperatures.append(net)
		else:
			temperatures = other

		temperatures = TemperatureArray(temperatures)  # TODO: think about copy=False

		mask = numpy.zeros(len(self), dtype="bool")
		for network in temperatures:
			mask |= self == network

		# no... we should flatten this.
		mask |= self == temperatures
		return mask


def is_temperature_type(obj):
	t = getattr(obj, "dtype", obj)

	try:
		return isinstance(t, CelsiusType) or issubclass(t, CelsiusType)

	except Exception:
		return False


# From https://github.com/scikit-hep/awkward-array/blob/2bbdb68d7a4fff2eeaed81eb76195e59232e8c13/awkward/array/base.py#L611
def _isstringslice(where):
	if isinstance(where, str):
		return True
	elif isinstance(where, bytes):
		raise TypeError("column selection must be str, not bytes, in Python 3")
	elif isinstance(where, tuple):
		return False
	elif isinstance(where,
					(numpy.ndarray, TemperatureArray)) and issubclass(where.dtype.type, (numpy.str, numpy.str_)):
		return True
	elif isinstance(where, (numpy.ndarray, TemperatureArray)) and issubclass(
			where.dtype.type, (numpy.object, numpy.object_)
			) and not issubclass(where.dtype.type, (numpy.bool, numpy.bool_)):
		return len(where) > 0 and all(isinstance(x, str) for x in where)
	elif isinstance(where, (numpy.ndarray, TemperatureArray)):
		return False
	try:
		assert len(where) > 0 and all(isinstance(x, str) for x in where)
	except (TypeError, AssertionError):
		return False
	else:
		return True
