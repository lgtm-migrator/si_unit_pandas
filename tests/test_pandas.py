#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  test_pandas.py
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

# 3rd party
import numpy  # type: ignore
import pandas  # type: ignore
import pandas.util.testing as tm  # type: ignore
import pytest
from hypothesis import given
from hypothesis.strategies import integers, lists
from pandas.core.internals import ExtensionBlock  # type: ignore

# this package
import si_unit_pandas
from si_unit_pandas.base import Celsius

# ----------------------------------------------------------------------------
# Block Methods
# ----------------------------------------------------------------------------


def test_concatenate_blocks():
	v1 = si_unit_pandas.TemperatureArray([1, 2, 3])
	s = pandas.Series(v1, index=pandas.RangeIndex(3), fastpath=True)
	result = pandas.concat([s, s], ignore_index=True)
	expected = pandas.Series(si_unit_pandas.TemperatureArray([1, 2, 3, 1, 2, 3]))
	tm.assert_series_equal(result, expected)


# ----------------------------------------------------------------------------
# Public Constructors
# ----------------------------------------------------------------------------


def test_series_constructor():
	v = si_unit_pandas.TemperatureArray([1, 2, 3])
	result = pandas.Series(v)
	assert result.dtype == v.dtype
	assert isinstance(result._data.blocks[0], ExtensionBlock)


def test_dataframe_constructor():
	v = si_unit_pandas.TemperatureArray([1, 2, 3])
	df = pandas.DataFrame({"A": v})
	assert isinstance(df.dtypes['A'], si_unit_pandas.CelsiusType)
	assert df.shape == (3, 1)
	str(df)


def test_dataframe_from_series_no_dict():
	s = pandas.Series(si_unit_pandas.TemperatureArray([1, 2, 3]))
	result = pandas.DataFrame(s)
	expected = pandas.DataFrame({0: s})
	tm.assert_frame_equal(result, expected)

	s = pandas.Series(si_unit_pandas.TemperatureArray([1, 2, 3]), name='A')
	result = pandas.DataFrame(s)
	expected = pandas.DataFrame({'A': s})
	tm.assert_frame_equal(result, expected)


def test_dataframe_from_series():
	s = pandas.Series(si_unit_pandas.TemperatureArray([0, 1, 2]))
	c = pandas.Series(pandas.Categorical(['a', 'b']))
	result = pandas.DataFrame({"A": s, 'B': c})
	assert isinstance(result.dtypes['A'], si_unit_pandas.CelsiusType)


def test_getitem_scalar():
	ser = pandas.Series(si_unit_pandas.TemperatureArray([0, 1, 2]))
	result = ser[1]
	assert result == Celsius(1)


def test_getitem_slice():
	ser = pandas.Series(si_unit_pandas.TemperatureArray([0, 1, 2]))
	result = ser[1:]
	expected = pandas.Series(si_unit_pandas.TemperatureArray([1, 2]), index=range(1, 3))
	tm.assert_series_equal(result, expected)


def test_setitem_scalar():
	ser = pandas.Series(si_unit_pandas.TemperatureArray([0, 1, 2]))
	ser[1] = Celsius(10)
	expected = pandas.Series(si_unit_pandas.TemperatureArray([0, 10, 2]))
	tm.assert_series_equal(ser, expected)


# --------------
# Public Methods
# --------------


@given(lists(integers(min_value=1, max_value=2**128 - 1)))
def test_argsort(ints):
	pass
	# result = pandas.Series(si_unit_pandas.TemperatureArray(ints)).argsort()
	# expected = pandas.Series(ints).argsort()
	# tm.assert_series_equal(result.si_unit_pandas.to_pyints(), expected)


# ---------
# Factorize
# ---------


@pytest.mark.xfail(reason="TODO")
def test_factorize():
	arr = si_unit_pandas.TemperatureArray([1, 1, 10, 10])
	labels, uniques = pandas.factorize(arr)

	expected_labels = numpy.array([0, 0, 1, 1])
	tm.assert_numpy_array_equal(labels, expected_labels)

	expected_uniques = si_unit_pandas.TemperatureArray([1, 10])
	assert uniques.equals(expected_uniques)


@pytest.mark.xfail(reason="TODO")
def test_groupby_make_grouper():
	df = pandas.DataFrame({"A": [1, 1, 2, 2], "B": si_unit_pandas.TemperatureArray([1, 1, 2, 2])})
	gr = df.groupby("B")
	result = gr.grouper.groupings[0].grouper
	assert result.equals(df.B.values)


@pytest.mark.xfail(reason="TODO")
def test_groupby_make_grouper_groupings():
	df = pandas.DataFrame({"A": [1, 1, 2, 2], "B": si_unit_pandas.TemperatureArray([1, 1, 2, 2])})
	p1 = df.groupby("A").grouper.groupings[0]
	p2 = df.groupby("B").grouper.groupings[0]

	result = {int(k): v for k, v in p2.groups.items()}
	assert result.keys() == p1.groups.keys()
	for k in result.keys():
		assert result[k].equals(p1.groups[k])
