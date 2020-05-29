import ipaddress
import operator

import pytest
import six
from hypothesis.strategies import integers, lists, tuples
from hypothesis import given, example

import numpy as np
import numpy.testing as npt
import pandas as pd
import si_unit_pandas
import pandas.util.testing as tm
from si_unit_pandas.base import Celsius


def test_make_container():
	values = si_unit_pandas.TemperatureArray([1, 2, 3])
	npt.assert_array_equal(
			values.data,
			np.array([1, 2, 3], dtype=values.dtype._record_type)
			)


def test_repr_works():
	values = si_unit_pandas.TemperatureArray([0, 1, 2, 3, 2 ** 32, 2 ** 64 + 1])
	result = repr(values)
	expected = ('TemperatureArray([0.0\u205f℃, 1.0\u205f℃, 2.0\u205f℃, 3.0\u205f℃, '
				'4294967296.0\u205f℃, 1.8446744073709552e+19\u205f℃])')
	assert result == expected


def test_isna():
	v = si_unit_pandas.TemperatureArray([0, 2, 2 ** 64, 2 ** 64 + 1, 2 ** 64 + 2])
	r1 = v.isna()
	r2 = pd.isna(v)
	expected = np.array([False, False, False, False, False])

	np.testing.assert_array_equal(r1, expected)
	np.testing.assert_array_equal(r2, expected)


def test_array():
	v = si_unit_pandas.TemperatureArray([1, 2, 3])
	result = np.array(v)
	expected = np.array([
			Celsius(1),
			Celsius(2),
			Celsius(3),
			])
	tm.assert_numpy_array_equal(result, expected)


def test_tolist():
	v = si_unit_pandas.TemperatureArray([1, 2, 3])
	result = v.tolist()
	expected = [1.0, 2.0, 3.0]
	assert result == expected


def test_equality():
	v1 = si_unit_pandas.to_temperature([30, 40])
	assert np.all(v1 == v1)
	assert v1.equals(v1)

	v2 = si_unit_pandas.to_temperature([20, 40])
	result = v1 == v2
	expected = np.array([False, True])
	tm.assert_numpy_array_equal(result, expected)

	result = bool(v1.equals(v2))
	assert result is False

	with pytest.raises(TypeError):
		v1.equals("a")


@pytest.mark.parametrize('op', [
		operator.lt,
		operator.le,
		operator.ge,
		operator.gt,
		])
@pytest.mark.skipif(six.PY2, reason="Flexible comparisons")
def test_comparison_raises(op):
	arr = si_unit_pandas.TemperatureArray([0, 1, 2])
	with pytest.raises(TypeError):
		op(arr, 'a')

	with pytest.raises(TypeError):
		op('a', arr)


@given(
		tuples(
				lists(integers(min_value=0, max_value=2**128 - 1)),
				lists(integers(min_value=0, max_value=2**128 - 1))
				).filter(lambda x: len(x[0]) == len(x[1]))
		)
@example((1, 1))
@example((0, 0))
@example((0, 1))
@example((1, 0))
@example((1, 2))
@example((2, 1))
# @pytest.mark.skip(reason="Flaky")
def test_ops(tup):
	a, b = tup
	v1 = si_unit_pandas.TemperatureArray(a)
	v2 = si_unit_pandas.TemperatureArray(b)

	r1 = v1 <= v2
	r2 = v2 >= v1
	tm.assert_numpy_array_equal(r1, r2)


def test_iter_works():
	x = si_unit_pandas.TemperatureArray([0, 1, 2])
	result = list(x)
	expected = [
			Celsius(0),
			Celsius(1),
			Celsius(2),
			]
	assert result == expected


def test_topyints():
	values = [0, 1, 2**32]
	arr = si_unit_pandas.TemperatureArray(values)
	result = [int(x) for x in arr]
	assert result == values


def test_getitem_scalar():
	ser = si_unit_pandas.TemperatureArray([0, 1, 2])
	result = ser[1]
	assert result == Celsius(1)


def test_getitem_slice():
	ser = si_unit_pandas.TemperatureArray([0, 1, 2])
	result = ser[1:]
	expected = si_unit_pandas.TemperatureArray([1, 2])
	assert result.equals(expected)


@pytest.mark.parametrize('value', [
		10.0,
		"10.0",
		10,
		Celsius(10),
		])
def test_setitem_scalar(value):
	ser = si_unit_pandas.TemperatureArray([0, 1, 2])
	ser[1] = Celsius(value)
	expected = si_unit_pandas.TemperatureArray([0, 10, 2])
	assert ser.equals(expected)


def test_setitem_array():
	ser = si_unit_pandas.TemperatureArray([0, 1, 2])
	ser[[1, 2]] = [10, 20]
	expected = si_unit_pandas.TemperatureArray([0, 10, 20])
	assert ser.equals(expected)


def test_unique():
	arr = si_unit_pandas.TemperatureArray([3, 3, 1, 2, 3])
	result = arr.unique()
	assert isinstance(result, si_unit_pandas.TemperatureArray)

	result = result.astype(object)
	expected = pd.unique(arr.astype(object))
	tm.assert_numpy_array_equal(result, expected)


def test_factorize():
	arr = si_unit_pandas.TemperatureArray([3, 3, 1, 2, 3])
	labels, uniques = arr.factorize()
	expected_labels, expected_uniques = pd.factorize(arr.astype(object))

	assert isinstance(uniques, si_unit_pandas.TemperatureArray)

	uniques = uniques.astype(object)
	tm.assert_numpy_array_equal(labels, expected_labels)
	tm.assert_numpy_array_equal(uniques, expected_uniques)


@pytest.mark.parametrize('values', [[0, 1, 2]])
def test_from_ndarray(values):
	result = si_unit_pandas.TemperatureArray(np.asarray(values))
	expected = si_unit_pandas.TemperatureArray(values)
	assert result.equals(expected)

