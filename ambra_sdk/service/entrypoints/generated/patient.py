""" Patient.

Do not edit this file by hand.
This is generated by parsing api.html service doc.
"""
from ambra_sdk.exceptions.service import AlreadyExists
from ambra_sdk.exceptions.service import AlreadyUsed
from ambra_sdk.exceptions.service import FilterNotFound
from ambra_sdk.exceptions.service import InvalidCondition
from ambra_sdk.exceptions.service import InvalidCustomfield
from ambra_sdk.exceptions.service import InvalidDate
from ambra_sdk.exceptions.service import InvalidEmail
from ambra_sdk.exceptions.service import InvalidField
from ambra_sdk.exceptions.service import InvalidPhone
from ambra_sdk.exceptions.service import InvalidPin
from ambra_sdk.exceptions.service import InvalidSortField
from ambra_sdk.exceptions.service import InvalidSortOrder
from ambra_sdk.exceptions.service import Lockout
from ambra_sdk.exceptions.service import MissingFields
from ambra_sdk.exceptions.service import NotFound
from ambra_sdk.exceptions.service import NotPermitted
from ambra_sdk.service.query import QueryO
from ambra_sdk.service.query import AsyncQueryO
from ambra_sdk.service.query import QueryOPS
from ambra_sdk.service.query import AsyncQueryOPS
from ambra_sdk.service.query import QueryOPSF
from ambra_sdk.service.query import AsyncQueryOPSF

