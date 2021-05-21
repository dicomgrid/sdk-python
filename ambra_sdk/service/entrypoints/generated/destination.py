""" Destination.

Do not edit this file by hand.
This is generated by parsing api.html service doc.
"""
from ambra_sdk.exceptions.service import DupAetitle
from ambra_sdk.exceptions.service import FilterNotFound
from ambra_sdk.exceptions.service import InsufficientCriteria
from ambra_sdk.exceptions.service import InvalidCdBurnInfo
from ambra_sdk.exceptions.service import InvalidCondition
from ambra_sdk.exceptions.service import InvalidDistributedDestination
from ambra_sdk.exceptions.service import InvalidField
from ambra_sdk.exceptions.service import InvalidFieldName
from ambra_sdk.exceptions.service import InvalidFlag
from ambra_sdk.exceptions.service import InvalidGatewayType
from ambra_sdk.exceptions.service import InvalidInteger
from ambra_sdk.exceptions.service import InvalidNodeType
from ambra_sdk.exceptions.service import InvalidRegexp
from ambra_sdk.exceptions.service import InvalidSchedule
from ambra_sdk.exceptions.service import InvalidSortField
from ambra_sdk.exceptions.service import InvalidSortOrder
from ambra_sdk.exceptions.service import InvalidType
from ambra_sdk.exceptions.service import InvalidValue
from ambra_sdk.exceptions.service import MissingFields
from ambra_sdk.exceptions.service import NodeNotFound
from ambra_sdk.exceptions.service import NotFound
from ambra_sdk.exceptions.service import NotPermitted
from ambra_sdk.exceptions.service import NotSupported
from ambra_sdk.exceptions.service import NotSysadmin
from ambra_sdk.service.query import QueryO
from ambra_sdk.service.query import QueryOPSF

