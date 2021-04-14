""" Customcode.

Do not edit this file by hand.
This is generated by parsing api.html service doc.
"""
from ambra_sdk.exceptions.service import Already
from ambra_sdk.exceptions.service import FilterNotFound
from ambra_sdk.exceptions.service import InvalidCondition
from ambra_sdk.exceptions.service import InvalidField
from ambra_sdk.exceptions.service import InvalidLanguage
from ambra_sdk.exceptions.service import InvalidSortField
from ambra_sdk.exceptions.service import InvalidSortOrder
from ambra_sdk.exceptions.service import InvalidType
from ambra_sdk.exceptions.service import IsDeployed
from ambra_sdk.exceptions.service import MissingFields
from ambra_sdk.exceptions.service import NotFound
from ambra_sdk.exceptions.service import NotHash
from ambra_sdk.exceptions.service import NotPermitted
from ambra_sdk.exceptions.service import OneZipOnly
from ambra_sdk.service.query import QueryO
from ambra_sdk.service.query import QueryOPSF

class Customcode:
    """Customcode."""

    def __init__(self, api):
        self._api = api

    
    def add(
        self,
        code,
        language,
        name,
        type,
        settings=None,
        zip=None,
    ):
        """Add.
        :param code: The code
        :param language: Language of code (PYTHON)
        :param name: The name of the code
        :param type: Type of code (AI_CUSTOM_VALIDATION_CODE)
        :param settings: JSON hash of settings (optional)
        :param zip: Base64 encoded ZIP file (optional)
        """
        request_data = {
           'code': code,
           'language': language,
           'name': name,
           'settings': settings,
           'type': type,
           'zip': zip,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_LANGUAGE', None)] = InvalidLanguage('Invalid language')
        errors_mapping[('INVALID_TYPE', None)] = InvalidType('Invalid type')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_HASH', None)] = NotHash('The field is not a hash')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to add code')
        query_data = {
            'api': self._api,
            'url': '/customcode/add',
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
        :param uuid: The code uuid
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The code can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view this code')
        query_data = {
            'api': self._api,
            'url': '/customcode/get',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def set(
        self,
        uuid,
        code=None,
        name=None,
        settings=None,
        zip=None,
    ):
        """Set.
        :param uuid: The code uuid
        :param code: The code (optional)
        :param name: The name of the code (optional)
        :param settings: JSON hash of settings (optional)
        :param zip: Base64 encoded ZIP file (optional)
        """
        request_data = {
           'code': code,
           'name': name,
           'settings': settings,
           'uuid': uuid,
           'zip': zip,
        }
	
        errors_mapping = {}
        errors_mapping[('IS_DEPLOYED', None)] = IsDeployed('The code is deployed and can not be edited')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_HASH', None)] = NotHash('The field is not a hash')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to edit the code')
        errors_mapping[('ONE_ZIP_ONLY', None)] = OneZipOnly('Only one code with an attached zip can be deployed to the namespace')
        query_data = {
            'api': self._api,
            'url': '/customcode/set',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def zip(
        self,
        uuid,
    ):
        """Zip.
        :param uuid: The code uuid
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        query_data = {
            'api': self._api,
            'url': '/customcode/zip',
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
        :param uuid: The code uuid
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('IS_DEPLOYED', None)] = IsDeployed('The code is deployed and can not be deleted')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to delete the code')
        query_data = {
            'api': self._api,
            'url': '/customcode/delete',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
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
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view code in this account')
        query_data = {
            'api': self._api,
            'url': '/customcode/list',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        query_data['paginated_field'] = 'customcodes'
        return QueryOPSF(**query_data)
    
    def deploy(
        self,
        namespace_id,
        uuid,
    ):
        """Deploy.
        :param namespace_id: uuid of the namespace
        :param uuid: uuid of the customcode
        """
        request_data = {
           'namespace_id': namespace_id,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('ALREADY', None)] = Already('The code is already deployed for this namespace')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The namespace or customcode can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to deploy code in this namespace')
        query_data = {
            'api': self._api,
            'url': '/customcode/deploy',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def undeploy(
        self,
        deployment_id,
    ):
        """Undeploy.
        :param deployment_id: Deployment uuid
        """
        request_data = {
           'deployment_id': deployment_id,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The deployment can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to undeploy code in this namespace')
        query_data = {
            'api': self._api,
            'url': '/customcode/undeploy',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def deploy_get(
        self,
        uuid,
    ):
        """Deploy get.
        :param uuid: uuid of customcode deployment
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The customcode deployment can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to do this')
        query_data = {
            'api': self._api,
            'url': '/customcode/deploy/get',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def deploy_list(
        self,
        customcode_id=None,
        namespace_id=None,
    ):
        """Deploy list.
        :param customcode_id: customcode_id
        :param namespace_id: namespace_id
        """
        request_data = {
           'customcode_id': customcode_id,
           'namespace_id': namespace_id,
        }
	
        errors_mapping = {}
        errors_mapping[('FILTER_NOT_FOUND', None)] = FilterNotFound('The filter can not be found. The error_subtype will hold the filter UUID')
        errors_mapping[('INVALID_CONDITION', None)] = InvalidCondition('The condition is not support. The error_subtype will hold the filter expression this applies to')
        errors_mapping[('INVALID_FIELD', None)] = InvalidField('The field is not valid for this object. The error_subtype will hold the filter expression this applies to')
        errors_mapping[('INVALID_SORT_FIELD', None)] = InvalidSortField('The field is not valid for this object. The error_subtype will hold the field name this applies to')
        errors_mapping[('INVALID_SORT_ORDER', None)] = InvalidSortOrder('The sort order for the field is invalid. The error_subtype will hold the field name this applies to')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The namespace or customcode can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to do this')
        query_data = {
            'api': self._api,
            'url': '/customcode/deploy/list',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        query_data['paginated_field'] = 'deployments'
        return QueryOPSF(**query_data)
    