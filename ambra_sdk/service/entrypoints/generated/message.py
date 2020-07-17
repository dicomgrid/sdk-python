""" Message.

Do not edit this file by hand.
This is generated by parsing api.html service doc.
"""
from ambra_sdk.exceptions.service import FilterNotFound
from ambra_sdk.exceptions.service import InvalidCondition
from ambra_sdk.exceptions.service import InvalidField
from ambra_sdk.exceptions.service import InvalidSortField
from ambra_sdk.exceptions.service import InvalidSortOrder
from ambra_sdk.exceptions.service import MissingFields
from ambra_sdk.exceptions.service import NotFound
from ambra_sdk.exceptions.service import NotPermitted
from ambra_sdk.service.query import QueryO
from ambra_sdk.service.query import QueryOPSF

class Message:
    """Message."""

    def __init__(self, api):
        self._api = api

    
    def list(
        self,
    ):
        """List.
        """
        request_data = {
        }
	
        errors_mapping = {}
        errors_mapping[('FILTER_NOT_FOUND', None)] = FilterNotFound('The filter can not be found. The error_subtype will hold the filter UUID')
        errors_mapping[('INVALID_CONDITION', None)] = InvalidCondition('The condition is not support. The error_subtype will hold the filter expression this applies to')
        errors_mapping[('INVALID_FIELD', None)] = InvalidField('The field is not valid for this object. The error_subtype will hold the filter expression this applies to')
        errors_mapping[('INVALID_SORT_FIELD', None)] = InvalidSortField('The field is not valid for this object. The error_subtype will hold the field name this applies to')
        errors_mapping[('INVALID_SORT_ORDER', None)] = InvalidSortOrder('The sort order for the field is invalid. The error_subtype will hold the field name this applies to')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        query_data = {
            'api': self._api,
            'url': '/message/list',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        query_data['paginated_field'] = 'messages'
        return QueryOPSF(**query_data)
    
    def add(
        self,
        body,
        account_id=None,
        email=None,
        group_id=None,
        location_id=None,
        namespace_id=None,
        parent_id=None,
        share_code=None,
        study_id=None,
        subject=None,
        user_id=None,
    ):
        """Add.
        :param body: The body of the message
        :param account_id: account_id
        :param email: email
        :param group_id: group_id
        :param location_id: location_id
        :param namespace_id: namespace_id
        :param parent_id: The uuid of the parent message (optional)
        :param share_code: share_code
        :param study_id: study_id
        :param subject: The subject of the message (optional)
        :param user_id: user_id

        Notes:
        (namespace_id OR user_id OR group_id OR location_id OR account_id OR email OR share_code OR study_id) - The namespace, entity, email, share code or study to send the message to
        """
        request_data = {
           'account_id': account_id,
           'body': body,
           'email': email,
           'group_id': group_id,
           'location_id': location_id,
           'namespace_id': namespace_id,
           'parent_id': parent_id,
           'share_code': share_code,
           'study_id': study_id,
           'subject': subject,
           'user_id': user_id,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The recipient or the parent message cannot be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to send to the recipient')
        query_data = {
            'api': self._api,
            'url': '/message/add',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def get(
        self,
        uuid,
    ):
        """Get.
        :param uuid: Id of the message
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The message can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view this message')
        query_data = {
            'api': self._api,
            'url': '/message/get',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def delete(
        self,
        uuid,
    ):
        """Delete.
        :param uuid: Id of the message
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The message can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to delete this message')
        query_data = {
            'api': self._api,
            'url': '/message/delete',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def count(
        self,
        reset=None,
    ):
        """Count.
        :param reset: Flag to reset counter back to zero (optional)
        """
        request_data = {
           'reset': reset,
        }
	
        errors_mapping = {}
        query_data = {
            'api': self._api,
            'url': '/message/count',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    