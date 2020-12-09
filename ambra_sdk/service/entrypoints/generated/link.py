""" Link.

Do not edit this file by hand.
This is generated by parsing api.html service doc.
"""
from ambra_sdk.exceptions.service import AccountNotSet
from ambra_sdk.exceptions.service import AccountUserNotFound
from ambra_sdk.exceptions.service import ChargeFailed
from ambra_sdk.exceptions.service import ChargeRequired
from ambra_sdk.exceptions.service import DecryptFailed
from ambra_sdk.exceptions.service import Disabled
from ambra_sdk.exceptions.service import Expired
from ambra_sdk.exceptions.service import FilterNotFound
from ambra_sdk.exceptions.service import InvalidAction
from ambra_sdk.exceptions.service import InvalidCharge
from ambra_sdk.exceptions.service import InvalidCondition
from ambra_sdk.exceptions.service import InvalidCredentials
from ambra_sdk.exceptions.service import InvalidEmail
from ambra_sdk.exceptions.service import InvalidField
from ambra_sdk.exceptions.service import InvalidFieldName
from ambra_sdk.exceptions.service import InvalidJson
from ambra_sdk.exceptions.service import InvalidPhiField
from ambra_sdk.exceptions.service import InvalidPhone
from ambra_sdk.exceptions.service import InvalidPin
from ambra_sdk.exceptions.service import InvalidRegexp
from ambra_sdk.exceptions.service import InvalidSortField
from ambra_sdk.exceptions.service import InvalidSortOrder
from ambra_sdk.exceptions.service import InvalidSource
from ambra_sdk.exceptions.service import InvalidUploadMatch
from ambra_sdk.exceptions.service import IpBlocked
from ambra_sdk.exceptions.service import LinkNotFound
from ambra_sdk.exceptions.service import MissingFields
from ambra_sdk.exceptions.service import MissingInfo
from ambra_sdk.exceptions.service import MissingParameters
from ambra_sdk.exceptions.service import NoFilter
from ambra_sdk.exceptions.service import NotFound
from ambra_sdk.exceptions.service import NotHash
from ambra_sdk.exceptions.service import NotList
from ambra_sdk.exceptions.service import NotPermitted
from ambra_sdk.exceptions.service import PinLockout
from ambra_sdk.exceptions.service import Validate
from ambra_sdk.service.query import QueryO
from ambra_sdk.service.query import QueryOPSF

