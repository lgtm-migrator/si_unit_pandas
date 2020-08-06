#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  base.py
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
import operator
import re

# 3rd party
import numpy as np  # type: ignore
from pandas.core.arrays import ExtensionArray  # type: ignore


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
	def _from_sequence(cls, scalars, dtype=None, copy=False):
		return cls(scalars, dtype=dtype)

	@classmethod
	def _from_factorized(cls, values, original):
		return cls(values)

	@property
	def shape(self):
		return (len(self.data), )

	def __len__(self) -> int:
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

	def copy(self, deep: bool = False):
		return type(self)(self.data.copy())

	@classmethod
	def _concat_same_type(cls, to_concat):
		return cls(np.concatenate([array.data for array in to_concat]))

	def tolist(self):
		return self.data.tolist()

	def argsort(self, axis=-1, kind='quicksort', order=None):
		return self.data.argsort()

	def unique(self) -> ExtensionArray:
		# https://github.com/pandas-dev/pandas/pull/19869
		_, indices = np.unique(self.data, return_index=True)
		data = self.data.take(np.sort(indices))
		return self._from_ndarray(data)


class Celsius(float):

	def __init__(self, value):
		if isinstance(value, str):
			value = re.split("[\u205F\u2103\u00B0C]", value)[0]

		float.__init__(value)

	def __new__(cls, value):
		return float.__new__(cls, value)

	def __str__(self) -> str:
		return f"{float(self)}\u205F\u2103"

	def __repr__(self) -> str:
		# return f"<{self.__class__.__name__} object with value {float(self)}>"
		return str(self)


class Fahrenheit(float):

	def __str__(self) -> str:
		return f"{float(self)}\u205F\u2109"

	def __repr__(self) -> str:
		# return f"<{self.__class__.__name__} object with value {float(self)}>"
		return str(self)
