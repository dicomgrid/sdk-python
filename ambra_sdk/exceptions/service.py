"""Ambra service exceptions."""

from ambra_sdk.exceptions.base import AmbraResponseException


class AuthorizationRequired(AmbraResponseException):
    """Authorization required."""

    def __init__(self, description=None):
        """Init.

        :param description: response description
        """
        code = 401
        if description is None:
            description = (
                'The call needs a valid, logged '
                'in session id (sid) or valid basic '
                'authentication user name and password.'
            )
        super().__init__(code, description)


class MethodNotAllowed(AmbraResponseException):
    """Method not allowed."""

    def __init__(self, description=None):
        """Init.

        :param description: response description
        """
        code = 405
        if description is None:
            description = 'The call must be a POST not a GET'
        super().__init__(code, description)


class PreconditionFailed(AmbraResponseException):
    """Precondition failed."""

    def __init__(self, description=None, error_subtype=None, error_data=None):
        """Init.

        :param description: response description
        :param error_subtype: error subtype
        :param error_data: error data
        """
        code = 412
        if description is None:
            description = (
                'The returned json data structure will '
                'have the status flag set to ERROR. '
                'The error_type and the optional error_subtype '
                'fields will hold tokens that describe the error. '
                'The optional error_data field can hold additional error data.'
            )
        super().__init__(code, description)
        self.error_subtype = error_subtype
        self.error_data = error_data

    def set_additional_info(self, error_subtype, error_data):
        """Set additional error info.

        :param error_subtype: error subtype
        :param error_data: error data
        """
        self.error_subtype = error_subtype
        self.error_data = error_data

    def __str__(self):
        """Get string represenation of exception.

        :return: string repr
        """
        return (
            '{description}.\n'
            'Error subtype: {error_subtype}\n'
            'Error data: {error_data}\n'
        ).format(
            description=self.description,
            error_subtype=self.error_subtype,
            error_data=self.error_data,
        )


class InvalidField(PreconditionFailed):
    """InvalidField.

    The field is not valid for this object.
    The error_subtype will hold the filter expression
    this applies to.
    """


class InvalidCondition(PreconditionFailed):
    """InvalidCondition.

    The condition is not support.
    The error_subtype will hold the filter expression
    this applies to.
    """


class FilterNotFound(PreconditionFailed):
    """FilterNotFound.

    The filter can not be found.
    The error_subtype will hold the filter UUID.
    """


class InvalidSortField(PreconditionFailed):
    """InvalidSortField.

    The field is not valid for this object.
    The error_subtype will hold the field name this applies to.
    """


class InvalidSortOrder(PreconditionFailed):
    """InvalidSortOrder.

    The sort order for the field is invalid.
    The error_subtype will hold the field name this applies to.
    """


class InvalidHl7Field(PreconditionFailed):
    """InvalidHl7Field."""


class Disabled(PreconditionFailed):
    """Disabled."""


class DupShareCode(PreconditionFailed):
    """DupShareCode."""


class NotAttending(PreconditionFailed):
    """NotAttending."""


class AlreadyThin(PreconditionFailed):
    """AlreadyThin."""


class NamespaceNotFound(PreconditionFailed):
    """NamespaceNotFound."""


class InvalidUrl(PreconditionFailed):
    """InvalidUrl."""


class InvalidVanity(PreconditionFailed):
    """InvalidVanity."""


class InvalidDicomTagObject(PreconditionFailed):
    """InvalidDicomTagObject."""


class InvalidSchedule(PreconditionFailed):
    """InvalidSchedule."""


class ParseFailed(PreconditionFailed):
    """ParseFailed."""


class InvalidSource(PreconditionFailed):
    """InvalidSource."""


class InvalidRange(PreconditionFailed):
    """InvalidRange."""


class NeedsAnyOrAll(PreconditionFailed):
    """NeedsAnyOrAll."""


class UnableToValidate(PreconditionFailed):
    """UnableToValidate."""


class InvalidAmount(PreconditionFailed):
    """InvalidAmount."""


class NotConfigured(PreconditionFailed):
    """NotConfigured."""


class WithNotFound(PreconditionFailed):
    """WithNotFound."""


class NoHl7Support(PreconditionFailed):
    """NoHl7Support."""


class NotFound(PreconditionFailed):
    """NotFound."""


class InvalidTag(PreconditionFailed):
    """InvalidTag."""


class Accepted(PreconditionFailed):
    """Accepted."""


class SidUserNotFound(PreconditionFailed):
    """SidUserNotFound."""


