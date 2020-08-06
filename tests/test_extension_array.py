# 3rd party
import numpy  # type: ignore
import pytest

# this package
from si_unit_pandas.temperature_array import CelsiusType, TemperatureArray

_non_empty_sets = [
		{1},
		{1, 2},
		{1, 2, 3},
		{1, 2, 3, 4},
		{1, 2, 3, 4, 5},
		]

_non_empty_lists = [
		[1],
		[1, 2],
		[1, 2, 3],
		[1, 2, 3, 4],
		[1, 2, 3, 4, 5],
		]

_non_empty_tuples = [
		(1, ),
		(1, 2),
		(1, 2, 3),
		(1, 2, 3, 4),
		(1, 2, 3, 4, 5),
		]

_non_empty_arrays = [
		numpy.array([1]),
		numpy.array([1, 2]),
		numpy.array([1, 2, 3]),
		numpy.array([1, 2, 3, 4]),
		numpy.array([1, 2, 3, 4, 5]),
		]


def test_temperature_array_members():
	# https://pandas.pydata.org/docs/reference/api/pandas.api.extensions.ExtensionArray.html
	assert hasattr(TemperatureArray, "_from_sequence")
	assert hasattr(TemperatureArray, "_from_factorized")
	assert hasattr(TemperatureArray, "__getitem__")
	assert hasattr(TemperatureArray, "__len__")
	assert hasattr(TemperatureArray, "__eq__")
	assert hasattr(TemperatureArray, "dtype")
	assert hasattr(TemperatureArray, "nbytes")
	assert hasattr(TemperatureArray, "isna")
	assert hasattr(TemperatureArray, "take")
	assert hasattr(TemperatureArray, "copy")
	assert hasattr(TemperatureArray, "_concat_same_type")


@pytest.mark.parametrize("seq", [*_non_empty_sets, *_non_empty_lists, *_non_empty_tuples, *_non_empty_arrays])
def test_temperature_array_from_sequence(seq):
	assert numpy.all(TemperatureArray._from_sequence(seq, None) == TemperatureArray(list(seq)))


@pytest.mark.parametrize("seq", _non_empty_arrays)
def test_temperature_array_from_ndarray(seq):
	assert numpy.all(TemperatureArray._from_ndarray(seq) == TemperatureArray(list(seq)))
	assert numpy.all(TemperatureArray._from_ndarray(seq, copy=False) == TemperatureArray(list(seq)))
	assert numpy.all(TemperatureArray._from_ndarray(seq, copy=True) == TemperatureArray(list(seq)))


@pytest.mark.parametrize("seq", [*_non_empty_sets, *_non_empty_lists, *_non_empty_tuples, *_non_empty_arrays])
def test_temperature_array(seq):
	assert numpy.all(TemperatureArray(seq).data == numpy.array(list(seq)))


@pytest.mark.parametrize("seq", [*_non_empty_lists, *_non_empty_tuples, *_non_empty_arrays])
def test_temperature_array_from_factorized(seq):
	assert numpy.all(
			TemperatureArray._from_factorized(numpy.array(seq), None) == TemperatureArray(numpy.array(list(seq)))
			)


def test_temperature_array_from_sequence_empty():
	assert numpy.all(TemperatureArray._from_sequence([]) == TemperatureArray([]))
	assert numpy.all(TemperatureArray._from_sequence({}) == TemperatureArray([]))
	assert numpy.all(TemperatureArray._from_sequence(()) == TemperatureArray([]))
	assert numpy.all(TemperatureArray._from_sequence(numpy.array([])) == TemperatureArray([]))


def test_temperature_array_from_ndarray_empty():
	assert numpy.all(TemperatureArray._from_ndarray(numpy.array([])) == TemperatureArray([]))
	assert numpy.all(TemperatureArray._from_ndarray(numpy.array([]), copy=False) == TemperatureArray([]))
	assert numpy.all(TemperatureArray._from_ndarray(numpy.array([]), copy=True) == TemperatureArray([]))


def test_temperature_array_from_factorized_empty():
	assert numpy.all(TemperatureArray._from_factorized(numpy.array([]), None) == TemperatureArray([]))
	assert numpy.all(TemperatureArray._from_factorized(numpy.array(()), None) == TemperatureArray([]))
	assert numpy.all(TemperatureArray._from_factorized(numpy.array(numpy.array([])), None) == TemperatureArray([]))


@pytest.mark.parametrize(
		"seq", [
				[],
				(),
				{},
				numpy.array([]),
				*_non_empty_sets,
				*_non_empty_lists,
				*_non_empty_tuples,
				*_non_empty_arrays,
				]
		)
def test_dtype(seq):
	assert isinstance(TemperatureArray(seq).dtype, CelsiusType)


