# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [3.21.3.0-2] - 2021-04-16
### Fixed
- api.Namespace.settings settings -> ai_settings


## [3.21.3.0-1] - 2021-04-07
### Added
- Service public api support: LBL0022 v45.0 2021-04-07
- Service models: LBL0022 v45.0 2021-04-07
- Storage public api support: LBL0038 v14.0 2021-02-24
- api.Addon.Addon.Job.wait_completion method
- Job support for api.Storage.Study.delete_images
- Job support for api.Storage.Study.post_attachemnt
- Job support for api.Storage.Study.delete_attachemnt
- Job support for api.Storage.Study.merge
- Job support for api.Storage.Study.anonymize
- Job support for api.Storage.Study.clone
- Job support for api.Storage.Image.upload
- Job support for api.Storage.Image.wrap

## [3.21.2.0-1] - 2021-02-24
### Added
- api.Addon.Dicom.upload method
- api.Addon.Study.upload_dir method
- api.Addon.Study.upload_paths method
- api.Addon.Study.upload_dir_and_get method
- api.Addon.Study.upload_paths_and_get method
- api.Addon.Addon.Job.wait method
- api.Addon.Dicom.get method
- Session level setup headers default_headers
- Session level setup headers service_default_headers
- Session level setup headers storage_default_headers
- special_headers_for_login in api constructor

### Changed
- api.Addon.Study.upload_dicom method deprecated
- api.Addon.Study.upload method deprecated
- api.Addon.Study.upload_and_get method deprecated
- api.Addon.Study.wait_job method deprecated
- api.Addon.Study.dicom method deprecated
- Query.requst_params -> Query.request_args You can modify request arguments for specific service call

## [3.21.1.0-1] - 2021-01-13
### Added
- Service public api support: LBL0022 v44.0 2021-02-24
- Service models: LBL0022 v44.0 2021-02-24
- Storage public api support: LBL0038 v13.0 2021-01-13
- api.Addon.Study.wait_job method
- api.Addon.Study.wait_anonymize_and_wait method
- api.Addon.Study.wait_anonymize_and_get method
- Support filtering using datetime with timezones

## [3.20.8.0-2] - 2020-11-18
### Added
- Service public api support: LBL0022 v42.0 2020-12-02
- Service models: LBL0022 v42.0 2020-12-02
- New method api.Storage.Image.dicom_payload: return dicom payload
- New method api.Addon.Study.dicom: return pydicom object

## [3.20.7.0-1] - 2020-10-07
### Added
- Service public api support: LBL0022 v41.0 2020-10-07
- Service models: LBL0022 v41.0 2020-10-07
- Storage public api support: LBL0038 v11.0 2020-10-07

### Changed
- Using dashes instead of underscores in SDK header names (for example SDK_VERSION -> SDK-VERSION)

## [3.20.6.0-2] - 2020-08-26
### Fixed
- Error handling with list error_subtype

## [3.20.6.0-1] - 2020-08-26
### Added
- Documentation updates
- Service public api support: LBL0022 v40.0 2020-08-26
- Service models: LBL0022 v40.0 2020-08-26
- Storage public api support: LBL0038 v10.0 2020-08-26

### Changed
- Removed 502, 503 errors from default retry service params
- Update python-box dependence to 5.1.1
- Update requests dependence to 2.24.0

## [3.20.5.0-1] - 2020-07-15
### Added
- url, full_url, request_data for service query objects
- only_prepare argument (default is False) for all storage methods. If it is True, method return PreparedRequest object
- Examples of using retry mechanism for specific methods
- client_name argument in Api constructors
- SDK_VERSION, SDK_CLIENT_NAME in default session headers
- SDK version in documentation
- Service public api support: LBL0022 v39.0 2020-07-15
- Service models: LBL0022 v39.0 2020-07-15

### Changed
- Update to pydicom==2.0.0
- Change INFO log level in ws to DEBUG

### Fixed
- Fix usage example in README
- Fix retrying requests with new SID

## [3.20.4.0-1] - 2020-06-03
### Added
- Storage api support: LBL0038 v9.0 2020-06-03
- Service public api support: LBL0022 v38.0 2020-05-27
- Service models: LBL0022 v38.0 2020-05-27
- get_tags and tag_by_name methods in Storage.Study.json Box response
- get_tags and tag_by_name methods in Storage.Study.image_json Box response
- Add InconsistencyConfict(409) error Storage.Study.schema

### Changed
- Box response type in storage methods now is optional (default return Box)

## [3.20.3.0-5] - 2020-05-06
### Added
- Doctests in sphinx documentation
- Testing on various types of storage

### Changed
- Storage.Image.cadsr return requests.Response
- Storage.Image.wrap return requests.Response
- Storage.Study.anonymize return requests.Response
- Storage.Study.attribute changed set of input variables
- Storage.Study.cache return requests.Response
- Storage.Study.crop return requests.Response
- Storage.Study.delete_attachment return requests.Response
- Storage.Study.delete_image return requests.Response
- Storage.Study.delete return requests.Response
- Storage.Study.diagnostic changed set of input variables
- Storage.Study.diagnostic return requests.Response
- Storage.Study.image_phi changed set of input variables
- Storage.Study.json return list of dicts
- Storage.Study.merge return requests.Response
- Storage.Study.post_attachment return requests.Response
- Storage.Study.thumbnail return requests.Response

### Fixed
- Some bugs in storage API
- Docs inconsistency

## [3.20.3.0-4] - 2020-04-24
### Changed
- Documentation moved to github pages

## [3.20.3.0-3] - 2020-04-13
### Added
- Storage api support: LBL0038 v8.0 2019-07-17
- Service public api support: LBL0022 v37.0 2020-04-15
- Service models: LBL0022 v37.0 2020-04-15
- Docker support: LBL0022 v37.0 2020-04-15
