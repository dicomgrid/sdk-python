"""Pythonization some names and fields."""
import types

FIELDS = types.MappingProxyType({
    'global': 'global_field',
    'type': 'type_field',
})

METHODS = types.MappingProxyType({
    'return': 'return_method',
})
