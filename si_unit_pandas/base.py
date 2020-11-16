#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  base.py
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
import operator
import re
from typing import Any, Sequence, Tuple, Union

# 3rd party
import numpy as np  # type: ignore
from domdf_python_tools import doctools
from pandas.core.arrays import ExtensionArray  # type: ignore
from pandas.core.dtypes.generic import ABCExtensionArray  # type: ignore
from typing_extensions import Literal


class NumPyBackedExtensionArrayMixin(ExtensionArray):
	"""
	Mixin for pandas extension backed by a numpy array.
	"""

	@property
	def dtype(self):
		"""
		The dtype for this extension array, CelsiusType
		"""

		return self._dtype

	@classmethod
	def _from_sequence(cls, scalars: Sequence, dtype=None, copy: bool = False):
		"""
		Construct a new ExtensionArray from a sequence of scalars.

		:param scalars: Each element will be an instance of the scalar type for this
			array, ``cls.dtype.type``.
		:param dtype: Construct for this particular dtype. This should be a Dtype
			compatible with the ExtensionArray.
		:type dtype: dtype, optional
		:param copy: If True, copy the underlying data.

		:return:
		:rtype:
		"""

		return cls(scalars, dtype=dtype)

	@classmethod
	def _from_factorized(cls, values: np.ndarray, original):
		"""
		Reconstruct an ExtensionArray after factorization.

		:param values: An integer ndarray with the factorized values.
		:type values: ndarray
		:param original: The original ExtensionArray that factorize was called on.
		:type original: ExtensionArray

		:return:
		:rtype:

		.. seealso::

			:meth:`pandas.pandas.api.extensions.ExtensionArray.factorize`
		"""

		return cls(values)

	@property
	def shape(self) -> Tuple[int, ...]:
		"""
		Return a tuple of the array dimensions.
		"""

		return (len(self.data), )

	def __len__(self) -> int:
		"""
		Length of this array
		"""

		return len(self.data)

	def __getitem__(self, item: Union[int, slice, np.ndarray]) -> Any:
		"""
		Select a subset of self.

		:param item:
			* int: The position in 'self' to get.

			* slice: A slice object, where 'start', 'stop', and 'step' are integers or None.

			* ndarray: A 1-d boolean NumPy ndarray the same length as 'self'
		:type item:

		:return:
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
		return np.array(self._format_values(), dtype='object')

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

		return cls(np.concatenate([array.data for array in to_concat]))

	def tolist(self):
		return self.data.tolist()

	def argsort(
			self,
			ascending: bool = True,
			kind: Union[Literal['quicksort'], Literal['mergesort'], Literal['heapsort']] = "quicksort",
			*args,
			**kwargs,
			) -> np.ndarray:
		r"""
		Return the indices that would sort this array.

		:param ascending: Whether the indices should result in an ascending
			or descending sort.
		:param kind: {'quicksort', 'mergesort', 'heapsort'}, optional
			Sorting algorithm.

		\*args and \*\*kwargs are passed through to :func:`numpy.argsort`.

		:return: Array of indices that sort ``self``. If NaN values are contained,
			NaN values are placed at the end.
		:rtype:

		.. seealso::

			:class:`numpy.argsort`: Sorting implementation used internally.
		"""

		return self.data.argsort()

	def unique(self) -> ExtensionArray:
		# https://github.com/pandas-dev/pandas/pull/19869
		_, indices = np.unique(self.data, return_index=True)
		data = self.data.take(np.sort(indices))
		return self._from_ndarray(data)


@doctools.append_docstring_from(float)
class Celsius(float):
	"""
	:class:`float` subclass representing a temperature in Celsius.
	"""

	def __init__(self, value):
		if isinstance(value, str):
			value = re.split("[\u205F\u2103\u00B0C]", value)[0]

		float.__init__(value)

	@doctools.append_docstring_from(float.__new__)
	def __new__(cls, value):
		return float.__new__(cls, value)

	def __str__(self) -> str:
		"""
		Return the temperature as a string.
		"""

		return f"{float(self)}\u205F\u2103"

	def __repr__(self) -> str:
		"""
		Return a string representation of the temperature.
		"""

		# return f"<{self.__class__.__name__} object with value {float(self)}>"
		return str(self)


@doctools.append_docstring_from(float)
class Fahrenheit(float):
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

		# return f"<{self.__class__.__name__} object with value {float(self)}>"
		return str(self)
