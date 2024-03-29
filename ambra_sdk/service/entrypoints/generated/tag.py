""" Tag.

Do not edit this file by hand.
This is generated by parsing api.html service doc.
"""
from ambra_sdk.exceptions.service import FilterNotFound
from ambra_sdk.exceptions.service import InvalidCondition
from ambra_sdk.exceptions.service import InvalidField
from ambra_sdk.exceptions.service import InvalidObject
from ambra_sdk.exceptions.service import InvalidSortField
from ambra_sdk.exceptions.service import InvalidSortOrder
from ambra_sdk.exceptions.service import MissingFields
from ambra_sdk.exceptions.service import NotFound
from ambra_sdk.exceptions.service import NotPermitted
from ambra_sdk.service.query import QueryO
from ambra_sdk.service.query import AsyncQueryO
from ambra_sdk.service.query import QueryOPSF
from ambra_sdk.service.query import AsyncQueryOPSF

class Tag:
    """Tag."""

    def __init__(self, api):
        self._api = api

    
    def list(
        self,
        object,
    ):
        """List.

        :param object: Object class (Study|User_account|Group|Location|Account|Patient|Case|Order|Message)
        """
        request_data = {
           'object': object,
        }
	
        errors_mapping = {}
        errors_mapping[('FILTER_NOT_FOUND', None)] = FilterNotFound('The filter can not be found. The error_subtype will hold the filter UUID')
        errors_mapping[('INVALID_CONDITION', None)] = InvalidCondition('The condition is not support. The error_subtype will hold the filter expression this applies to')
        errors_mapping[('INVALID_FIELD', None)] = InvalidField('The field is not valid for this object. The error_subtype will hold the filter expression this applies to')
        errors_mapping[('INVALID_SORT_FIELD', None)] = InvalidSortField('The field is not valid for this object. The error_subtype will hold the field name this applies to')
        errors_mapping[('INVALID_SORT_ORDER', None)] = InvalidSortOrder('The sort order for the field is invalid. The error_subtype will hold the field name this applies to')
        query_data = {
            'api': self._api,
            'url': '/tag/list',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        query_data['paginated_field'] = 'tags'
        return QueryOPSF(**query_data)
    
    def add(
        self,
        object,
        object_id,
        tag,
    ):
        """Add.

        :param object: Object class to apply it to (Study|User_account|Group|Location|Account|Patient|Case|Order|Message|Query)
        :param object_id: UUID of the object
        :param tag: Value of the tag
        """
        request_data = {
           'object': object,
           'object_id': object_id,
           'tag': tag,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_OBJECT', None)] = InvalidObject('The object type is invalid')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The object was not found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to tag this object')
        query_data = {
            'api': self._api,
            'url': '/tag/add',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def delete(
        self,
        object,
        object_id,
        tag,
    ):
        """Delete.

        :param object: Object class to apply it to (Study|User_account|Group|Location|Account|Patient|Case|Order)
        :param object_id: UUID of the object
        :param tag: Value of the tag
        """
        request_data = {
           'object': object,
           'object_id': object_id,
           'tag': tag,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_OBJECT', None)] = InvalidObject('The object type is invalid')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The object was not found')
        query_data = {
            'api': self._api,
            'url': '/tag/delete',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    


class AsyncTag:
    """AsyncTag."""

    def __init__(self, api):
        self._api = api

    
    def list(
        self,
        object,
    ):
        """List.

        :param object: Object class (Study|User_account|Group|Location|Account|Patient|Case|Order|Message)
        """
        request_data = {
           'object': object,
        }
	
        errors_mapping = {}
        errors_mapping[('FILTER_NOT_FOUND', None)] = FilterNotFound('The filter can not be found. The error_subtype will hold the filter UUID')
        errors_mapping[('INVALID_CONDITION', None)] = InvalidCondition('The condition is not support. The error_subtype will hold the filter expression this applies to')
        errors_mapping[('INVALID_FIELD', None)] = InvalidField('The field is not valid for this object. The error_subtype will hold the filter expression this applies to')
        errors_mapping[('INVALID_SORT_FIELD', None)] = InvalidSortField('The field is not valid for this object. The error_subtype will hold the field name this applies to')
        errors_mapping[('INVALID_SORT_ORDER', None)] = InvalidSortOrder('The sort order for the field is invalid. The error_subtype will hold the field name this applies to')
        query_data = {
            'api': self._api,
            'url': '/tag/list',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        query_data['paginated_field'] = 'tags'
        return AsyncQueryOPSF(**query_data)
    
    def add(
        self,
        object,
        object_id,
        tag,
    ):
        """Add.

        :param object: Object class to apply it to (Study|User_account|Group|Location|Account|Patient|Case|Order|Message|Query)
        :param object_id: UUID of the object
        :param tag: Value of the tag
        """
        request_data = {
           'object': object,
           'object_id': object_id,
           'tag': tag,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_OBJECT', None)] = InvalidObject('The object type is invalid')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The object was not found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to tag this object')
        query_data = {
            'api': self._api,
            'url': '/tag/add',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return AsyncQueryO(**query_data)
    
    def delete(
        self,
        object,
        object_id,
        tag,
    ):
        """Delete.

        :param object: Object class to apply it to (Study|User_account|Group|Location|Account|Patient|Case|Order)
        :param object_id: UUID of the object
        :param tag: Value of the tag
        """
        request_data = {
           'object': object,
           'object_id': object_id,
           'tag': tag,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_OBJECT', None)] = InvalidObject('The object type is invalid')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The object was not found')
        query_data = {
            'api': self._api,
            'url': '/tag/delete',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return AsyncQueryO(**query_data)
    