class Link:
    """Link."""

    def __init__(self, api):
        self._api = api

    
    def list(
        self,
        account_id=None,
        study_id=None,
        user_id=None,
    ):
        """List.
        :param account_id: account_id
        :param study_id: study_id
        :param user_id: user_id

        Notes:
        (study_id OR user_id OR account_id) - uuid of the study, user or account to get the links for
        """
        request_data = {
           'account_id': account_id,
           'study_id': study_id,
           'user_id': user_id,
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
            'url': '/link/list',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        query_data['paginated_field'] = 'links'
        return QueryOPSF(**query_data)
    
    def add(
        self,
        action,
        prompt_for_anonymize,
        acceptance_required=None,
        account_id=None,
        anonymize=None,
        charge_amount=None,
        charge_currency=None,
        charge_description=None,
        email=None,
        filter=None,
        include_priors=None,
        max_hits=None,
        meeting_id=None,
        message=None,
        minutes_alive=None,
        mobile_phone=None,
        namespace_id=None,
        notify=None,
        parameters=None,
        password=None,
        password_is_dob=None,
        password_max_attempts=None,
        pin_auth=None,
        referer=None,
        share_code=None,
        share_on_view=None,
        skip_email_prompt=None,
        study_id=None,
        upload_match=None,
        upload_study_customfields=None,
        use_share_code=None,
    ):
        """Add.
        :param action: Link action (STUDY_LIST|STUDY_VIEW|STUDY_UPLOAD)
        :param prompt_for_anonymize: Flag to prompt if the anonymization rules should be applied on ingress
        :param acceptance_required: Flag that acceptance of TOS is required (optional)
        :param account_id: account_id
        :param anonymize: Anonymization rules to the applied to any STUDY_UPLOAD done with this link. Rules are formatted as per the rules parameter in /namespace/anonymize  (optional)
        :param charge_amount: Amount to charge in pennies before the link can be accessed (optional)
        :param charge_currency: Charge currency (optional)
        :param charge_description: Charge description (optional)
        :param email: Email the link to these addresses (optional)
        :param filter: filter
        :param include_priors: Include prior studies (optional)
        :param max_hits: The maximum number of times the link can be used (optional)
        :param meeting_id: UUID of the meeting to associate the link with (optional)
        :param message: Message to include in the email (optional)
        :param minutes_alive: The maximum number of minutes the link will be alive for (optional)
        :param mobile_phone: Send the link to this phone number (optional)
        :param namespace_id: namespace_id
        :param notify: Comma or space separated list of additional emails to notify of link usage (optional)
        :param parameters: JSON array of parameters to add to the redirect URL or return in /namespace/share_code if an upload (optional)
        :param password: Link password (optional)
        :param password_is_dob: Flag that the password is the patient_birth_date for the study (study_id is required) (optional)
        :param password_max_attempts: The maximum number of failed password attempt (optional)
        :param pin_auth: An account member email and PIN authentication is required (optional)
        :param referer: The link can only be accessed from the specified referer. The referer can be a regexp to match multiple referers (optional)
        :param share_code: share code for a STUDY_UPLOAD (optional)
        :param share_on_view: Flag to share the study with the email after it is viewed (optional)
        :param skip_email_prompt: Skip the prompt for email step (optional)
        :param study_id: study_id
        :param upload_match: A JSON hash of DICOM tags and regular expressions they must match uploaded against this link (optional)
        :param upload_study_customfields: A JSON hash of customfields that will be mapped to a study on study upload. A key is a customfield UUID, a value is a value for the field (optional)
        :param use_share_code: Flag to use the namespace share code settings for a STUDY_UPLOAD (optional)

        Notes:
        (study_id OR filter AND account_id OR namespace_id) - uuid of the study or a JSON hash of the study filter expression and the account_id or namespace_id if the action is STUDY_UPLOAD
        """
        request_data = {
           'acceptance_required': acceptance_required,
           'account_id': account_id,
           'action': action,
           'anonymize': anonymize,
           'charge_amount': charge_amount,
           'charge_currency': charge_currency,
           'charge_description': charge_description,
           'email': email,
           'filter': filter,
           'include_priors': include_priors,
           'max_hits': max_hits,
           'meeting_id': meeting_id,
           'message': message,
           'minutes_alive': minutes_alive,
           'mobile_phone': mobile_phone,
           'namespace_id': namespace_id,
           'notify': notify,
           'parameters': parameters,
           'password': password,
           'password_is_dob': password_is_dob,
           'password_max_attempts': password_max_attempts,
           'pin_auth': pin_auth,
           'prompt_for_anonymize': prompt_for_anonymize,
           'referer': referer,
           'share_code': share_code,
           'share_on_view': share_on_view,
           'skip_email_prompt': skip_email_prompt,
           'study_id': study_id,
           'upload_match': upload_match,
           'upload_study_customfields': upload_study_customfields,
           'use_share_code': use_share_code,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_ACTION', None)] = InvalidAction('An invalid action was passed')
        errors_mapping[('INVALID_CHARGE', None)] = InvalidCharge('The charge is invalid. The error_subtype holds the details on the error')
        errors_mapping[('INVALID_EMAIL', None)] = InvalidEmail('An invalid email address was passed')
        errors_mapping[('INVALID_FIELD_NAME', None)] = InvalidFieldName('The field name in the rules hash is invalid. The error_subtype holds the invalid field name')
        errors_mapping[('INVALID_JSON', None)] = InvalidJson('The field is not in valid JSON format. The error_subtype holds the name of the field')
        errors_mapping[('INVALID_PHI_FIELD', None)] = InvalidPhiField('The password_is_phi field is invalid or a study_id was not passed')
        errors_mapping[('INVALID_PHONE', None)] = InvalidPhone('An invalid cellular phone number was passed')
        errors_mapping[('INVALID_REGEXP', None)] = InvalidRegexp('Invalid regular expression. The error_subtype holds the invalid regexp.')
        errors_mapping[('INVALID_UPLOAD_MATCH', None)] = InvalidUploadMatch('The upload_match is invalid. The error_subtype holds the details on the error')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The patient or study could not be found. The error_subtype holds the uuid that can not be found')
        errors_mapping[('NOT_HASH', None)] = NotHash('The rules field is not a hash')
        errors_mapping[('NOT_LIST', None)] = NotList('The field is not a JSON array. The error_subtype holds the name of the field')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to create links')
        errors_mapping[('VALIDATE', None)] = Validate('A validation error. The error_subtype holds the details on the error')
        query_data = {
            'api': self._api,
            'url': '/link/add',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def get(
        self,
        acceptance_required,
        account_id,
        action,
        anonymize,
        charge_amount,
        charge_currency,
        charge_description,
        created,
        description,
        email,
        filter,
        has_password,
        include_priors,
        is_meeting,
        max_hits,
        message,
        minutes_alive,
        mobile_phone,
        namespace_id,
        namespace_name,
        notify,
        parameters,
        password_is_dob,
        password_max_attempts,
        pin_auth,
        prompt_for_anonymize,
        redirect_url,
        referer,
        share_on_view,
        skip_email_prompt,
        study_id,
        upload_match,
        upload_study_customfields,
        url,
        use_share_code,
        user_id,
        uuid,
    ):
        """Get.
        :param acceptance_required: Flag that acceptance of TOS is required
        :param account_id: The account id
        :param action: Link action
        :param anonymize: Any anonymization rules
        :param charge_amount: Amount to charge in pennies before the link can be accessed
        :param charge_currency: Charge currency
        :param charge_description: Charge description
        :param created: Created datetime stamp of the link
        :param description: Description of the link
        :param email: Email address the link was sent to
        :param filter: The filter expression
        :param has_password: Flag if the link has a password or not
        :param include_priors: Include prior studies
        :param is_meeting: Flag if the link is for a meeting
        :param max_hits: The maximum number of times the link can be used
        :param message: Message to include in the email
        :param minutes_alive: The maximum number of minutes the link will be alive for
        :param mobile_phone: Cellular phone number the link was sent to
        :param namespace_id: Id of the namespace for upload links
        :param namespace_name: Name of the namespace for upload links
        :param notify: Comma or space separated list of additional emails to notify of link usage
        :param parameters: JSON array parameters to add to the redirect URL
        :param password_is_dob: Flag that the password is the patient_birth_date for the study
        :param password_max_attempts: The maximum number of failed password attempt
        :param pin_auth: An account member email and PIN authentication is required
        :param prompt_for_anonymize: Flag to prompt if the anonymization rules should be applied on ingress
        :param redirect_url: URL for the /link/redirect API  which will take you directly to the study viewer or uploader
        :param referer: The link can only be accessed from the specified referer
        :param share_on_view: Flag to share the study with the email after it is viewed
        :param skip_email_prompt: Skip the prompt for email step
        :param study_id: uuid of the study
        :param upload_match: A JSON hash of DICOM tags and regular expressions they must match uploaded against this link
        :param upload_study_customfields: A JSON hash of customfields that will be mapped to a study on study upload
        :param url: URL for the link which will take you to the UI entry point for links to enter email, password etc.
        :param use_share_code: Flag to use the namespace share code settings for a STUDY_UPLOAD
        :param user_id: The user id
        :param uuid: Id of the link
        """
        request_data = {
           'acceptance_required': acceptance_required,
           'account_id': account_id,
           'action': action,
           'anonymize': anonymize,
           'charge_amount': charge_amount,
           'charge_currency': charge_currency,
           'charge_description': charge_description,
           'created': created,
           'description': description,
           'email': email,
           'filter': filter,
           'has_password': has_password,
           'include_priors': include_priors,
           'is_meeting': is_meeting,
           'max_hits': max_hits,
           'message': message,
           'minutes_alive': minutes_alive,
           'mobile_phone': mobile_phone,
           'namespace_id': namespace_id,
           'namespace_name': namespace_name,
           'notify': notify,
           'parameters': parameters,
           'password_is_dob': password_is_dob,
           'password_max_attempts': password_max_attempts,
           'pin_auth': pin_auth,
           'prompt_for_anonymize': prompt_for_anonymize,
           'redirect_url': redirect_url,
           'referer': referer,
           'share_on_view': share_on_view,
           'skip_email_prompt': skip_email_prompt,
           'study_id': study_id,
           'upload_match': upload_match,
           'upload_study_customfields': upload_study_customfields,
           'url': url,
           'use_share_code': use_share_code,
           'user_id': user_id,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The link was not found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view the link')
        query_data = {
            'api': self._api,
            'url': '/link/get',
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
        :param uuid: Id of the link
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The link was not found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to delete the link')
        query_data = {
            'api': self._api,
            'url': '/link/delete',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def status(
        self,
        link_charge_id=None,
        pin=None,
        uuid=None,
    ):
        """Status.
        :param link_charge_id: The uuid of the prior charge against this link (optional)
        :param pin: pin
        :param uuid: uuid

        Notes:
        (uuid OR pin) - Id or PIN of the link
        """
        request_data = {
           'link_charge_id': link_charge_id,
           'pin': pin,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_PIN', None)] = InvalidPin('An invalid PIN was entered')
        errors_mapping[('INVALID_SOURCE', None)] = InvalidSource('The referer is invalid')
        errors_mapping[('IP_BLOCKED', None)] = IpBlocked('An IP whitelist blocked access')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The link was not found')
        errors_mapping[('PIN_LOCKOUT', None)] = PinLockout('Too many invalid PIN entries')
        query_data = {
            'api': self._api,
            'url': '/link/status',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': False,
        }
        return QueryO(**query_data)
    
    def session(
        self,
        email_address=None,
        link_charge_id=None,
        password=None,
        pin=None,
        uuid=None,
    ):
        """Session.
        :param email_address: The users email (optional)
        :param link_charge_id: The uuid of the prior charge against this link (optional)
        :param password: Password if needed (optional)
        :param pin: pin
        :param uuid: uuid

        Notes:
        (uuid OR pin) - Id or PIN of the link
        """
        request_data = {
           'email_address': email_address,
           'link_charge_id': link_charge_id,
           'password': password,
           'pin': pin,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('CHARGE_REQUIRED', None)] = ChargeRequired('A charge is required to access this link')
        errors_mapping[('DISABLED', None)] = Disabled('This call is disabled for the account, you must use /link/redirect')
        errors_mapping[('INVALID_CREDENTIALS', None)] = InvalidCredentials('Invalid password or email if pin_auth is required.')
        errors_mapping[('INVALID_PIN', None)] = InvalidPin('An invalid PIN was entered')
        errors_mapping[('INVALID_SOURCE', None)] = InvalidSource('The referer is invalid')
        errors_mapping[('IP_BLOCKED', None)] = IpBlocked('An IP whitelist blocked access')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The link was not found')
        errors_mapping[('PIN_LOCKOUT', None)] = PinLockout('Too many invalid PIN entries')
        query_data = {
            'api': self._api,
            'url': '/link/session',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': False,
        }
        return QueryO(**query_data)
    
    def redirect(
        self,
        link_charge_id=None,
        password=None,
        pin=None,
        uuid=None,
    ):
        """Redirect.
        :param link_charge_id: The uuid of the prior charge against this link (optional)
        :param password: Password if needed (optional)
        :param pin: pin
        :param uuid: uuid

        Notes:
        (uuid OR pin) - Id or PIN of the link
        """
        request_data = {
           'link_charge_id': link_charge_id,
           'password': password,
           'pin': pin,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('EXPIRED', None)] = Expired('The link has expired')
        errors_mapping[('INVALID_CREDENTIALS', None)] = InvalidCredentials('Invalid password.')
        errors_mapping[('INVALID_PIN', None)] = InvalidPin('An invalid PIN was entered')
        errors_mapping[('INVALID_SOURCE', None)] = InvalidSource('The referer is invalid')
        errors_mapping[('IP_BLOCKED', None)] = IpBlocked('An IP whitelist blocked access')
        errors_mapping[('LINK_NOT_FOUND', None)] = LinkNotFound('The link was not found')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('The configuration of this link requires the link UI be used instead of direct access')
        errors_mapping[('PIN_LOCKOUT', None)] = PinLockout('Too many invalid PIN entries')
        query_data = {
            'api': self._api,
            'url': '/link/redirect',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def external(
        self,
        u,
        v=None,
    ):
        """External.
        :param u: The uuid of the user_account record to create the guest link as
        :param v: 
        A JSON hash with the following keys pairs. The JSON must be encrypted and base64 encoded:
        filter.*=&gt;Filter field(s) as per the /study/list to specify the study(s) to construct the link for.
        The include_priors link option value can be passed as a key.
        Any additional fields will the saved in the study audit trail and the following fields email_address, redirect_url, integration_key and skip_email_prompt will be available in /namespace/share_code if this is an upload link .
        """
        request_data = {
           'u': u,
           'v': v,
        }
	
        errors_mapping = {}
        errors_mapping[('ACCOUNT_NOT_SET', None)] = AccountNotSet('The account is not setup for the integration')
        errors_mapping[('ACCOUNT_USER_NOT_FOUND', None)] = AccountUserNotFound('The account user record was not found')
        errors_mapping[('DECRYPT_FAILED', None)] = DecryptFailed('The decryption failed')
        errors_mapping[('INVALID_SOURCE', None)] = InvalidSource('The referer is invalid')
        errors_mapping[('MISSING_PARAMETERS', None)] = MissingParameters('The u or v parameter is missing')
        errors_mapping[('NOT_HASH', None)] = NotHash('The v parameter is not a JSON hash')
        errors_mapping[('NO_FILTER', None)] = NoFilter('A filter expressions was not passed')
        query_data = {
            'api': self._api,
            'url': '/link/external',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': False,
        }
        return QueryO(**query_data)
    
    def sso(
        self,
        u,
        v,
    ):
        """Sso.
        :param u: The uuid of the user_account record
        :param v: An encrypted JSON hash as per the instructions in the SSO to a PHR account with a study share section of the documentation
        """
        request_data = {
           'u': u,
           'v': v,
        }
	
        errors_mapping = {}
        errors_mapping[('ACCOUNT_NOT_SET', None)] = AccountNotSet('The account is not setup for the integration')
        errors_mapping[('ACCOUNT_USER_NOT_FOUND', None)] = AccountUserNotFound('The account user record was not found')
        errors_mapping[('DECRYPT_FAILED', None)] = DecryptFailed('The decryption failed')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('MISSING_INFO', None)] = MissingInfo('User information is missing from the hash')
        errors_mapping[('NOT_HASH', None)] = NotHash('The v parameter is not a JSON hash')
        query_data = {
            'api': self._api,
            'url': '/link/sso',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': False,
        }
        return QueryO(**query_data)
    
    def sid(
        self,
        email,
        uuid,
    ):
        """Sid.
        :param email: Email address to associate with this usage
        :param uuid: The uuid of the link usage
        """
        request_data = {
           'email': email,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('NOT_FOUND', None)] = NotFound('The usage was not found')
        query_data = {
            'api': self._api,
            'url': '/link/sid',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': False,
        }
        return QueryO(**query_data)
    
    def mail(
        self,
        email,
        uuid,
    ):
        """Mail.
        :param email: Email address
        :param uuid: The uuid of the link
        """
        request_data = {
           'email': email,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_EMAIL', None)] = InvalidEmail('Enter a valid email address')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The link was not found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to do this')
        query_data = {
            'api': self._api,
            'url': '/link/mail',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def charge(
        self,
        charge_token,
        uuid,
    ):
        """Charge.
        :param charge_token: The stripe charge token
        :param uuid: The uuid of the link
        """
        request_data = {
           'charge_token': charge_token,
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('CHARGE_FAILED', None)] = ChargeFailed('The charge failed. The error_subtype holds the details on the error')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The link was not found')
        query_data = {
            'api': self._api,
            'url': '/link/charge',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': False,
        }
        return QueryO(**query_data)
    
    def pin(
        self,
        uuid,
    ):
        """Pin.
        :param uuid: The uuid of the link
        """
        request_data = {
           'uuid': uuid,
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The link was not found')
        query_data = {
            'api': self._api,
            'url': '/link/pin',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    