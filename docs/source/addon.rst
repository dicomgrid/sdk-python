Addon methods
-------------

Addon methods include useful methods not described in `AmbraHealth API` documentation.


Study
^^^^^

Study level addon methods.


.. _study_upload_dir:

upload_dir
~~~~~~~~~~

[New in 3.21.2.0]

This method for uploading study directory to some namespace in storage::

  from pathlib import Path

  study_dir = Path(...)

  study_uid, image_params = api.Addon.Study.upload_dir(
      study_dir=study_dir,
      namespace_id=namespace_id,
  )

upload_paths
~~~~~~~~~~~~

[New in 3.21.2.0]

This method for uploading study using dicoms paths::

  from pathlib import Path

  study_dir = Path(...)

  study_uid, image_params = api.Addon.Study.upload_paths(
      dicom_paths=study_dir.glob('**/*.dcm'),
      namespace_id=namespace_id,
  )

It can be useful if you would like to use some user specific dicom path iterator.
For example, tqdm progress bar usage::

  from pathlib import Path
  from tqdm import tqdm

  study_dir = Path(...)

  study_uid, image_params = api.Addon.Study.upload_paths(
      dicom_paths=iter(tqdm(study_dir.glob('**/*.dcm'))),
      namespace_id=namespace_id,
  )


wait
~~~~

Wait for a new study (not phantom) in namespace::

  study = api.Addon.Study.wait(
      study_uid,
      namespace_id,
      timeout=10,
  )

.. _study_upload_dir_and_get:

upload_dir_and_get
~~~~~~~~~~~~~~~~~~

[New in 3.21.2.0]

Upload dicoms from specific study dir using :py:meth:`api.Addon.Study.upload_dir` method and wait for this object to appear in `v3services`::

  from pathlib import Path

  study_dir = Path(...)

  new_study = api.Addon.Study.upload_dir_and_get(
      study_dir=study_dir,
      namespace_id=namespace_id,
  )



upload_paths_and_get
~~~~~~~~~~~~~~~~~~~~

[New in 3.21.2.0]

Upload dicoms from paths iterator using :py:meth:`api.Addon.Study.upload_paths` method and wait for this object to appear in `v3services`::

  from pathlib import Path

  study_dir = Path(...)

  new_study = api.Addon.Study.upload_dir_and_get(
      dicom_paths=study_dir.glob('**/*.dcm'),
      namespace_id=namespace_id,
  )


duplicate_and_get
~~~~~~~~~~~~~~~~~

This method calls :py:meth:`api.Study.duplicate` async method and waits for new duplicated study::

  duplicated_study = api.Addon.Study.duplicate_and_get(
      uuid=some_study.uuid,
      namespace_id=to_namespace_id,
  )


anonymize_and_wait
~~~~~~~~~~~~~~~~~~

[New in 3.21.1.0]

Start anonymization and wait for completion::

  api.Addon.Study.anonymize_and_wait(
      engine_fqdn,
      namespace,
      study_uid,
      region,
      namespace_id,
      timeout=10,
  )


anonymize_and_get
~~~~~~~~~~~~~~~~~

[New in 3.21.1.0]

Start anonymization and get anonymized study::

  anonymized_study = api.Addon.Study.anonymize_and_get(
      engine_fqdn,
      namespace,
      study_uid,
      region,
      namespace_id,
      timeout=10,
  )



wait_job [DEPRECATED]
~~~~~~~~~~~~~~~~~~~~~

[New in 3.21.1.0]
[DEPRECATED in 3.21.2.0]

.. warning::
   Instead of this use :ref:`job_wait` method.

Wait for a job done (for example storage anonymization job)::

  api.Addon.Study.wait_job(
      job_id,
      namespace_id,
      timeout=10,
  )



dicom [DEPRECATED]
~~~~~~~~~~~~~~~~~~

[New in 3.20.8.0]
[DEPRECATED in 3.21.2.0]

.. warning::
   Instead of this use :ref:`dicom_get` method.

Get pydicom specific object from storage::

  dicom = api.Addon.Study.dicom(
            namespace_id=storage_namespace,
            study_uid=study_uid,
            image_uid=image['id'],
        )



upload_dicom [DEPRECATED]
~~~~~~~~~~~~~~~~~~~~~~~~~

[DEPRECATED in 3.21.2.0]

.. warning::

   Instead of this use :ref:`dicom_upload_from_path` method.

This method is for uploading dicom to the some namespace in storage::

  from pathlib import Path

  dicom_path = Path(...)

  image_params = api.Addon.Study.upload_dicom(
      dicom_path,
      namespace_id,
  )

This method gets `engine_fqdn` from the service API for a specific namespace_id and then uploads dicom to the storage using :py:meth:`api.Storage.Image.upload` method.


upload [DEPRECATED]
~~~~~~~~~~~~~~~~~~~

[DEPRECATED in 3.21.2.0]

.. warning::
   Instead of this use :ref:`study_upload_dir` method.

This method creates a new `thin` study, uploads all dicom files (`**/*.dcm`) from a specific study path to storage, and calls sync for this study::

  from pathlib import Path

  study_path = Path(...)

  study_uuid, image_params  = api.Addon.Study.upload(
      study_path,
      namespace_id,
  )


upload_and_get [DEPRECATED]
~~~~~~~~~~~~~~~~~~~~~~~~~~~

[DEPRECATED in 3.21.2.0]

.. warning::
   Instead of this use :ref:`study_upload_dir_and_get` method.

Upload dicoms from specific study dir using :py:meth:`api.Addon.Study.upload` method and wait for this object to appear in `v3services`::

  new_study = api.Addon.Study.upload_and_get(
      study_dir=study_dir,
      namespace_id=namespace_id,
  )


Job
^^^

Job level addon methods.

.. _job_wait:

wait
~~~~

[New in 3.21.2.0]

Wait for storage job done (for example storage anonymization job)::

  api.Addon.Job.wait(
      job_id=job_id,
      namespace_id=namespace_id,
      timeout=10,
      ws_timeout=1,
  )


wait_completion
~~~~~~~~~~~~~~~

[New in 3.21.3.0]

Execute storage method and wait this job. This is a anonymize and wait example::

  anonymized_study_uid = api.Addon.Job.wait_completion(
      api.Storage.Study.anonymize,
      engine_fqdn=engine_fqdn,
      namespace=namespace,
      study_uid=study_uid,
      region=region,
      to_namespace=to_namespace,
      new_study_uid=new_study_uid,
      keep_image_uids=keep_image_uids,
      color=color,
      only_prepare=only_prepare,
  )
 


Dicom
^^^^^

Dicom level addon methods.


.. _dicom_get:

get
~~~

[New in 3.21.2.0]

Get pydicom specific object from storage::

  dicom = api.Addon.Dicom.get(
            namespace_id=storage_namespace,
            study_uid=study_uid,
            image_uid=image['id'],
        )

upload
~~~~~~

[New in 3.21.2.0]

Upload dicom file to storage namespace::

  with open('dicom.dcm', 'rb') as dicom_file:
      uploaded_image_params = api.Addon.Dicom.upload(
          dicom_file=dicom_file,
          namespace_id=namespace_id,
      )

.. _dicom_upload_from_path:

upload_from_path
~~~~~~~~~~~~~~~~

[New in 3.21.2.0]

Upload dicom from path to storage namespace::

  from pathlib import Path

  dicom_path = Path(..)

  uploaded_image_params = api.Addon.Dicom.upload_from_path(
      dicom_path=dicom_path,
      namespace_id=namespace_id,
  )

