"""Ambra storage exceptions.

 Version: a1038f4611d60145d59bbfcf734c7eefc191fc64 (storage commit)

https://github.com/dicomgrid/v3storage/blob/master/GridV2WebServices/src/main/java/com/dicomgrid/webservice/exception/handling/ApiException.java#L132

~/dev/v3storage/GridV2WebServices/src/main/java/com/dicomgrid/webservice/exception/handling/ApiException.java
"""

import inspect
import types
from http import HTTPStatus

from ambra_sdk.exceptions.base import AmbraResponseException


class StorageResponseException(AmbraResponseException):  # NOQA:WPS230
    """Storage response exception."""

    def __init__(  # NOQA:WPS211
        self,
        *,
        http_status_code,
        exception_data,
        storage_code,
        description,
        readable_status,
        created,
        extended,
    ):
        """Init.

        :param http_status_code: http status code
        :param exception_data: exception data
        :param storage_code: storage code
        :param description: description
        :param readable_status: readable status
        :param created: created
        :param extended: extended
        """
        super().__init__(http_status_code, description)
        self.exception_data = exception_data
        self.storage_code = storage_code
        self.description = description
        self.http_status_code = http_status_code
        self.readable_status = readable_status
        self.created = created
        self.extended = extended


class Unknown(StorageResponseException):
    """Unknown."""

    storage_code = 1
    description = 'Internal server error'
    http_status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
    readable_status = 'UNKNOWN'


class Forbidden(StorageResponseException):
    """Forbidden."""

    storage_code = 2
    description = 'Access forbidden'
    http_status_code = HTTPStatus.FORBIDDEN.value
    readable_status = 'FORBIDDEN'


class NotFound(StorageResponseException):
    """NotFound."""

    storage_code = 3
    description = 'Entity not found'
    http_status_code = HTTPStatus.NOT_FOUND.value
    readable_status = 'NOT_FOUND'


class Unauthorized(StorageResponseException):
    """Unauthorized."""

    storage_code = 4
    description = 'Unauthorized request, supply valid auth token'
    http_status_code = HTTPStatus.UNAUTHORIZED.value
    readable_status = 'UNAUTHORIZED'


class BadRequest(StorageResponseException):
    """BadRequest."""

    storage_code = 5
    description = 'Bad request'
    http_status_code = HTTPStatus.BAD_REQUEST.value
    readable_status = 'BAD_REQUEST'


class NotAcceptable(StorageResponseException):
    """NotAcceptable."""

    storage_code = 6
    description = 'Not acceptable format'
    http_status_code = HTTPStatus.NOT_ACCEPTABLE.value
    readable_status = 'NOT_ACCEPTABLE'


class AccessDenied(StorageResponseException):
    """AccessDenied."""

    storage_code = 7
    description = (
        'Access denied for this resource.'
        " You don't have permissions on it"
    )
    http_status_code = HTTPStatus.FORBIDDEN.value
    readable_status = 'ACCESS_DENIED'


class JsonDeserializeException(StorageResponseException):
    """JsonDeserializeException."""

    storage_code = 8
    description = 'Json deserialize exception'
    http_status_code = HTTPStatus.BAD_REQUEST.value
    readable_status = 'JSON_DESERIALIZE_EXCEPTION'


class JsonSerializeException(StorageResponseException):
    """JsonSerializeException."""

    storage_code = 9
    description = 'Json serialize exception'
    http_status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
    readable_status = 'JSON_SERIALIZE_EXCEPTION'


class StorageExceptionOccurred(StorageResponseException):
    """StorageExceptionOccurred."""

    storage_code = 10
    description = 'An error occurred while contacting with object storage'
    http_status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
    readable_status = 'STORAGE_EXCEPTION_OCCURRED'


class Conflict(StorageResponseException):
    """Conflict."""

    storage_code = 11
    description = 'Resource is use in other process, try again later'
    http_status_code = HTTPStatus.CONFLICT.value
    readable_status = 'CONFLICT'


class DownstreamNotAvailable(StorageResponseException):
    """DownstreamNotAvailable."""

    storage_code = 12
    description = 'Downstream service not available'
    http_status_code = HTTPStatus.NOT_FOUND.value
    readable_status = 'DOWNSTREAM_NOT_AVAILABLE'


class DownstreamServerError(StorageResponseException):
    """DownstreamServerError."""

    storage_code = 13
    description = 'Third party service returned error on request'
    http_status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
    readable_status = 'DOWNSTREAM_SERVER_ERROR'


class ImageNotFound(StorageResponseException):
    """ImageNotFound."""

    storage_code = 14
    description = 'Image not found by ids'
    http_status_code = HTTPStatus.NOT_FOUND.value
    readable_status = 'IMAGE_NOT_FOUND'


