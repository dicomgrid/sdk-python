""" Site.

Do not edit this file by hand.
This is generated by parsing api.html service doc.
"""
from ambra_sdk.exceptions.service import AlreadyExists
from ambra_sdk.exceptions.service import DifferentAccounts
from ambra_sdk.exceptions.service import FilterNotFound
from ambra_sdk.exceptions.service import InvalidCondition
from ambra_sdk.exceptions.service import InvalidField
from ambra_sdk.exceptions.service import InvalidFlag
from ambra_sdk.exceptions.service import InvalidSortField
from ambra_sdk.exceptions.service import InvalidSortOrder
from ambra_sdk.exceptions.service import MissingFields
from ambra_sdk.exceptions.service import NestedSatelliteSite
from ambra_sdk.exceptions.service import NotFound
from ambra_sdk.exceptions.service import NotPermitted
from ambra_sdk.exceptions.service import UserNotFound
from ambra_sdk.service.query import QueryO
from ambra_sdk.service.query import AsyncQueryO
from ambra_sdk.service.query import QueryOPSF
from ambra_sdk.service.query import AsyncQueryOPSF

class Site:
    """Site."""

    def __init__(self, api):
        self._api = api

    
    def list(
        self,
        account_id,
    ):
        """List.

        :param account_id: uuid of the account
        """
        request_data = {
           'account_id': account_id,
        }
	
        errors_mapping = {}
        errors_mapping[('FILTER_NOT_FOUND', None)] = FilterNotFound('The filter can not be found. The error_subtype will hold the filter UUID')
        errors_mapping[('INVALID_CONDITION', None)] = InvalidCondition('The condition is not support. The error_subtype will hold the filter expression this applies to')
        errors_mapping[('INVALID_FIELD', None)] = InvalidField('The field is not valid for this object. The error_subtype will hold the filter expression this applies to')
        errors_mapping[('INVALID_SORT_FIELD', None)] = InvalidSortField('The field is not valid for this object. The error_subtype will hold the field name this applies to')
        errors_mapping[('INVALID_SORT_ORDER', None)] = InvalidSortOrder('The sort order for the field is invalid. The error_subtype will hold the field name this applies to')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The account can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view sites in this account')
        query_data = {
            'api': self._api,
            'url': '/site/list',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        query_data['paginated_field'] = 'sites'
        return QueryOPSF(**query_data)
    
    def add(
        self,
        account_id,
        name,
        city=None,
        site_id=None,
        state=None,
        zip=None,
    ):
        """Add.

        :param account_id: uuid of the account to add them to
        :param name: The sites name
        :param city: The city the site is located in (optional)
        :param site_id: The site to attach them to as a satellite site (optional)
        :param state: The state code of the site (optional)
        :param zip: The zip code of the site (optional)
        """
        request_data = {
           'account_id': account_id,
           'city': city,
           'name': name,
           'site_id': site_id,
           'state': state,
           'zip': zip,
        }
	
        errors_mapping = {}
        errors_mapping[('DIFFERENT_ACCOUNTS', None)] = DifferentAccounts('The site and satellite sites are from different accounts')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NESTED_SATELLITE_SITE', None)] = NestedSatelliteSite('The satellite site has its satellite sites')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The object was not found. The error_subtype holds the type of object not found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to add a site to the account')
        query_data = {
            'api': self._api,
            'url': '/site/add',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def set(
        self,
        uuid,
        city=None,
        inactive=None,
        name=None,
        site_id=None,
        state=None,
        zip=None,
    ):
        """Set.

        :param uuid: The site uuid
        :param city: The city the site is located in (optional)
        :param inactive: Flag if the site is actively used. Might be used to filter out inactive sites (optional)
        :param name: The sites name (optional)
        :param site_id: The site to attach them to as a satellite site (optional)
        :param state: The state code of the site (optional)
        :param zip: The zip code of the site (optional)
        """
        request_data = {
           'city': city,
           'inactive': inactive,
           'name': name,
           'site_id': site_id,
           'state': state,
           'uuid': uuid,
           'zip': zip,
        }
	
        errors_mapping = {}
        errors_mapping[('DIFFERENT_ACCOUNTS', None)] = DifferentAccounts('The site and satellite sites are from different accounts')
        errors_mapping[('INVALID_FLAG', None)] = InvalidFlag('An invalid flag was passed. The error_subtype holds the name of the invalid flag')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NESTED_SATELLITE_SITE', None)] = NestedSatelliteSite('The satellite site has its satellite sites')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The site can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to edit the site')
        query_data = {
            'api': self._api,
            'url': '/site/set',
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

        :param uuid: The site uuid
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The site can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view this site')
        query_data = {
            'api': self._api,
            'url': '/site/get',
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

        :param uuid: The site uuid
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The site can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to delete the site')
        query_data = {
            'api': self._api,
            'url': '/site/delete',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def user_add(
        self,
        role_name,
        uuid,
        email=None,
        user_id=None,
    ):
        """User add.

        :param role_name: The role name that should be used for the user in groups
        :param uuid: The group id
        :param email: email
        :param user_id: user_id
        """
        request_data = {
           'email': email,
           'role_name': role_name,
           'user_id': user_id,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('ALREADY_EXISTS', None)] = AlreadyExists('The user is in the contact list already')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The site can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to add users to the site')
        errors_mapping[('USER_NOT_FOUND', None)] = UserNotFound('The user was not found')
        query_data = {
            'api': self._api,
            'url': '/site/user/add',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def user_set(
        self,
        uuid,
        email=None,
        role_name=None,
        user_id=None,
    ):
        """User set.

        :param uuid: The site id
        :param email: email
        :param role_name: The role name that should be used for the user in groups (optional)
        :param user_id: user_id
        """
        request_data = {
           'email': email,
           'role_name': role_name,
           'user_id': user_id,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The site can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to edit users in the site')
        errors_mapping[('USER_NOT_FOUND', None)] = UserNotFound('The user was not found in the contact list')
        query_data = {
            'api': self._api,
            'url': '/site/user/set',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def user_list(
        self,
        uuid,
    ):
        """User list.

        :param uuid: The site id
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('FILTER_NOT_FOUND', None)] = FilterNotFound('The filter can not be found. The error_subtype will hold the filter UUID')
        errors_mapping[('INVALID_CONDITION', None)] = InvalidCondition('The condition is not support. The error_subtype will hold the filter expression this applies to')
        errors_mapping[('INVALID_FIELD', None)] = InvalidField('The field is not valid for this object. The error_subtype will hold the filter expression this applies to')
        errors_mapping[('INVALID_SORT_FIELD', None)] = InvalidSortField('The field is not valid for this object. The error_subtype will hold the field name this applies to')
        errors_mapping[('INVALID_SORT_ORDER', None)] = InvalidSortOrder('The sort order for the field is invalid. The error_subtype will hold the field name this applies to')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The site can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted list the site contact list')
        query_data = {
            'api': self._api,
            'url': '/site/user/list',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        query_data['paginated_field'] = 'users'
        return QueryOPSF(**query_data)
    
    def user_delete(
        self,
        user_id,
        uuid,
    ):
        """User delete.

        :param user_id: Id of the user
        :param uuid: The site id
        """
        request_data = {
           'user_id': user_id,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The site can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to delete users from the contact list')
        errors_mapping[('USER_NOT_FOUND', None)] = UserNotFound('The user can not be found in the contact list')
        query_data = {
            'api': self._api,
            'url': '/site/user/delete',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    


class AsyncSite:
    """AsyncSite."""

    def __init__(self, api):
        self._api = api

    
    def list(
        self,
        account_id,
    ):
        """List.

        :param account_id: uuid of the account
        """
        request_data = {
           'account_id': account_id,
        }
	
        errors_mapping = {}
        errors_mapping[('FILTER_NOT_FOUND', None)] = FilterNotFound('The filter can not be found. The error_subtype will hold the filter UUID')
        errors_mapping[('INVALID_CONDITION', None)] = InvalidCondition('The condition is not support. The error_subtype will hold the filter expression this applies to')
        errors_mapping[('INVALID_FIELD', None)] = InvalidField('The field is not valid for this object. The error_subtype will hold the filter expression this applies to')
        errors_mapping[('INVALID_SORT_FIELD', None)] = InvalidSortField('The field is not valid for this object. The error_subtype will hold the field name this applies to')
        errors_mapping[('INVALID_SORT_ORDER', None)] = InvalidSortOrder('The sort order for the field is invalid. The error_subtype will hold the field name this applies to')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The account can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view sites in this account')
        query_data = {
            'api': self._api,
            'url': '/site/list',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        query_data['paginated_field'] = 'sites'
        return AsyncQueryOPSF(**query_data)
    
    def add(
        self,
        account_id,
        name,
        city=None,
        site_id=None,
        state=None,
        zip=None,
    ):
        """Add.

        :param account_id: uuid of the account to add them to
        :param name: The sites name
        :param city: The city the site is located in (optional)
        :param site_id: The site to attach them to as a satellite site (optional)
        :param state: The state code of the site (optional)
        :param zip: The zip code of the site (optional)
        """
        request_data = {
           'account_id': account_id,
           'city': city,
           'name': name,
           'site_id': site_id,
           'state': state,
           'zip': zip,
        }
	
        errors_mapping = {}
        errors_mapping[('DIFFERENT_ACCOUNTS', None)] = DifferentAccounts('The site and satellite sites are from different accounts')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NESTED_SATELLITE_SITE', None)] = NestedSatelliteSite('The satellite site has its satellite sites')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The object was not found. The error_subtype holds the type of object not found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to add a site to the account')
        query_data = {
            'api': self._api,
            'url': '/site/add',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return AsyncQueryO(**query_data)
    
    def set(
        self,
        uuid,
        city=None,
        inactive=None,
        name=None,
        site_id=None,
        state=None,
        zip=None,
    ):
        """Set.

        :param uuid: The site uuid
        :param city: The city the site is located in (optional)
        :param inactive: Flag if the site is actively used. Might be used to filter out inactive sites (optional)
        :param name: The sites name (optional)
        :param site_id: The site to attach them to as a satellite site (optional)
        :param state: The state code of the site (optional)
        :param zip: The zip code of the site (optional)
        """
        request_data = {
           'city': city,
           'inactive': inactive,
           'name': name,
           'site_id': site_id,
           'state': state,
           'uuid': uuid,
           'zip': zip,
        }
	
        errors_mapping = {}
        errors_mapping[('DIFFERENT_ACCOUNTS', None)] = DifferentAccounts('The site and satellite sites are from different accounts')
        errors_mapping[('INVALID_FLAG', None)] = InvalidFlag('An invalid flag was passed. The error_subtype holds the name of the invalid flag')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NESTED_SATELLITE_SITE', None)] = NestedSatelliteSite('The satellite site has its satellite sites')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The site can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to edit the site')
        query_data = {
            'api': self._api,
            'url': '/site/set',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return AsyncQueryO(**query_data)
    
    def get(
        self,
        uuid,
    ):
        """Get.

        :param uuid: The site uuid
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The site can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view this site')
        query_data = {
            'api': self._api,
            'url': '/site/get',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return AsyncQueryO(**query_data)
    
    def delete(
        self,
        uuid,
    ):
        """Delete.

        :param uuid: The site uuid
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The site can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to delete the site')
        query_data = {
            'api': self._api,
            'url': '/site/delete',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return AsyncQueryO(**query_data)
    
    def user_add(
        self,
        role_name,
        uuid,
        email=None,
        user_id=None,
    ):
        """User add.

        :param role_name: The role name that should be used for the user in groups
        :param uuid: The group id
        :param email: email
        :param user_id: user_id
        """
        request_data = {
           'email': email,
           'role_name': role_name,
           'user_id': user_id,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('ALREADY_EXISTS', None)] = AlreadyExists('The user is in the contact list already')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The site can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to add users to the site')
        errors_mapping[('USER_NOT_FOUND', None)] = UserNotFound('The user was not found')
        query_data = {
            'api': self._api,
            'url': '/site/user/add',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return AsyncQueryO(**query_data)
    
    def user_set(
        self,
        uuid,
        email=None,
        role_name=None,
        user_id=None,
    ):
        """User set.

        :param uuid: The site id
        :param email: email
        :param role_name: The role name that should be used for the user in groups (optional)
        :param user_id: user_id
        """
        request_data = {
           'email': email,
           'role_name': role_name,
           'user_id': user_id,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The site can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to edit users in the site')
        errors_mapping[('USER_NOT_FOUND', None)] = UserNotFound('The user was not found in the contact list')
        query_data = {
            'api': self._api,
            'url': '/site/user/set',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return AsyncQueryO(**query_data)
    
    def user_list(
        self,
        uuid,
    ):
        """User list.

        :param uuid: The site id
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('FILTER_NOT_FOUND', None)] = FilterNotFound('The filter can not be found. The error_subtype will hold the filter UUID')
        errors_mapping[('INVALID_CONDITION', None)] = InvalidCondition('The condition is not support. The error_subtype will hold the filter expression this applies to')
        errors_mapping[('INVALID_FIELD', None)] = InvalidField('The field is not valid for this object. The error_subtype will hold the filter expression this applies to')
        errors_mapping[('INVALID_SORT_FIELD', None)] = InvalidSortField('The field is not valid for this object. The error_subtype will hold the field name this applies to')
        errors_mapping[('INVALID_SORT_ORDER', None)] = InvalidSortOrder('The sort order for the field is invalid. The error_subtype will hold the field name this applies to')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The site can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted list the site contact list')
        query_data = {
            'api': self._api,
            'url': '/site/user/list',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        query_data['paginated_field'] = 'users'
        return AsyncQueryOPSF(**query_data)
    
    def user_delete(
        self,
        user_id,
        uuid,
    ):
        """User delete.

        :param user_id: Id of the user
        :param uuid: The site id
        """
        request_data = {
           'user_id': user_id,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The site can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to delete users from the contact list')
        errors_mapping[('USER_NOT_FOUND', None)] = UserNotFound('The user can not be found in the contact list')
        query_data = {
            'api': self._api,
            'url': '/site/user/delete',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return AsyncQueryO(**query_data)
    