""" Order.

Do not edit this file by hand.
This is generated by parsing api.html service doc.
"""
from ambra_sdk.exceptions.service import FilterNotFound
from ambra_sdk.exceptions.service import InvalidCondition
from ambra_sdk.exceptions.service import InvalidCustomfield
from ambra_sdk.exceptions.service import InvalidField
from ambra_sdk.exceptions.service import InvalidSortField
from ambra_sdk.exceptions.service import InvalidSortOrder
from ambra_sdk.exceptions.service import InvalidStatus
from ambra_sdk.exceptions.service import MissingFields
from ambra_sdk.exceptions.service import NotFound
from ambra_sdk.exceptions.service import NotPermitted
from ambra_sdk.service.query import QueryO
from ambra_sdk.service.query import AsyncQueryO
from ambra_sdk.service.query import QueryOF
from ambra_sdk.service.query import AsyncQueryOF
from ambra_sdk.service.query import QueryOPSF
from ambra_sdk.service.query import AsyncQueryOPSF

class Order:
    """Order."""

    def __init__(self, api):
        self._api = api

    
    def add(
        self,
        accession_number,
        account_id,
        patient_birth_date,
        patient_name,
        patient_sex,
        patientid,
        referring_physician,
        sending_facility,
        customfield_param=None,
    ):
        """Add.

        :param accession_number: Accession number
        :param account_id: uuid of the account to add them to
        :param patient_birth_date: DOB
        :param patient_name: Patient name
        :param patient_sex: Gender
        :param patientid: Patient MRN
        :param referring_physician: Referring physician
        :param sending_facility: Sending facility
        :param customfield_param: Expected values are CUSTOMFIELD_UUID. Custom field(s) (optional)
        """
        request_data = {
           'accession_number': accession_number,
           'account_id': account_id,
           'patient_birth_date': patient_birth_date,
           'patient_name': patient_name,
           'patient_sex': patient_sex,
           'patientid': patientid,
           'referring_physician': referring_physician,
           'sending_facility': sending_facility,
        }
        if customfield_param is not None:
            customfield_param_dict = {'{prefix}{k}'.format(prefix='customfield-', k=k): v for k,v in customfield_param.items()}
            request_data.update(customfield_param_dict)
	
        errors_mapping = {}
        errors_mapping[('INVALID_CUSTOMFIELD', None)] = InvalidCustomfield('Invalid custom field(s) name or value were passed. The error_subtype holds an array of the error details')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The account was not found. The error_subtype holds the type of field not found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to add a order to the account')
        query_data = {
            'api': self._api,
            'url': '/order/add',
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

        :param uuid: The order uuid
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The order can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view this order')
        query_data = {
            'api': self._api,
            'url': '/order/get',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def set(
        self,
        accession_number,
        patient_birth_date,
        patient_name,
        patient_sex,
        patientid,
        referring_physician,
        sending_facility,
        uuid,
        customfield_param=None,
    ):
        """Set.

        :param accession_number: Accession number
        :param patient_birth_date: DOB
        :param patient_name: Patient name
        :param patient_sex: Gender
        :param patientid: Patient MRN
        :param referring_physician: Referring physician
        :param sending_facility: Sending facility
        :param uuid: The order uuid
        :param customfield_param: Expected values are CUSTOMFIELD_UUID. Custom field(s) (optional)
        """
        request_data = {
           'accession_number': accession_number,
           'patient_birth_date': patient_birth_date,
           'patient_name': patient_name,
           'patient_sex': patient_sex,
           'patientid': patientid,
           'referring_physician': referring_physician,
           'sending_facility': sending_facility,
           'uuid': uuid,
        }
        if customfield_param is not None:
            customfield_param_dict = {'{prefix}{k}'.format(prefix='customfield-', k=k): v for k,v in customfield_param.items()}
            request_data.update(customfield_param_dict)
	
        errors_mapping = {}
        errors_mapping[('INVALID_CUSTOMFIELD', None)] = InvalidCustomfield('Invalid custom field(s) name or value were passed. The error_subtype holds an array of the error details')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The order can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to edit the order')
        query_data = {
            'api': self._api,
            'url': '/order/set',
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

        :param uuid: The order uuid
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The order can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to delete the order')
        query_data = {
            'api': self._api,
            'url': '/order/delete',
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
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view orders in this account')
        query_data = {
            'api': self._api,
            'url': '/order/list',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        query_data['paginated_field'] = 'orders'
        return QueryOPSF(**query_data)
    
    def sps_add(
        self,
        modality,
        order_id,
        requested_procedure_description,
        requested_procedure_id,
        scheduled_procedure_step_description,
        scheduled_procedure_step_id,
        scheduled_procedure_step_start_date,
        scheduled_procedure_step_start_time,
        scheduled_station_aetitle,
    ):
        """Sps add.

        :param modality: Modality
        :param order_id: uuid of the order
        :param requested_procedure_description: Procedure description
        :param requested_procedure_id: Procedure ID
        :param scheduled_procedure_step_description: Step description
        :param scheduled_procedure_step_id: Step ID
        :param scheduled_procedure_step_start_date: Start date
        :param scheduled_procedure_step_start_time: Start time
        :param scheduled_station_aetitle: Station AE title
        """
        request_data = {
           'modality': modality,
           'order_id': order_id,
           'requested_procedure_description': requested_procedure_description,
           'requested_procedure_id': requested_procedure_id,
           'scheduled_procedure_step_description': scheduled_procedure_step_description,
           'scheduled_procedure_step_id': scheduled_procedure_step_id,
           'scheduled_procedure_step_start_date': scheduled_procedure_step_start_date,
           'scheduled_procedure_step_start_time': scheduled_procedure_step_start_time,
           'scheduled_station_aetitle': scheduled_station_aetitle,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The order can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to edit orders in this account')
        query_data = {
            'api': self._api,
            'url': '/order/sps/add',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def sps_set(
        self,
        uuid,
        modality=None,
        requested_procedure_description=None,
        requested_procedure_id=None,
        scheduled_procedure_step_description=None,
        scheduled_procedure_step_id=None,
        scheduled_procedure_step_start_date=None,
        scheduled_procedure_step_start_time=None,
        scheduled_station_aetitle=None,
    ):
        """Sps set.

        :param uuid: UUID of the SPS
        :param modality: Modality (optional)
        :param requested_procedure_description: Procedure description (optional)
        :param requested_procedure_id: Procedure ID (optional)
        :param scheduled_procedure_step_description: Step description (optional)
        :param scheduled_procedure_step_id: Step ID (optional)
        :param scheduled_procedure_step_start_date: Start date (optional)
        :param scheduled_procedure_step_start_time: Start time (optional)
        :param scheduled_station_aetitle: Station AE title (optional)
        """
        request_data = {
           'modality': modality,
           'requested_procedure_description': requested_procedure_description,
           'requested_procedure_id': requested_procedure_id,
           'scheduled_procedure_step_description': scheduled_procedure_step_description,
           'scheduled_procedure_step_id': scheduled_procedure_step_id,
           'scheduled_procedure_step_start_date': scheduled_procedure_step_start_date,
           'scheduled_procedure_step_start_time': scheduled_procedure_step_start_time,
           'scheduled_station_aetitle': scheduled_station_aetitle,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The SPS can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to edit orders in this account')
        query_data = {
            'api': self._api,
            'url': '/order/sps/set',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def sps_delete(
        self,
        uuid,
    ):
        """Sps delete.

        :param uuid: UUID of the SPS
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The SPS can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to edit orders in this account')
        query_data = {
            'api': self._api,
            'url': '/order/sps/delete',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def sps_status(
        self,
        mpps_status,
        mpps_uid,
        serial_no,
        uuid,
    ):
        """Sps status.

        :param mpps_status: The mpps status to set (PENDING|IN_PROGRESS|DISCONTINUED|COMPLETED)
        :param mpps_uid: The mpps UUID of the SPS
        :param serial_no: The serial number of the node
        :param uuid: The node id
        """
        request_data = {
           'mpps_status': mpps_status,
           'mpps_uid': mpps_uid,
           'serial_no': serial_no,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_STATUS', None)] = InvalidStatus('An invalid status was passed')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The SPS can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to set the status')
        query_data = {
            'api': self._api,
            'url': '/order/sps/status',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': False,
        }
        return QueryO(**query_data)
    
    def sps_find(
        self,
        account_id,
        node_id=None,
        serial_no=None,
    ):
        """Sps find.

        :param account_id: The account uuid if sid authentication is used
        :param node_id: node_id
        :param serial_no: serial_no
        """
        request_data = {
           'account_id': account_id,
           'node_id': node_id,
           'serial_no': serial_no,
        }
	
        errors_mapping = {}
        errors_mapping[('FILTER_NOT_FOUND', None)] = FilterNotFound('The filter can not be found. The error_subtype will hold the filter UUID')
        errors_mapping[('INVALID_CONDITION', None)] = InvalidCondition('The condition is not support. The error_subtype will hold the filter expression this applies to')
        errors_mapping[('INVALID_FIELD', None)] = InvalidField('The field is not valid for this object. The error_subtype will hold the filter expression this applies to')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The node can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view orders in this account')
        query_data = {
            'api': self._api,
            'url': '/order/sps/find',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryOF(**query_data)
    


class AsyncOrder:
    """AsyncOrder."""

    def __init__(self, api):
        self._api = api

    
    def add(
        self,
        accession_number,
        account_id,
        patient_birth_date,
        patient_name,
        patient_sex,
        patientid,
        referring_physician,
        sending_facility,
        customfield_param=None,
    ):
        """Add.

        :param accession_number: Accession number
        :param account_id: uuid of the account to add them to
        :param patient_birth_date: DOB
        :param patient_name: Patient name
        :param patient_sex: Gender
        :param patientid: Patient MRN
        :param referring_physician: Referring physician
        :param sending_facility: Sending facility
        :param customfield_param: Expected values are CUSTOMFIELD_UUID. Custom field(s) (optional)
        """
        request_data = {
           'accession_number': accession_number,
           'account_id': account_id,
           'patient_birth_date': patient_birth_date,
           'patient_name': patient_name,
           'patient_sex': patient_sex,
           'patientid': patientid,
           'referring_physician': referring_physician,
           'sending_facility': sending_facility,
        }
        if customfield_param is not None:
            customfield_param_dict = {'{prefix}{k}'.format(prefix='customfield-', k=k): v for k,v in customfield_param.items()}
            request_data.update(customfield_param_dict)
	
        errors_mapping = {}
        errors_mapping[('INVALID_CUSTOMFIELD', None)] = InvalidCustomfield('Invalid custom field(s) name or value were passed. The error_subtype holds an array of the error details')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The account was not found. The error_subtype holds the type of field not found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to add a order to the account')
        query_data = {
            'api': self._api,
            'url': '/order/add',
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

        :param uuid: The order uuid
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The order can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view this order')
        query_data = {
            'api': self._api,
            'url': '/order/get',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return AsyncQueryO(**query_data)
    
    def set(
        self,
        accession_number,
        patient_birth_date,
        patient_name,
        patient_sex,
        patientid,
        referring_physician,
        sending_facility,
        uuid,
        customfield_param=None,
    ):
        """Set.

        :param accession_number: Accession number
        :param patient_birth_date: DOB
        :param patient_name: Patient name
        :param patient_sex: Gender
        :param patientid: Patient MRN
        :param referring_physician: Referring physician
        :param sending_facility: Sending facility
        :param uuid: The order uuid
        :param customfield_param: Expected values are CUSTOMFIELD_UUID. Custom field(s) (optional)
        """
        request_data = {
           'accession_number': accession_number,
           'patient_birth_date': patient_birth_date,
           'patient_name': patient_name,
           'patient_sex': patient_sex,
           'patientid': patientid,
           'referring_physician': referring_physician,
           'sending_facility': sending_facility,
           'uuid': uuid,
        }
        if customfield_param is not None:
            customfield_param_dict = {'{prefix}{k}'.format(prefix='customfield-', k=k): v for k,v in customfield_param.items()}
            request_data.update(customfield_param_dict)
	
        errors_mapping = {}
        errors_mapping[('INVALID_CUSTOMFIELD', None)] = InvalidCustomfield('Invalid custom field(s) name or value were passed. The error_subtype holds an array of the error details')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The order can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to edit the order')
        query_data = {
            'api': self._api,
            'url': '/order/set',
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

        :param uuid: The order uuid
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The order can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to delete the order')
        query_data = {
            'api': self._api,
            'url': '/order/delete',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return AsyncQueryO(**query_data)
    
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
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view orders in this account')
        query_data = {
            'api': self._api,
            'url': '/order/list',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        query_data['paginated_field'] = 'orders'
        return AsyncQueryOPSF(**query_data)
    
    def sps_add(
        self,
        modality,
        order_id,
        requested_procedure_description,
        requested_procedure_id,
        scheduled_procedure_step_description,
        scheduled_procedure_step_id,
        scheduled_procedure_step_start_date,
        scheduled_procedure_step_start_time,
        scheduled_station_aetitle,
    ):
        """Sps add.

        :param modality: Modality
        :param order_id: uuid of the order
        :param requested_procedure_description: Procedure description
        :param requested_procedure_id: Procedure ID
        :param scheduled_procedure_step_description: Step description
        :param scheduled_procedure_step_id: Step ID
        :param scheduled_procedure_step_start_date: Start date
        :param scheduled_procedure_step_start_time: Start time
        :param scheduled_station_aetitle: Station AE title
        """
        request_data = {
           'modality': modality,
           'order_id': order_id,
           'requested_procedure_description': requested_procedure_description,
           'requested_procedure_id': requested_procedure_id,
           'scheduled_procedure_step_description': scheduled_procedure_step_description,
           'scheduled_procedure_step_id': scheduled_procedure_step_id,
           'scheduled_procedure_step_start_date': scheduled_procedure_step_start_date,
           'scheduled_procedure_step_start_time': scheduled_procedure_step_start_time,
           'scheduled_station_aetitle': scheduled_station_aetitle,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The order can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to edit orders in this account')
        query_data = {
            'api': self._api,
            'url': '/order/sps/add',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return AsyncQueryO(**query_data)
    
    def sps_set(
        self,
        uuid,
        modality=None,
        requested_procedure_description=None,
        requested_procedure_id=None,
        scheduled_procedure_step_description=None,
        scheduled_procedure_step_id=None,
        scheduled_procedure_step_start_date=None,
        scheduled_procedure_step_start_time=None,
        scheduled_station_aetitle=None,
    ):
        """Sps set.

        :param uuid: UUID of the SPS
        :param modality: Modality (optional)
        :param requested_procedure_description: Procedure description (optional)
        :param requested_procedure_id: Procedure ID (optional)
        :param scheduled_procedure_step_description: Step description (optional)
        :param scheduled_procedure_step_id: Step ID (optional)
        :param scheduled_procedure_step_start_date: Start date (optional)
        :param scheduled_procedure_step_start_time: Start time (optional)
        :param scheduled_station_aetitle: Station AE title (optional)
        """
        request_data = {
           'modality': modality,
           'requested_procedure_description': requested_procedure_description,
           'requested_procedure_id': requested_procedure_id,
           'scheduled_procedure_step_description': scheduled_procedure_step_description,
           'scheduled_procedure_step_id': scheduled_procedure_step_id,
           'scheduled_procedure_step_start_date': scheduled_procedure_step_start_date,
           'scheduled_procedure_step_start_time': scheduled_procedure_step_start_time,
           'scheduled_station_aetitle': scheduled_station_aetitle,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The SPS can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to edit orders in this account')
        query_data = {
            'api': self._api,
            'url': '/order/sps/set',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return AsyncQueryO(**query_data)
    
    def sps_delete(
        self,
        uuid,
    ):
        """Sps delete.

        :param uuid: UUID of the SPS
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The SPS can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to edit orders in this account')
        query_data = {
            'api': self._api,
            'url': '/order/sps/delete',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return AsyncQueryO(**query_data)
    
    def sps_status(
        self,
        mpps_status,
        mpps_uid,
        serial_no,
        uuid,
    ):
        """Sps status.

        :param mpps_status: The mpps status to set (PENDING|IN_PROGRESS|DISCONTINUED|COMPLETED)
        :param mpps_uid: The mpps UUID of the SPS
        :param serial_no: The serial number of the node
        :param uuid: The node id
        """
        request_data = {
           'mpps_status': mpps_status,
           'mpps_uid': mpps_uid,
           'serial_no': serial_no,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_STATUS', None)] = InvalidStatus('An invalid status was passed')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The SPS can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to set the status')
        query_data = {
            'api': self._api,
            'url': '/order/sps/status',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': False,
        }
        return AsyncQueryO(**query_data)
    
    def sps_find(
        self,
        account_id,
        node_id=None,
        serial_no=None,
    ):
        """Sps find.

        :param account_id: The account uuid if sid authentication is used
        :param node_id: node_id
        :param serial_no: serial_no
        """
        request_data = {
           'account_id': account_id,
           'node_id': node_id,
           'serial_no': serial_no,
        }
	
        errors_mapping = {}
        errors_mapping[('FILTER_NOT_FOUND', None)] = FilterNotFound('The filter can not be found. The error_subtype will hold the filter UUID')
        errors_mapping[('INVALID_CONDITION', None)] = InvalidCondition('The condition is not support. The error_subtype will hold the filter expression this applies to')
        errors_mapping[('INVALID_FIELD', None)] = InvalidField('The field is not valid for this object. The error_subtype will hold the filter expression this applies to')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The node can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view orders in this account')
        query_data = {
            'api': self._api,
            'url': '/order/sps/find',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return AsyncQueryOF(**query_data)
    