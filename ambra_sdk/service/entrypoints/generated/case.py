""" Case.

Do not edit this file by hand.
This is generated by parsing api.html service doc.
"""
from ambra_sdk.exceptions.service import FilterNotFound
from ambra_sdk.exceptions.service import InvalidCaseStatus
from ambra_sdk.exceptions.service import InvalidCondition
from ambra_sdk.exceptions.service import InvalidCustomfield
from ambra_sdk.exceptions.service import InvalidField
from ambra_sdk.exceptions.service import InvalidSortField
from ambra_sdk.exceptions.service import InvalidSortOrder
from ambra_sdk.exceptions.service import Locked
from ambra_sdk.exceptions.service import MissingFields
from ambra_sdk.exceptions.service import NotFound
from ambra_sdk.exceptions.service import NotInAccount
from ambra_sdk.exceptions.service import NotPermitted
from ambra_sdk.service.query import QueryO
from ambra_sdk.service.query import AsyncQueryO
from ambra_sdk.service.query import QueryOPSF
from ambra_sdk.service.query import AsyncQueryOPSF

class Case:
    """Case."""

    def __init__(self, api):
        self._api = api

    
    def get(
        self,
        uuid,
    ):
        """Get.

        :param uuid: The case uuid
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The case can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view this case')
        query_data = {
            'api': self._api,
            'url': '/case/get',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def set(
        self,
        uuid,
        assigned_admin_id=None,
        assigned_medical_id=None,
        case_status=None,
        closed=None,
        completed=None,
        customfield_param=None,
        name=None,
        submitted=None,
    ):
        """Set.

        :param uuid: The case uuid
        :param assigned_admin_id: Id of the admin user assigned to the case (optional)
        :param assigned_medical_id: Id of the medical user assigned to the case (optional)
        :param case_status: The case status (optional)
        :param closed: Flag if the case is closed (optional)
        :param completed: Flag if the case is completed (optional)
        :param customfield_param: Custom field(s) (optional)
        :param name: case name (optional)
        :param submitted: Flag if the case is submitted (optional)
        """
        request_data = {
           'assigned_admin_id': assigned_admin_id,
           'assigned_medical_id': assigned_medical_id,
           'case_status': case_status,
           'closed': closed,
           'completed': completed,
           'name': name,
           'submitted': submitted,
           'uuid': uuid,
        }
        if customfield_param is not None:
            customfield_param_dict = {'{prefix}{k}'.format(prefix='customfield-', k=k): v for k,v in customfield_param.items()}
            request_data.update(customfield_param_dict)
	
        errors_mapping = {}
        errors_mapping[('INVALID_CASE_STATUS', None)] = InvalidCaseStatus('Invalid case status')
        errors_mapping[('INVALID_CUSTOMFIELD', None)] = InvalidCustomfield('Invalid custom field(s) name or value were passed. The error_subtype holds an array of the error details')
        errors_mapping[('LOCKED', None)] = Locked('The case is locked by another user')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The case or assigned user can not be found')
        errors_mapping[('NOT_IN_ACCOUNT', None)] = NotInAccount('The assigned user is not in the account')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to edit the case')
        query_data = {
            'api': self._api,
            'url': '/case/set',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def return_method(
        self,
        reason,
        uuid,
    ):
        """Return.

        :param reason: The reason the case was returned
        :param uuid: The case uuid
        """
        request_data = {
           'reason': reason,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('NOT_FOUND', None)] = NotFound('The case can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to return the case')
        query_data = {
            'api': self._api,
            'url': '/case/return',
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

        :param uuid: The case uuid
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The case can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to delete the case')
        query_data = {
            'api': self._api,
            'url': '/case/delete',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def list(
        self,
        account_id=None,
    ):
        """List.

        :param account_id: uuid of the account (optional)
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
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view cases in this account')
        query_data = {
            'api': self._api,
            'url': '/case/list',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        query_data['paginated_field'] = 'cases'
        return QueryOPSF(**query_data)
    
    def attach(
        self,
        study_id,
        uuid,
        detach=None,
    ):
        """Attach.

        :param study_id: Study uuid
        :param uuid: Case uuid
        :param detach: Flag to detach the study from the case (optional)
        """
        request_data = {
           'detach': detach,
           'study_id': study_id,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The case or study can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to do this')
        query_data = {
            'api': self._api,
            'url': '/case/attach',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    


class AsyncCase:
    """AsyncCase."""

    def __init__(self, api):
        self._api = api

    
    def get(
        self,
        uuid,
    ):
        """Get.

        :param uuid: The case uuid
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The case can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view this case')
        query_data = {
            'api': self._api,
            'url': '/case/get',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return AsyncQueryO(**query_data)
    
    def set(
        self,
        uuid,
        assigned_admin_id=None,
        assigned_medical_id=None,
        case_status=None,
        closed=None,
        completed=None,
        customfield_param=None,
        name=None,
        submitted=None,
    ):
        """Set.

        :param uuid: The case uuid
        :param assigned_admin_id: Id of the admin user assigned to the case (optional)
        :param assigned_medical_id: Id of the medical user assigned to the case (optional)
        :param case_status: The case status (optional)
        :param closed: Flag if the case is closed (optional)
        :param completed: Flag if the case is completed (optional)
        :param customfield_param: Custom field(s) (optional)
        :param name: case name (optional)
        :param submitted: Flag if the case is submitted (optional)
        """
        request_data = {
           'assigned_admin_id': assigned_admin_id,
           'assigned_medical_id': assigned_medical_id,
           'case_status': case_status,
           'closed': closed,
           'completed': completed,
           'name': name,
           'submitted': submitted,
           'uuid': uuid,
        }
        if customfield_param is not None:
            customfield_param_dict = {'{prefix}{k}'.format(prefix='customfield-', k=k): v for k,v in customfield_param.items()}
            request_data.update(customfield_param_dict)
	
        errors_mapping = {}
        errors_mapping[('INVALID_CASE_STATUS', None)] = InvalidCaseStatus('Invalid case status')
        errors_mapping[('INVALID_CUSTOMFIELD', None)] = InvalidCustomfield('Invalid custom field(s) name or value were passed. The error_subtype holds an array of the error details')
        errors_mapping[('LOCKED', None)] = Locked('The case is locked by another user')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The case or assigned user can not be found')
        errors_mapping[('NOT_IN_ACCOUNT', None)] = NotInAccount('The assigned user is not in the account')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to edit the case')
        query_data = {
            'api': self._api,
            'url': '/case/set',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return AsyncQueryO(**query_data)
    
    def return_method(
        self,
        reason,
        uuid,
    ):
        """Return.

        :param reason: The reason the case was returned
        :param uuid: The case uuid
        """
        request_data = {
           'reason': reason,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('NOT_FOUND', None)] = NotFound('The case can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to return the case')
        query_data = {
            'api': self._api,
            'url': '/case/return',
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

        :param uuid: The case uuid
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The case can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to delete the case')
        query_data = {
            'api': self._api,
            'url': '/case/delete',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return AsyncQueryO(**query_data)
    
    def list(
        self,
        account_id=None,
    ):
        """List.

        :param account_id: uuid of the account (optional)
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
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view cases in this account')
        query_data = {
            'api': self._api,
            'url': '/case/list',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        query_data['paginated_field'] = 'cases'
        return AsyncQueryOPSF(**query_data)
    
    def attach(
        self,
        study_id,
        uuid,
        detach=None,
    ):
        """Attach.

        :param study_id: Study uuid
        :param uuid: Case uuid
        :param detach: Flag to detach the study from the case (optional)
        """
        request_data = {
           'detach': detach,
           'study_id': study_id,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The case or study can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to do this')
        query_data = {
            'api': self._api,
            'url': '/case/attach',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return AsyncQueryO(**query_data)
    