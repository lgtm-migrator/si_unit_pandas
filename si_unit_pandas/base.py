import operator
import re

import numpy as np

from pandas.core.arrays import ExtensionArray


class NumPyBackedExtensionArrayMixin(ExtensionArray):
	@property
	def dtype(self):
		"""
		The dtype for this extension array, CelsiusType
		"""

		return self._dtype

	@classmethod
	def _from_sequence(cls, scalars, dtype=None, copy=False):
		return cls(scalars, dtype=dtype)

	@classmethod
	def _from_factorized(cls, values, original):
		return cls(values)

	@property
	def shape(self):
		return (len(self.data),)

	def __len__(self):
		return len(self.data)

	def __getitem__(self, *args):
		result = operator.getitem(self.data, *args)
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
	def nbytes(self):
		return self._itemsize * len(self)

	def _formatting_values(self):
		return np.array(self._format_values(), dtype='object')

	def copy(self, deep=False):
		return type(self)(self.data.copy())

	@classmethod
	def _concat_same_type(cls, to_concat):
		return cls(np.concatenate([array.data for array in to_concat]))

	def tolist(self):
		return self.data.tolist()

	def argsort(self, axis=-1, kind='quicksort', order=None):
		return self.data.argsort()

	def unique(self):
		# type: () -> ExtensionArray
		# https://github.com/pandas-dev/pandas/pull/19869
		_, indices = np.unique(self.data, return_index=True)
		data = self.data.take(np.sort(indices))
		return self._from_ndarray(data)


class Celsius(float):
	def __init__(self, value):
		if isinstance(value, str):
			value = re.split("\u205F|\u2103|\u00B0|C", value)[0]

		float.__init__(value)

	def __new__(cls, value):
		return float.__new__(cls, value)

	def __str__(self):
		return f"{float(self)}\u205F\u2103"

	def __repr__(self):
		# return f"<{self.__class__.__name__} object with value {float(self)}>"
		return str(self)


class Fahrenheit(float):
	def __str__(self):
		return f"{float(self)}\u205F\u2109"

	def __repr__(self):
		# return f"<{self.__class__.__name__} object with value {float(self)}>"
		return str(self)
