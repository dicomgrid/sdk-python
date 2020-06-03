""" Terminology.

Do not edit this file by hand.
This is generated by parsing api.html service doc.
"""
from ambra_sdk.exceptions.service import MissingFields
from ambra_sdk.exceptions.service import NoValue
from ambra_sdk.exceptions.service import NotFound
from ambra_sdk.exceptions.service import NotPermitted
from ambra_sdk.exceptions.service import NotSysadminOrSupport
from ambra_sdk.service.query import QueryO

class Terminology:
    """Terminology."""

    def __init__(self, api):
        self._api = api

    
    def account_overrides(
        self,
        account_id=None,
        phi_namespace=None,
        storage_namespace=None,
        study_uid=None,
        vanity=None,
    ):
        """Account overrides.
        :param account_id: account_id
        :param phi_namespace: phi_namespace
        :param storage_namespace: storage_namespace
        :param study_uid: study_uid
        :param vanity: vanity

        Notes:
        (account_id OR vanity OR study_uid AND storage_namespace AND phi_namespace) - The uuid or vanity name of the account or study triplet to apply any account overrides for (optional)
        """
        request_data = {
           'account_id': account_id,
           'study_uid': study_uid,
           'vanity': vanity,
           'storage_namespace': storage_namespace,
           'phi_namespace': phi_namespace,
        }
	
        errors_mapping = {}
        errors_mapping['MISSING_FIELDS'] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping['NOT_FOUND'] = NotFound('The account or vanity was not found')
        query_data = {
            'api': self._api,
            'url': '/terminology/account/overrides',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def tags(
        self,
        language,
        account_id=None,
        phi_namespace=None,
        storage_namespace=None,
        study_uid=None,
        tags=None,
        vanity=None,
    ):
        """Tags.
        :param language: The ISO 639-1 language code
        :param account_id: account_id
        :param phi_namespace: phi_namespace
        :param storage_namespace: storage_namespace
        :param study_uid: study_uid
        :param tags: A comma separated list of the terminology tags to look up (optional)
        :param vanity: vanity

        Notes:
        (account_id OR vanity OR study_uid AND storage_namespace AND phi_namespace) - The uuid or vanity name of the account or study triplet to apply any account overrides for (optional)
        """
        request_data = {
           'account_id': account_id,
           'study_uid': study_uid,
           'vanity': vanity,
           'language': language,
           'tags': tags,
           'storage_namespace': storage_namespace,
           'phi_namespace': phi_namespace,
        }
	
        errors_mapping = {}
        errors_mapping['MISSING_FIELDS'] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        query_data = {
            'api': self._api,
            'url': '/terminology/tags',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': False,
        }
        return QueryO(**query_data)
    
    def set(
        self,
        language,
        tag,
        value,
        account_id=None,
        vanity=None,
    ):
        """Set.
        :param language: The ISO 639-1 language code
        :param tag: The tag to set
        :param value: The value of the tag. If this is empty the tag is deleted
        :param account_id: The uuid of the account to apply the tag for (optional)
        :param vanity: Vanity to apply the tag for (optional)
        """
        request_data = {
           'tag': tag,
           'vanity': vanity,
           'language': language,
           'value': value,
           'account_id': account_id,
        }
	
        errors_mapping = {}
        errors_mapping['MISSING_FIELDS'] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping['NOT_FOUND'] = NotFound('The account was not found')
        errors_mapping['NOT_PERMITTED'] = NotPermitted('The user is not an account administrator  and is trying to set account tags')
        errors_mapping['NOT_SYSADMIN_OR_SUPPORT'] = NotSysadminOrSupport('The user is not a sysadmin or support user and is trying to set global tags')
        errors_mapping['NO_VALUE'] = NoValue('The value parameter was not passed')
        query_data = {
            'api': self._api,
            'url': '/terminology/set',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def list(
        self,
        language,
        tags,
        account_id=None,
        vanity=None,
    ):
        """List.
        :param language: The ISO 639-1 language code
        :param tags: A comma separated list of the terminology tags to look up
        :param account_id: account_id
        :param vanity: vanity

        Notes:
        (account_id OR vanity) - The uuid or vanity name of the account to apply any account overrides for (optional)
        """
        request_data = {
           'vanity': vanity,
           'language': language,
           'tags': tags,
           'account_id': account_id,
        }
	
        errors_mapping = {}
        errors_mapping['MISSING_FIELDS'] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        query_data = {
            'api': self._api,
            'url': '/terminology/list',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': False,
        }
        return QueryO(**query_data)
    
    def i18next(
        self,
        lng,
        account_id=None,
        vanity=None,
    ):
        """I18next.
        :param lng: The language code
        :param account_id: account_id
        :param vanity: vanity

        Notes:
        (account_id OR vanity) - The uuid or vanity name of the account to apply any account overrides for (optional)
        """
        request_data = {
           'lng': lng,
           'vanity': vanity,
           'account_id': account_id,
        }
	
        errors_mapping = {}
        errors_mapping['MISSING_FIELDS'] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        query_data = {
            'api': self._api,
            'url': '/terminology/i18next',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': False,
        }
        return QueryO(**query_data)
    