class Patient:
    """Patient."""

    def __init__(self, api):
        self._api = api

    
    def add(
        self,
        account_id,
        alt_email=None,
        alt_mobile_phone=None,
        birth_date=None,
        customfield_param=None,
        email=None,
        event_new_report=None,
        event_share=None,
        first=None,
        last=None,
        mobile_phone=None,
        mrn=None,
        name=None,
        sex=None,
        study_id=None,
    ):
        """Add.

        :param account_id: uuid of the account to add them to
        :param alt_email: Alternate email address (optional)
        :param alt_mobile_phone: Alternate mobile phone number (optional)
        :param birth_date: Birth date (optional)
        :param customfield_param: Custom field(s) (optional)
        :param email: Email address (optional)
        :param event_new_report: Notify the patient if a report is attached on the patient portal (optional)
        :param event_share: Notify the patient if a new study is available on the patient portal (optional)
        :param first: first
        :param last: last
        :param mobile_phone: Mobile phone number (optional)
        :param mrn: MRN (optional if study_id is used)
        :param name: name
        :param sex: Gender (optional)
        :param study_id: Id of the study to create a patient from (optional)
        """
        request_data = {
           'account_id': account_id,
           'alt_email': alt_email,
           'alt_mobile_phone': alt_mobile_phone,
           'birth_date': birth_date,
           'email': email,
           'event_new_report': event_new_report,
           'event_share': event_share,
           'first': first,
           'last': last,
           'mobile_phone': mobile_phone,
           'mrn': mrn,
           'name': name,
           'sex': sex,
           'study_id': study_id,
        }
        if customfield_param is not None:
            customfield_param_dict = {'{prefix}{k}'.format(prefix='customfield-', k=k): v for k,v in customfield_param.items()}
            request_data.update(customfield_param_dict)
	
        errors_mapping = {}
        errors_mapping[('ALREADY_EXISTS', None)] = AlreadyExists('The patient is already in the account')
        errors_mapping[('ALREADY_USED', None)] = AlreadyUsed('The email or phone number is already used by another patient. The error_subtype holds the field that is already used')
        errors_mapping[('INVALID_CUSTOMFIELD', None)] = InvalidCustomfield('Invalid custom field(s) name or value were passed. The error_subtype holds an array of the error details')
        errors_mapping[('INVALID_EMAIL', None)] = InvalidEmail('The email is invalid')
        errors_mapping[('INVALID_PHONE', None)] = InvalidPhone('The phone number is invalid')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The account or study was not found. The error_subtype holds the type of field not found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to add a patient to the account')
        query_data = {
            'api': self._api,
            'url': '/patient/add',
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

        :param uuid: The patient uuid
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The patient can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view this patient')
        query_data = {
            'api': self._api,
            'url': '/patient/get',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def set(
        self,
        birth_date,
        mrn,
        sex,
        uuid,
        alt_email=None,
        alt_mobile_phone=None,
        customfield_param=None,
        email=None,
        event_new_report=None,
        event_share=None,
        first=None,
        last=None,
        mobile_phone=None,
        name=None,
    ):
        """Set.

        :param birth_date: Birth date
        :param mrn: MRN
        :param sex: Gender
        :param uuid: The patient uuid
        :param alt_email: Alternate email address (optional)
        :param alt_mobile_phone: Alternate mobile phone number (optional)
        :param customfield_param: Custom field(s) (optional)
        :param email: Email address (optional)
        :param event_new_report: Notify the patient if a report is attached on the patient portal (optional)
        :param event_share: Notify the patient if a new study is available on the patient portal (optional)
        :param first: first
        :param last: last
        :param mobile_phone: Mobile phone number (optional)
        :param name: name
        """
        request_data = {
           'alt_email': alt_email,
           'alt_mobile_phone': alt_mobile_phone,
           'birth_date': birth_date,
           'email': email,
           'event_new_report': event_new_report,
           'event_share': event_share,
           'first': first,
           'last': last,
           'mobile_phone': mobile_phone,
           'mrn': mrn,
           'name': name,
           'sex': sex,
           'uuid': uuid,
        }
        if customfield_param is not None:
            customfield_param_dict = {'{prefix}{k}'.format(prefix='customfield-', k=k): v for k,v in customfield_param.items()}
            request_data.update(customfield_param_dict)
	
        errors_mapping = {}
        errors_mapping[('ALREADY_EXISTS', None)] = AlreadyExists('The MRN is in use by another patient')
        errors_mapping[('ALREADY_USED', None)] = AlreadyUsed('The email or phone number is already used by another patient. The error_subtype holds the field that is already used')
        errors_mapping[('INVALID_CUSTOMFIELD', None)] = InvalidCustomfield('Invalid custom field(s) name or value were passed. The error_subtype holds an array of the error details')
        errors_mapping[('INVALID_EMAIL', None)] = InvalidEmail('The email is invalid')
        errors_mapping[('INVALID_PHONE', None)] = InvalidPhone('The phone number is invalid')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The patient can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to edit the patient')
        query_data = {
            'api': self._api,
            'url': '/patient/set',
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

        :param uuid: The patient uuid
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The patient can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to delete the patient')
        query_data = {
            'api': self._api,
            'url': '/patient/delete',
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
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view patients in this account')
        query_data = {
            'api': self._api,
            'url': '/patient/list',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        query_data['paginated_field'] = 'patients'
        return QueryOPSF(**query_data)
    
    def study_list(
        self,
        uuid,
        viewable_only,
    ):
        """Study list.

        :param uuid: The patient id
        :param viewable_only: Flag if they only want the studies the user can view
        """
        request_data = {
           'uuid': uuid,
           'viewable_only': viewable_only,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The patient can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view this patient')
        query_data = {
            'api': self._api,
            'url': '/patient/study/list',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def portal_find(
        self,
        birth_date,
        first,
        last,
        mrn,
    ):
        """Portal find.

        :param birth_date: Date of birth
        :param first: The first name
        :param last: The last name
        :param mrn: MRN (required if the require_mrn_for_patient_portal account setting is on)
        """
        request_data = {
           'birth_date': birth_date,
           'first': first,
           'last': last,
           'mrn': mrn,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_DATE', None)] = InvalidDate('An invalid date was passed')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The patient can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to perform this search')
        query_data = {
            'api': self._api,
            'url': '/patient/portal/find',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': False,
        }
        return QueryO(**query_data)
    
    def portal_pin(
        self,
        alt_email,
        alt_mobile_phone,
        email,
        mobile_phone,
        patient_id,
    ):
        """Portal pin.

        :param alt_email: Flag if they want the PIN sent via the alt_email
        :param alt_mobile_phone: Flag if they want the PIN sent via SMS to the alt_mobile_phone
        :param email: Flag if they want the PIN sent via email
        :param mobile_phone: Flag if they want the PIN sent via SMS
        :param patient_id: The patient id
        """
        request_data = {
           'alt_email': alt_email,
           'alt_mobile_phone': alt_mobile_phone,
           'email': email,
           'mobile_phone': mobile_phone,
           'patient_id': patient_id,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The patient can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to do this')
        query_data = {
            'api': self._api,
            'url': '/patient/portal/pin',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': False,
        }
        return QueryO(**query_data)
    
    def portal_login(
        self,
        patient_id,
        pin,
    ):
        """Portal login.

        :param patient_id: The patient id
        :param pin: The PIN
        """
        request_data = {
           'patient_id': patient_id,
           'pin': pin,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_PIN', None)] = InvalidPin('The PIN is invalid or expired')
        errors_mapping[('LOCKOUT', None)] = Lockout('Too many failed attempts')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The patient can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to do this')
        query_data = {
            'api': self._api,
            'url': '/patient/portal/login',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': False,
        }
        return QueryO(**query_data)
    
    def portal_list(
        self,
    ):
        """Portal list.

        """
        request_data = {
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_SORT_FIELD', None)] = InvalidSortField('The field is not valid for this object. The error_subtype will hold the field name this applies to')
        errors_mapping[('INVALID_SORT_ORDER', None)] = InvalidSortOrder('The sort order for the field is invalid. The error_subtype will hold the field name this applies to')
        query_data = {
            'api': self._api,
            'url': '/patient/portal/list',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': False,
        }
        query_data['paginated_field'] = 'portals'
        return QueryOPS(**query_data)
    


class AsyncPatient:
    """AsyncPatient."""

    def __init__(self, api):
        self._api = api

    
    def add(
        self,
        account_id,
        alt_email=None,
        alt_mobile_phone=None,
        birth_date=None,
        customfield_param=None,
        email=None,
        event_new_report=None,
        event_share=None,
        first=None,
        last=None,
        mobile_phone=None,
        mrn=None,
        name=None,
        sex=None,
        study_id=None,
    ):
        """Add.

        :param account_id: uuid of the account to add them to
        :param alt_email: Alternate email address (optional)
        :param alt_mobile_phone: Alternate mobile phone number (optional)
        :param birth_date: Birth date (optional)
        :param customfield_param: Custom field(s) (optional)
        :param email: Email address (optional)
        :param event_new_report: Notify the patient if a report is attached on the patient portal (optional)
        :param event_share: Notify the patient if a new study is available on the patient portal (optional)
        :param first: first
        :param last: last
        :param mobile_phone: Mobile phone number (optional)
        :param mrn: MRN (optional if study_id is used)
        :param name: name
        :param sex: Gender (optional)
        :param study_id: Id of the study to create a patient from (optional)
        """
        request_data = {
           'account_id': account_id,
           'alt_email': alt_email,
           'alt_mobile_phone': alt_mobile_phone,
           'birth_date': birth_date,
           'email': email,
           'event_new_report': event_new_report,
           'event_share': event_share,
           'first': first,
           'last': last,
           'mobile_phone': mobile_phone,
           'mrn': mrn,
           'name': name,
           'sex': sex,
           'study_id': study_id,
        }
        if customfield_param is not None:
            customfield_param_dict = {'{prefix}{k}'.format(prefix='customfield-', k=k): v for k,v in customfield_param.items()}
            request_data.update(customfield_param_dict)
	
        errors_mapping = {}
        errors_mapping[('ALREADY_EXISTS', None)] = AlreadyExists('The patient is already in the account')
        errors_mapping[('ALREADY_USED', None)] = AlreadyUsed('The email or phone number is already used by another patient. The error_subtype holds the field that is already used')
        errors_mapping[('INVALID_CUSTOMFIELD', None)] = InvalidCustomfield('Invalid custom field(s) name or value were passed. The error_subtype holds an array of the error details')
        errors_mapping[('INVALID_EMAIL', None)] = InvalidEmail('The email is invalid')
        errors_mapping[('INVALID_PHONE', None)] = InvalidPhone('The phone number is invalid')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The account or study was not found. The error_subtype holds the type of field not found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to add a patient to the account')
        query_data = {
            'api': self._api,
            'url': '/patient/add',
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

        :param uuid: The patient uuid
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The patient can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view this patient')
        query_data = {
            'api': self._api,
            'url': '/patient/get',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return AsyncQueryO(**query_data)
    
    def set(
        self,
        birth_date,
        mrn,
        sex,
        uuid,
        alt_email=None,
        alt_mobile_phone=None,
        customfield_param=None,
        email=None,
        event_new_report=None,
        event_share=None,
        first=None,
        last=None,
        mobile_phone=None,
        name=None,
    ):
        """Set.

        :param birth_date: Birth date
        :param mrn: MRN
        :param sex: Gender
        :param uuid: The patient uuid
        :param alt_email: Alternate email address (optional)
        :param alt_mobile_phone: Alternate mobile phone number (optional)
        :param customfield_param: Custom field(s) (optional)
        :param email: Email address (optional)
        :param event_new_report: Notify the patient if a report is attached on the patient portal (optional)
        :param event_share: Notify the patient if a new study is available on the patient portal (optional)
        :param first: first
        :param last: last
        :param mobile_phone: Mobile phone number (optional)
        :param name: name
        """
        request_data = {
           'alt_email': alt_email,
           'alt_mobile_phone': alt_mobile_phone,
           'birth_date': birth_date,
           'email': email,
           'event_new_report': event_new_report,
           'event_share': event_share,
           'first': first,
           'last': last,
           'mobile_phone': mobile_phone,
           'mrn': mrn,
           'name': name,
           'sex': sex,
           'uuid': uuid,
        }
        if customfield_param is not None:
            customfield_param_dict = {'{prefix}{k}'.format(prefix='customfield-', k=k): v for k,v in customfield_param.items()}
            request_data.update(customfield_param_dict)
	
        errors_mapping = {}
        errors_mapping[('ALREADY_EXISTS', None)] = AlreadyExists('The MRN is in use by another patient')
        errors_mapping[('ALREADY_USED', None)] = AlreadyUsed('The email or phone number is already used by another patient. The error_subtype holds the field that is already used')
        errors_mapping[('INVALID_CUSTOMFIELD', None)] = InvalidCustomfield('Invalid custom field(s) name or value were passed. The error_subtype holds an array of the error details')
        errors_mapping[('INVALID_EMAIL', None)] = InvalidEmail('The email is invalid')
        errors_mapping[('INVALID_PHONE', None)] = InvalidPhone('The phone number is invalid')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The patient can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to edit the patient')
        query_data = {
            'api': self._api,
            'url': '/patient/set',
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

        :param uuid: The patient uuid
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The patient can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to delete the patient')
        query_data = {
            'api': self._api,
            'url': '/patient/delete',
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
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view patients in this account')
        query_data = {
            'api': self._api,
            'url': '/patient/list',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        query_data['paginated_field'] = 'patients'
        return AsyncQueryOPSF(**query_data)
    
    def study_list(
        self,
        uuid,
        viewable_only,
    ):
        """Study list.

        :param uuid: The patient id
        :param viewable_only: Flag if they only want the studies the user can view
        """
        request_data = {
           'uuid': uuid,
           'viewable_only': viewable_only,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The patient can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view this patient')
        query_data = {
            'api': self._api,
            'url': '/patient/study/list',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return AsyncQueryO(**query_data)
    
    def portal_find(
        self,
        birth_date,
        first,
        last,
        mrn,
    ):
        """Portal find.

        :param birth_date: Date of birth
        :param first: The first name
        :param last: The last name
        :param mrn: MRN (required if the require_mrn_for_patient_portal account setting is on)
        """
        request_data = {
           'birth_date': birth_date,
           'first': first,
           'last': last,
           'mrn': mrn,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_DATE', None)] = InvalidDate('An invalid date was passed')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The patient can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to perform this search')
        query_data = {
            'api': self._api,
            'url': '/patient/portal/find',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': False,
        }
        return AsyncQueryO(**query_data)
    
    def portal_pin(
        self,
        alt_email,
        alt_mobile_phone,
        email,
        mobile_phone,
        patient_id,
    ):
        """Portal pin.

        :param alt_email: Flag if they want the PIN sent via the alt_email
        :param alt_mobile_phone: Flag if they want the PIN sent via SMS to the alt_mobile_phone
        :param email: Flag if they want the PIN sent via email
        :param mobile_phone: Flag if they want the PIN sent via SMS
        :param patient_id: The patient id
        """
        request_data = {
           'alt_email': alt_email,
           'alt_mobile_phone': alt_mobile_phone,
           'email': email,
           'mobile_phone': mobile_phone,
           'patient_id': patient_id,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The patient can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to do this')
        query_data = {
            'api': self._api,
            'url': '/patient/portal/pin',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': False,
        }
        return AsyncQueryO(**query_data)
    
    def portal_login(
        self,
        patient_id,
        pin,
    ):
        """Portal login.

        :param patient_id: The patient id
        :param pin: The PIN
        """
        request_data = {
           'patient_id': patient_id,
           'pin': pin,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_PIN', None)] = InvalidPin('The PIN is invalid or expired')
        errors_mapping[('LOCKOUT', None)] = Lockout('Too many failed attempts')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The patient can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to do this')
        query_data = {
            'api': self._api,
            'url': '/patient/portal/login',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': False,
        }
        return AsyncQueryO(**query_data)
    
    def portal_list(
        self,
    ):
        """Portal list.

        """
        request_data = {
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_SORT_FIELD', None)] = InvalidSortField('The field is not valid for this object. The error_subtype will hold the field name this applies to')
        errors_mapping[('INVALID_SORT_ORDER', None)] = InvalidSortOrder('The sort order for the field is invalid. The error_subtype will hold the field name this applies to')
        query_data = {
            'api': self._api,
            'url': '/patient/portal/list',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': False,
        }
        query_data['paginated_field'] = 'portals'
        return AsyncQueryOPS(**query_data)
    