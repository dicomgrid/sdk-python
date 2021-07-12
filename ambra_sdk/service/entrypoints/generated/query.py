""" Query.

Do not edit this file by hand.
This is generated by parsing api.html service doc.
"""
from ambra_sdk.exceptions.service import FilterNotFound
from ambra_sdk.exceptions.service import InvalidCondition
from ambra_sdk.exceptions.service import InvalidField
from ambra_sdk.exceptions.service import InvalidGroup
from ambra_sdk.exceptions.service import InvalidSortField
from ambra_sdk.exceptions.service import InvalidSortOrder
from ambra_sdk.exceptions.service import InvalidTag
from ambra_sdk.exceptions.service import InvalidType
from ambra_sdk.exceptions.service import MissingFields
from ambra_sdk.exceptions.service import NotConfigured
from ambra_sdk.exceptions.service import NotFound
from ambra_sdk.exceptions.service import NotPermitted
from ambra_sdk.exceptions.service import NotPhantom
from ambra_sdk.exceptions.service import Stale
from ambra_sdk.exceptions.service import StudyQueryGroupChange
from ambra_sdk.exceptions.service import Thumbnail
from ambra_sdk.exceptions.service import TooBig
from ambra_sdk.service.query import QueryO
from ambra_sdk.service.query import AsyncQueryO
from ambra_sdk.service.query import QueryOPSF
from ambra_sdk.service.query import AsyncQueryOPSF

