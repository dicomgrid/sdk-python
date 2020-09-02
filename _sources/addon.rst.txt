Addon methods
-------------

Addon methods include useful methods not described in `AmbraHealth API` documentation.


Study
^^^^^

Study level addon methods.

upload_dicom
~~~~~~~~~~~~

This method is for uploading dicom to the some namespace in storage::

  from pathlib import Path

  dicom_path = Path(...)

  image_params = api.Addon.Study.upload_dicom(
      dicom_path,
      namespace_id,
  )

This method gets `engine_fqdn` from the service API for a specific namespace_id and then uploads dicom to the storage using :py:meth:`api.Storage.Image.upload` method.

upload
~~~~~~

This method creates a new `thin` study, uploads all dicom files (`**/*.dcm`) from a specific study path to storage, and calls sync for this study::

  from pathlib import Path

  study_path = Path(...)

  study_uuid, image_params  = api.Addon.Study.upload(
      study_path,
      namespace_id,
  )


wait
~~~~

Wait for a new study (not phantom) in namespace::

  new_study = api.Addon.Study.wait(
      study_uid,
      namespace_id,
      timeout=10,
  )


upload_and_get
~~~~~~~~~~~~~~

Upload dicoms from specific study dir using :py:meth:`api.Addon.Study.upload` method and wait for this object to appear in `v3services`::

  new_study = api.Addon.Study.upload_and_get(
      study_dir=study_dir,
      namespace_id=namespace_id,
  )

duplicate_and_get
~~~~~~~~~~~~~~~~~

This method calls :py:meth:`api.Study.duplicate` async method and waits for new duplicated study::

  duplicated_study = api.Addon.Study.duplicate_and_get(
      uuid=some_study.uuid,
      namespace_id=to_namespace_id,
  )
