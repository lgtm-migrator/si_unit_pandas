# 3rd party
import numpy  # type: ignore
import pandas  # type: ignore
import pandas.testing as tm  # type: ignore
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
	df = pandas.DataFrame({'A': v})
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
	result = pandas.DataFrame({'A': s, 'B': c})
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
	df = pandas.DataFrame({'A': [1, 1, 2, 2], 'B': si_unit_pandas.TemperatureArray([1, 1, 2, 2])})
	gr = df.groupby('B')
	result = gr.grouper.groupings[0].grouper
	assert result.equals(df.B.values)


@pytest.mark.xfail(reason="TODO")
def test_groupby_make_grouper_groupings():
	df = pandas.DataFrame({'A': [1, 1, 2, 2], 'B': si_unit_pandas.TemperatureArray([1, 1, 2, 2])})
	p1 = df.groupby('A').grouper.groupings[0]
	p2 = df.groupby('B').grouper.groupings[0]

	result = {int(k): v for k, v in p2.groups.items()}
	assert result.keys() == p1.groups.keys()
	for k in result.keys():
		assert result[k].equals(p1.groups[k])
