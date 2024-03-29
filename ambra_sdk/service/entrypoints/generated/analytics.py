""" Analytics.

Do not edit this file by hand.
This is generated by parsing api.html service doc.
"""
from ambra_sdk.exceptions.service import InvalidCount
from ambra_sdk.exceptions.service import InvalidEmail
from ambra_sdk.exceptions.service import InvalidEndDate
from ambra_sdk.exceptions.service import InvalidFlag
from ambra_sdk.exceptions.service import InvalidParameters
from ambra_sdk.exceptions.service import InvalidPeriod
from ambra_sdk.exceptions.service import InvalidUuid
from ambra_sdk.exceptions.service import MissingFields
from ambra_sdk.exceptions.service import MultipleAccounts
from ambra_sdk.exceptions.service import NotFound
from ambra_sdk.exceptions.service import NotList
from ambra_sdk.exceptions.service import NotPermitted
from ambra_sdk.exceptions.service import PhrNamespace
from ambra_sdk.exceptions.service import ValidationFailed
from ambra_sdk.service.query import QueryO
from ambra_sdk.service.query import AsyncQueryO

class Analytics:
    """Analytics."""

    def __init__(self, api):
        self._api = api

    
    def study(
        self,
        count,
        period,
        account_id=None,
        customfield_param=None,
        email=None,
        end_date=None,
        modality=None,
        namespace_id=None,
        time_zone=None,
    ):
        """Study.

        :param count: The number of periods to get
        :param period: The time period (day|week|month|year)
        :param account_id: account_id
        :param customfield_param: Expected values are CUSTOMFIELD_UUID. Filter analytics by a subset of study customfields (optional)
        :param email: Send the report to this email address(es) when it is done (optional)
        :param end_date: The end date, default is today if not passed (optional)
        :param modality: Filter analytics by modality (optional)
        :param namespace_id: namespace_id
        :param time_zone: The report's time zone. Time zone selection order: current user's time zone, time_zone parameter, UTC by default.
          report Flag if the result should be returned as a report (optional)
        """
        request_data = {
           'account_id': account_id,
           'count': count,
           'email': email,
           'end_date': end_date,
           'modality': modality,
           'namespace_id': namespace_id,
           'period': period,
           'time_zone': time_zone,
        }
        if customfield_param is not None:
            customfield_param_dict = {'{prefix}{k}'.format(prefix='customfield-', k=k): v for k,v in customfield_param.items()}
            request_data.update(customfield_param_dict)
	
        errors_mapping = {}
        errors_mapping[('INVALID_COUNT', None)] = InvalidCount('Invalid or excessive count value')
        errors_mapping[('INVALID_EMAIL', None)] = InvalidEmail('An invalid email address was passed')
        errors_mapping[('INVALID_END_DATE', None)] = InvalidEndDate('An invalid period')
        errors_mapping[('INVALID_FLAG', None)] = InvalidFlag('An invalid flag was passed. The error_subtype holds the name of the invalid flag')
        errors_mapping[('INVALID_PARAMETERS', None)] = InvalidParameters('Only pass a account_id or namespace_id')
        errors_mapping[('INVALID_PERIOD', None)] = InvalidPeriod('An invalid period')
        errors_mapping[('INVALID_UUID', None)] = InvalidUuid('The field is not a valid UUID. The error_subtype holds the name of the field')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('MULTIPLE_ACCOUNTS', None)] = MultipleAccounts('Namespaces from different accounts provided')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The account or namespace can not be found')
        errors_mapping[('NOT_LIST', None)] = NotList('The field is not a JSON array. The error_subtype holds the name of the field')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view analytics for this account or namespace')
        errors_mapping[('PHR_NAMESPACE', None)] = PhrNamespace('Only pass non-PHR namespaces')
        errors_mapping[('VALIDATION_FAILED', None)] = ValidationFailed('The modality parameter validation failed')
        query_data = {
            'api': self._api,
            'url': '/analytics/study',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def patient_portal(
        self,
        account_id,
        count,
        period,
        time_zone,
        end_date=None,
        patient_id=None,
    ):
        """Patient portal.

        :param account_id: The account id
        :param count: The number of periods to get
        :param period: The time period (day|week|month|year)
        :param time_zone: The report's time zone. Time zone selection order: current user's time zone, time_zone parameter, UTC by default.
        :param end_date: The end date, default is today if not passed (optional)
        :param patient_id: Patient filter (optional)
        """
        request_data = {
           'account_id': account_id,
           'count': count,
           'end_date': end_date,
           'patient_id': patient_id,
           'period': period,
           'time_zone': time_zone,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_COUNT', None)] = InvalidCount('Invalid or excessive count value')
        errors_mapping[('INVALID_END_DATE', None)] = InvalidEndDate('An invalid period')
        errors_mapping[('INVALID_PERIOD', None)] = InvalidPeriod('An invalid period')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The account or patient can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view analytics for this account or namespace')
        query_data = {
            'api': self._api,
            'url': '/analytics/patient/portal',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def radreport(
        self,
        account_id,
        count,
        period,
        time_zone,
        end_date=None,
        namespace_id=None,
        user_id=None,
    ):
        """Radreport.

        :param account_id: The account id
        :param count: The number of periods to get
        :param period: The time period (day|week|month|year)
        :param time_zone: The report's time zone. Time zone selection order: current user's time zone, time_zone parameter, UTC by default.
        :param end_date: The end date, default is today if not passed (optional)
        :param namespace_id: Namespace filter (optional)
        :param user_id: User filter (optional)
        """
        request_data = {
           'account_id': account_id,
           'count': count,
           'end_date': end_date,
           'namespace_id': namespace_id,
           'period': period,
           'time_zone': time_zone,
           'user_id': user_id,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_COUNT', None)] = InvalidCount('Invalid or excessive count value')
        errors_mapping[('INVALID_END_DATE', None)] = InvalidEndDate('An invalid period')
        errors_mapping[('INVALID_PERIOD', None)] = InvalidPeriod('An invalid period')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The account or patient can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view analytics for this account or namespace')
        query_data = {
            'api': self._api,
            'url': '/analytics/radreport',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    
    def user(
        self,
        account_id,
        count,
        period,
        time_zone,
        end_date=None,
        end_time=None,
        namespace_id=None,
        user_id=None,
    ):
        """User.

        :param account_id: The account id
        :param count: The number of periods to get
        :param period: The time period (hour|day|week|month|year)
        :param time_zone: The report's time zone. Time zone selection order: current user's time zone, time_zone parameter, UTC by default.
        :param end_date: The end date, for backwards compatibility (optional)
        :param end_time: The end date and time, default is now if not passed (optional)
        :param namespace_id: Namespace filter (optional)
        :param user_id: User filter (optional)
        """
        request_data = {
           'account_id': account_id,
           'count': count,
           'end_date': end_date,
           'end_time': end_time,
           'namespace_id': namespace_id,
           'period': period,
           'time_zone': time_zone,
           'user_id': user_id,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_COUNT', None)] = InvalidCount('Invalid or excessive count value')
        errors_mapping[('INVALID_END_DATE', None)] = InvalidEndDate('An invalid period')
        errors_mapping[('INVALID_PERIOD', None)] = InvalidPeriod('An invalid period')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The account or patient can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view analytics for this account or namespace')
        query_data = {
            'api': self._api,
            'url': '/analytics/user',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return QueryO(**query_data)
    


class AsyncAnalytics:
    """AsyncAnalytics."""

    def __init__(self, api):
        self._api = api

    
    def study(
        self,
        count,
        period,
        account_id=None,
        customfield_param=None,
        email=None,
        end_date=None,
        modality=None,
        namespace_id=None,
        time_zone=None,
    ):
        """Study.

        :param count: The number of periods to get
        :param period: The time period (day|week|month|year)
        :param account_id: account_id
        :param customfield_param: Expected values are CUSTOMFIELD_UUID. Filter analytics by a subset of study customfields (optional)
        :param email: Send the report to this email address(es) when it is done (optional)
        :param end_date: The end date, default is today if not passed (optional)
        :param modality: Filter analytics by modality (optional)
        :param namespace_id: namespace_id
        :param time_zone: The report's time zone. Time zone selection order: current user's time zone, time_zone parameter, UTC by default.
          report Flag if the result should be returned as a report (optional)
        """
        request_data = {
           'account_id': account_id,
           'count': count,
           'email': email,
           'end_date': end_date,
           'modality': modality,
           'namespace_id': namespace_id,
           'period': period,
           'time_zone': time_zone,
        }
        if customfield_param is not None:
            customfield_param_dict = {'{prefix}{k}'.format(prefix='customfield-', k=k): v for k,v in customfield_param.items()}
            request_data.update(customfield_param_dict)
	
        errors_mapping = {}
        errors_mapping[('INVALID_COUNT', None)] = InvalidCount('Invalid or excessive count value')
        errors_mapping[('INVALID_EMAIL', None)] = InvalidEmail('An invalid email address was passed')
        errors_mapping[('INVALID_END_DATE', None)] = InvalidEndDate('An invalid period')
        errors_mapping[('INVALID_FLAG', None)] = InvalidFlag('An invalid flag was passed. The error_subtype holds the name of the invalid flag')
        errors_mapping[('INVALID_PARAMETERS', None)] = InvalidParameters('Only pass a account_id or namespace_id')
        errors_mapping[('INVALID_PERIOD', None)] = InvalidPeriod('An invalid period')
        errors_mapping[('INVALID_UUID', None)] = InvalidUuid('The field is not a valid UUID. The error_subtype holds the name of the field')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('MULTIPLE_ACCOUNTS', None)] = MultipleAccounts('Namespaces from different accounts provided')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The account or namespace can not be found')
        errors_mapping[('NOT_LIST', None)] = NotList('The field is not a JSON array. The error_subtype holds the name of the field')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view analytics for this account or namespace')
        errors_mapping[('PHR_NAMESPACE', None)] = PhrNamespace('Only pass non-PHR namespaces')
        errors_mapping[('VALIDATION_FAILED', None)] = ValidationFailed('The modality parameter validation failed')
        query_data = {
            'api': self._api,
            'url': '/analytics/study',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return AsyncQueryO(**query_data)
    
    def patient_portal(
        self,
        account_id,
        count,
        period,
        time_zone,
        end_date=None,
        patient_id=None,
    ):
        """Patient portal.

        :param account_id: The account id
        :param count: The number of periods to get
        :param period: The time period (day|week|month|year)
        :param time_zone: The report's time zone. Time zone selection order: current user's time zone, time_zone parameter, UTC by default.
        :param end_date: The end date, default is today if not passed (optional)
        :param patient_id: Patient filter (optional)
        """
        request_data = {
           'account_id': account_id,
           'count': count,
           'end_date': end_date,
           'patient_id': patient_id,
           'period': period,
           'time_zone': time_zone,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_COUNT', None)] = InvalidCount('Invalid or excessive count value')
        errors_mapping[('INVALID_END_DATE', None)] = InvalidEndDate('An invalid period')
        errors_mapping[('INVALID_PERIOD', None)] = InvalidPeriod('An invalid period')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The account or patient can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view analytics for this account or namespace')
        query_data = {
            'api': self._api,
            'url': '/analytics/patient/portal',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return AsyncQueryO(**query_data)
    
    def radreport(
        self,
        account_id,
        count,
        period,
        time_zone,
        end_date=None,
        namespace_id=None,
        user_id=None,
    ):
        """Radreport.

        :param account_id: The account id
        :param count: The number of periods to get
        :param period: The time period (day|week|month|year)
        :param time_zone: The report's time zone. Time zone selection order: current user's time zone, time_zone parameter, UTC by default.
        :param end_date: The end date, default is today if not passed (optional)
        :param namespace_id: Namespace filter (optional)
        :param user_id: User filter (optional)
        """
        request_data = {
           'account_id': account_id,
           'count': count,
           'end_date': end_date,
           'namespace_id': namespace_id,
           'period': period,
           'time_zone': time_zone,
           'user_id': user_id,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_COUNT', None)] = InvalidCount('Invalid or excessive count value')
        errors_mapping[('INVALID_END_DATE', None)] = InvalidEndDate('An invalid period')
        errors_mapping[('INVALID_PERIOD', None)] = InvalidPeriod('An invalid period')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The account or patient can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view analytics for this account or namespace')
        query_data = {
            'api': self._api,
            'url': '/analytics/radreport',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return AsyncQueryO(**query_data)
    
    def user(
        self,
        account_id,
        count,
        period,
        time_zone,
        end_date=None,
        end_time=None,
        namespace_id=None,
        user_id=None,
    ):
        """User.

        :param account_id: The account id
        :param count: The number of periods to get
        :param period: The time period (hour|day|week|month|year)
        :param time_zone: The report's time zone. Time zone selection order: current user's time zone, time_zone parameter, UTC by default.
        :param end_date: The end date, for backwards compatibility (optional)
        :param end_time: The end date and time, default is now if not passed (optional)
        :param namespace_id: Namespace filter (optional)
        :param user_id: User filter (optional)
        """
        request_data = {
           'account_id': account_id,
           'count': count,
           'end_date': end_date,
           'end_time': end_time,
           'namespace_id': namespace_id,
           'period': period,
           'time_zone': time_zone,
           'user_id': user_id,
        }
	
        errors_mapping = {}
        errors_mapping[('INVALID_COUNT', None)] = InvalidCount('Invalid or excessive count value')
        errors_mapping[('INVALID_END_DATE', None)] = InvalidEndDate('An invalid period')
        errors_mapping[('INVALID_PERIOD', None)] = InvalidPeriod('An invalid period')
        errors_mapping[('MISSING_FIELDS', None)] = MissingFields('A required field is missing or does not have data in it. The error_subtype holds a array of all the missing fields')
        errors_mapping[('NOT_FOUND', None)] = NotFound('The account or patient can not be found')
        errors_mapping[('NOT_PERMITTED', None)] = NotPermitted('You are not permitted to view analytics for this account or namespace')
        query_data = {
            'api': self._api,
            'url': '/analytics/user',
            'request_data': request_data,
            'errors_mapping': errors_mapping,
            'required_sid': True,
        }
        return AsyncQueryO(**query_data)
    