""" Customfield.

Do not edit this file by hand.
This is generated by parsing api.html service doc.
"""
from ambra_sdk.exceptions.service import FilterNotFound
from ambra_sdk.exceptions.service import InvalidCondition
from ambra_sdk.exceptions.service import InvalidDicomTag
from ambra_sdk.exceptions.service import InvalidDicomTagObject
from ambra_sdk.exceptions.service import InvalidField
from ambra_sdk.exceptions.service import InvalidHl7Field
from ambra_sdk.exceptions.service import InvalidHl7Object
from ambra_sdk.exceptions.service import InvalidHl7Segment
from ambra_sdk.exceptions.service import InvalidJson
from ambra_sdk.exceptions.service import InvalidObject
from ambra_sdk.exceptions.service import InvalidOptions
from ambra_sdk.exceptions.service import InvalidSearchSource
from ambra_sdk.exceptions.service import InvalidSortField
from ambra_sdk.exceptions.service import InvalidSortOrder
from ambra_sdk.exceptions.service import InvalidType
from ambra_sdk.exceptions.service import MissingFields
from ambra_sdk.exceptions.service import NoDicomTagDefined
from ambra_sdk.exceptions.service import NotASearch
from ambra_sdk.exceptions.service import NotFound
from ambra_sdk.exceptions.service import NotPermitted
from ambra_sdk.service.query import QueryO
from ambra_sdk.service.query import QueryOPSF