class Destination:
    """Destination."""

    def __init__(self, api):
        self._api = api

    
    def list(
        self,
        account_id,
        uuid,
        node_id=None,
        serial_no=None,
    ):
        """List.
        :param account_id: uuid of the account
        :param uuid: uuid of the destination
        :param node_id: node_id
        :param serial_no: serial_no
        """
        request_data = {
           'account_id': account_id,
           'node_id': node_id,
           'serial_no': serial_no,
           'uuid': uuid,
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
            'url': '/destination/list',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        query_data['paginated_field'] = 'destinations'
        return QueryOPSF(**query_data)
    
    def add(
        self,
        account_id,
        address,
        aetitle,
        distributed_destinations,
        linked_destination,
        linked_qr_activity_in_referred_account,
        linked_qr_to_referred_account,
        name,
        node_id,
        path,
        port,
        c_echo_interval=None,
        c_echo_schedule=None,
        can_mwl_search=None,
        can_push_hl7=None,
        can_query_retrieve=None,
        can_retrieve_thin=None,
        can_search=None,
        cd_burn_info=None,
        cd_burn_name=None,
        cd_burn_priority=None,
        default_query_retrieve_level=None,
        fire_webhooks=None,
        gateway_settings=None,
        hl7_address=None,
        hl7_fetch_filter=None,
        hl7_port=None,
        manual_push_roles=None,
        push_related_studies=None,
        sort_order=None,
        sqlch_psh_if_img_unchg=None,
        sqlch_psh_if_route_hl7=None,
        type=None,
        ui_json=None,
    ):
        """Add.
        :param account_id: uuid of the account
        :param address: Address of the destination (required if DICOM type)
        :param aetitle: Aetitle of the destination (required if DICOM type)
        :param distributed_destinations: A JSON array of destination ids. This list will be used to process requests in round robin manner. Meaningful for DISTRIBUTING destination type only (opional)
        :param linked_destination: uuid of the destination for LINKED destinations
        :param linked_qr_activity_in_referred_account: A flag to create DESTINATION_SEARCH activities in the linked destination's account. Meaningful for LINKED destinations only (opional)
        :param linked_qr_to_referred_account: A flag to create resultant studies in the linked destination's account (not the account of LINKED destination where the search was initiated). Meaningful for LINKED destinations only (opional)
        :param name: Name of the destination
        :param node_id: uuid of the node that handles the destination
        :param path: Path of the folder for a FOLDER type of destination (required if FOLDER type)
        :param port: Port of the destination (required if DICOM type)
        :param c_echo_interval: Interval in seconds to C echo the destination (optional)
        :param c_echo_schedule: C echo schedule (optional)
        :param can_mwl_search: Can this destination support searching a modality work list (optional)
        :param can_push_hl7: Can this destination support pushong Hl7 messages (optional)
        :param can_query_retrieve: Can this destination support query retrieve from HL7 messages (optional)
        :param can_retrieve_thin: Can this destination support retrieving thin studies (optional)
        :param can_search: Can this destination support searching (optional)
        :param cd_burn_info: A JSON hash with the CD burning information (optional)
        :param cd_burn_name: Name for the CD burner software (optional)
        :param cd_burn_priority: Integer value for the burner priority (optional)
        :param default_query_retrieve_level: Default query retrieve level this can be either (study|series|image) and defaults to study if not specified (optional)
        :param fire_webhooks: Fire webhooks for events associated with this destination (optional)
        :param gateway_settings: Gateway settings (optional)
        :param hl7_address: Address of an attached HL7 destination (optional except for VIRTUAL destinations)
        :param hl7_fetch_filter: A transform condition expression (see /transform/add for format) to match against the HL7 message. Only fire a query retrieve if the message matches the condition (optional)
        :param hl7_port: Port of an attached HL7 destination (optional except for VIRTUAL destinations)
        :param manual_push_roles: A comma separated list of role uuids, a user is required to have one of them to manually push to this destination (optional)
        :param push_related_studies: Push all the related studies (same MRN/patientid) in the namespace when a study is pushed (optional)
        :param sort_order: Integer value for sorting (optional)
        :param sqlch_psh_if_img_unchg: Squelch pushes to the destination if the image count has not changed and the push is by a routing rule (optional)
        :param sqlch_psh_if_route_hl7: Squelch pushes to the destination if the push was generated by HL7 triggered routing (optional)
        :param type: Type of the destination either DICOM, FOLDER, ACCELERATOR,VIRTUAL, BURNER, XDS, LINKED, DISTRIBUTING or UPLOADER. Defaults to DICOM (optional)
        :param ui_json: JSON for UI settings (optional)
        """
        request_data = {
           'account_id': account_id,
           'address': address,
           'aetitle': aetitle,
           'c_echo_interval': c_echo_interval,
           'c_echo_schedule': c_echo_schedule,
           'can_mwl_search': can_mwl_search,
           'can_push_hl7': can_push_hl7,
           'can_query_retrieve': can_query_retrieve,
           'can_retrieve_thin': can_retrieve_thin,
           'can_search': can_search,
           'cd_burn_info': cd_burn_info,
           'cd_burn_name': cd_burn_name,
           'cd_burn_priority': cd_burn_priority,
           'default_query_retrieve_level': default_query_retrieve_level,
           'distributed_destinations': distributed_destinations,
           'fire_webhooks': fire_webhooks,
           'gateway_settings': gateway_settings,
           'hl7_address': hl7_address,
           'hl7_fetch_filter': hl7_fetch_filter,
           'hl7_port': hl7_port,
           'linked_destination': linked_destination,
           'linked_qr_activity_in_referred_account': linked_qr_activity_in_referred_account,
           'linked_qr_to_referred_account': linked_qr_to_referred_account,
           'manual_push_roles': manual_push_roles,
           'name': name,
           'node_id': node_id,
           'path': path,
           'port': port,
           'push_related_studies': push_related_studies,
           'sort_order': sort_order,
           'sqlch_psh_if_img_unchg': sqlch_psh_if_img_unchg,
           'sqlch_psh_if_route_hl7': sqlch_psh_if_route_hl7,
           'type': type,
           'ui_json': ui_json,
        }
	
        errors_mapping = {}
        errors_mapping[('DUP_AETITLE', None)] = DupAetitle('Duplicate aetitle. All destinations for the same node must have a unique aetitle')
        errors_mapping[('INVALID_CD_BURN_INFO', None)] = InvalidCdBurnInfo('Invalid cd_burn_info. The error_subtype holds more detail')
        errors_mapping[('INVALID_DISTRIBUTED_DESTINATION', None)] = InvalidDistributedDestination('distributed_destinations configuration is invalid')
        errors_mapping[('INVALID_FLAG', None)] = InvalidFlag('An invalid flag was passed. The error_subtype holds the name of the invalid flag')
        errors_mapping[('INVALID_GATEWAY_TYPE', None)] = InvalidGatewayType('The type is wrong for the gateway it is getting attached to')
        errors_mapping[('INVALID_INTEGER', None)] = InvalidInteger('An invalid integer was passed. The error_subtype holds the name of the invalid integer')
        errors_mapping[('INVALID_NODE_TYPE', None)] = InvalidNodeType('The node is not a harvester')
        errors_mapping[('INVALID_NODE_TYPE', None)] = InvalidNodeType('The node type is invalid for this type of destination')
        errors_mapping[('INVALID_SCHEDULE', None)] = InvalidSchedule('The schedule is invalid. The error_subtype holds the error detail')
        errors_mapping[('INVALID_TYPE', None)] = InvalidType('An invalid type was passed')
        errors_mapping[('INVALID_VALUE', None)] = InvalidValue('An invalid value was passed. The error_subtype holds the value')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NODE_NOT_FOUND', None)] = NodeNotFound('The node can not be found')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The account can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to add a destination to this account')
        errors_mapping[('NOT_SYSADMIN', None)] = NotSysadmin('The user is not a sysadmin user')
        query_data = {
            'api': self._api,
            'url': '/destination/add',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def set(
        self,
        distributed_destinations,
        linked_qr_activity_in_referred_account,
        linked_qr_to_referred_account,
        uuid,
        address=None,
        aetitle=None,
        c_echo_interval=None,
        c_echo_schedule=None,
        can_mwl_search=None,
        can_push_hl7=None,
        can_query_retrieve=None,
        can_retrieve_thin=None,
        can_search=None,
        cd_burn_info=None,
        cd_burn_name=None,
        cd_burn_priority=None,
        default_query_retrieve_level=None,
        fire_webhooks=None,
        gateway_settings=None,
        hl7_address=None,
        hl7_fetch_filter=None,
        hl7_port=None,
        manual_push_roles=None,
        name=None,
        node_id=None,
        path=None,
        port=None,
        push_related_studies=None,
        sort_order=None,
        sqlch_psh_if_img_unchg=None,
        sqlch_psh_if_route_hl7=None,
        ui_json=None,
    ):
        """Set.
        :param distributed_destinations: A JSON array of destination ids. This list will be used to process requests in round robin manner. Meaningful for DISTRIBUTING destination type only (opional)
        :param linked_qr_activity_in_referred_account: A flag to create DESTINATION_SEARCH activities in the linked destination's account. Meaningful for LINKED destinations only (opional)
        :param linked_qr_to_referred_account: A flag to create resultant studies in the linked destination's account (not the account of LINKED destination where the search was initiated). Meaningful for LINKED destinations only (opional)
        :param uuid: uuid of the destination
        :param address: Address of the destination (optional)
        :param aetitle: Aetitle of the destination (optional)
        :param c_echo_interval: Interval in seconds to C echo the destination (optional)
        :param c_echo_schedule: C echo schedule (optional)
        :param can_mwl_search: Can this destination support searching a modality work list (optional)
        :param can_push_hl7: Can this destination support pushong Hl7 messages (optional)
        :param can_query_retrieve: Can this destination support query retrieve from HL7 messages (optional)
        :param can_retrieve_thin: Can this destination support retrieving thin studies (optional)
        :param can_search: Can this destination support searching (optional)
        :param cd_burn_info: A JSON hash with the CD burning information (optional)
        :param cd_burn_name: Name for the CD burner software (optional)
        :param cd_burn_priority: Integer value for the burner priority (optional)
        :param default_query_retrieve_level: Default query retrieve level this can be either (study|series|image) and defaults to study if not specified (optional)
        :param fire_webhooks: Fire webhooks for events associated with this destination (optional)
        :param gateway_settings: Gateway settings (optional)
        :param hl7_address: Address of an attached HL7 destination (optional)
        :param hl7_fetch_filter: A transform condition expression (see /transform/add for format) to match against the HL7 message. Only fire a query retrieve if the message matches the condition (optional)
        :param hl7_port: Port of an attached HL7 destination (optional)
        :param manual_push_roles: A comma separated list of role uuids, a user is required to have one of them to manually push to this destination (optional)
        :param name: Name of the destination (optional)
        :param node_id: uuid of the node that handles the destination (optional)
        :param path: Path of the folder (optional)
        :param port: Port of the destination (optional)
        :param push_related_studies: Push all the related studies (same MRN/patientid) in the namespace when a study is pushed (optional)
        :param sort_order: Integer value for sorting (optional)
        :param sqlch_psh_if_img_unchg: Squelch pushes to the destination if the image count has not changed and the push is by a routing rule (optional)
        :param sqlch_psh_if_route_hl7: Squelch pushes to the destination if the push was generated by HL7 triggered routing (optional)
        :param ui_json: JSON for UI settings (optional)
        """
        request_data = {
           'address': address,
           'aetitle': aetitle,
           'c_echo_interval': c_echo_interval,
           'c_echo_schedule': c_echo_schedule,
           'can_mwl_search': can_mwl_search,
           'can_push_hl7': can_push_hl7,
           'can_query_retrieve': can_query_retrieve,
           'can_retrieve_thin': can_retrieve_thin,
           'can_search': can_search,
           'cd_burn_info': cd_burn_info,
           'cd_burn_name': cd_burn_name,
           'cd_burn_priority': cd_burn_priority,
           'default_query_retrieve_level': default_query_retrieve_level,
           'distributed_destinations': distributed_destinations,
           'fire_webhooks': fire_webhooks,
           'gateway_settings': gateway_settings,
           'hl7_address': hl7_address,
           'hl7_fetch_filter': hl7_fetch_filter,
           'hl7_port': hl7_port,
           'linked_qr_activity_in_referred_account': linked_qr_activity_in_referred_account,
           'linked_qr_to_referred_account': linked_qr_to_referred_account,
           'manual_push_roles': manual_push_roles,
           'name': name,
           'node_id': node_id,
           'path': path,
           'port': port,
           'push_related_studies': push_related_studies,
           'sort_order': sort_order,
           'sqlch_psh_if_img_unchg': sqlch_psh_if_img_unchg,
           'sqlch_psh_if_route_hl7': sqlch_psh_if_route_hl7,
           'ui_json': ui_json,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('DUP_AETITLE', None)] = DupAetitle('Duplicate aetitle. All destinations for the same node must have a unique aetitle')
        errors_mapping[('INVALID_CD_BURN_INFO', None)] = InvalidCdBurnInfo('Invalid cd_burn_info. The error_subtype holds more detail')
        errors_mapping[('INVALID_DISTRIBUTED_DESTINATION', None)] = InvalidDistributedDestination('distributed_destinations configuration is invalid')
        errors_mapping[('INVALID_FLAG', None)] = InvalidFlag('An invalid flag was passed. The error_subtype holds the name of the invalid flag')
        errors_mapping[('INVALID_INTEGER', None)] = InvalidInteger('An invalid integer was passed. The error_subtype holds the name of the invalid integer')
        errors_mapping[('INVALID_NODE_TYPE', None)] = InvalidNodeType('The node is not a harvester')
        errors_mapping[('INVALID_SCHEDULE', None)] = InvalidSchedule('The schedule is invalid. The error_subtype holds the error detail')
        errors_mapping[('INVALID_VALUE', None)] = InvalidValue('An invalid value was passed. The error_subtype holds the value')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NODE_NOT_FOUND', None)] = NodeNotFound('The node can not be found')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The destination can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to edit the destination')
        query_data = {
            'api': self._api,
            'url': '/destination/set',
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
        :param uuid: uuid of the destination
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The destination can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view the destination')
        query_data = {
            'api': self._api,
            'url': '/destination/get',
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
        :param uuid: uuid of the destination
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The destination can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to delete the destination')
        query_data = {
            'api': self._api,
            'url': '/destination/delete',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def search(
        self,
        uuid,
        accession_number=None,
        anonymize=None,
        anonymize_param=None,
        bundle_id=None,
        copy_to=None,
        create_study=None,
        create_thin=None,
        customfield_param=None,
        end_datetime=None,
        modality=None,
        node_id=None,
        patient_birth_date=None,
        patient_name=None,
        patient_sex=None,
        patientid=None,
        push_to=None,
        query_fields=None,
        referring_physician=None,
        result_fields=None,
        serial_no=None,
        share_email=None,
        start_datetime=None,
        study_request_id=None,
        study_uid=None,
    ):
        """Search.
        :param uuid: uuid of the destination
        :param accession_number: Accession number to find (optional)
        :param anonymize: A JSON hash of anonymization rules to apply to retrieved studies (optional)
        :param anonymize_param: The anonymization rules breakdown. This overrides the anonymize parameter if passed (optional)
        :param bundle_id: An integral number Used internally to track searches initiated from a single bundle (optional)
        :param copy_to: uuid of a namespace to copy the retrieved or create_thin studies into (optional)
        :param create_study: The maximum number of studies to retrieve from this search instead of creating an activity for the search results (optional)
        :param create_thin: The maximum number of thin studies to create from this search instead of creating an activity for the search results (optional)
        :param customfield_param: Custom field(s) will be set for the resultant studies after /destination/retrieve call (optional)
        :param end_datetime: DICOM end date time stamp to bound the search (optional)
        :param modality: Modality (optional)
        :param node_id: node_id
        :param patient_birth_date: Birth date to find (optional)
        :param patient_name: Patient name to find (optional)
        :param patient_sex: Gender to find (optional)
        :param patientid: Patient id to find (optional)
        :param push_to: uuid of a destination to push the retrieved studies to (optional)
        :param query_fields: A JSON hash of additional query fields (optional)
        :param referring_physician: Referring physician to find (optional)
        :param result_fields: A JSON array of DICOM tags that the destination should return (optional)
        :param serial_no: serial_no
        :param share_email: Email to share retrieved studies with on subsequent /destination/retrieve (optional)
        :param start_datetime: DICOM start date time stamp to bound the search (optional)
        :param study_request_id: uuid of a study request (optional)
        :param study_uid: Study uid to find (optional)
        """
        request_data = {
           'accession_number': accession_number,
           'anonymize': anonymize,
           'bundle_id': bundle_id,
           'copy_to': copy_to,
           'create_study': create_study,
           'create_thin': create_thin,
           'end_datetime': end_datetime,
           'modality': modality,
           'node_id': node_id,
           'patient_birth_date': patient_birth_date,
           'patient_name': patient_name,
           'patient_sex': patient_sex,
           'patientid': patientid,
           'push_to': push_to,
           'query_fields': query_fields,
           'referring_physician': referring_physician,
           'result_fields': result_fields,
           'serial_no': serial_no,
           'share_email': share_email,
           'start_datetime': start_datetime,
           'study_request_id': study_request_id,
           'study_uid': study_uid,
           'uuid': uuid,
        }
        if anonymize_param is not None:
            anonymize_param_dict = {'{prefix}{k}'.format(prefix='anonymize_', k=k): v for k,v in anonymize_param.items()}
            request_data.update(anonymize_param_dict)
        if customfield_param is not None:
            customfield_param_dict = {'{prefix}{k}'.format(prefix='customfield-', k=k): v for k,v in customfield_param.items()}
            request_data.update(customfield_param_dict)
	
        errors_mapping = {}
        errors_mapping[('INSUFFICIENT_CRITERIA', None)] = InsufficientCriteria('Not enough search fields are populated')
        errors_mapping[('INVALID_FIELD_NAME', None)] = InvalidFieldName('The field cannot be used in anonymization rules. The error_subtype holds the invalid field name.')
        errors_mapping[('INVALID_REGEXP', None)] = InvalidRegexp('Invalid anonymization rule regular expression. The error_subtype holds the invalid regexp.')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The destination, namespace or study request can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to search the destination')
        errors_mapping[('NOT_SUPPORTED', None)] = NotSupported('The destination does not support searching a destination')
        query_data = {
            'api': self._api,
            'url': '/destination/search',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def retrieve(
        self,
        activity_id,
        send_method,
        study_request_found_id,
        customfield_param=None,
    ):
        """Retrieve.
        :param activity_id: uuid of the DESTINATION_SEARCH activity to retrieve from
        :param send_method: The method to send a study as a study request response (share|duplicate)
        :param study_request_found_id: UUID of a study request search results to retrieve and send as study request response
        :param customfield_param: Custom field(s) will be set for the study retrieved (optional)
        """
        request_data = {
           'activity_id': activity_id,
           'send_method': send_method,
           'study_request_found_id': study_request_found_id,
        }
        if customfield_param is not None:
            customfield_param_dict = {'{prefix}{k}'.format(prefix='customfield-', k=k): v for k,v in customfield_param.items()}
            request_data.update(customfield_param_dict)
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The activity can not be found')
        query_data = {
            'api': self._api,
            'url': '/destination/retrieve',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def search_mwl(
        self,
        study_id,
        uuid,
        accession_number=None,
        order_date=None,
        order_number=None,
        patient_birth_date=None,
        patient_name=None,
        patient_sex=None,
        patientid=None,
    ):
        """Search mwl.
        :param study_id: The id of the study we are searching for orders for
        :param uuid: uuid of the destination
        :param accession_number: Accession number to find (optional)
        :param order_date: Order date to find (optional)
        :param order_number: Order number to find (optional)
        :param patient_birth_date: Birth date to find (optional)
        :param patient_name: Patient name to find (optional)
        :param patient_sex: Gender to find (optional)
        :param patientid: Patient id to find (optional)
        """
        request_data = {
           'accession_number': accession_number,
           'order_date': order_date,
           'order_number': order_number,
           'patient_birth_date': patient_birth_date,
           'patient_name': patient_name,
           'patient_sex': patient_sex,
           'patientid': patientid,
           'study_id': study_id,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('INSUFFICIENT_CRITERIA', None)] = InsufficientCriteria('Not enough search fields are populated')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The destination or study can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to search the destination')
        errors_mapping[('NOT_SUPPORTED', None)] = NotSupported('The destination does not support searching a destination')
        query_data = {
            'api': self._api,
            'url': '/destination/search/mwl',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    