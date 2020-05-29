"""
Custom Temperature dtype for pandas
"""

from .temperature_array import (
	CelsiusType,
	TemperatureArray,
	)

from .parser import to_temperature

__version__ = "0.0.1"

__all__ = [
		'__version__',
		'TemperatureArray',
		'CelsiusType',
		'to_temperature',
		]