class InvalidSettingValue(PreconditionFailed):
    """InvalidSettingValue."""


class NotAvailable(PreconditionFailed):
    """NotAvailable."""


class NoNodeOverride(PreconditionFailed):
    """NoNodeOverride."""


class NoValue(PreconditionFailed):
    """NoValue."""


class InvalidDate(PreconditionFailed):
    """InvalidDate."""


class AuthFailed(PreconditionFailed):
    """AuthFailed."""


class InvalidPhiField(PreconditionFailed):
    """InvalidPhiField."""


class InvalidLookup(PreconditionFailed):
    """InvalidLookup."""


class NotPermitted(PreconditionFailed):
    """NotPermitted."""


class InvalidCredentials(PreconditionFailed):
    """InvalidCredentials."""


class Already(PreconditionFailed):
    """Already."""


class NotList(PreconditionFailed):
    """NotList."""


class InvalidReplacement(PreconditionFailed):
    """InvalidReplacement."""


class AlreadyDone(PreconditionFailed):
    """AlreadyDone."""


class DestinationNotFound(PreconditionFailed):
    """DestinationNotFound."""


class OnlyOneFlag(PreconditionFailed):
    """OnlyOneFlag."""


class AccountNotSet(PreconditionFailed):
    """AccountNotSet."""


class AllDone(PreconditionFailed):
    """AllDone."""


class InUse(PreconditionFailed):
    """InUse."""


class TokenFailed(PreconditionFailed):
    """TokenFailed."""


class NotMember(PreconditionFailed):
    """NotMember."""


class InvalidValue(PreconditionFailed):
    """InvalidValue."""


class DuplicateName(PreconditionFailed):
    """DuplicateName."""


class InvalidStatus(PreconditionFailed):
    """InvalidStatus."""


class InvalidLink(PreconditionFailed):
    """InvalidLink."""


class InvalidFilterField(PreconditionFailed):
    """InvalidFilterField."""


class InvalidRegexp(PreconditionFailed):
    """InvalidRegexp."""


class NoFreshArchive(PreconditionFailed):
    """NoFreshArchive."""


class UnableToGenerate(PreconditionFailed):
    """UnableToGenerate."""


class InvalidMetric(PreconditionFailed):
    """InvalidMetric."""


class ByNotFound(PreconditionFailed):
    """ByNotFound."""


class Lockout(PreconditionFailed):
    """Lockout."""


class StudyNotFound(PreconditionFailed):
    """StudyNotFound."""


class InvalidCaseStatus(PreconditionFailed):
    """InvalidCaseStatus."""


class DuplicateOrderBy(PreconditionFailed):
    """DuplicateOrderBy."""


class InvalidEndDate(PreconditionFailed):
    """InvalidEndDate."""


class InvalidEvent(PreconditionFailed):
    """InvalidEvent."""


class BadPassword(PreconditionFailed):
    """BadPassword."""


class PinExpired(PreconditionFailed):
    """PinExpired."""


class InvalidPassword(PreconditionFailed):
    """InvalidPassword."""


class InvalidAction(PreconditionFailed):
    """InvalidAction."""


class RoleNotFound(PreconditionFailed):
    """RoleNotFound."""


class InvalidOtherNamespaces(PreconditionFailed):
    """InvalidOtherNamespaces."""


class InvalidDateTime(PreconditionFailed):
    """InvalidDateTime."""


class MissingInformation(PreconditionFailed):
    """MissingInformation."""


class InvalidCount(PreconditionFailed):
    """InvalidCount."""


class DuplicateEmail(PreconditionFailed):
    """DuplicateEmail."""


class NodeNotSetup(PreconditionFailed):
    """NodeNotSetup."""


class AccountNotFound(PreconditionFailed):
    """AccountNotFound."""


class IncompleteFilter(PreconditionFailed):
    """IncompleteFilter."""


class InvalidVendor(PreconditionFailed):
    """InvalidVendor."""


class ChargeRequired(PreconditionFailed):
    """ChargeRequired."""


class NoFilter(PreconditionFailed):
    """NoFilter."""


class NoAttachment(PreconditionFailed):
    """NoAttachment."""


class HasDestinations(PreconditionFailed):
    """HasDestinations."""


class DelayOrMatch(PreconditionFailed):
    """DelayOrMatch."""


class NotInAccount(PreconditionFailed):
    """NotInAccount."""


class NoDicomTagDefined(PreconditionFailed):
    """NoDicomTagDefined."""


class InvalidCharge(PreconditionFailed):
    """InvalidCharge."""


class InvalidCustomfield(PreconditionFailed):
    """InvalidCustomfield."""


