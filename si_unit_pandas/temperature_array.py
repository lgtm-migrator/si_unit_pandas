import abc
import collections
import ipaddress

import numpy as np
import pandas as pd
import six
from pandas.api.extensions import ExtensionDtype

from .base import Celsius, Fahrenheit, NumPyBackedExtensionArrayMixin


# -----------------------------------------------------------------------------
# Extension Type
# -----------------------------------------------------------------------------


@six.add_metaclass(abc.ABCMeta)
class TemperatureBase(object):
	"""Metaclass providing a common base class for Temperatures."""
	pass


TemperatureBase.register(Celsius)
TemperatureBase.register(Fahrenheit)


@pd.api.extensions.register_extension_dtype
class CelsiusType(ExtensionDtype):
	name = 'celsius'
	type = TemperatureBase
	kind = 'O'
	_record_type = np.float
	na_value = np.nan

	@classmethod
	def construct_from_string(cls, string):
		if string == cls.name:
			return cls()
		else:
			raise TypeError(f"Cannot construct a '{cls.__name__}' from '{string}'")

	@classmethod
	def construct_array_type(cls):
		return TemperatureArray


# -----------------------------------------------------------------------------
# Extension Container
# -----------------------------------------------------------------------------


class TemperatureArray(NumPyBackedExtensionArrayMixin):
	"""Holder for Temperatures.

	TemperatureArray is a container for Temperatures. It satisfies pandas'
	extension array interface, and so can be stored inside
	:class:`pandas.Series` and :class:`pandas.DataFrame`.

	See :ref:`usage` for more.
	"""

	__array_priority__ = 1000
	_dtype = CelsiusType()
	_itemsize = 16
	ndim = 1
	can_hold_na = True

	def __init__(self, values, dtype=None, copy=False):
		from .parser import _to_temperature_array

		values = _to_temperature_array(values)  # TODO: avoid potential copy
		# TODO: dtype?
		if copy:
			values = values.copy()
		self.data = values

	@classmethod
	def _from_ndarray(cls, data, copy=False):
		"""
		Zero-copy construction of a TemperatureArray from an ndarray.

		Parameters
		----------
		data : ndarray
			This should have CelsiusType._record_type dtype
		copy : bool, default False
			Whether to copy the data.

		Returns
		-------
		ExtensionArray
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
		"""The missing value

		``numpy.nan`` is used

		Examples
		--------
		>>> TemperatureArray([]).na_value
		``numpy.nan``
		"""

		return self.dtype.na_value

	def take(self, indices, allow_fill=False, fill_value=None):
		# Can't use pandas' take yet
		# 1. axis
		# 2. I don't know how to do the reshaping correctly.

		indices = np.asarray(indices, dtype='int')

		if allow_fill and fill_value is None:
			fill_value = self.na_value
		elif allow_fill and not isinstance(fill_value, tuple):
			if not np.isnan(fill_value):
				fill_value = int(fill_value)

		if allow_fill:
			mask = (indices == -1)
			if not len(self):
				if not (indices == -1).all():
					msg = "Invalid take for empty array. Must be all -1."
					raise IndexError(msg)
				else:
					# all NA take from and empty array
					took = (np.full(
							(len(indices), 2),
							fill_value, dtype='>u8',
							).reshape(-1).astype(self.dtype._record_type))
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

	def __repr__(self):
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
		from .parser import to_temperature
		return to_temperature

	def append(self, value):
		from .parser import to_temperature

		value = to_temperature(value).data
		self.data = np.append(self.data, value)

	def __setitem__(self, key, value):
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
		return super(TemperatureArray, self).astype(dtype)

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
		# TDOO: scalar ipaddress
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
		if not isinstance(other, TemperatureArray):
			raise TypeError("Cannot compare 'TemperatureArray' "
							"to type '{}'".format(type(other)))
		# TODO: missing
		return (self.data == other.data).all()

	def _values_for_factorize(self):
		return self.astype(object), ipaddress.IPv4Address(0)

	def isna(self):
		"""
		Indicator for whether each element is missing.

		A temperature of 0.0 ℃ is used to indecate missing values.

		Examples
		--------
		>>> TemperatureArray([0, 14]).isna()
		array([ True, False])
		"""

		return self.data == self.na_value

	def isin(self, other):
		"""Check whether elements of `self` are in `other`.

		Comparison is done elementwise.

		Parameters
		----------
		other : str or sequences
			For ``str`` `other`, the argument is attempted to
			be converted to an :class:`ipaddress.IPv4Network` or
			a :class:`ipaddress.IPv6Network` or an :class:`IPArray`.
			If all those conversions fail, a TypeError is raised.

			For a sequence of strings, the same conversion is attempted.
			You should not mix networks with addresses.

			Finally, other may be an ``IPArray`` of addresses to compare to.

		Returns
		-------
		contained : ndarray
			A 1-D boolean ndarray with the same length as self.

		"""
		box = (isinstance(other, str) or
			   not isinstance(other, (TemperatureArray, collections.Sequence)))
		if box:
			other = [other]

		temperatures = []

		if not isinstance(other, TemperatureArray):
			for net in other:
				net = Celsius(net)
				temperatures.append(net)
		else:
			temperatures = other

		# Flatten all the addresses
		temperatures = TemperatureArray(temperatures)  # TODO: think about copy=False

		mask = np.zeros(len(self), dtype='bool')
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
