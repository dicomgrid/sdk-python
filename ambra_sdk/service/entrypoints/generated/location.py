""" Location.

Do not edit this file by hand.
This is generated by parsing api.html service doc.
"""
from ambra_sdk.exceptions.service import AccountNotFound
from ambra_sdk.exceptions.service import DupShareCode
from ambra_sdk.exceptions.service import FilterNotFound
from ambra_sdk.exceptions.service import InvalidCondition
from ambra_sdk.exceptions.service import InvalidCustomfield
from ambra_sdk.exceptions.service import InvalidField
from ambra_sdk.exceptions.service import InvalidFlag
from ambra_sdk.exceptions.service import InvalidJson
from ambra_sdk.exceptions.service import InvalidSortField
from ambra_sdk.exceptions.service import InvalidSortOrder
from ambra_sdk.exceptions.service import MissingFields
from ambra_sdk.exceptions.service import NotEmpty
from ambra_sdk.exceptions.service import NotFound
from ambra_sdk.exceptions.service import NotPermitted
from ambra_sdk.exceptions.service import RoleNotFound
from ambra_sdk.exceptions.service import UserNotFound
from ambra_sdk.service.query import QueryO
from ambra_sdk.service.query import QueryOPSF

class Location:
    """Location."""

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
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view this list')
        query_data = {
            'api': self._api,
            'url': '/location/list',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        query_data['paginated_field'] = 'locations'
        return QueryOPSF(**query_data)
    
    def add(
        self,
        account_id,
        name,
        customfield_param=None,
        hl7_template=None,
        must_approve=None,
        must_approve_harvest=None,
        must_approve_move=None,
        must_approve_upload=None,
        no_share=None,
        role_id=None,
        search_threshold=None,
        share_code=None,
        share_description=None,
        share_settings=None,
        share_via_gateway=None,
    ):
        """Add.
        :param account_id: uuid of the account
        :param name: Name of the location
        :param customfield_param: Custom field(s) (optional)
        :param hl7_template: The HL7 reporting template for the location (optional)
        :param must_approve: Flag if shared studies must be approved for the location (optional)
        :param must_approve_harvest: Flag if harvested studies must be approved (optional)
        :param must_approve_move: Flag if moved studies must be approved (optional)
        :param must_approve_upload: Flag if uploaded studies must be approved (optional)
        :param no_share: Flag if studies can not be shared with this location (optional). Studies can still be shared with users in the location.
        :param role_id: Id for the default role for the location (optional)
        :param search_threshold: The number of studies record in the namespace to switch the UI from list to search mode (optional)
        :param share_code: The share code of the location (optional)
        :param share_description: The share description of the location (optional)
        :param share_settings: Share settings JSON structure of the share display settings (optional)
        :param share_via_gateway: Flag if a gateway share is allowed (optional)
        """
        request_data = {
           'account_id': account_id,
           'hl7_template': hl7_template,
           'must_approve': must_approve,
           'must_approve_harvest': must_approve_harvest,
           'must_approve_move': must_approve_move,
           'must_approve_upload': must_approve_upload,
           'name': name,
           'no_share': no_share,
           'role_id': role_id,
           'search_threshold': search_threshold,
           'share_code': share_code,
           'share_description': share_description,
           'share_settings': share_settings,
           'share_via_gateway': share_via_gateway,
        }
        if customfield_param is not None:
            customfield_param_dict = {'{prefix}{k}'.format(prefix='customfield-', k=k): v for k,v in customfield_param.items()}
            request_data.update(customfield_param_dict)
	
        errors_mapping = {}
        errors_mapping[('ACCOUNT_NOT_FOUND', None)] = AccountNotFound('The account was not found')
        errors_mapping[('DUP_SHARE_CODE', None)] = DupShareCode('The share code is already used')
        errors_mapping[('INVALID_CUSTOMFIELD', None)] = InvalidCustomfield('Invalid custom field(s) name or value were passed. The error_subtype holds an array of the error details')
        errors_mapping[('INVALID_FLAG', None)] = InvalidFlag('An invalid flag was passed. The error_subtype holds the name of the invalid flag')
        errors_mapping[('INVALID_JSON', None)] = InvalidJson('The field is not in valid JSON format. The error_subtype holds the name of the field')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The object was not found. The error_subtype holds the name of field that triggered the error')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to add a location to the account')
        errors_mapping[('NOT_PERMITTED', 'ROLE_FOR_NAMESPACE_TYPE')] = NotPermitted('The role cannot be used for the location')
        query_data = {
            'api': self._api,
            'url': '/location/add',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def set(
        self,
        uuid,
        customfield_param=None,
        hl7_template=None,
        must_approve=None,
        must_approve_harvest=None,
        must_approve_move=None,
        must_approve_upload=None,
        name=None,
        no_share=None,
        role_id=None,
        search_threshold=None,
        share_code=None,
        share_description=None,
        share_settings=None,
        share_via_gateway=None,
    ):
        """Set.
        :param uuid: The location uuid
        :param customfield_param: Custom field(s) (optional)
        :param hl7_template: The HL7 reporting template for the location (optional)
        :param must_approve: Flag if shared studies must be approved for the location (optional)
        :param must_approve_harvest: Flag if harvested studies must be approved (optional)
        :param must_approve_move: Flag if moved studies must be approved (optional)
        :param must_approve_upload: Flag if uploaded studies must be approved (optional)
        :param name: Name of the location (optional)
        :param no_share: Flag if studies can not be shared with this location (optional). Studies can still be shared with users in the location.
        :param role_id: Id for the default role for the location (optional)
        :param search_threshold: The number of studies record in the namespace to switch the UI from list to search mode (optional)
        :param share_code: The share code of the location (optional)
        :param share_description: The share description of the location (optional)
        :param share_settings: Share settings JSON structure of the share display settings (optional)
        :param share_via_gateway: Flag if a gateway share is allowed (optional)
        """
        request_data = {
           'hl7_template': hl7_template,
           'must_approve': must_approve,
           'must_approve_harvest': must_approve_harvest,
           'must_approve_move': must_approve_move,
           'must_approve_upload': must_approve_upload,
           'name': name,
           'no_share': no_share,
           'role_id': role_id,
           'search_threshold': search_threshold,
           'share_code': share_code,
           'share_description': share_description,
           'share_settings': share_settings,
           'share_via_gateway': share_via_gateway,
           'uuid': uuid,
        }
        if customfield_param is not None:
            customfield_param_dict = {'{prefix}{k}'.format(prefix='customfield-', k=k): v for k,v in customfield_param.items()}
            request_data.update(customfield_param_dict)
	
        errors_mapping = {}
        errors_mapping[('DUP_SHARE_CODE', None)] = DupShareCode('The share code is already used')
        errors_mapping[('INVALID_CUSTOMFIELD', None)] = InvalidCustomfield('Invalid custom field(s) name or value were passed. The error_subtype holds an array of the error details')
        errors_mapping[('INVALID_FLAG', None)] = InvalidFlag('An invalid flag was passed. The error_subtype holds the name of the invalid flag')
        errors_mapping[('INVALID_JSON', None)] = InvalidJson('The field is not in valid JSON format. The error_subtype holds the name of the field')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The object was not found. The error_subtype holds the name of field that triggered the error')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to edit the location')
        errors_mapping[('NOT_PERMITTED', 'ROLE_FOR_NAMESPACE_TYPE')] = NotPermitted('The role cannot be used for the location')
        query_data = {
            'api': self._api,
            'url': '/location/set',
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
        :param uuid: The location uuid
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The location can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view this location')
        query_data = {
            'api': self._api,
            'url': '/location/get',
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
        :param uuid: The location uuid
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_EMPTY', None)] = NotEmpty('The location still has studies in it')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The location can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to delete the location')
        query_data = {
            'api': self._api,
            'url': '/location/delete',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def user_add(
        self,
        event_upload_fail,
        user_id,
        uuid,
        event_approve=None,
        event_case_assignment=None,
        event_harvest=None,
        event_link=None,
        event_link_mine=None,
        event_message=None,
        event_new_report=None,
        event_node=None,
        event_report_remove=None,
        event_share=None,
        event_status_change=None,
        event_study_comment=None,
        event_thin_study_fail=None,
        event_thin_study_success=None,
        event_upload=None,
        no_physician_alias_share=None,
        role_id=None,
    ):
        """User add.
        :param event_upload_fail: Notify the user on a failed upload into the location namespace
        :param user_id: Id of the user
        :param uuid: The location id
        :param event_approve: Notify the user on a approval needed into the location namespace (optional)
        :param event_case_assignment: Notify the user when they are assigned a case as a medical or admin user (optional)
        :param event_harvest: Notify the user on a harvest into the location namespace (optional)
        :param event_link: Notify the user when an anonymous link is hit in the namespace (optional)
        :param event_link_mine: Notify the user when an anonymous link created by the user is hit in the namespace (optional)
        :param event_message: Notify the user when a message is sent to the location namespace (optional)
        :param event_new_report: Notify the user when a report is attached in the location namespace (optional)
        :param event_node: Notify the user when a location  node sends an event (optional)
        :param event_report_remove: Notify the user when a report is removed in the location namespace (optional)
        :param event_share: Notify the user on a share into the location namespace (optional)
        :param event_status_change: Notify the user when the status of a study is changed (optional)
        :param event_study_comment: Notify the user when a comment is attached to a study in the namespace (optional)
        :param event_thin_study_fail: Notify the user when a thin study retrieval they initiated fails (optional)
        :param event_thin_study_success: Notify the user when a thin study retrieval they initiated succeeds (optional)
        :param event_upload: Notify the user on an upload into the location namespace (optional)
        :param no_physician_alias_share: Flag to exclude this location from a physician alias share (optional)
        :param role_id: Id of the users role within the location (optional). If not passed the default location role will be assigned
        """
        request_data = {
           'event_approve': event_approve,
           'event_case_assignment': event_case_assignment,
           'event_harvest': event_harvest,
           'event_link': event_link,
           'event_link_mine': event_link_mine,
           'event_message': event_message,
           'event_new_report': event_new_report,
           'event_node': event_node,
           'event_report_remove': event_report_remove,
           'event_share': event_share,
           'event_status_change': event_status_change,
           'event_study_comment': event_study_comment,
           'event_thin_study_fail': event_thin_study_fail,
           'event_thin_study_success': event_thin_study_success,
           'event_upload': event_upload,
           'event_upload_fail': event_upload_fail,
           'no_physician_alias_share': no_physician_alias_share,
           'role_id': role_id,
           'user_id': user_id,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_FLAG', None)] = InvalidFlag('An invalid flag was passed. The error_subtype holds the name of the invalid flag')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The location can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to edit the location')
        errors_mapping[('NOT_PERMITTED', 'ROLE_FOR_NAMESPACE_TYPE')] = NotPermitted('The role cannot be used for the location')
        errors_mapping[('ROLE_NOT_FOUND', None)] = RoleNotFound('The role was not found or is not in the account')
        errors_mapping[('USER_NOT_FOUND', None)] = UserNotFound('The user was not found or is not in the account')
        query_data = {
            'api': self._api,
            'url': '/location/user/add',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def user_delete(
        self,
        user_id,
        uuid,
    ):
        """User delete.
        :param user_id: The user id
        :param uuid: The location id
        """
        request_data = {
           'user_id': user_id,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The location can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to edit the location')
        query_data = {
            'api': self._api,
            'url': '/location/user/delete',
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
        :param uuid: The location id
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
        errors_mapping[('NOT_FOUND', None)] = NotFound('The location can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted list the users at the location')
        query_data = {
            'api': self._api,
            'url': '/location/user/list',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        query_data['paginated_field'] = 'users'
        return QueryOPSF(**query_data)
    