class RecentNamespaceSplit(PreconditionFailed):
    """RecentNamespaceSplit."""


class NotThin(PreconditionFailed):
    """NotThin."""


class MissingInfo(PreconditionFailed):
    """MissingInfo."""


class NotANumber(PreconditionFailed):
    """NotANumber."""


class InvalidJson(PreconditionFailed):
    """InvalidJson."""


class InvalidPeriod(PreconditionFailed):
    """InvalidPeriod."""


class InProcess(PreconditionFailed):
    """InProcess."""


class Locked(PreconditionFailed):
    """Locked."""


class InvalidFilter(PreconditionFailed):
    """InvalidFilter."""


class Stale(PreconditionFailed):
    """Stale."""


class OnlyAll(PreconditionFailed):
    """OnlyAll."""


class SidUserNotInAccount(PreconditionFailed):
    """SidUserNotInAccount."""


class CanNotPromote(PreconditionFailed):
    """CanNotPromote."""


class InvalidGatewayType(PreconditionFailed):
    """InvalidGatewayType."""


class NoOtherRoleEdit(PreconditionFailed):
    """NoOtherRoleEdit."""


class ChargeFailed(PreconditionFailed):
    """ChargeFailed."""


class InvalidManualRoles(PreconditionFailed):
    """InvalidManualRoles."""


class InvalidObject(PreconditionFailed):
    """InvalidObject."""


class OneZipOnly(PreconditionFailed):
    """OneZipOnly."""


class Blocked(PreconditionFailed):
    """Blocked."""


class InvalidSearchSource(PreconditionFailed):
    """InvalidSearchSource."""


class InvalidPermissionValue(PreconditionFailed):
    """InvalidPermissionValue."""


class InvalidPin(PreconditionFailed):
    """InvalidPin."""


class Phantom(PreconditionFailed):
    """Phantom."""


class AlreadyUsed(PreconditionFailed):
    """AlreadyUsed."""


class InvalidCode(PreconditionFailed):
    """InvalidCode."""


class AlreadyExists(PreconditionFailed):
    """AlreadyExists."""


class InvalidPhone(PreconditionFailed):
    """InvalidPhone."""


class InvalidUploadMatch(PreconditionFailed):
    """InvalidUploadMatch."""


class ShareFailed(PreconditionFailed):
    """ShareFailed."""


class NotEnabled(PreconditionFailed):
    """NotEnabled."""


class InvalidToken(PreconditionFailed):
    """InvalidToken."""


class InvalidParameters(PreconditionFailed):
    """InvalidParameters."""


class NotSupported(PreconditionFailed):
    """NotSupported."""


class NotWithCron(PreconditionFailed):
    """NotWithCron."""


class ValidationFailed(PreconditionFailed):
    """ValidationFailed."""


class InvalidEmail(PreconditionFailed):
    """InvalidEmail."""


class InvalidConfiguration(PreconditionFailed):
    """InvalidConfiguration."""


class InvalidOptions(PreconditionFailed):
    """InvalidOptions."""


class GtZero(PreconditionFailed):
    """GtZero."""


class SfdcMissingFields(PreconditionFailed):
    """SfdcMissingFields."""


class InvalidHl7Object(PreconditionFailed):
    """InvalidHl7Object."""


class InvalidInteger(PreconditionFailed):
    """InvalidInteger."""


class InvalidDicomTag(PreconditionFailed):
    """InvalidDicomTag."""


class MissingFields(PreconditionFailed):
    """MissingFields."""


class Pending(PreconditionFailed):
    """Pending."""


class NotDisabled(PreconditionFailed):
    """NotDisabled."""


class ReportError(PreconditionFailed):
    """ReportError."""


class PendingMustMatch(PreconditionFailed):
    """PendingMustMatch."""


class DuplicateVanity(PreconditionFailed):
    """DuplicateVanity."""


class Validate(PreconditionFailed):
    """Validate."""


class PdfFailed(PreconditionFailed):
    """PdfFailed."""


class InvalidMethod(PreconditionFailed):
    """InvalidMethod."""


class InvalidPermission(PreconditionFailed):
    """InvalidPermission."""


class InvalidTimeZone(PreconditionFailed):
    """InvalidTimeZone."""


class LinkNotFound(PreconditionFailed):
    """LinkNotFound."""


class InvalidLinkage(PreconditionFailed):
    """InvalidLinkage."""


class InvalidNodeType(PreconditionFailed):
    """InvalidNodeType."""


class ExamNotFound(PreconditionFailed):
    """ExamNotFound."""


