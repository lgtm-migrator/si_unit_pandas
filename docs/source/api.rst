API
===

.. currentmodule:: cyberpandas

Cyberpandas provides two extension types, :class:`TemperatureArray` and :class:`MACArray`.

:class:`IP Array`
-----------------

.. autoclass:: TemperatureArray

Constructors
""""""""""""

The class constructor is flexible, and accepts integers, strings, or bytes.
Dedicated alternate constructors are also available.

.. automethod:: TemperatureArray.from_pyints
.. automethod:: TemperatureArray.from_bytes

Finally, the top-level ``ip_range`` method can be used.

.. autofunction:: ip_range

Serialization
"""""""""""""

Convert the TemperatureArray to various formats.

.. automethod:: TemperatureArray.to_pyipaddress
.. automethod:: TemperatureArray.to_pyints
.. automethod:: TemperatureArray.to_bytes


Methods
"""""""

Various methods that are useful for pandas. When a Series contains
an TemperatureArray, calling the Series method will dispatch to these methods.

.. automethod:: TemperatureArray.take
.. automethod:: TemperatureArray.unique
.. automethod:: TemperatureArray.isin
.. automethod:: TemperatureArray.isna

IP Address Attributes
"""""""""""""""""""""

IP addresss-specific attributes.

.. autoattribute:: TemperatureArray.is_ipv4
.. autoattribute:: TemperatureArray.is_ipv6
.. autoattribute:: TemperatureArray.version
.. autoattribute:: TemperatureArray.is_multicast
.. autoattribute:: TemperatureArray.is_private
.. autoattribute:: TemperatureArray.is_global
.. autoattribute:: TemperatureArray.is_unspecified
.. autoattribute:: TemperatureArray.is_reserved
.. autoattribute:: TemperatureArray.is_loopback
.. autoattribute:: TemperatureArray.is_link_local
.. automethod:: TemperatureArray.netmask
.. automethod:: TemperatureArray.hostmask
.. automethod:: TemperatureArray.mask



:class:`MACArray`
-----------------
utofun
.. autoclass:: MACArray