def test_init_copy():
	arr = numpy.array([1, 2, 3, 4, 5], dtype=CelsiusType._record_type)

	assert TemperatureArray(arr).data is arr
	assert id(TemperatureArray(arr).data) == id(arr)

	assert TemperatureArray(arr, copy=False).data is arr
	assert id(TemperatureArray(arr, copy=False).data) == id(arr)

	assert TemperatureArray(arr, copy=True).data is not arr
	assert id(TemperatureArray(arr, copy=True).data) != id(arr)

	arr2 = numpy.array([1, 2, 3, 4, 5])

	assert TemperatureArray(arr2).data is not arr2
	assert id(TemperatureArray(arr2).data) != id(arr2)

	assert TemperatureArray(arr2, copy=False).data is not arr2
	assert id(TemperatureArray(arr2, copy=False).data) != id(arr2)

	assert TemperatureArray(arr2, copy=True).data is not arr2
	assert id(TemperatureArray(arr2, copy=True).data) != id(arr2)


def test_eq():
	assert numpy.alltrue(TemperatureArray([1, 2, 3, 4, 5]) == TemperatureArray([1, 2, 3, 4, 5]))
	assert not numpy.alltrue(TemperatureArray([1, 2, 3, 4, 5]) == TemperatureArray([2, 3, 4, 5, 6]))
	assert not numpy.alltrue(TemperatureArray([1, 2, 3, 4, 5]) == TemperatureArray([0, 1, 2, 3, 4]))


def test_equals():
	assert TemperatureArray([1, 2, 3, 4, 5]).equals(TemperatureArray([1, 2, 3, 4, 5]))
	assert not TemperatureArray([1, 2, 3, 4, 5]).equals(TemperatureArray([2, 3, 4, 5, 6]))
	assert not TemperatureArray([1, 2, 3, 4, 5]).equals(TemperatureArray([0, 1, 2, 3, 4]))
	#
	# with pytest.raises(TypeError):
	TemperatureArray([1, 2, 3, 4, 5]).equals(numpy.array((1, 2, 3, 4, 5)))
	#
	# with pytest.raises(TypeError):
	TemperatureArray([1, 2, 3, 4, 5]).equals([1, 2, 3, 4, 5])
	#
	# with pytest.raises(TypeError):
	TemperatureArray([1, 2, 3, 4, 5]).equals((1, 2, 3, 4, 5))
	#
	# with pytest.raises(TypeError):
	TemperatureArray([1, 2, 3, 4, 5]).equals({1, 2, 3, 4, 5})


def test_le():
	assert numpy.alltrue(TemperatureArray([1, 2, 3, 4, 5]) <= TemperatureArray([1, 2, 3, 4, 5]))
	assert numpy.alltrue(TemperatureArray([1, 2, 3, 4, 5]) <= TemperatureArray([2, 3, 4, 5, 6]))
	assert not numpy.alltrue(TemperatureArray([1, 2, 3, 4, 5]) <= TemperatureArray([0, 1, 2, 3, 4]))


def test_ge():
	assert numpy.alltrue(TemperatureArray([1, 2, 3, 4, 5]) >= TemperatureArray([1, 2, 3, 4, 5]))
	assert numpy.alltrue(TemperatureArray([1, 2, 3, 4, 5]) >= TemperatureArray([0, 1, 2, 3, 4]))
	assert not numpy.alltrue(TemperatureArray([1, 2, 3, 4, 5]) >= TemperatureArray([2, 3, 4, 5, 6]))


def test_lt():
	assert not numpy.alltrue(TemperatureArray([1, 2, 3, 4, 5]) < TemperatureArray([1, 2, 3, 4, 5]))
	assert numpy.alltrue(TemperatureArray([1, 2, 3, 4, 5]) < TemperatureArray([2, 3, 4, 5, 6]))
	assert not numpy.alltrue(TemperatureArray([1, 2, 3, 4, 5]) < TemperatureArray([0, 1, 2, 3, 4]))


def test_gt():
	assert not numpy.alltrue(TemperatureArray([1, 2, 3, 4, 5]) > TemperatureArray([1, 2, 3, 4, 5]))
	assert numpy.alltrue(TemperatureArray([1, 2, 3, 4, 5]) > TemperatureArray([0, 1, 2, 3, 4]))
	assert not numpy.alltrue(TemperatureArray([1, 2, 3, 4, 5]) > TemperatureArray([2, 3, 4, 5, 6]))


def test_astype():
	arr = TemperatureArray([1, 2, 3, 4, 5]).astype(float)
	assert isinstance(arr, numpy.ndarray)
	assert arr.dtype is numpy.dtype(numpy.float64)
	assert arr.dtype is numpy.dtype(float)

	arr = TemperatureArray([1, 2, 3, 4, 5]).astype(int)
	assert isinstance(arr, numpy.ndarray)
	assert arr.dtype == numpy.dtype(numpy.int)
	assert arr.dtype == numpy.dtype(int)


def test_isna():
	assert TemperatureArray([2, 3, 4, 5, numpy.nan]).na_value is numpy.nan

	assert not numpy.any(TemperatureArray([1, 2, 3, 4, 5]).isna())
	assert not numpy.any(TemperatureArray([0, 1, 2, 3, 4]).isna())
	assert not numpy.any(TemperatureArray([2, 3, 4, 5, 6]).isna())
	assert numpy.any(TemperatureArray([2, 3, 4, 5, numpy.nan]).isna())
	assert TemperatureArray([2, 3, 4, 5, numpy.nan]).isna()[4]