class Customfield:
    """Customfield."""

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
            'url': '/customfield/list',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        query_data['paginated_field'] = 'customfields'
        return QueryOPSF(**query_data)
    
    def add(
        self,
        account_id,
        capture_on_share_code,
        dicom_only,
        display_order,
        name,
        object,
        required,
        type,
        wrapped_dicom_only,
        dicom_tag=None,
        dicom_tag_ignore_empty=None,
        field_flag=None,
        hl7_component=None,
        hl7_field=None,
        hl7_segment=None,
        load_dicom_tag=None,
        load_from_sr=None,
        load_hl7=None,
        load_hl7_filter=None,
        options=None,
        other_dicom_tags=None,
    ):
        """Add.
        :param account_id: uuid of the account
        :param capture_on_share_code: Flag if the field should be captured during a share code exchange (only applicable to study fields)
        :param dicom_only: Only capture for non-wrapped DICOM uploads during a share code exchange
        :param display_order: Integer to order how the fields should be displayed
        :param name: Name of the customfield
        :param object: The object to associate the customfield with (Study|User_account|Group|Location|Account|Patient|Case|Order|Appointment|Dicomdata)
        :param required: Flag if the field is required
        :param type: Type of the custom field (text|number|date|memo|select|multiselect|radio|checkbox|search)
        :param wrapped_dicom_only: Only capture for wrapped DICOM uploads during a share code exchange
        :param dicom_tag: DICOM tag to map this field to. Format should be of form (1234,1234). (only applicable to study fields) (optional)
        :param dicom_tag_ignore_empty: Flag to not map an empty custom field to the DICOM tag. (only applicable if a dicom_tag is specified) (optional)
        :param field_flag: Default customfield flag (optional)
        :param hl7_component: Component number to map  this field to in HL7 ORM messages. Valid values are 1 to 64. (only applicable to study fields) (optional)
        :param hl7_field: Segment field number to map  this field to in HL7 ORM messages. Valid values are 1 to 64. (only applicable to study fields) (optional)
        :param hl7_segment: Segment to map this field to in HL7 ORM messages. Valid values are (NTE|PID|PID1|PV1|PV2|OBR|DG1|OBX|CTI|BLG|ORC) (only applicable to study fields) (optional)
        :param load_dicom_tag: Flag to load the current value from the study into this field. (only applicable if a dicom_tag is specified) (optional)
        :param load_from_sr: Load the value from the structured reports in the study (only applicable to study fields) .(optional)
        :param load_hl7: If this is set to a HL7 message type the value of this field will be updated from the hl7_segment, hl7_field and hl7_component from incoming HL7 messages of the matching message type (only applicable to study fields) (optional)
        :param load_hl7_filter: Filter token for the load_hl7 option (only applicable to study fields) (optional)
        :param options: Additional options in JSON format (optional)
        :param other_dicom_tags: JSON array of other DICOM tags to map this field to. (only applicable to study fields) (optional)
        """
        request_data = {
           'account_id': account_id,
           'capture_on_share_code': capture_on_share_code,
           'dicom_only': dicom_only,
           'dicom_tag': dicom_tag,
           'dicom_tag_ignore_empty': dicom_tag_ignore_empty,
           'display_order': display_order,
           'field_flag': field_flag,
           'hl7_component': hl7_component,
           'hl7_field': hl7_field,
           'hl7_segment': hl7_segment,
           'load_dicom_tag': load_dicom_tag,
           'load_from_sr': load_from_sr,
           'load_hl7': load_hl7,
           'load_hl7_filter': load_hl7_filter,
           'name': name,
           'object': object,
           'options': options,
           'other_dicom_tags': other_dicom_tags,
           'required': required,
           'type': type,
           'wrapped_dicom_only': wrapped_dicom_only,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_DICOM_TAG', None)] = InvalidDicomTag('The DICOM tag is invalid')
        errors_mapping[('INVALID_DICOM_TAG_OBJECT', None)] = InvalidDicomTagObject('DICOM tags can only be applied to study fields')
        errors_mapping[('INVALID_HL7_OBJECT', None)] = InvalidHl7Object('HL7 fields can only be applied to study fields')
        errors_mapping[('INVALID_HL7_SEGMENT', None)] = InvalidHl7Segment('Invalid segment name')
        errors_mapping[('INVALID_JSON', None)] = InvalidJson('The field is not in valid JSON format. The error_subtype holds the name of the field')
        errors_mapping[('INVALID_OBJECT', None)] = InvalidObject('An invalid object was passed.')
        errors_mapping[('INVALID_OPTIONS', None)] = InvalidOptions('An option is invalid. The error_subtype holds the specific error message')
        errors_mapping[('INVALID_SEARCH_SOURCE', None)] = InvalidSearchSource('An invalid search source was passed.')
        errors_mapping[('INVALID_TYPE', None)] = InvalidType('An invalid type was passed.')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The account can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to add a customfield to this account')
        errors_mapping[('NO_DICOM_TAG_DEFINED', None)] = NoDicomTagDefined('The load_dicom_tag flag is set but the dicom_tag field is not defined')
        query_data = {
            'api': self._api,
            'url': '/customfield/add',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def set(
        self,
        uuid,
        capture_on_share_code=None,
        dicom_only=None,
        dicom_tag=None,
        dicom_tag_ignore_empty=None,
        display_order=None,
        field_flag=None,
        hl7_component=None,
        hl7_field=None,
        hl7_segment=None,
        load_dicom_tag=None,
        load_from_sr=None,
        load_hl7=None,
        load_hl7_filter=None,
        name=None,
        options=None,
        other_dicom_tags=None,
        required=None,
        wrapped_dicom_only=None,
    ):
        """Set.
        :param uuid: uuid of the customfield
        :param capture_on_share_code: Flag if the study type field should be captured during a share code exchange (optional)
        :param dicom_only: Only capture for non-wrapped DICOM uploads during a share code exchange (optional)
        :param dicom_tag: Dicom tag to map this field to. Format should be of form (1234,1234). (only applicable to study fields) (optional)
        :param dicom_tag_ignore_empty: Flag to not map an empty custom field to the DICOM tag. (only applicable if a dicom_tag is specified) (optional)
        :param display_order: Integer to order how the fields should be displayed (optional)
        :param field_flag: Default customfield flag (optional)
        :param hl7_component: Component number to map  this field to in HL7 ORM messages. Valid values are 1 to 64. (only applicable to study fields) (optional)
        :param hl7_field: Segment field number to map  this field to in HL7 ORM messages. Valid values are 1 to 64. (only applicable to study fields) (optional)
        :param hl7_segment: Segment to map this field to in HL7 ORM messages. Valid values are (NTE|PID|PID1|PV1|PV2|OBR|DG1|OBX|CTI|BLG|ORC) (only applicable to study fields) (optional)
        :param load_dicom_tag: Flag to load the current value from the study into this field. (only applicable if a dicom_tag is specified) (optional)
        :param load_from_sr: Load the value from the structured reports in the study. (only applicable to study fields) .(optional)
        :param load_hl7: If this is set to a HL7 message type the value of this field will be updated from the hl7_segment, hl7_field and hl7_component from incoming HL7 messages of the matching message type (only applicable to study fields) (optional)
        :param load_hl7_filter: Filter token for the load_hl7 option (only applicable to study fields) (optional)
        :param name: Name of the customfield (optional)
        :param options: Additional options in JSON format (optional)
        :param other_dicom_tags: JSON array of other DICOM tags to map this field to. (only applicable to study fields) (optional)
        :param required: Flag if the field is required (optional)
        :param wrapped_dicom_only: Only capture for wrapped DICOM uploads during a share code exchange (optional)
        """
        request_data = {
           'capture_on_share_code': capture_on_share_code,
           'dicom_only': dicom_only,
           'dicom_tag': dicom_tag,
           'dicom_tag_ignore_empty': dicom_tag_ignore_empty,
           'display_order': display_order,
           'field_flag': field_flag,
           'hl7_component': hl7_component,
           'hl7_field': hl7_field,
           'hl7_segment': hl7_segment,
           'load_dicom_tag': load_dicom_tag,
           'load_from_sr': load_from_sr,
           'load_hl7': load_hl7,
           'load_hl7_filter': load_hl7_filter,
           'name': name,
           'options': options,
           'other_dicom_tags': other_dicom_tags,
           'required': required,
           'uuid': uuid,
           'wrapped_dicom_only': wrapped_dicom_only,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_DICOM_TAG', None)] = InvalidDicomTag('The DICOM tag is invalid')
        errors_mapping[('INVALID_DICOM_TAG_OBJECT', None)] = InvalidDicomTagObject('DICOM tags can only be applied to study fields')
        errors_mapping[('INVALID_HL7_FIELD', None)] = InvalidHl7Field('Invalid field number')
        errors_mapping[('INVALID_HL7_OBJECT', None)] = InvalidHl7Object('HL7 fields can only be applied to study fields')
        errors_mapping[('INVALID_HL7_SEGMENT', None)] = InvalidHl7Segment('Invalid segment name')
        errors_mapping[('INVALID_JSON', None)] = InvalidJson('The field is not in valid JSON format. The error_subtype holds the name of the field')
        errors_mapping[('INVALID_OPTIONS', None)] = InvalidOptions('An option is invalid. The error_subtype holds the specific error message')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The customfield can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to edit the customfield')
        errors_mapping[('NO_DICOM_TAG_DEFINED', None)] = NoDicomTagDefined('The load_dicom_tag flag is set but the dicom_tag field is not defined')
        query_data = {
            'api': self._api,
            'url': '/customfield/set',
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
        :param uuid: uuid of the customfield
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The customfield can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view the customfield')
        query_data = {
            'api': self._api,
            'url': '/customfield/get',
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
        :param uuid: uuid of the customfield
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The customfield can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to delete the customfield')
        query_data = {
            'api': self._api,
            'url': '/customfield/delete',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def lookup(
        self,
        account_id,
        name,
    ):
        """Lookup.
        :param account_id: uuid of the account
        :param name: Name of the customfield
        """
        request_data = {
           'account_id': account_id,
           'name': name,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The customfield can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to do this')
        query_data = {
            'api': self._api,
            'url': '/customfield/lookup',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def search(
        self,
        uuid,
        search=None,
    ):
        """Search.
        :param uuid: uuid of the customfield
        :param search: The value to search for (optional)
        """
        request_data = {
           'search': search,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_A_SEARCH', None)] = NotASearch('This is not a search type of customfield')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The customfield can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to do this')
        query_data = {
            'api': self._api,
            'url': '/customfield/search',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    