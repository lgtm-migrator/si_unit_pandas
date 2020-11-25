# 3rd party
import pandas  # type: ignore
from domdf_python_tools.testing import check_file_regression
from pandas._testing import assert_frame_equal  # type: ignore
from pytest_regressions.file_regression import FileRegressionFixture

# this package
import si_unit_pandas


def test_output(file_regression: FileRegressionFixture):
	s = pandas.Series(si_unit_pandas.TemperatureArray([1, 2, 3]))
	result = pandas.DataFrame(s)
	expected = pandas.DataFrame({0: s})
	assert_frame_equal(result, expected)

	check_file_regression(str(expected), file_regression)