class ImagesNotFound(StorageResponseException):
    """ImagesNotFound."""

    storage_code = 15
    description = 'Images not found by ids'
    http_status_code = HTTPStatus.NOT_FOUND.value
    readable_status = 'IMAGES_NOT_FOUND'


class AttachmentNotFoundException(StorageResponseException):
    """AttachmentNotFoundException."""

    storage_code = 16
    description = 'Attachment not found exception'
    http_status_code = HTTPStatus.NOT_FOUND.value
    readable_status = 'ATTACHMENT_NOT_FOUND_EXCEPTION'


class SeriesNotFound(StorageResponseException):
    """SeriesNotFound."""

    storage_code = 17
    description = 'Series not found by following ids'
    http_status_code = HTTPStatus.NOT_FOUND.value
    readable_status = 'SERIES_NOT_FOUND'


class StudyNotFound(StorageResponseException):
    """StudyNotFound."""

    storage_code = 18
    description = "Study wasn't found by provided ids"
    http_status_code = HTTPStatus.NOT_FOUND.value
    readable_status = 'STUDY_NOT_FOUND'


class PayloadTooLarge(StorageResponseException):
    """PayloadTooLarge."""

    storage_code = 19
    description = 'Payload too large to process the entity'
    http_status_code = HTTPStatus.REQUEST_ENTITY_TOO_LARGE.value
    readable_status = 'PAYLOAD_TOO_LARGE'


class StoreOperationFailed(StorageResponseException):
    """StoreOperationFailed."""

    storage_code = 20
    description = (
        'An error occurred while trying to persist image into storage'
    )
    http_status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
    readable_status = 'STORE_OPERATION_FAILED'


class VirusDetected(StorageResponseException):
    """VirusDetected."""

    storage_code = 21
    description = 'Virus detected in uploading entity'
    http_status_code = HTTPStatus.FORBIDDEN.value
    readable_status = 'VIRUS_DETECTED'


class AnonymizeRegionsException(StorageResponseException):
    """AnonymizeRegionsException."""

    storage_code = 22
    description = (
        'An error occurred during anonymizing regions of supplied DICOM'
    )
    http_status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
    readable_status = 'ANONYMIZE_REGIONS_EXCEPTION'


class ErrorOnReadingDicomTags(StorageResponseException):
    """ErrorOnReadingDicomTags."""

    storage_code = 23
    description = 'Error occurred during reading dicom tags into memory'
    http_status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
    readable_status = 'ERROR_ON_READING_DICOM_TAGS'


class ErrorDuringUploadProcess(StorageResponseException):
    """ErrorDuringUploadProcess."""

    storage_code = 24
    description = 'Error occurred during I/O operation'
    http_status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
    readable_status = 'ERROR_DURING_UPLOAD_PROCESS'


class ErrorOnFixingTags(StorageResponseException):
    """ErrorOnFixingTags."""

    storage_code = 25
    description = 'An error occurred on modifying and fixing DICOM tags data'
    http_status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
    readable_status = 'ERROR_ON_FIXING_TAGS'


class ErrorOnReadingEmbeddedThinkingSystem(StorageResponseException):
    """ErrorOnReadingEmbeddedThinkingSystem."""

    storage_code = 26
    description = (
        'An error occurred during reading embedded thinking system PR '
        'and fixing tags'
    )
    http_status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
    readable_status = 'ERROR_ON_READING_EMBEDDED_THINKING_SYSTEM'


class TranscodingServiceUriBuildError(StorageResponseException):
    """TranscodingServiceUriBuildError."""

    storage_code = 27
    description = (
        'An error occured during'
        ' building URL for transcoding service'
    )
    http_status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
    readable_status = 'TRANSCODING_SERVICE_URI_BUILD_ERROR'


class ErrorOccurredWhileExtractingDatumFromDicom(StorageResponseException):
    """ErrorOccurredWhileExtractingDatumFromDicom."""

    storage_code = 28
    description = (
        'An error occurred while extracting DATUM tags from DICOM, and '
        'splitting this DICOM'
    )
    http_status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
    readable_status = 'ERROR_OCCURRED_WHILE_EXTRACTING_DATUM_FROM_DICOM'


class WritingDatumToFilesystemFailed(StorageResponseException):
    """WritingDatumToFilesystemFailed."""

    storage_code = 29
    description = (
        'An error occurred while writing DATUM file to filesytem before '
        'processing and saving to storage'
    )
    http_status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
    readable_status = 'WRITING_DATUM_TO_FILESYSTEM_FAILED'


class UploadingDatumToStorageFailed(StorageResponseException):
    """UploadingDatumToStorageFailed."""

    storage_code = 30
    description = 'An error occurred while uploading DATUM to storage'
    http_status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
    readable_status = 'UPLOADING_DATUM_TO_STORAGE_FAILED'


