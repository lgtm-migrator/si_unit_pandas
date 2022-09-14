#!/usr/bin/env python3
#
#  base.py
"""
Base functionality.
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
#  _isstringslice based on awkward-array
#  https://github.com/scikit-hep/awkward-array
#  Copyright (c) 2018-2019, Jim Pivarski
#  Licensed under the BSD 3-Clause License
#

# stdlib
from abc import abstractmethod
from numbers import Real
from typing import Dict, Iterable, List, Optional, Sequence, SupportsFloat, Tuple, Type, TypeVar, Union, overload

# 3rd party
import numpy  # type: ignore
from domdf_python_tools.doctools import prettify_docstrings
from pandas.core.arrays import ExtensionArray  # type: ignore
from pandas.core.dtypes.base import ExtensionDtype  # type: ignore
from pandas.core.dtypes.generic import ABCExtensionArray  # type: ignore
from typing_extensions import Literal, Protocol

__all__ = ["NumPyBackedExtensionArrayMixin"]


class NumPyBackedExtensionArrayMixin(ExtensionArray):
	"""
	Mixin for pandas extension backed by a numpy array.
	"""

	_dtype: Type[ExtensionDtype]

	@property
	def dtype(self):
		"""
		The dtype for this extension array, :class:`~.CelsiusType`.
		"""

		return self._dtype

	@classmethod
	def _from_sequence(cls, scalars: Iterable, dtype=None, copy: bool = False):
		"""
		Construct a new ExtensionArray from a sequence of scalars.

		:param scalars: Each element will be an instance of the scalar type for this
			array, ``cls.dtype.type``.
		:param dtype: Construct for this particular dtype. This should be a Dtype
			compatible with the ExtensionArray.
		:type dtype: dtype, optional
		:param copy: If True, copy the underlying data.
		"""

		return cls(scalars, dtype=dtype)

	@classmethod
	def _from_factorized(cls, values: numpy.ndarray, original: ExtensionArray):
		"""
		Reconstruct an ExtensionArray after factorization.

		:param values: An integer ndarray with the factorized values.
		:param original: The original ExtensionArray that factorize was called on.

		.. seealso::

			:meth:`pandas.pandas.api.extensions.ExtensionArray.factorize`
		"""

		return cls(values)

	@property
	def shape(self) -> Tuple[int]:
		"""
		Return a tuple of the array dimensions.
		"""

		return len(self.data),

	def __len__(self) -> int:
		"""
		Returns the length of this array.
		"""

		return len(self.data)

	def setitem(self, indexer, value):
		"""
		Set the 'value' inplace.
		"""

		# I think having a separate than __setitem__ is good
		# since we have to return here, but __setitem__ doesn't.

		self[indexer] = value
		return self

	@property
	def nbytes(self) -> int:
		"""
		The number of bytes needed to store this object in memory.
		"""

		return self._itemsize * len(self)

	def _formatting_values(self):
		return numpy.array(self._format_values(), dtype="object")

	def copy(self, deep: bool = False) -> ABCExtensionArray:
		"""
		Return a copy of the array.

		:param deep:

		:return:
		:rtype:
		"""

		return type(self)(self.data.copy())

	@classmethod
	def _concat_same_type(cls, to_concat: Sequence[ABCExtensionArray]) -> ABCExtensionArray:
		"""
		Concatenate multiple arrays.

		:param to_concat: sequence of this type
		"""

		return cls(numpy.concatenate([array.data for array in to_concat]))

	def tolist(self) -> List:
		"""
		Convert the array to a Python list.
		"""

		return self.data.tolist()

	def argsort(
			self,
			ascending: bool = True,
			kind: Union[Literal["quicksort"], Literal["mergesort"], Literal["heapsort"]] = "quicksort",
			*args,
			**kwargs,
			) -> numpy.ndarray:
		r"""
		Return the indices that would sort this array.

		:param ascending: Whether the indices should result in an ascending
			or descending sort.
		:param kind: {'quicksort', 'mergesort', 'heapsort'}, optional
			Sorting algorithm.

		\*args and \*\*kwargs are passed through to :func:`numpy.argsort`.

		:return: Array of indices that sort ``self``. If NaN values are contained,
			NaN values are placed at the end.

		.. seealso::

			:class:`numpy.argsort`: Sorting implementation used internally.
		"""

		return self.data.argsort()

	def unique(self) -> ExtensionArray:  # noqa: D102
		# https://github.com/pandas-dev/pandas/pull/19869
		_, indices = numpy.unique(self.data, return_index=True)
		data = self.data.take(numpy.sort(indices))
		return self._from_ndarray(data)


_A = TypeVar("_A")


class BaseArray(numpy.lib.mixins.NDArrayOperatorsMixin, NumPyBackedExtensionArrayMixin):
	ndim: int = 1
	data: numpy.ndarray

	@classmethod
	def _from_ndarray(cls: _A, data: numpy.ndarray, copy: bool = False) -> _A:
		"""
		Zero-copy construction of a BaseArray from an ndarray.

		:param data: This should have CelsiusType._record_type dtype
		:param copy: Whether to copy the data.

		:return:
		"""

		if copy:
			data = data.copy()

		new = cls([])  # type: ignore
		new.data = data

		return new

	@property
	def na_value(self):
		"""
		The missing value.

		**Example:**

		.. code-block::

			>>> BaseArray([]).na_value
			numpy.nan
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

	def __repr__(self) -> str:
		formatted = self._format_values()
		return f"{self.__class__.__name__}({formatted!r})"

	def isna(self):
		"""
		Indicator for whether each element is missing.
		"""

		if numpy.isnan(self.na_value):
			return numpy.isnan(self.data)
		else:
			return self.data == self.na_value

	# From https://github.com/scikit-hep/awkward-array/blob/2bbdb68d7a4fff2eeaed81eb76195e59232e8c13/awkward/array/base.py#L611
	def _isstringslice(self, where):
		if isinstance(where, str):
			return True
		elif isinstance(where, bytes):
			raise TypeError("column selection must be str, not bytes, in Python 3")
		elif isinstance(where, tuple):
			return False
		elif (
				isinstance(where, (numpy.ndarray, self.__class__))
				and issubclass(where.dtype.type, (numpy.str, numpy.str_))
				):
			return True
		elif isinstance(where, (numpy.ndarray, self.__class__)) and issubclass(
				where.dtype.type, (numpy.object, numpy.object_)
				) and not issubclass(where.dtype.type, (numpy.bool, numpy.bool_)):
			return len(where) > 0 and all(isinstance(x, str) for x in where)
		elif isinstance(where, (numpy.ndarray, self.__class__)):
			return False
		try:
			assert len(where) > 0
			assert all(isinstance(x, str) for x in where)
		except (TypeError, AssertionError):
			return False
		else:
			return True

	def __delitem__(self, where):
		if isinstance(where, str):
			del self.data[where]
		elif self._isstringslice(where):
			for x in where:
				del self.data[x]
		else:
			raise TypeError(f"invalid index for removing column from Table: {where}")

	@property
	@abstractmethod
	def _parser(self):
		raise NotImplementedError

	def append(self, value) -> None:
		"""
		Append a value to this BaseArray.

		:param value:
		"""

		self.data = numpy.append(self.data, self._parser(value).data)

	def __setitem__(self, key, value):

		value = self._parser(value).data
		self.data[key] = value


