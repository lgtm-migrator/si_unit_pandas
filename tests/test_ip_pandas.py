"""Tests involving pandas, not just the new array.
"""
import ipaddress

import pytest
import numpy as np
from hypothesis.strategies import integers, lists
from hypothesis import given
import pandas as pd
from pandas.core.internals import ExtensionBlock
import pandas.util.testing as tm

import si_unit_pandas as ip
from si_unit_pandas.base import Celsius


# ----------------------------------------------------------------------------
# Block Methods
# ----------------------------------------------------------------------------


def test_concatenate_blocks():
    v1 = ip.TemperatureArray([1, 2, 3])
    s = pd.Series(v1, index=pd.RangeIndex(3), fastpath=True)
    result = pd.concat([s, s], ignore_index=True)
    expected = pd.Series(ip.TemperatureArray([1, 2, 3, 1, 2, 3]))
    tm.assert_series_equal(result, expected)


# ----------------------------------------------------------------------------
# Public Constructors
# ----------------------------------------------------------------------------


def test_series_constructor():
    v = ip.TemperatureArray([1, 2, 3])
    result = pd.Series(v)
    assert result.dtype == v.dtype
    assert isinstance(result._data.blocks[0], ExtensionBlock)


def test_dataframe_constructor():
    v = ip.TemperatureArray([1, 2, 3])
    df = pd.DataFrame({"A": v})
    assert isinstance(df.dtypes['A'], ip.CelsiusType)
    assert df.shape == (3, 1)
    str(df)


def test_dataframe_from_series_no_dict():
    s = pd.Series(ip.TemperatureArray([1, 2, 3]))
    result = pd.DataFrame(s)
    expected = pd.DataFrame({0: s})
    tm.assert_frame_equal(result, expected)

    s = pd.Series(ip.TemperatureArray([1, 2, 3]), name='A')
    result = pd.DataFrame(s)
    expected = pd.DataFrame({'A': s})
    tm.assert_frame_equal(result, expected)


def test_dataframe_from_series():
    s = pd.Series(ip.TemperatureArray([0, 1, 2]))
    c = pd.Series(pd.Categorical(['a', 'b']))
    result = pd.DataFrame({"A": s, 'B': c})
    assert isinstance(result.dtypes['A'], ip.CelsiusType)


def test_getitem_scalar():
    ser = pd.Series(ip.TemperatureArray([0, 1, 2]))
    result = ser[1]
    assert result == Celsius(1)


def test_getitem_slice():
    ser = pd.Series(ip.TemperatureArray([0, 1, 2]))
    result = ser[1:]
    expected = pd.Series(ip.TemperatureArray([1, 2]), index=range(1, 3))
    tm.assert_series_equal(result, expected)


def test_setitem_scalar():
    ser = pd.Series(ip.TemperatureArray([0, 1, 2]))
    ser[1] = Celsius(10)
    expected = pd.Series(ip.TemperatureArray([0, 10, 2]))
    tm.assert_series_equal(ser, expected)


# --------------
# Public Methods
# --------------


@given(lists(integers(min_value=1, max_value=2**128 - 1)))
def test_argsort(ints):
    pass
    # result = pd.Series(si_unit_pandas.TemperatureArray(ints)).argsort()
    # expected = pd.Series(ints).argsort()
    # tm.assert_series_equal(result.si_unit_pandas.to_pyints(), expected)


# ---------
# Factorize
# ---------


@pytest.mark.xfail(reason="TODO")
def test_factorize():
    arr = ip.TemperatureArray([1, 1, 10, 10])
    labels, uniques = pd.factorize(arr)

    expected_labels = np.array([0, 0, 1, 1])
    tm.assert_numpy_array_equal(labels, expected_labels)

    expected_uniques = ip.TemperatureArray([1, 10])
    assert uniques.equals(expected_uniques)


@pytest.mark.xfail(reason="TODO")
def test_groupby_make_grouper():
    df = pd.DataFrame({"A": [1, 1, 2, 2],
                       "B": ip.TemperatureArray([1, 1, 2, 2])})
    gr = df.groupby("B")
    result = gr.grouper.groupings[0].grouper
    assert result.equals(df.B.values)


@pytest.mark.xfail(reason="TODO")
def test_groupby_make_grouper_groupings():
    df = pd.DataFrame({"A": [1, 1, 2, 2],
                       "B": ip.TemperatureArray([1, 1, 2, 2])})
    p1 = df.groupby("A").grouper.groupings[0]
    p2 = df.groupby("B").grouper.groupings[0]

    result = {int(k): v for k, v in p2.groups.items()}
    assert result.keys() == p1.groups.keys()
    for k in result.keys():
        assert result[k].equals(p1.groups[k])