class DatumTempFileHasNotExpectedSize(StorageResponseException):
    """DatumTempFileHasNotExpectedSize."""

    storage_code = 31
    description = (
        'An error occurred while copying DATUM file for processing in '
        'the storage, file length is 0'
    )
    http_status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
    readable_status = 'DATUM_TEMP_FILE_HAS_NOT_EXPECTED_SIZE'


class DicomTagTooLarge(StorageResponseException):
    """DicomTagTooLarge."""

    storage_code = 32
    description = (
        'An error occurred while reading DATUM and DICOM data from Datum '
        'input stream'
    )
    http_status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
    readable_status = 'DICOM_TAG_TOO_LARGE'


class UnknownErrorDuringReadingDatumDicomFileToObject(  # NOQA:WPS118
    StorageResponseException,
):
    """UnknownErrorDuringReadingDatumDicomFileToObject."""

    storage_code = 33
    description = (
        'An error occurred while reading DATUM and DICOM data from Datum '
        'input stream to Dicom and Datum objects'
    )
    http_status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
    readable_status = 'UNKNOWN_ERROR_DURING_READING_DATUM_DICOM_FILE_TO_OBJECT'


class FailedToStoreDicom(StorageResponseException):
    """FailedToStoreDicom."""

    storage_code = 34
    description = 'Failed to store DATUM DICOM'
    http_status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
    readable_status = 'FAILED_TO_STORE_DICOM'


class TranscodingServiceError(StorageResponseException):
    """TranscodingServiceError."""

    storage_code = 35
    description = 'Error persisted during trying transcoding service task'
    http_status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
    readable_status = 'TRANSCODING_SERVICE_ERROR'


class NoImagesInStudy(StorageResponseException):
    """NoImagesInStudy."""

    storage_code = 36
    description = 'There are no images in study schema'
    http_status_code = HTTPStatus.NOT_ACCEPTABLE.value
    readable_status = 'NO_IMAGES_IN_STUDY'


class ErrorOnStudyPull(StorageResponseException):
    """ErrorOnStudyPull."""

    storage_code = 37
    description = 'Wrapped error when executing request to pull study'
    http_status_code = HTTPStatus.INTERNAL_SERVER_ERROR.value
    readable_status = 'ERROR_ON_STUDY_PULL'


class NotVideoInImage(StorageResponseException):
    """NotVideoInImage."""

    storage_code = 38
    description = (
        'Video in DICOM requested, but wrapped file is another content'
    )
    http_status_code = HTTPStatus.UNSUPPORTED_MEDIA_TYPE.value
    readable_status = 'NOT_VIDEO_IN_IMAGE'


class NotPdfFile(StorageResponseException):
    """NotPdfFile."""

    storage_code = 39
    description = 'PDF requested from wrapped DICOM, wrong format found'
    http_status_code = HTTPStatus.UNSUPPORTED_MEDIA_TYPE.value
    readable_status = 'NOT_PDF_FILE'


class RequestedRangeNotSatisfiable(StorageResponseException):
    """RequestedRangeNotSatisfiable."""

    storage_code = 40
    description = (
        'Range of bytes requested within this entity has wrong interval'
    )
    http_status_code = HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE.value
    readable_status = 'REQUESTED_RANGE_NOT_SATISFIABLE'


class AnonymizeTagsFormatError(StorageResponseException):
    """AnonymizeTagsFormatError."""

    storage_code = 41
    description = (
        'Bad anonymize_tags parameter format, the proper one '
        'ex. anonymize_tags={{tag_id_int_1}}='
        '{{tag_value_1}},{{tag_id_int_2}}={{tag_value_2}}'
    )
    http_status_code = HTTPStatus.PRECONDITION_FAILED.value
    readable_status = 'ANONYMIZE_TAGS_FORMAT_ERROR'


class MissingRequiredDicomTag(StorageResponseException):
    """MissingRequiredDicomTag."""

    storage_code = 42
    description = (
        'Some of the required tags for ingestion are not present in the '
        'DICOM file'
    )
    http_status_code = HTTPStatus.PRECONDITION_FAILED.value
    readable_status = 'MISSING_REQUIRED_DICOM_TAG'


class ValidationError(StorageResponseException):
    """ValidationError."""

    storage_code = 99
    description = 'Request validation failed'
    http_status_code = HTTPStatus.PRECONDITION_FAILED.value
    readable_status = 'VALIDATION_ERROR'


errors = [
    err for err in list(locals().values())  # NOQA:WPS421
    if inspect.isclass(err) and err != StorageResponseException
    and issubclass(err, StorageResponseException)  # NOQA:W503
]

# This is a good to have a map storage_code: error, but
# we have a bug in v3storage (some errors have a same code)

STORAGE_ERRORS = types.MappingProxyType(
    {err.readable_status: err for err in errors},
)

STORAGE_ERROR_CODES = frozenset((err.http_status_code for err in errors))
