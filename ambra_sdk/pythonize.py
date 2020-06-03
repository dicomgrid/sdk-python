"""Pythonization some names and fields."""
import types

FIELDS = types.MappingProxyType({
    'global': 'global_field',
    'type': 'type_field',
})

METHODS = types.MappingProxyType({
    'return': 'return_method',
})

PARAMS = types.MappingProxyType({
    'global': 'global_param',
    'limit.hl7': 'limit_hl7',
})
