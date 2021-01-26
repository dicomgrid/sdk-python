""" Session.

Do not edit this file by hand.
This is generated by parsing api.html service doc.
"""
from ambra_sdk.exceptions.service import AuthFailed
from ambra_sdk.exceptions.service import BadPassword
from ambra_sdk.exceptions.service import Blocked
from ambra_sdk.exceptions.service import BrandNotAllowed
from ambra_sdk.exceptions.service import Disabled
from ambra_sdk.exceptions.service import Expired
from ambra_sdk.exceptions.service import InvalidCode
from ambra_sdk.exceptions.service import InvalidCredentials
from ambra_sdk.exceptions.service import InvalidPin
from ambra_sdk.exceptions.service import InvalidSid
from ambra_sdk.exceptions.service import InvalidUrl
from ambra_sdk.exceptions.service import InvalidVendor
from ambra_sdk.exceptions.service import Lockout
from ambra_sdk.exceptions.service import MissingFields
from ambra_sdk.exceptions.service import MissingInformation
from ambra_sdk.exceptions.service import NoOauth
from ambra_sdk.exceptions.service import NotFound
from ambra_sdk.exceptions.service import OtherOauth
from ambra_sdk.exceptions.service import PasswordReset
from ambra_sdk.exceptions.service import PinExpired
from ambra_sdk.exceptions.service import SsoOnly
from ambra_sdk.exceptions.service import ValidationFailed
from ambra_sdk.exceptions.service import WhitelistLockout
from ambra_sdk.service.query import QueryO

