# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

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