class Query:
    """Query."""

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
        query_data = {
            'api': self._api,
            'url': '/query/list',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        query_data['paginated_field'] = 'queries'
        return QueryOPSF(**query_data)
    
    def add(
        self,
        group_id,
        subject,
        body=None,
        customfield_param=None,
        notify=None,
        owner_namespace_id=None,
        owner_user_id=None,
        query_type=None,
        recipients=None,
        study_id=None,
    ):
        """Add.
        :param group_id: Id of the group associated to a trial site to add them to
        :param subject: Subject line of the query
        :param body: The query body (optional)
        :param customfield_param: Custom field(s) (optional)
        :param notify: Comma delimited list of the emails to be notified of the query events (optional)
        :param owner_namespace_id: The namespace owning the query. The account default from the default_query_owner_namespace account setting is used if not passed through the parameter (optional)
        :param owner_user_id: The user owning the query (optional)
        :param query_type: The query type (optional)
        :param recipients: JSON array of the user UUIDs to add to the query as recipients (optional)
        :param study_id: The study the query is related to (optional)
        """
        request_data = {
           'body': body,
           'group_id': group_id,
           'notify': notify,
           'owner_namespace_id': owner_namespace_id,
           'owner_user_id': owner_user_id,
           'query_type': query_type,
           'recipients': recipients,
           'study_id': study_id,
           'subject': subject,
        }
        if customfield_param is not None:
            customfield_param_dict = {'{prefix}{k}'.format(prefix='customfield-', k=k): v for k,v in customfield_param.items()}
            request_data.update(customfield_param_dict)
	
        errors_mapping = {}
        errors_mapping[('INVALID_GROUP', None)] = InvalidGroup('The group passed is not linked to a trial site')
        errors_mapping[('INVALID_TYPE', None)] = InvalidType('The passed type is not valid for the group and patient arm')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_CONFIGURED', None)] = NotConfigured('The group&#39;s account is not configured')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The object was not found. The error_subtype holds the type of object not found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to add a query to the namespace')
        query_data = {
            'api': self._api,
            'url': '/query/add',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def set(
        self,
        uuid,
        body=None,
        customfield_param=None,
        group_id=None,
        notify=None,
        owner_user_id=None,
        query_type=None,
        recipients=None,
        subject=None,
    ):
        """Set.
        :param uuid: The query uuid
        :param body: The query body (optional)
        :param customfield_param: Custom field(s) (optional)
        :param group_id: Id of the group associated to a trial site to add them to. Group change is not allowed for study-related queries (optional)
        :param notify: Comma delimited list of the emails to be notified of the query events (optional)
        :param owner_user_id: The user owning the query (optional)
        :param query_type: The query type (optional)
        :param recipients: JSON array of the user UUIDs to add to the query as recipients (optional)
        :param subject: Subject line of the query (optional)
        """
        request_data = {
           'body': body,
           'group_id': group_id,
           'notify': notify,
           'owner_user_id': owner_user_id,
           'query_type': query_type,
           'recipients': recipients,
           'subject': subject,
           'uuid': uuid,
        }
        if customfield_param is not None:
            customfield_param_dict = {'{prefix}{k}'.format(prefix='customfield-', k=k): v for k,v in customfield_param.items()}
            request_data.update(customfield_param_dict)
	
        errors_mapping = {}
        errors_mapping[('INVALID_GROUP', None)] = InvalidGroup('The group passed is not linked to a trial site or is from another account')
        errors_mapping[('INVALID_TYPE', None)] = InvalidType('The passed type is not valid for the group and patient arm')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_CONFIGURED', None)] = NotConfigured('The group&#39;s account is not configured')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The object was not found. The error_subtype holds the type of object not found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to edit the query')
        errors_mapping[('STUDY_QUERY_GROUP_CHANGE', None)] = StudyQueryGroupChange('Cannot change group for the study-related query')
        query_data = {
            'api': self._api,
            'url': '/query/set',
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
        :param uuid: The query uuid
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The query can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view the query')
        query_data = {
            'api': self._api,
            'url': '/query/get',
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
        :param uuid: The query uuid
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The query can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to delete the query')
        query_data = {
            'api': self._api,
            'url': '/query/delete',
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
        :param new: The new query status value
        :param old: The old query status value
        :param uuid: Query uuid
        """
        request_data = {
           'new': new,
           'old': old,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_TAG', None)] = InvalidTag('The query status new value is not a valid value')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The query can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to set the status for this query')
        errors_mapping[('STALE', None)] = Stale('The query status you have is stale')
        query_data = {
            'api': self._api,
            'url': '/query/status/set',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def attachment_add(
        self,
        length,
        name,
        query_id,
        type,
        thumbnail_length=None,
        thumbnail_type=None,
    ):
        """Attachment add.
        :param length: The attachment size in bytes
        :param name: The attachment display name
        :param query_id: Query UUID
        :param type: The attachment MIME-type
        :param thumbnail_length: The attachment's thumbnail MIME-type (optional)
        :param thumbnail_type: The attachment's thumbnail size in bytes (optional)
        """
        request_data = {
           'length': length,
           'name': name,
           'query_id': query_id,
           'thumbnail_length': thumbnail_length,
           'thumbnail_type': thumbnail_type,
           'type': type,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_CONFIGURED', None)] = NotConfigured('The Azure keys are not configured')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The query can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to add attachments to this query')
        errors_mapping[('TOO_BIG', None)] = TooBig('The attachment size exceeds the limit')
        query_data = {
            'api': self._api,
            'url': '/query/attachment/add',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def attachment_commit(
        self,
        uuid,
    ):
        """Attachment commit.
        :param uuid: Attachment UUID
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_CONFIGURED', None)] = NotConfigured('The Azure keys are not configured')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The query attachment can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not the creator of the query attachment')
        errors_mapping[('NOT_PHANTOM', None)] = NotPhantom('The attachment is not phantom')
        query_data = {
            'api': self._api,
            'url': '/query/attachment/commit',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def attachment_delete(
        self,
        uuid,
    ):
        """Attachment delete.
        :param uuid: Attachment UUID
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_CONFIGURED', None)] = NotConfigured('The Azure keys are not configured')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The query attachment can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to delete attachments from this query')
        errors_mapping[('THUMBNAIL', None)] = Thumbnail('The attachment is a thumbnail for the attachment, Use the main attachment to delete the thumbnail')
        query_data = {
            'api': self._api,
            'url': '/query/attachment/delete',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    


class AsyncQuery:
    """AsyncQuery."""

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
        query_data = {
            'api': self._api,
            'url': '/query/list',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        query_data['paginated_field'] = 'queries'
        return AsyncQueryOPSF(**query_data)
    
    def add(
        self,
        group_id,
        subject,
        body=None,
        customfield_param=None,
        notify=None,
        owner_namespace_id=None,
        owner_user_id=None,
        query_type=None,
        recipients=None,
        study_id=None,
    ):
        """Add.
        :param group_id: Id of the group associated to a trial site to add them to
        :param subject: Subject line of the query
        :param body: The query body (optional)
        :param customfield_param: Custom field(s) (optional)
        :param notify: Comma delimited list of the emails to be notified of the query events (optional)
        :param owner_namespace_id: The namespace owning the query. The account default from the default_query_owner_namespace account setting is used if not passed through the parameter (optional)
        :param owner_user_id: The user owning the query (optional)
        :param query_type: The query type (optional)
        :param recipients: JSON array of the user UUIDs to add to the query as recipients (optional)
        :param study_id: The study the query is related to (optional)
        """
        request_data = {
           'body': body,
           'group_id': group_id,
           'notify': notify,
           'owner_namespace_id': owner_namespace_id,
           'owner_user_id': owner_user_id,
           'query_type': query_type,
           'recipients': recipients,
           'study_id': study_id,
           'subject': subject,
        }
        if customfield_param is not None:
            customfield_param_dict = {'{prefix}{k}'.format(prefix='customfield-', k=k): v for k,v in customfield_param.items()}
            request_data.update(customfield_param_dict)
	
        errors_mapping = {}
        errors_mapping[('INVALID_GROUP', None)] = InvalidGroup('The group passed is not linked to a trial site')
        errors_mapping[('INVALID_TYPE', None)] = InvalidType('The passed type is not valid for the group and patient arm')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_CONFIGURED', None)] = NotConfigured('The group&#39;s account is not configured')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The object was not found. The error_subtype holds the type of object not found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to add a query to the namespace')
        query_data = {
            'api': self._api,
            'url': '/query/add',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return AsyncQueryO(**query_data)
    
    def set(
        self,
        uuid,
        body=None,
        customfield_param=None,
        group_id=None,
        notify=None,
        owner_user_id=None,
        query_type=None,
        recipients=None,
        subject=None,
    ):
        """Set.
        :param uuid: The query uuid
        :param body: The query body (optional)
        :param customfield_param: Custom field(s) (optional)
        :param group_id: Id of the group associated to a trial site to add them to. Group change is not allowed for study-related queries (optional)
        :param notify: Comma delimited list of the emails to be notified of the query events (optional)
        :param owner_user_id: The user owning the query (optional)
        :param query_type: The query type (optional)
        :param recipients: JSON array of the user UUIDs to add to the query as recipients (optional)
        :param subject: Subject line of the query (optional)
        """
        request_data = {
           'body': body,
           'group_id': group_id,
           'notify': notify,
           'owner_user_id': owner_user_id,
           'query_type': query_type,
           'recipients': recipients,
           'subject': subject,
           'uuid': uuid,
        }
        if customfield_param is not None:
            customfield_param_dict = {'{prefix}{k}'.format(prefix='customfield-', k=k): v for k,v in customfield_param.items()}
            request_data.update(customfield_param_dict)
	
        errors_mapping = {}
        errors_mapping[('INVALID_GROUP', None)] = InvalidGroup('The group passed is not linked to a trial site or is from another account')
        errors_mapping[('INVALID_TYPE', None)] = InvalidType('The passed type is not valid for the group and patient arm')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_CONFIGURED', None)] = NotConfigured('The group&#39;s account is not configured')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The object was not found. The error_subtype holds the type of object not found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to edit the query')
        errors_mapping[('STUDY_QUERY_GROUP_CHANGE', None)] = StudyQueryGroupChange('Cannot change group for the study-related query')
        query_data = {
            'api': self._api,
            'url': '/query/set',
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
        :param uuid: The query uuid
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The query can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view the query')
        query_data = {
            'api': self._api,
            'url': '/query/get',
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
        :param uuid: The query uuid
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The query can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to delete the query')
        query_data = {
            'api': self._api,
            'url': '/query/delete',
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
        :param new: The new query status value
        :param old: The old query status value
        :param uuid: Query uuid
        """
        request_data = {
           'new': new,
           'old': old,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_TAG', None)] = InvalidTag('The query status new value is not a valid value')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The query can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to set the status for this query')
        errors_mapping[('STALE', None)] = Stale('The query status you have is stale')
        query_data = {
            'api': self._api,
            'url': '/query/status/set',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return AsyncQueryO(**query_data)
    
    def attachment_add(
        self,
        length,
        name,
        query_id,
        type,
        thumbnail_length=None,
        thumbnail_type=None,
    ):
        """Attachment add.
        :param length: The attachment size in bytes
        :param name: The attachment display name
        :param query_id: Query UUID
        :param type: The attachment MIME-type
        :param thumbnail_length: The attachment's thumbnail MIME-type (optional)
        :param thumbnail_type: The attachment's thumbnail size in bytes (optional)
        """
        request_data = {
           'length': length,
           'name': name,
           'query_id': query_id,
           'thumbnail_length': thumbnail_length,
           'thumbnail_type': thumbnail_type,
           'type': type,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_CONFIGURED', None)] = NotConfigured('The Azure keys are not configured')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The query can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to add attachments to this query')
        errors_mapping[('TOO_BIG', None)] = TooBig('The attachment size exceeds the limit')
        query_data = {
            'api': self._api,
            'url': '/query/attachment/add',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return AsyncQueryO(**query_data)
    
    def attachment_commit(
        self,
        uuid,
    ):
        """Attachment commit.
        :param uuid: Attachment UUID
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_CONFIGURED', None)] = NotConfigured('The Azure keys are not configured')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The query attachment can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not the creator of the query attachment')
        errors_mapping[('NOT_PHANTOM', None)] = NotPhantom('The attachment is not phantom')
        query_data = {
            'api': self._api,
            'url': '/query/attachment/commit',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return AsyncQueryO(**query_data)
    
    def attachment_delete(
        self,
        uuid,
    ):
        """Attachment delete.
        :param uuid: Attachment UUID
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_CONFIGURED', None)] = NotConfigured('The Azure keys are not configured')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The query attachment can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to delete attachments from this query')
        errors_mapping[('THUMBNAIL', None)] = Thumbnail('The attachment is a thumbnail for the attachment, Use the main attachment to delete the thumbnail')
        query_data = {
            'api': self._api,
            'url': '/query/attachment/delete',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return AsyncQueryO(**query_data)
    