""" Qctask.

Do not edit this file by hand.
This is generated by parsing api.html service doc.
"""
from ambra_sdk.exceptions.service import InvalidInteger
from ambra_sdk.exceptions.service import InvalidTag
from ambra_sdk.exceptions.service import InvisibleQuery
from ambra_sdk.exceptions.service import MissingFields
from ambra_sdk.exceptions.service import NamespaceNotAccountRelated
from ambra_sdk.exceptions.service import NotFound
from ambra_sdk.exceptions.service import NotOwningNamespace
from ambra_sdk.exceptions.service import NotPermitted
from ambra_sdk.exceptions.service import Stale
from ambra_sdk.service.query import QueryO
from ambra_sdk.service.query import AsyncQueryO

class Qctask:
    """Qctask."""

    def __init__(self, api):
        self._api = api

    
    def add(
        self,
        namespace_id,
        priority,
        customfield_param=None,
        message=None,
        qctask_status=None,
        queries=None,
        query_id=None,
        studies=None,
        user_id=None,
    ):
        """Add.

        :param namespace_id: Id of the namespace assigned to the QC Task
        :param priority: QC Task priority
        :param customfield_param: Expected values are CUSTOMFIELD_UUID. Custom field(s) (optional)
        :param message: Explanatory message for the QC Task (optional)
        :param qctask_status: Status of the QC task, Open by default (Open|InProgress|Closed) (optional)
        :param queries: A JSON array of the query uuid(s) associate the QC Task to (optional)
        :param query_id: Id of the query to associate the QC Task to (optional)
        :param studies: A JSON array of the study uuid(s) (optional)
        :param user_id: Id of the user to assign the QC Task to (optional)
        """
        request_data = {
           'message': message,
           'namespace_id': namespace_id,
           'priority': priority,
           'qctask_status': qctask_status,
           'queries': queries,
           'query_id': query_id,
           'studies': studies,
           'user_id': user_id,
        }
        if customfield_param is not None:
            customfield_param_dict = {'{prefix}{k}'.format(prefix='customfield-', k=k): v for k,v in customfield_param.items()}
            request_data.update(customfield_param_dict)
	
        errors_mapping = {}
        errors_mapping[('INVALID_INTEGER', None)] = InvalidInteger('An invalid integer was passed. The error_subtype holds the name of the invalid integer')
        errors_mapping[('INVISIBLE_QUERY', None)] = InvisibleQuery('The passed Query is not visible to the user the QC Task is being assigned to')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NAMESPACE_NOT_ACCOUNT_RELATED', None)] = NamespaceNotAccountRelated('The assigned namespace is not associated with an Account (it is a PHR account)')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The object was not found. The error_subtype holds the type of object not found')
        errors_mapping[('NOT_OWNING_NAMESPACE', None)] = NotOwningNamespace('The assigned namespace is not an owning namespace for the passed Query')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to assign a QC Task to the namespace')
        query_data = {
            'api': self._api,
            'url': '/qctask/add',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def set(
        self,
        uuid,
        customfield_param=None,
        message=None,
        priority=None,
        queries=None,
        studies=None,
        user_id=None,
    ):
        """Set.

        :param uuid: The QC Task uuid
        :param customfield_param: Expected values are CUSTOMFIELD_UUID. Custom field(s) (optional)
        :param message: Explanatory message for the QC Task (optional)
        :param priority: QC Task priority (optional)
        :param queries: A JSON array of the query uuid(s) associate the QC Task to (optional)
        :param studies: A JSON array of the study uuid(s) (optional)
        :param user_id: Id of the user to assign the QC Task to (optional)
        """
        request_data = {
           'message': message,
           'priority': priority,
           'queries': queries,
           'studies': studies,
           'user_id': user_id,
           'uuid': uuid,
        }
        if customfield_param is not None:
            customfield_param_dict = {'{prefix}{k}'.format(prefix='customfield-', k=k): v for k,v in customfield_param.items()}
            request_data.update(customfield_param_dict)
	
        errors_mapping = {}
        errors_mapping[('INVALID_INTEGER', None)] = InvalidInteger('An invalid integer was passed. The error_subtype holds the name of the invalid integer')
        errors_mapping[('INVISIBLE_QUERY', None)] = InvisibleQuery('The passed Query is not visible to the user the QC Task is being assigned to')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The object was not found. The error_subtype holds the type of object not found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to edit the QC Task')
        query_data = {
            'api': self._api,
            'url': '/qctask/set',
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

        :param uuid: The QC Task uuid
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The QC Task can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view the QC Task')
        query_data = {
            'api': self._api,
            'url': '/qctask/get',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def status_set(
        self,
        new,
        old,
        uuid,
    ):
        """Status set.

        :param new: The new QC task status value (Open|InProgress|Closed)
        :param old: The old QC task status value
        :param uuid: QC task uuid
        """
        request_data = {
           'new': new,
           'old': old,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_TAG', None)] = InvalidTag('The QC task status new value is not a valid value')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The QC task can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to set the status for this QC task')
        errors_mapping[('STALE', None)] = Stale('The QC task status you have is stale')
        query_data = {
            'api': self._api,
            'url': '/qctask/status/set',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    


class AsyncQctask:
    """AsyncQctask."""

    def __init__(self, api):
        self._api = api

    
    def add(
        self,
        namespace_id,
        priority,
        customfield_param=None,
        message=None,
        qctask_status=None,
        queries=None,
        query_id=None,
        studies=None,
        user_id=None,
    ):
        """Add.

        :param namespace_id: Id of the namespace assigned to the QC Task
        :param priority: QC Task priority
        :param customfield_param: Expected values are CUSTOMFIELD_UUID. Custom field(s) (optional)
        :param message: Explanatory message for the QC Task (optional)
        :param qctask_status: Status of the QC task, Open by default (Open|InProgress|Closed) (optional)
        :param queries: A JSON array of the query uuid(s) associate the QC Task to (optional)
        :param query_id: Id of the query to associate the QC Task to (optional)
        :param studies: A JSON array of the study uuid(s) (optional)
        :param user_id: Id of the user to assign the QC Task to (optional)
        """
        request_data = {
           'message': message,
           'namespace_id': namespace_id,
           'priority': priority,
           'qctask_status': qctask_status,
           'queries': queries,
           'query_id': query_id,
           'studies': studies,
           'user_id': user_id,
        }
        if customfield_param is not None:
            customfield_param_dict = {'{prefix}{k}'.format(prefix='customfield-', k=k): v for k,v in customfield_param.items()}
            request_data.update(customfield_param_dict)
	
        errors_mapping = {}
        errors_mapping[('INVALID_INTEGER', None)] = InvalidInteger('An invalid integer was passed. The error_subtype holds the name of the invalid integer')
        errors_mapping[('INVISIBLE_QUERY', None)] = InvisibleQuery('The passed Query is not visible to the user the QC Task is being assigned to')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NAMESPACE_NOT_ACCOUNT_RELATED', None)] = NamespaceNotAccountRelated('The assigned namespace is not associated with an Account (it is a PHR account)')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The object was not found. The error_subtype holds the type of object not found')
        errors_mapping[('NOT_OWNING_NAMESPACE', None)] = NotOwningNamespace('The assigned namespace is not an owning namespace for the passed Query')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to assign a QC Task to the namespace')
        query_data = {
            'api': self._api,
            'url': '/qctask/add',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return AsyncQueryO(**query_data)
    
    def set(
        self,
        uuid,
        customfield_param=None,
        message=None,
        priority=None,
        queries=None,
        studies=None,
        user_id=None,
    ):
        """Set.

        :param uuid: The QC Task uuid
        :param customfield_param: Expected values are CUSTOMFIELD_UUID. Custom field(s) (optional)
        :param message: Explanatory message for the QC Task (optional)
        :param priority: QC Task priority (optional)
        :param queries: A JSON array of the query uuid(s) associate the QC Task to (optional)
        :param studies: A JSON array of the study uuid(s) (optional)
        :param user_id: Id of the user to assign the QC Task to (optional)
        """
        request_data = {
           'message': message,
           'priority': priority,
           'queries': queries,
           'studies': studies,
           'user_id': user_id,
           'uuid': uuid,
        }
        if customfield_param is not None:
            customfield_param_dict = {'{prefix}{k}'.format(prefix='customfield-', k=k): v for k,v in customfield_param.items()}
            request_data.update(customfield_param_dict)
	
        errors_mapping = {}
        errors_mapping[('INVALID_INTEGER', None)] = InvalidInteger('An invalid integer was passed. The error_subtype holds the name of the invalid integer')
        errors_mapping[('INVISIBLE_QUERY', None)] = InvisibleQuery('The passed Query is not visible to the user the QC Task is being assigned to')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The object was not found. The error_subtype holds the type of object not found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to edit the QC Task')
        query_data = {
            'api': self._api,
            'url': '/qctask/set',
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

        :param uuid: The QC Task uuid
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The QC Task can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view the QC Task')
        query_data = {
            'api': self._api,
            'url': '/qctask/get',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return AsyncQueryO(**query_data)
    
    def status_set(
        self,
        new,
        old,
        uuid,
    ):
        """Status set.

        :param new: The new QC task status value (Open|InProgress|Closed)
        :param old: The old QC task status value
        :param uuid: QC task uuid
        """
        request_data = {
           'new': new,
           'old': old,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_TAG', None)] = InvalidTag('The QC task status new value is not a valid value')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The QC task can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to set the status for this QC task')
        errors_mapping[('STALE', None)] = Stale('The QC task status you have is stale')
        query_data = {
            'api': self._api,
            'url': '/qctask/status/set',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return AsyncQueryO(**query_data)
    