class InvalidFieldName(PreconditionFailed):
    """InvalidFieldName."""


class NoUserOverride(PreconditionFailed):
    """NoUserOverride."""


class InsufficientCriteria(PreconditionFailed):
    """InsufficientCriteria."""


class WhitelistLockout(PreconditionFailed):
    """WhitelistLockout."""


class InvalidCurrency(PreconditionFailed):
    """InvalidCurrency."""


class MissingParameters(PreconditionFailed):
    """MissingParameters."""


class InvalidHl7(PreconditionFailed):
    """InvalidHl7."""


class ErrorCreatingStudy(PreconditionFailed):
    """ErrorCreatingStudy."""


class TryLater(PreconditionFailed):
    """TryLater."""


class AlreadyMember(PreconditionFailed):
    """AlreadyMember."""


class PasswordReset(PreconditionFailed):
    """PasswordReset."""


class InvalidHl7Segment(PreconditionFailed):
    """InvalidHl7Segment."""


class NoOauth(PreconditionFailed):
    """NoOauth."""


class Running(PreconditionFailed):
    """Running."""


class CaptchaFailed(PreconditionFailed):
    """CaptchaFailed."""


class Singleton(PreconditionFailed):
    """Singleton."""


class ReportFailed(PreconditionFailed):
    """ReportFailed."""


class UserNotFound(PreconditionFailed):
    """UserNotFound."""


class NotASearch(PreconditionFailed):
    """NotASearch."""


class CustomNotHash(PreconditionFailed):
    """CustomNotHash."""


class AccountUserNotFound(PreconditionFailed):
    """AccountUserNotFound."""


class Failed(PreconditionFailed):
    """Failed."""


class InvalidDelay(PreconditionFailed):
    """InvalidDelay."""


class Retrieve(PreconditionFailed):
    """Retrieve."""


class InvalidTemplate(PreconditionFailed):
    """InvalidTemplate."""


class SfdcNotHash(PreconditionFailed):
    """SfdcNotHash."""


class InvalidOption(PreconditionFailed):
    """InvalidOption."""


class InvalidType(PreconditionFailed):
    """InvalidType."""


class OtherOauth(PreconditionFailed):
    """OtherOauth."""


class InvalidSid(PreconditionFailed):
    """InvalidSid."""


class LookupFailed(PreconditionFailed):
    """LookupFailed."""


class InvalidCron(PreconditionFailed):
    """InvalidCron."""


class NoQueryDestination(PreconditionFailed):
    """NoQueryDestination."""


class InvalidFlag(PreconditionFailed):
    """InvalidFlag."""


class InvalidTransformCondition(PreconditionFailed):
    """InvalidTransformCondition."""


class InvalidNpi(PreconditionFailed):
    """InvalidNpi."""


class NotEmpty(PreconditionFailed):
    """NotEmpty."""


class Expired(PreconditionFailed):
    """Expired."""


class NodeNotFound(PreconditionFailed):
    """NodeNotFound."""


class InvalidCdBurnInfo(PreconditionFailed):
    """InvalidCdBurnInfo."""


class NotHash(PreconditionFailed):
    """NotHash."""


class NotSysadminOrSupport(PreconditionFailed):
    """NotSysadminOrSupport."""


class IsDeployed(PreconditionFailed):
    """IsDeployed."""


class InvalidUuid(PreconditionFailed):
    """InvalidUuid."""


class DupAetitle(PreconditionFailed):
    """DupAetitle."""


class InvalidMessage(PreconditionFailed):
    """InvalidMessage."""


class InvalidSetting(PreconditionFailed):
    """InvalidSetting."""


class IpBlocked(PreconditionFailed):
    """IpBlocked."""


class InvalidBucket(PreconditionFailed):
    """InvalidBucket."""


class InvalidLanguage(PreconditionFailed):
    """InvalidLanguage."""


class DecryptFailed(PreconditionFailed):
    """DecryptFailed."""


class ScheduleIsOff(PreconditionFailed):
    """ScheduleIsOff."""


class NotReady(PreconditionFailed):
    """NotReady."""


class RouteNotMatched(PreconditionFailed):
    """RouteNotMatched."""


class NotSysadmin(PreconditionFailed):
    """NotSysadmin."""


class PinLockout(PreconditionFailed):
    """PinLockout."""


class AlreadyConnected(PreconditionFailed):
    """AlreadyConnected."""


class NotCustomfieldsPricing(PreconditionFailed):
    """NotCustomfieldsPricing.

    The namespace is set up to charge by modality
    """
