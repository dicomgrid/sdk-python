""" Dictionary.

Do not edit this file by hand.
This is generated by parsing api.html service doc.
"""
from ambra_sdk.exceptions.service import FilterNotFound
from ambra_sdk.exceptions.service import InvalidCondition
from ambra_sdk.exceptions.service import InvalidField
from ambra_sdk.exceptions.service import InvalidFlag
from ambra_sdk.exceptions.service import InvalidInteger
from ambra_sdk.exceptions.service import InvalidLookup
from ambra_sdk.exceptions.service import InvalidObject
from ambra_sdk.exceptions.service import InvalidRegexp
from ambra_sdk.exceptions.service import InvalidSortField
from ambra_sdk.exceptions.service import InvalidSortOrder
from ambra_sdk.exceptions.service import MissingFields
from ambra_sdk.exceptions.service import NotFound
from ambra_sdk.exceptions.service import NotList
from ambra_sdk.exceptions.service import NotPermitted
from ambra_sdk.service.query import QueryO
from ambra_sdk.service.query import QueryOPSF

class Dictionary:
    """Dictionary."""

    def __init__(self, api):
        self._api = api

    
    def list(
        self,
        account_id,
    ):
        """List.
        :param account_id: The account id
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
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to do this')
        query_data = {
            'api': self._api,
            'url': '/dictionary/list',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        query_data['paginated_field'] = 'dictionaries'
        return QueryOPSF(**query_data)
    
    def add(
        self,
        account_id,
        case_sensitive,
        lookup,
        name,
        object,
        replace,
    ):
        """Add.
        :param account_id: The account id
        :param case_sensitive: Flag if the dictionary lookup is case sensitive or not
        :param lookup: A JSON array of field names that will be concatenated and MD5 hashed for the dictionary lookup value
        :param name: The dictionary name
        :param object: Object this is applied against (Study|Order|User_account|Case|Patient)
        :param replace: A JSON array of the field names that will be replaced for a successful lookup
        """
        request_data = {
           'account_id': account_id,
           'case_sensitive': case_sensitive,
           'lookup': lookup,
           'name': name,
           'object': object,
           'replace': replace,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_FIELD', None)] = InvalidField('An invalid field name was passed. The error_subtype holds the name of the invalid field')
        errors_mapping[('INVALID_FLAG', None)] = InvalidFlag('An invalid flag was passed. The error_subtype holds the name of the invalid flag')
        errors_mapping[('INVALID_OBJECT', None)] = InvalidObject('An invalid object was passed')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The account can not be found')
        errors_mapping[('NOT_LIST', None)] = NotList('The field is not a JSON array. The error_subtype holds the name of the field')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to do this')
        query_data = {
            'api': self._api,
            'url': '/dictionary/add',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def set(
        self,
        name,
        uuid,
    ):
        """Set.
        :param name: The dictionary name
        :param uuid: The dictionary id
        """
        request_data = {
           'name': name,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The dictionary can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to do this')
        query_data = {
            'api': self._api,
            'url': '/dictionary/set',
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
        :param uuid: The dictionary id
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The dictionary can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to do this')
        query_data = {
            'api': self._api,
            'url': '/dictionary/get',
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
        :param uuid: The dictionary id
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The dictionary can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to do this')
        query_data = {
            'api': self._api,
            'url': '/dictionary/delete',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def entries(
        self,
        uuid,
        lookup=None,
    ):
        """Entries.
        :param uuid: The dictionary id
        :param lookup: Only return the entry for the optional lookup entry (optional)
        """
        request_data = {
           'lookup': lookup,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The dictionary can not be found')
        errors_mapping[('NOT_LIST', None)] = NotList('The field is not a JSON array. The error_subtype holds the name of the field')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to do this')
        query_data = {
            'api': self._api,
            'url': '/dictionary/entries',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def entry_add(
        self,
        lookup,
        replace,
        uuid,
        regexp=None,
    ):
        """Entry add.
        :param lookup: The JSON array of the lookup values to add. Alternatively a regular expression if the regexp parameter is passed
        :param replace: The JSON array of the replacement field values
        :param uuid: The dictionary id
        :param regexp: An integer value that indicates that this entry is a regular expression (optional)
        """
        request_data = {
           'lookup': lookup,
           'regexp': regexp,
           'replace': replace,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_INTEGER', None)] = InvalidInteger('Invalid integer. The error_subtype holds the invalid integer.')
        errors_mapping[('INVALID_LOOKUP', None)] = InvalidLookup('The lookup does not have the required number of fields')
        errors_mapping[('INVALID_REGEXP', None)] = InvalidRegexp('Invalid regular expression. The error_subtype holds the invalid regexp.')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The dictionary can not be found')
        errors_mapping[('NOT_LIST', None)] = NotList('The field is not a JSON array. The error_subtype holds the name of the field')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to do this')
        query_data = {
            'api': self._api,
            'url': '/dictionary/entry/add',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def entry_delete(
        self,
        lookup,
        uuid,
    ):
        """Entry delete.
        :param lookup: The JSON array of the lookup values or the regular expression to delete
        :param uuid: The dictionary id
        """
        request_data = {
           'lookup': lookup,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The dictionary or entry  can not be found')
        errors_mapping[('NOT_LIST', None)] = NotList('The field is not a JSON array. The error_subtype holds the name of the field')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to do this')
        query_data = {
            'api': self._api,
            'url': '/dictionary/entry/delete',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def attach(
        self,
        uuid,
        account_id=None,
        add_if_no_match=None,
        approve_if_match=None,
        delay=None,
        global_counter=None,
        namespace_id=None,
        run_once=None,
        sequence=None,
        skip_if_lookup_unchanged=None,
        skip_if_replace_has_value=None,
    ):
        """Attach.
        :param uuid: The dictionary id
        :param account_id: account_id
        :param add_if_no_match: Flag to add the lookup and replace values to the dictionary if no match occurs (optional)
        :param approve_if_match: Approve the object if there was a match (optional)
        :param delay: An integer number of seconds to delay the dictionary application (optional)
        :param global_counter: A flag if you want the counter to run against the account namespace instead of the object namespace (optional)
        :param namespace_id: namespace_id
        :param run_once: Flag to make dictionary apply only once per object (optional)
        :param sequence: An integer value. Attachments are processed from low number to high number (optional)
        :param skip_if_lookup_unchanged: Flag to skip the lookup if the lookup field(s) are un-changed (optional)
        :param skip_if_replace_has_value: Flag to skip the lookup if the replace field already has a value (optional)

        Notes:
        (account_id OR namespace_id) - uuid of the account or namespace to the dictionary to
        """
        request_data = {
           'account_id': account_id,
           'add_if_no_match': add_if_no_match,
           'approve_if_match': approve_if_match,
           'delay': delay,
           'global_counter': global_counter,
           'namespace_id': namespace_id,
           'run_once': run_once,
           'sequence': sequence,
           'skip_if_lookup_unchanged': skip_if_lookup_unchanged,
           'skip_if_replace_has_value': skip_if_replace_has_value,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The dictionary or entry  can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to do this')
        query_data = {
            'api': self._api,
            'url': '/dictionary/attach',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def attach_set(
        self,
        uuid,
        add_if_no_match=None,
        approve_if_match=None,
        delay=None,
        global_counter=None,
        run_once=None,
        sequence=None,
        skip_if_lookup_unchanged=None,
        skip_if_replace_has_value=None,
    ):
        """Attach set.
        :param uuid: The dictionary attach id
        :param add_if_no_match: Flag to add the lookup and replace values to the dictionary if no match occurs (optional)
        :param approve_if_match: Approve the object if there was a match (optional)
        :param delay: An integer number of seconds to delay the dictionary application (optional)
        :param global_counter: A flag if you want the counter to run against the account namespace instead of the object namespace (optional)
        :param run_once: Flag to make dictionary apply only once per object (optional)
        :param sequence: An integer value. Attachments are processed from low number to high number (optional)
        :param skip_if_lookup_unchanged: Flag to skip the lookup if the lookup field(s) are un-changed (optional)
        :param skip_if_replace_has_value: Flag to skip the lookup if any of the replace fields already has a value (optional)
        """
        request_data = {
           'add_if_no_match': add_if_no_match,
           'approve_if_match': approve_if_match,
           'delay': delay,
           'global_counter': global_counter,
           'run_once': run_once,
           'sequence': sequence,
           'skip_if_lookup_unchanged': skip_if_lookup_unchanged,
           'skip_if_replace_has_value': skip_if_replace_has_value,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The dictionary attachment can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to do this')
        query_data = {
            'api': self._api,
            'url': '/dictionary/attach/set',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def detach(
        self,
        uuid,
    ):
        """Detach.
        :param uuid: The dictionary attach id
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The dictionary attachment can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to do this')
        query_data = {
            'api': self._api,
            'url': '/dictionary/detach',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    