class Session:
    """Session."""

    def __init__(self, api):
        self._api = api

    
    def login(
        self,
        login,
        password,
        account_login=None,
        account_name=None,
        email=None,
        location=None,
        new_password=None,
        remember_device=None,
        validate_session=None,
        vanity=None,
    ):
        """Login.
        :param login: The user account_login or email address
        :param password: The password
        :param account_login: account_login
        :param account_name: account_name
        :param email: email
        :param location: Login location. (optional)
        :param new_password: Change the password or account password to this. (optional)
        :param remember_device: Remember the device as trusted. (optional)
        :param validate_session: If you would like to validate an existing session rather than create a new one pass in the sid of the session to valid in this parameter. It will check if the session is still valid and the credentials are for the session. (optional)
        :param vanity: The account vanity name. (optional)

        Notes:
        email OR account_name AND account_login - The users email address or the account name and account_login (DEPRECIATED - Use login and vanity)
        """
        request_data = {
           'account_login': account_login,
           'account_name': account_name,
           'email': email,
           'location': location,
           'login': login,
           'new_password': new_password,
           'password': password,
           'remember_device': remember_device,
           'validate_session': validate_session,
           'vanity': vanity,
        }
	
        errors_mapping = {}
        errors_mapping[('BAD_PASSWORD', None)] = BadPassword('The new_password does not meet the password requirements')
        errors_mapping[('BLOCKED', None)] = Blocked('The user is blocked from the system')
        errors_mapping[('BRAND_NOT_ALLOWED', None)] = BrandNotAllowed('The user is limited to some brands to login with allowed_login_brands setting')
        errors_mapping[('DISABLED', None)] = Disabled('The user is disabled and needs to be /user/enabled to allow access')
        errors_mapping[('INVALID_CREDENTIALS', None)] = InvalidCredentials('Invalid user name or password.')
        errors_mapping[('LOCKOUT', None)] = Lockout('Too many failed attempts')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('PASSWORD_RESET', None)] = PasswordReset('The password needs to be changed')
        errors_mapping[('SSO_ONLY', None)] = SsoOnly('The user can only login via SSO')
        errors_mapping[('VALIDATION_FAILED', None)] = ValidationFailed('The session validation failed')
        errors_mapping[('WHITELIST_LOCKOUT', None)] = WhitelistLockout('Login blocked by the account whitelist')
        query_data = {
            'api': self._api,
            'url': '/session/login',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': False,
        }
        return QueryO(**query_data)
    
    def user(
        self,
        settings=None,
    ):
        """User.
        :param settings: A JSON list of user settings set via /setting/set to return (optional)
        """
        request_data = {
           'settings': settings,
        }
	
        errors_mapping = {}
        query_data = {
            'api': self._api,
            'url': '/session/user',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def permissions(
        self,
        account_id=None,
        namespace_id=None,
    ):
        """Permissions.
        :param account_id: account_id
        :param namespace_id: namespace_id

        Notes:
        (account_id OR namespace_id) - Either the account or namespaces to get the users permissions for
        """
        request_data = {
           'account_id': account_id,
           'namespace_id': namespace_id,
        }
	
        errors_mapping = {}
        query_data = {
            'api': self._api,
            'url': '/session/permissions',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def logout(
        self,
    ):
        """Logout.
        """
        request_data = {
        }
	
        errors_mapping = {}
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The sid was not found')
        query_data = {
            'api': self._api,
            'url': '/session/logout',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def csrf_enable(
        self,
        redirect_uri,
    ):
        """Csrf enable.
        :param redirect_uri: The URL to redirect to
        """
        request_data = {
           'redirect_uri': redirect_uri,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_URL', None)] = InvalidUrl('The URL must be a relative URL')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        query_data = {
            'api': self._api,
            'url': '/session/csrf/enable',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def uuid(
        self,
    ):
        """Uuid.
        """
        request_data = {
        }
	
        errors_mapping = {}
        query_data = {
            'api': self._api,
            'url': '/session/uuid',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': False,
        }
        return QueryO(**query_data)
    
    def oauth_start(
        self,
    ):
        """Oauth start.
        """
        request_data = {
        }
	
        errors_mapping = {}
        errors_mapping[('NO_OAUTH', None)] = NoOauth('OAuth is not setup for the associated brand')
        query_data = {
            'api': self._api,
            'url': '/session/oauth/start',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': False,
        }
        return QueryO(**query_data)
    
    def oauth(
        self,
        code,
        redirect_uri,
        vendor,
    ):
        """Oauth.
        :param code: The OAuth code
        :param redirect_uri: The redirect_uri used to get the code parameter
        :param vendor: The OAuth vendor (doximity|google|brand)
        """
        request_data = {
           'code': code,
           'redirect_uri': redirect_uri,
           'vendor': vendor,
        }
	
        errors_mapping = {}
        errors_mapping[('AUTH_FAILED', None)] = AuthFailed('OAuth failed or a user id was not returned')
        errors_mapping[('INVALID_CODE', None)] = InvalidCode('Invalid code')
        errors_mapping[('INVALID_VENDOR', None)] = InvalidVendor('Invalid vendor')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('MISSING_INFORMATION', None)] = MissingInformation('The response from the OAuth provider is missing either the email, first_name or last_name fields')
        errors_mapping[('NO_OAUTH', None)] = NoOauth('OAuth is not setup for the associated brand')
        errors_mapping[('OTHER_OAUTH', None)] = OtherOauth('The user is already setup to OAuth via another vendor')
        query_data = {
            'api': self._api,
            'url': '/session/oauth',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': False,
        }
        return QueryO(**query_data)
    
    def oauth_token(
        self,
        client_id,
        client_secret,
        grant_type,
        duration=None,
    ):
        """Oauth token.
        :param client_id: The users email address
        :param client_secret: The users password
        :param grant_type: The grant type, set to client_credentials
        :param duration: The number of seconds the token is valid for (optional and defaults to 3600 with a maximum value of 86400)
        """
        request_data = {
           'client_id': client_id,
           'client_secret': client_secret,
           'duration': duration,
           'grant_type': grant_type,
        }
	
        errors_mapping = {}
        errors_mapping[('AUTH_FAILED', None)] = AuthFailed('Authentication failed')
        errors_mapping[('LOCKOUT', None)] = Lockout('Too many failed attempts')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        query_data = {
            'api': self._api,
            'url': '/session/oauth/token',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': False,
        }
        return QueryO(**query_data)
    
    def pin(
        self,
        pin,
    ):
        """Pin.
        :param pin: The PIN
        """
        request_data = {
           'pin': pin,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_PIN', None)] = InvalidPin('Invalid PIN')
        errors_mapping[('INVALID_SID', None)] = InvalidSid('Invalid sid')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('PIN_EXPIRED', None)] = PinExpired('The PIN has expired')
        query_data = {
            'api': self._api,
            'url': '/session/pin',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def ttl(
        self,
    ):
        """Ttl.
        """
        request_data = {
        }
	
        errors_mapping = {}
        errors_mapping[('EXPIRED', None)] = Expired('Expired')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        query_data = {
            'api': self._api,
            'url': '/session/ttl',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    