""" Node.

Do not edit this file by hand.
This is generated by parsing api.html service doc.
"""
from ambra_sdk.exceptions.service import AccountNotFound
from ambra_sdk.exceptions.service import AlreadyConnected
from ambra_sdk.exceptions.service import AlreadyDone
from ambra_sdk.exceptions.service import FilterNotFound
from ambra_sdk.exceptions.service import HasDestinations
from ambra_sdk.exceptions.service import InvalidCondition
from ambra_sdk.exceptions.service import InvalidConfiguration
from ambra_sdk.exceptions.service import InvalidDateTime
from ambra_sdk.exceptions.service import InvalidEvent
from ambra_sdk.exceptions.service import InvalidField
from ambra_sdk.exceptions.service import InvalidFilter
from ambra_sdk.exceptions.service import InvalidJson
from ambra_sdk.exceptions.service import InvalidLinkage
from ambra_sdk.exceptions.service import InvalidMetric
from ambra_sdk.exceptions.service import InvalidRange
from ambra_sdk.exceptions.service import InvalidSortField
from ambra_sdk.exceptions.service import InvalidSortOrder
from ambra_sdk.exceptions.service import InvalidStatus
from ambra_sdk.exceptions.service import InvalidType
from ambra_sdk.exceptions.service import InvalidUuid
from ambra_sdk.exceptions.service import MissingFields
from ambra_sdk.exceptions.service import NoNodeOverride
from ambra_sdk.exceptions.service import NotFound
from ambra_sdk.exceptions.service import NotPermitted
from ambra_sdk.exceptions.service import ScheduleIsOff
from ambra_sdk.exceptions.service import TryLater
from ambra_sdk.service.query import QueryO
from ambra_sdk.service.query import QueryOPSF

