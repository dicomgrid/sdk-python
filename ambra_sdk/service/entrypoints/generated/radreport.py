""" Radreport.

Do not edit this file by hand.
This is generated by parsing api.html service doc.
"""
from ambra_sdk.exceptions.service import FilterNotFound
from ambra_sdk.exceptions.service import InvalidAction
from ambra_sdk.exceptions.service import InvalidCondition
from ambra_sdk.exceptions.service import InvalidEmail
from ambra_sdk.exceptions.service import InvalidField
from ambra_sdk.exceptions.service import InvalidJson
from ambra_sdk.exceptions.service import InvalidPhone
from ambra_sdk.exceptions.service import InvalidSortField
from ambra_sdk.exceptions.service import InvalidSortOrder
from ambra_sdk.exceptions.service import MissingFields
from ambra_sdk.exceptions.service import NoAttachment
from ambra_sdk.exceptions.service import NotEnabled
from ambra_sdk.exceptions.service import NotFound
from ambra_sdk.exceptions.service import NotPermitted
from ambra_sdk.exceptions.service import NotSysadminOrSupport
from ambra_sdk.exceptions.service import PdfFailed
from ambra_sdk.service.query import QueryO
from ambra_sdk.service.query import QueryOPSF

class Radreport:
    """Radreport."""

    def __init__(self, api):
        self._api = api

    
    def add(
        self,
        study_id,
        type,
        fields=None,
    ):
        """Add.
        :param study_id: Id of the study to add the radreport to
        :param type: The type of the radreport
        :param fields: A JSON hash of the fields in the report (optional)
        """
        request_data = {
           'fields': fields,
           'study_id': study_id,
           'type': type,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_JSON', None)] = InvalidJson('The field is not in valid JSON format. The error_subtype holds the name of the field')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The study was not found.')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to add a radreport to the study')
        query_data = {
            'api': self._api,
            'url': '/radreport/add',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def set(
        self,
        uuid,
        attachment=None,
        fields=None,
    ):
        """Set.
        :param uuid: Id of the radreport
        :param attachment: A JSON hash of the storage attachment information (optional)
        :param fields: A JSON hash of the fields in the report (optional)
        """
        request_data = {
           'attachment': attachment,
           'fields': fields,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_JSON', None)] = InvalidJson('The field is not in valid JSON format. The error_subtype holds the name of the field')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The study was not found.')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to add a radreport to the study')
        query_data = {
            'api': self._api,
            'url': '/radreport/set',
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
        :param uuid: Id of the radreport
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The radreport  was not found.')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view the radreport')
        query_data = {
            'api': self._api,
            'url': '/radreport/get',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def audit(
        self,
        action,
        detail,
        uuid,
    ):
        """Audit.
        :param action: The audit action (SIGNED|MEDICAL_EDIT|ADMIN_EDIT|REPORT_GENERATED)
        :param detail: Additional information
        :param uuid: The id of the radreport
        """
        request_data = {
           'action': action,
           'detail': detail,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_ACTION', None)] = InvalidAction('An invalid action was passed')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The radreport can not be found')
        query_data = {
            'api': self._api,
            'url': '/radreport/audit',
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
        :param uuid: Id of the radreport
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The radreport  was not found.')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to delete the radreport')
        query_data = {
            'api': self._api,
            'url': '/radreport/delete',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def description(
        self,
        uuid,
    ):
        """Description.
        :param uuid: Id of the radreport
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The radreport  was not found.')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view the radreport')
        query_data = {
            'api': self._api,
            'url': '/radreport/description',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def user_list(
        self,
        user_id,
    ):
        """User list.
        :param user_id: The user id
        """
        request_data = {
           'user_id': user_id,
        }
	
        errors_mapping = {}
        errors_mapping[('FILTER_NOT_FOUND', None)] = FilterNotFound('The filter can not be found. The error_subtype will hold the filter UUID')
        errors_mapping[('INVALID_CONDITION', None)] = InvalidCondition('The condition is not support. The error_subtype will hold the filter expression this applies to')
        errors_mapping[('INVALID_FIELD', None)] = InvalidField('The field is not valid for this object. The error_subtype will hold the filter expression this applies to')
        errors_mapping[('INVALID_SORT_FIELD', None)] = InvalidSortField('The field is not valid for this object. The error_subtype will hold the field name this applies to')
        errors_mapping[('INVALID_SORT_ORDER', None)] = InvalidSortOrder('The sort order for the field is invalid. The error_subtype will hold the field name this applies to')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The user was not found.')
        query_data = {
            'api': self._api,
            'url': '/radreport/user/list',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        query_data['paginated_field'] = 'radreports'
        return QueryOPSF(**query_data)
    
    def pdf(
        self,
        uuid,
    ):
        """Pdf.
        :param uuid: The radreport uuid
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('NOT_FOUND', None)] = NotFound('Not found')
        query_data = {
            'api': self._api,
            'url': '/radreport/pdf',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def fax(
        self,
        number,
        uuid,
    ):
        """Fax.
        :param number: The fax number to send the PDF report to
        :param uuid: The radreport uuid
        """
        request_data = {
           'number': number,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_PHONE', None)] = InvalidPhone('The fax number is invalid')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_ENABLED', None)] = NotEnabled('The radreport mailing out is not enabled for the account')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The radreport can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to do this')
        errors_mapping[('NO_ATTACHMENT', None)] = NoAttachment('The radreport does not have an attached report')
        errors_mapping[('PDF_FAILED', None)] = PdfFailed('The PDF report failed to generate')
        query_data = {
            'api': self._api,
            'url': '/radreport/fax',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def email(
        self,
        email,
        uuid,
    ):
        """Email.
        :param email: The email address(es) to send the radreport to
        :param uuid: The radreport uuid
        """
        request_data = {
           'email': email,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_EMAIL', None)] = InvalidEmail('An invalid email address was passed')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_ENABLED', None)] = NotEnabled('The radreport mailing out is not enabled for the account')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The radreport can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to do this')
        errors_mapping[('NO_ATTACHMENT', None)] = NoAttachment('The radreport does not have an attached report')
        errors_mapping[('PDF_FAILED', None)] = PdfFailed('The PDF report failed to generate')
        query_data = {
            'api': self._api,
            'url': '/radreport/email',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def template_list(
        self,
        account_id,
        active=None,
        type=None,
    ):
        """Template list.
        :param account_id: uuid of the account
        :param active: Limit to active templates (optional)
        :param type: Limit to this type (optional)
        """
        request_data = {
           'account_id': account_id,
           'active': active,
           'type': type,
        }
	
        errors_mapping = {}
        errors_mapping[('FILTER_NOT_FOUND', None)] = FilterNotFound('The filter can not be found. The error_subtype will hold the filter UUID')
        errors_mapping[('INVALID_CONDITION', None)] = InvalidCondition('The condition is not support. The error_subtype will hold the filter expression this applies to')
        errors_mapping[('INVALID_FIELD', None)] = InvalidField('The field is not valid for this object. The error_subtype will hold the filter expression this applies to')
        errors_mapping[('INVALID_SORT_FIELD', None)] = InvalidSortField('The field is not valid for this object. The error_subtype will hold the field name this applies to')
        errors_mapping[('INVALID_SORT_ORDER', None)] = InvalidSortOrder('The sort order for the field is invalid. The error_subtype will hold the field name this applies to')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to perform this operation')
        query_data = {
            'api': self._api,
            'url': '/radreport/template/list',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        query_data['paginated_field'] = 'templates'
        return QueryOPSF(**query_data)
    
    def template_add(
        self,
        account_id,
        body,
        name,
        type,
        options=None,
        preview=None,
    ):
        """Template add.
        :param account_id: uuid of the account
        :param body: Body of the template
        :param name: Name of the template
        :param type: Type of radreport
        :param options: JSON options of the template (optional)
        :param preview: Preview of the template (optional)
        """
        request_data = {
           'account_id': account_id,
           'body': body,
           'name': name,
           'options': options,
           'preview': preview,
           'type': type,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_SYSADMIN_OR_SUPPORT', None)] = NotSysadminOrSupport('The user is not a sysadmin or support user')
        query_data = {
            'api': self._api,
            'url': '/radreport/template/add',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def template_set(
        self,
        uuid,
        body=None,
        name=None,
        options=None,
        preview=None,
        type=None,
    ):
        """Template set.
        :param uuid: uuid of the template
        :param body: Body of the template (optional)
        :param name: Name of the template (optional)
        :param options: JSON options of the template (optional)
        :param preview: Preview of the template (optional)
        :param type: Type of radreport (optional)
        """
        request_data = {
           'body': body,
           'name': name,
           'options': options,
           'preview': preview,
           'type': type,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_SYSADMIN_OR_SUPPORT', None)] = NotSysadminOrSupport('You are not permitted to perform this operation')
        query_data = {
            'api': self._api,
            'url': '/radreport/template/set',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def template_get(
        self,
        uuid,
    ):
        """Template get.
        :param uuid: uuid of the template
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The radreport template can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to perform this operation')
        query_data = {
            'api': self._api,
            'url': '/radreport/template/get',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def template_get_type(
        self,
        account_id,
        type,
    ):
        """Template get type.
        :param account_id: uuid of the account
        :param type: Type of the template
        """
        request_data = {
           'account_id': account_id,
           'type': type,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The radreport template can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to perform this operation')
        query_data = {
            'api': self._api,
            'url': '/radreport/template/get/type',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def template_delete(
        self,
        uuid,
    ):
        """Template delete.
        :param uuid: uuid of the template
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_SYSADMIN_OR_SUPPORT', None)] = NotSysadminOrSupport('The user is not a sysadmin or support user')
        query_data = {
            'api': self._api,
            'url': '/radreport/template/delete',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def template_activate(
        self,
        uuid,
    ):
        """Template activate.
        :param uuid: uuid of the template
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The radreport template can not be found')
        errors_mapping[('NOT_SYSADMIN_OR_SUPPORT', None)] = NotSysadminOrSupport('The user is not a sysadmin or support user')
        query_data = {
            'api': self._api,
            'url': '/radreport/template/activate',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    