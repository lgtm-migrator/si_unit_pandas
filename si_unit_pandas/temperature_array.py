#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  temperature_array.py
#
#  Copyright (c) 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#  Based on cyberpandas
#  https://github.com/ContinuumIO/cyberpandas
#  Copyright (c) 2018, Anaconda, Inc.
#  Licensed under the BSD 3-Clause License:
#  |
#  |  Redistribution and use in source and binary forms, with or without
#  |  modification, are permitted provided that the following conditions are met:
#  |
#  |  * Redistributions of source code must retain the above copyright notice, this
#  |    list of conditions and the following disclaimer.
#  |
#  |  * Redistributions in binary form must reproduce the above copyright notice,
#  |    this list of conditions and the following disclaimer in the documentation
#  |    and/or other materials provided with the distribution.
#  |
#  |  * Neither the name of the copyright holder nor the names of its
#  |    contributors may be used to endorse or promote products derived from
#  |    this software without specific prior written permission.
#  |
#  |  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#  |  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  |  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#  |  DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#  |  FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#  |  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#  |  SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#  |  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#  |  OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  |  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

# stdlib
import abc
import collections
import ipaddress

# 3rd party
from typing import Sequence, Type, Union

import numpy  # type: ignore
import pandas  # type: ignore
import six
from pandas.api.extensions import ExtensionDtype  # type: ignore

# this package
from .base import Celsius, Fahrenheit, NumPyBackedExtensionArrayMixin

_to_temp_types = Union[float, str, Sequence[Union[float, str]]]


# -----------------------------------------------------------------------------
# Extension Type
# -----------------------------------------------------------------------------


@six.add_metaclass(abc.ABCMeta)
class TemperatureBase:
	"""Metaclass providing a common base class for Temperatures."""
	pass


TemperatureBase.register(Celsius)
TemperatureBase.register(Fahrenheit)


@pandas.api.extensions.register_extension_dtype
class CelsiusType(ExtensionDtype):
	name: str = 'celsius'
	type: Type = TemperatureBase
	kind: str = 'O'
	_record_type: Type = numpy.float
	na_value = numpy.nan

	@classmethod
	def construct_from_string(cls, string):
		if string == cls.name:
			return cls()
		else:
			raise TypeError(f"Cannot construct a '{cls.__name__}' from '{string}'")

	@classmethod
	def construct_array_type(cls) -> Type["TemperatureArray"]:
		return TemperatureArray


# -----------------------------------------------------------------------------
# Extension Container
# -----------------------------------------------------------------------------


class TemperatureArray(NumPyBackedExtensionArrayMixin):
	"""
	Holder for Temperatures.

	TemperatureArray is a container for Temperatures. It satisfies pandas'
	extension array interface, and so can be stored inside
	:class:`pandas.Series` and :class:`pandas.DataFrame`.

	See :ref:`usage` for more.
	"""

	__array_priority__: int = 1000
	_dtype = CelsiusType()
	_itemsize: int = 16
	ndim: int = 1
	can_hold_na: bool = True

	def __init__(self, values, dtype=None, copy: bool = False):
		# this package
		from .parser import _to_temperature_array

		values = _to_temperature_array(values)  # TODO: avoid potential copy

		# TODO: dtype?

		if copy:
			values = values.copy()

		self.data = values

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

		indices = numpy.asarray(indices, dtype='int')

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
									dtype='>u8',
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

	#
	# def __iter__(self):
	# 	from .parser import to_temperature
	#
	# 	return iter(to_temperature(self))

	def astype(self, dtype, copy=True):
		if isinstance(dtype, CelsiusType):
			if copy:
				self = self.copy()
			return self
		return super().astype(dtype)

	# ------------------------------------------------------------------------
	# Ops
	# ------------------------------------------------------------------------

	def __eq__(self, other):
		if not isinstance(other, TemperatureArray):
			return NotImplemented

		mask = self.isna() | other.isna()
		result = self.data == other.data
		result[mask] = False
		return result

	def __lt__(self, other):
		if not isinstance(other, TemperatureArray):
			return NotImplemented

		mask = self.isna() | other.isna()
		result = (self.data <= other.data)
		result[mask] = False
		return result

	def __le__(self, other):
		if not isinstance(other, TemperatureArray):
			return NotImplemented

		mask = self.isna() | other.isna()
		result = (self.data <= other.data)
		result[mask] = False
		return result

	def __gt__(self, other):
		if not isinstance(other, TemperatureArray):
			return NotImplemented

		return other < self

	def __ge__(self, other):
		if not isinstance(other, TemperatureArray):
			return NotImplemented

		return other <= self

	def equals(self, other):
		"""

		:param other:
		:type other:

		:return:
		:rtype:
		"""

		if not isinstance(other, TemperatureArray):
			raise TypeError(f"Cannot compare 'TemperatureArray' to type '{type(other)}'")

		# TODO: missing

		return (self.data == other.data).all()

	def _values_for_factorize(self):
		return self.astype(object), ipaddress.IPv4Address(0)

	def isna(self):
		"""
		Indicator for whether each element is missing.

		A temperature of 0.0 ℃ is used to indicate missing values.

		**Examples**

		>>> TemperatureArray([0, 14]).isna()
		array([ True, False])
		"""

		return self.data == self.na_value

	def isin(self, other) -> numpy.ndarray:
		"""
		Check whether elements of `self` are in `other`.

		Comparison is done elementwise.

		:param other:
		:type other: str or sequences

		:return: A 1-D boolean ndarray with the same length as self.
		"""

		if (
				isinstance(other, (str, float))
				or not isinstance(other, (TemperatureArray, collections.Sequence))
			):
			other = [other]

		temperatures = []

		if not isinstance(other, TemperatureArray):
			for net in other:
				net = Celsius(net)
				temperatures.append(net)
		else:
			temperatures = other

		temperatures = TemperatureArray(temperatures)  # TODO: think about copy=False

		mask = numpy.zeros(len(self), dtype='bool')
		for network in temperatures:
			mask |= self == network

		# no... we should flatten this.
		mask |= self == temperatures
		return mask


def is_temperature_type(obj):
	t = getattr(obj, 'dtype', obj)

	try:
		return isinstance(t, CelsiusType) or issubclass(t, CelsiusType)

	except Exception:
		return False
