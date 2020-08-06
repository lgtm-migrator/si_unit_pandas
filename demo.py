# this package
from si_unit_pandas.temperature_array import Celsius, TemperatureArray

# print(Celsius(24))
print(repr(Celsius(24)))

arr = TemperatureArray([Celsius(24), 25, 26.3, 27])
print(repr(arr))
print(arr[0])
print(type(arr[0]))
print(arr.take([2]))
arr.append(17)
for x in arr:
	print(x)
# # print(TemperatureArray([]).na_value)
#
# print(TemperatureArray((Celsius(24), 25)))
#
# print(arr.isin([24]))
#
# print(TemperatureArray([0]).isna())
# print(TemperatureArray([]).na_value)

# 3rd party
import pandas  # type: ignore

df = pandas.DataFrame({"Hour": [1, 2, 3, 4, 5], "Average Temperature": arr})
print(df)
# print(df["Average Temperature"].temperature.isin(5))

print(TemperatureArray(14))
print(TemperatureArray(14.5))
print(TemperatureArray("14.5"))
print(TemperatureArray("14"))

print(df.to_csv())