class Node:
    """Node."""

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
            'url': '/node/list',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        query_data['paginated_field'] = 'nodes'
        return QueryOPSF(**query_data)
    
    def public(
        self,
        account_id,
    ):
        """Public.
        :param account_id: The account the user is in
        """
        request_data = {
           'account_id': account_id,
        }
	
        errors_mapping = {}
        errors_mapping[('FILTER_NOT_FOUND', None)] = FilterNotFound('The filter can not be found. The error_subtype will hold the filter UUID')
        errors_mapping[('INVALID_CONDITION', None)] = InvalidCondition('The condition is not support. The error_subtype will hold the filter expression this applies to')
        errors_mapping[('INVALID_FIELD', None)] = InvalidField('The field is not valid for this object. The error_subtype will hold the filter expression this applies to')
        errors_mapping[('INVALID_FILTER', None)] = InvalidFilter('Invalid filter field')
        errors_mapping[('INVALID_SORT_FIELD', None)] = InvalidSortField('The field is not valid for this object. The error_subtype will hold the field name this applies to')
        errors_mapping[('INVALID_SORT_ORDER', None)] = InvalidSortOrder('The sort order for the field is invalid. The error_subtype will hold the field name this applies to')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The node or account can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to do this')
        query_data = {
            'api': self._api,
            'url': '/node/public',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        query_data['paginated_field'] = 'nodes'
        return QueryOPSF(**query_data)
    
    def connect(
        self,
        account_id,
        uuid,
        message=None,
    ):
        """Connect.
        :param account_id: The account the user is in
        :param uuid: The node id
        :param message: Message (optional)
        """
        request_data = {
           'account_id': account_id,
           'message': message,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('ALREADY_CONNECTED', None)] = AlreadyConnected('The node is already connected to the account')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The node or account can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to do this')
        query_data = {
            'api': self._api,
            'url': '/node/connect',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def add(
        self,
        accelerator_id,
        name,
        type,
        account_id=None,
        category=None,
        ctc_bucket=None,
        facility_contact=None,
        facility_contact_title=None,
        facility_email=None,
        facility_name=None,
        facility_notes=None,
        facility_zip=None,
        group_id=None,
        is_public=None,
        location_id=None,
        uuid=None,
    ):
        """Add.
        :param accelerator_id: uuid of the accelerator if this is an accelerator node
        :param name: Description of the node
        :param type: Type of node (STORAGE|HARVESTER|ACCELERATOR|CLEARINGHOUSE|VIRTUAL|UTILITY|XDS)
        :param account_id: account_id
        :param category: Node category (ACTIVE|INACTIVE|MIGRATION|TEST|DUPLICATE|INTEGRATED|ACCELERATOR) (optional)
        :param ctc_bucket: Name of the S3 bucket to use for a cloud to cloud gateway (optional)
        :param facility_contact: Name of the facility contact (optional)
        :param facility_contact_title: Title of the facility contact (optional)
        :param facility_email: Email of the facility contact (optional)
        :param facility_name: Name of the facility it is installed at (optional)
        :param facility_notes: Notes about the facility (optional)
        :param facility_zip: Zip code of the facility it is installed at (optional)
        :param group_id: group_id
        :param is_public: Flag if the node is public (optional)
        :param location_id: location_id
        :param uuid: uuid of the node (optional, you can use this to explicitly set the UUID)

        Notes:
        (account_id OR location_id OR group_id) - uuid of the account, location or group to link this node to
        """
        request_data = {
           'accelerator_id': accelerator_id,
           'account_id': account_id,
           'category': category,
           'ctc_bucket': ctc_bucket,
           'facility_contact': facility_contact,
           'facility_contact_title': facility_contact_title,
           'facility_email': facility_email,
           'facility_name': facility_name,
           'facility_notes': facility_notes,
           'facility_zip': facility_zip,
           'group_id': group_id,
           'is_public': is_public,
           'location_id': location_id,
           'name': name,
           'type': type,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('ACCOUNT_NOT_FOUND', None)] = AccountNotFound('The account was not found')
        errors_mapping[('INVALID_LINKAGE', None)] = InvalidLinkage('The linkage is invalid')
        errors_mapping[('INVALID_TYPE', None)] = InvalidType('Invalid type of node')
        errors_mapping[('INVALID_UUID', None)] = InvalidUuid('Invalid uuid format or this uuid is already in use')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to add a node to this account')
        query_data = {
            'api': self._api,
            'url': '/node/add',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def set(
        self,
        uuid,
        category=None,
        configuration=None,
        ctc_bucket=None,
        facility_contact=None,
        facility_contact_title=None,
        facility_email=None,
        facility_name=None,
        facility_notes=None,
        facility_zip=None,
        is_public=None,
        monitor_email=None,
        monitor_node_last_send=None,
        monitor_node_last_send_threshold=None,
        monitor_node_ping=None,
        monitor_node_slow_push=None,
        monitor_node_slow_push_threshold=None,
        monitor_study_create=None,
        monitor_study_create_threshold=None,
        name=None,
        reload_configuration=None,
        serial_no=None,
        setting_param=None,
        settings=None,
        storage_namespace=None,
        warning_email=None,
    ):
        """Set.
        :param uuid: The node id
        :param category: Node category (ACTIVE|INACTIVE|MIGRATION|TEST|DUPLICATE|INTEGRATED) (optional)
        :param configuration: The configuration as a JSON hash of key values pairs (optional)
        :param ctc_bucket: Name of the S3 bucket to use for a cloud to cloud gateway (optional)
        :param facility_contact: Name of the facility contact (optional)
        :param facility_contact_title: Title of the facility contact (optional)
        :param facility_email: Email of the facility contact (optional)
        :param facility_name: Name of the facility it is installed at (optional)
        :param facility_notes: Notes about the facility (optional)
        :param facility_zip: Zip code of the facility it is installed at (optional)
        :param is_public: Flag if the node is public (optional)
        :param monitor_email: Email address(es) to send monitor failure notices (optional)
        :param monitor_node_last_send: Check if the node has sent a study recently (optional)
        :param monitor_node_last_send_threshold: Threshold in minutes for triggering the monitor_node_last_send notification (optional)
        :param monitor_node_ping: Check if the node is pinging (optional)
        :param monitor_node_slow_push: Check if the node is pushing slowly (optional)
        :param monitor_node_slow_push_threshold: Threshold in minutes for triggering the monitor_node_slow_push notification (optional)
        :param monitor_study_create: Check if the node is sending studies normally (optional)
        :param monitor_study_create_threshold: Threshold in minutes for triggering the monitor_study_create notification (optional)
        :param name: Description of the node (optional)
        :param reload_configuration: If this flag is set the node will be instructed to reload it&#39;s configuration on the next ping (optional)
        :param serial_no: serial_no
        :param setting_param: Set an individual setting. This is an alternative to the settings hash for easier use in the API tester (optional)
        :param settings: A hash of the account settings that the node can override (optional)
        :param storage_namespace: Namespace uuid to attach the node to. This requires a sysadmin sid and must be within the same account (optional)
        :param warning_email: Email address(es) to send warning notices (optional)

        Notes:
        (sid OR serial_no) - The session id or serial number of the node
        """
        request_data = {
           'category': category,
           'configuration': configuration,
           'ctc_bucket': ctc_bucket,
           'facility_contact': facility_contact,
           'facility_contact_title': facility_contact_title,
           'facility_email': facility_email,
           'facility_name': facility_name,
           'facility_notes': facility_notes,
           'facility_zip': facility_zip,
           'is_public': is_public,
           'monitor_email': monitor_email,
           'monitor_node_last_send': monitor_node_last_send,
           'monitor_node_last_send_threshold': monitor_node_last_send_threshold,
           'monitor_node_ping': monitor_node_ping,
           'monitor_node_slow_push': monitor_node_slow_push,
           'monitor_node_slow_push_threshold': monitor_node_slow_push_threshold,
           'monitor_study_create': monitor_study_create,
           'monitor_study_create_threshold': monitor_study_create_threshold,
           'name': name,
           'reload_configuration': reload_configuration,
           'serial_no': serial_no,
           'settings': settings,
           'storage_namespace': storage_namespace,
           'uuid': uuid,
           'warning_email': warning_email,
        }
        if setting_param is not None:
            setting_param_dict = {'{prefix}{k}'.format(prefix='setting_', k=k): v for k,v in setting_param.items()}
            request_data.update(setting_param_dict)
	
        errors_mapping = {}
        errors_mapping[('INVALID_CONFIGURATION', None)] = InvalidConfiguration('An invalid combination of configuration options was set. The error_subtype will hold more detail')
        errors_mapping[('INVALID_JSON', None)] = InvalidJson('The field is not in valid JSON format. The error_subtype holds the name of the field')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The node can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to edit this node')
        errors_mapping[('NO_NODE_OVERRIDE', None)] = NoNodeOverride('The setting does not allow a node override')
        query_data = {
            'api': self._api,
            'url': '/node/set',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def get(
        self,
        uuid,
        serial_no=None,
    ):
        """Get.
        :param uuid: The node id
        :param serial_no: serial_no

        Notes:
        (sid OR serial_no) - The session id or serial number of the node
        """
        request_data = {
           'serial_no': serial_no,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The node can not be found')
        query_data = {
            'api': self._api,
            'url': '/node/get',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def ping(
        self,
        ack,
        serial_no,
        uuid,
    ):
        """Ping.
        :param ack: Flag if the gateway wants to use the acknowledge workflow
        :param serial_no: The serial number of the node
        :param uuid: The node id
        """
        request_data = {
           'ack': ack,
           'serial_no': serial_no,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The node can not be found')
        query_data = {
            'api': self._api,
            'url': '/node/ping',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': False,
        }
        return QueryO(**query_data)
    
    def ping_ack(
        self,
        serial_no,
        uuid,
    ):
        """Ping ack.
        :param serial_no: The serial number of the node
        :param uuid: The node id
        """
        request_data = {
           'serial_no': serial_no,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The node can not be found')
        query_data = {
            'api': self._api,
            'url': '/node/ping/ack',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': False,
        }
        return QueryO(**query_data)
    
    def deliver(
        self,
        serial_no,
        status,
        uuid,
        ack=None,
        destination_id=None,
        email_reason=None,
        is_local=None,
        job_id=None,
        status_reason=None,
        study_uid=None,
    ):
        """Deliver.
        :param serial_no: The serial number of the node
        :param status: Status code of the job (S|F|P|B|U) - Success, failure, partial transfer, blocked or uncached
        :param uuid: The node id
        :param ack: The HL7 ACK if this was an HL7 job (optional)
        :param destination_id: The uuid of the destination, required for local pushes (optional)
        :param email_reason: Email the user this reason for the status change (optional)
        :param is_local: The flag used to indicate the local push (optional)
        :param job_id: The uuid of the push job, not used for local pushes (optional)
        :param status_reason: Detail on the status change (optional)
        :param study_uid: The study uid of the local push, required for local pushes only (optional)
        """
        request_data = {
           'ack': ack,
           'destination_id': destination_id,
           'email_reason': email_reason,
           'is_local': is_local,
           'job_id': job_id,
           'serial_no': serial_no,
           'status': status,
           'status_reason': status_reason,
           'study_uid': study_uid,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_STATUS', None)] = InvalidStatus('Invalid status code')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The node or job can not be found')
        query_data = {
            'api': self._api,
            'url': '/node/deliver',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': False,
        }
        return QueryO(**query_data)
    
    def retrieve(
        self,
        job_id,
        serial_no,
        status,
        uuid,
    ):
        """Retrieve.
        :param job_id: The uuid of the fetch job
        :param serial_no: The serial number of the node
        :param status: Status code of the job (S|F|P) - Success, failure, partial transfer
        :param uuid: The node id
        """
        request_data = {
           'job_id': job_id,
           'serial_no': serial_no,
           'status': status,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_STATUS', None)] = InvalidStatus('Invalid status code')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The node or job can not be found')
        query_data = {
            'api': self._api,
            'url': '/node/retrieve',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': False,
        }
        return QueryO(**query_data)
    
    def webhook(
        self,
        serial_no,
        status,
        uuid,
        webhook_id,
        error_message=None,
    ):
        """Webhook.
        :param serial_no: The serial number of the node
        :param status: Status code of the job (S|F) - Success, failure
        :param uuid: The node id
        :param webhook_id: The uuid of the webhook job
        :param error_message: Detailed error message (optional)
        """
        request_data = {
           'error_message': error_message,
           'serial_no': serial_no,
           'status': status,
           'uuid': uuid,
           'webhook_id': webhook_id,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_STATUS', None)] = InvalidStatus('Invalid status code')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The node or webhook can not be found')
        query_data = {
            'api': self._api,
            'url': '/node/webhook',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': False,
        }
        return QueryO(**query_data)
    
    def configuration(
        self,
        serial_no,
        uuid,
    ):
        """Configuration.
        :param serial_no: The serial number of the node
        :param uuid: The node id
        """
        request_data = {
           'serial_no': serial_no,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The node can not be found')
        query_data = {
            'api': self._api,
            'url': '/node/configuration',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': False,
        }
        return QueryO(**query_data)
    
    def delete(
        self,
        uuid,
    ):
        """Delete.
        :param uuid: The node id
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('HAS_DESTINATIONS', None)] = HasDestinations('The node has associated destinations')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The node can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to delete this node')
        query_data = {
            'api': self._api,
            'url': '/node/delete',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def study_queued(
        self,
        serial_no,
        study_uid,
        uuid,
    ):
        """Study queued.
        :param serial_no: The serial number of the node
        :param study_uid: The study uid
        :param uuid: The node id
        """
        request_data = {
           'serial_no': serial_no,
           'study_uid': study_uid,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The node can not be found')
        query_data = {
            'api': self._api,
            'url': '/node/study/queued',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': False,
        }
        return QueryO(**query_data)
    
    def found(
        self,
        search_id,
        serial_no,
        studies,
        uuid,
    ):
        """Found.
        :param search_id: The id of the search request
        :param serial_no: The serial number of the node
        :param studies: A JSON array of the studies found. Each object has the following fields:
            study_uid - The study_uid
            study_date - The study date
            accession_number - The accession number
            referring_physician - The referring physician
            patient_name - Patient name
            patientid - Patient ID
            patient_sex - Gender
            patient_birth_date - Birth date
            study_description - Study description
            modality - Modality
            result_fields - A JSON structure with the answers for the requested result_fields in /destination/search (optional)
        :param uuid: The node id
        """
        request_data = {
           'search_id': search_id,
           'serial_no': serial_no,
           'studies': studies,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('ALREADY_DONE', None)] = AlreadyDone('The search has already had results returned against it')
        errors_mapping[('INVALID_JSON', None)] = InvalidJson('The field is not in valid JSON format. The error_subtype holds the name of the field')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The node or search can not be found')
        query_data = {
            'api': self._api,
            'url': '/node/found',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': False,
        }
        return QueryO(**query_data)
    
    def found_mwl(
        self,
        orders,
        search_id,
        serial_no,
        uuid,
    ):
        """Found mwl.
        :param orders: A JSON array of the orders found. Each object has the following fields:
            patient_name - Patient name
            patientid - Patient id
            accession_number - Accession number
            patient_sex - Gender
            patient_birth_date - Birth date
            order_number - Order number
            order_date - Order date
        :param search_id: The id of the search request
        :param serial_no: The serial number of the node
        :param uuid: The node id
        """
        request_data = {
           'orders': orders,
           'search_id': search_id,
           'serial_no': serial_no,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('ALREADY_DONE', None)] = AlreadyDone('The search has already had results returned against it')
        errors_mapping[('INVALID_JSON', None)] = InvalidJson('The field is not in valid JSON format. The error_subtype holds the name of the field')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The node or search can not be found')
        query_data = {
            'api': self._api,
            'url': '/node/found/mwl',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': False,
        }
        return QueryO(**query_data)
    
    def event(
        self,
        destination_id,
        event,
        serial_no,
        uuid,
    ):
        """Event.
        :param destination_id: The id of the destination if the event is associated with a destination
        :param event: The event (c_echo_error)
        :param serial_no: The serial number of the node
        :param uuid: The node id
        """
        request_data = {
           'destination_id': destination_id,
           'event': event,
           'serial_no': serial_no,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_EVENT', None)] = InvalidEvent('Invalid event')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The node or destination can not be found')
        errors_mapping[('SCHEDULE_IS_OFF', None)] = ScheduleIsOff('The event is outside of its scheduled time')
        query_data = {
            'api': self._api,
            'url': '/node/event',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': False,
        }
        return QueryO(**query_data)
    
    def log(
        self,
        end,
        start,
        type,
        uuid,
    ):
        """Log.
        :param end: End time stamp in YYYY-MM-DD HH:MM:SS format
        :param start: Start time stamp in YYYY-MM-DD HH:MM:SS format
        :param type: Type of log (log|dicom|queue|system) defaults to log if not passed
        :param uuid: The node id
        """
        request_data = {
           'end': end,
           'start': start,
           'type': type,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_DATE_TIME', None)] = InvalidDateTime('The timestamp is invalid')
        errors_mapping[('INVALID_RANGE', None)] = InvalidRange('An invalid time range was specified')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The node can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to perform this action')
        errors_mapping[('TRY_LATER', None)] = TryLater('The log search queue is full')
        query_data = {
            'api': self._api,
            'url': '/node/log',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def metric(
        self,
        job_id,
        metric,
        serial_no,
        uuid,
    ):
        """Metric.
        :param job_id: The uuid of the push job
        :param metric: The metric to record
        :param serial_no: The serial number of the node
        :param uuid: The node id
        """
        request_data = {
           'job_id': job_id,
           'metric': metric,
           'serial_no': serial_no,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_METRIC', None)] = InvalidMetric('The metric is invalid for this job type')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The node or job can not be found')
        query_data = {
            'api': self._api,
            'url': '/node/metric',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': False,
        }
        return QueryO(**query_data)
    
    def performance_set(
        self,
        data,
        serial_no,
        uuid,
    ):
        """Performance set.
        :param data: A JSON data structure with performance data
        :param serial_no: The serial number of the node
        :param uuid: The node id
        """
        request_data = {
           'data': data,
           'serial_no': serial_no,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The node can not be found')
        query_data = {
            'api': self._api,
            'url': '/node/performance/set',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': False,
        }
        return QueryO(**query_data)
    
    def performance_get(
        self,
        uuid,
        serial_no=None,
    ):
        """Performance get.
        :param uuid: The node id
        :param serial_no: serial_no

        Notes:
        (sid OR serial_no) - The session id or serial number of the node
        """
        request_data = {
           'serial_no': serial_no,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('NOT_FOUND', None)] = NotFound('The node can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view this node')
        query_data = {
            'api': self._api,
            'url': '/node/performance/get',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def progress_add(
        self,
        queue,
        serial_no,
        state,
        uuid,
        accession_number=None,
        destination_id=None,
        detail=None,
        patientid=None,
        study_uid=None,
    ):
        """Progress add.
        :param queue: The queue
        :param serial_no: The serial number of the node
        :param state: The status
        :param uuid: The node id
        :param accession_number: DICOM tag (0008,0050) (optional)
        :param destination_id: The destination uuid (optional)
        :param detail: JSON detail (optional)
        :param patientid: DICOM tag (0010,0020) (optional)
        :param study_uid: Study uid (optional)
        """
        request_data = {
           'accession_number': accession_number,
           'destination_id': destination_id,
           'detail': detail,
           'patientid': patientid,
           'queue': queue,
           'serial_no': serial_no,
           'state': state,
           'study_uid': study_uid,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The node or destination can not be found')
        query_data = {
            'api': self._api,
            'url': '/node/progress/add',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': False,
        }
        return QueryO(**query_data)
    
    def progress_list(
        self,
        destination_id=None,
        node_id=None,
    ):
        """Progress list.
        :param destination_id: destination_id
        :param node_id: node_id

        Notes:
        (node_id OR destination_id) - The node or destination id
        """
        request_data = {
           'destination_id': destination_id,
           'node_id': node_id,
        }
	
        errors_mapping = {}
        errors_mapping[('FILTER_NOT_FOUND', None)] = FilterNotFound('The filter can not be found. The error_subtype will hold the filter UUID')
        errors_mapping[('INVALID_CONDITION', None)] = InvalidCondition('The condition is not support. The error_subtype will hold the filter expression this applies to')
        errors_mapping[('INVALID_FIELD', None)] = InvalidField('The field is not valid for this object. The error_subtype will hold the filter expression this applies to')
        errors_mapping[('INVALID_SORT_FIELD', None)] = InvalidSortField('The field is not valid for this object. The error_subtype will hold the field name this applies to')
        errors_mapping[('INVALID_SORT_ORDER', None)] = InvalidSortOrder('The sort order for the field is invalid. The error_subtype will hold the field name this applies to')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The node can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to do this')
        query_data = {
            'api': self._api,
            'url': '/node/progress/list',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        query_data['paginated_field'] = 'progresses'
        return QueryOPSF(**query_data)
    
    def progress_get(
        self,
        uuid,
    ):
        """Progress get.
        :param uuid: The node progress uuid
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The record can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to do this')
        query_data = {
            'api': self._api,
            'url': '/node/progress/get',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    