class _SupportsIndex(Protocol):

	def __index__(self) -> int: ...


_F = TypeVar("_F", bound="UserFloat")


@prettify_docstrings
class UserFloat(Real):
	"""
	Class that simulates a float.

	:param value: Values to initialise the :class:`~domdf_python_tools.bases.UserFloat` with.

	.. versionadded:: 1.6.0
	"""

	def __init__(self, value: Union[SupportsFloat, _SupportsIndex, str, bytes, bytearray] = 0.0):
		self._value = (float(value), )

	def as_integer_ratio(self) -> Tuple[int, int]:
		return float(self).as_integer_ratio()

	def hex(self) -> str:  # noqa: A003  # pylint: disable=redefined-builtin
		return float(self).hex()

	def is_integer(self) -> bool:
		return float(self).is_integer()

	@classmethod
	def fromhex(cls: Type[_F], __s: str) -> _F:
		return cls(float.fromhex(__s))

	def __add__(self: _F, other: float) -> _F:
		return self.__class__(float(self).__add__(other))

	def __sub__(self: _F, other: float) -> _F:
		return self.__class__(float(self).__sub__(other))

	def __mul__(self: _F, other: float) -> _F:
		return self.__class__(float(self).__mul__(other))

	def __floordiv__(self: _F, other: float) -> _F:  # type: ignore
		return self.__class__(float(self).__floordiv__(other))

	def __truediv__(self: _F, other: float) -> _F:
		return self.__class__(float(self).__truediv__(other))

	def __mod__(self: _F, other: float) -> _F:
		return self.__class__(float(self).__mod__(other))

	def __divmod__(self: _F, other: float) -> Tuple[_F, _F]:
		return tuple(self.__class__(x) for x in float(self).__divmod__(other))  # type: ignore

	def __pow__(self: _F, other: float, mod=None) -> _F:
		return self.__class__(float(self).__pow__(other, mod))

	def __radd__(self: _F, other: float) -> _F:
		return self.__class__(float(self).__radd__(other))

	def __rsub__(self: _F, other: float) -> _F:
		return self.__class__(float(self).__rsub__(other))

	def __rmul__(self: _F, other: float) -> _F:
		return self.__class__(float(self).__rmul__(other))

	def __rfloordiv__(self: _F, other: float) -> _F:  # type: ignore
		return self.__class__(float(self).__rfloordiv__(other))

	def __rtruediv__(self: _F, other: float) -> _F:
		return self.__class__(float(self).__rtruediv__(other))

	def __rmod__(self: _F, other: float) -> _F:
		return self.__class__(float(self).__rmod__(other))

	def __rdivmod__(self: _F, other: float) -> Tuple[_F, _F]:
		return tuple(self.__class__(x) for x in float(self).__rdivmod__(other))  # type: ignore

	def __rpow__(self: _F, other: float, mod=None) -> _F:
		return self.__class__(float(self).__rpow__(other, mod))

	def __getnewargs__(self) -> Tuple[float]:
		return self._value

	def __trunc__(self) -> int:
		return float(self).__trunc__()

	@overload
	def __round__(self, ndigits: int) -> float: ...

	@overload
	def __round__(self, ndigits: None = ...) -> int: ...

	def __round__(self, ndigits: Optional[int] = None) -> Union[int, float]:
		return float(self).__round__(ndigits)

	def __eq__(self, other: object) -> bool:
		if isinstance(other, UserFloat):
			return self._value == other._value
		else:
			return float(self).__eq__(other)

	def __ne__(self, other: object) -> bool:
		if isinstance(other, UserFloat):
			return self._value != other._value
		else:
			return float(self).__ne__(other)

	def __lt__(self, other: float) -> bool:
		if isinstance(other, UserFloat):
			return self._value < other._value
		else:
			return float(self).__lt__(other)

	def __le__(self, other: float) -> bool:
		if isinstance(other, UserFloat):
			return self._value <= other._value
		else:
			return float(self).__le__(other)

	def __gt__(self, other: float) -> bool:
		if isinstance(other, UserFloat):
			return self._value > other._value
		else:
			return float(self).__gt__(other)

	def __ge__(self, other: float) -> bool:
		if isinstance(other, UserFloat):
			return self._value >= other._value
		else:
			return float(self).__ge__(other)

	def __neg__(self: _F) -> _F:
		return self.__class__(float(self).__neg__())

	def __pos__(self: _F) -> _F:
		return self.__class__(float(self).__pos__())

	def __str__(self) -> str:
		return str(float(self))

	def __int__(self) -> int:
		return int(float(self))

	def __float__(self) -> float:
		return self._value[0]

	def __abs__(self: _F) -> _F:
		return self.__class__(float(self).__abs__())

	def __hash__(self) -> int:
		return float(self).__hash__()

	def __repr__(self) -> str:
		return str(self)

	def __ceil__(self):
		raise NotImplementedError

	def __floor__(self):
		raise NotImplementedError
