""" Setting.

Do not edit this file by hand.
This is generated by parsing api.html service doc.
"""
from ambra_sdk.exceptions.service import MissingFields
from ambra_sdk.service.query import QueryO
from ambra_sdk.service.query import AsyncQueryO

class Setting:
    """Setting."""

    def __init__(self, api):
        self._api = api

    
    def set(
        self,
        key,
        value,
        user_id=None,
    ):
        """Set.

        :param key: The key to store the value under. If the key name begins with temp_ it is only available for the session.
        :param value: The value to store
        :param user_id: A sysadmin user can set the value for a specific user (optional)
        """
        request_data = {
           'key': key,
           'user_id': user_id,
           'value': value,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        query_data = {
            'api': self._api,
            'url': '/setting/set',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def get(
        self,
        key,
        user_id=None,
    ):
        """Get.

        :param key: The key to get
        :param user_id: A sysadmin user can get the value for a specific user (optional)
        """
        request_data = {
           'key': key,
           'user_id': user_id,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        query_data = {
            'api': self._api,
            'url': '/setting/get',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def get_all(
        self,
    ):
        """Get all.

        """
        request_data = {
        }
	
        errors_mapping = {}
        query_data = {
            'api': self._api,
            'url': '/setting/get/all',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    


class AsyncSetting:
    """AsyncSetting."""

    def __init__(self, api):
        self._api = api

    
    def set(
        self,
        key,
        value,
        user_id=None,
    ):
        """Set.

        :param key: The key to store the value under. If the key name begins with temp_ it is only available for the session.
        :param value: The value to store
        :param user_id: A sysadmin user can set the value for a specific user (optional)
        """
        request_data = {
           'key': key,
           'user_id': user_id,
           'value': value,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        query_data = {
            'api': self._api,
            'url': '/setting/set',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return AsyncQueryO(**query_data)
    
    def get(
        self,
        key,
        user_id=None,
    ):
        """Get.

        :param key: The key to get
        :param user_id: A sysadmin user can get the value for a specific user (optional)
        """
        request_data = {
           'key': key,
           'user_id': user_id,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        query_data = {
            'api': self._api,
            'url': '/setting/get',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return AsyncQueryO(**query_data)
    
    def get_all(
        self,
    ):
        """Get all.

        """
        request_data = {
        }
	
        errors_mapping = {}
        query_data = {
            'api': self._api,
            'url': '/setting/get/all',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return AsyncQueryO(**query_data)
    