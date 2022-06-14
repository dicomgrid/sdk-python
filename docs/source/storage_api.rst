.. _storage-api:

.. testsetup::

        from dynaconf import settings
	from ambra_sdk.api import Api
	url = settings.API['url']
	username = settings.API['username']
	password = settings.API['password']
	api = Api.with_creds(url, username, password)
	sid = 'SOME BAD SID'
	client_name = 'SOME_CLIENT_NAME'

Storage API
-----------

This section describes the interaction with `AmbraHealth storage API`_.

The footer of this document shows the current version of `AmbraHealth API`.
Make sure the current version of `ambra-sdk` is not lower.

.. doctest::

    >>> from ambra_sdk import STORAGE_VERSION
    >>> print(STORAGE_VERSION)
    LBL0038 v22.0 2022-05-18

A description of all existing methods can be found in the :ref:`Storage API reference<referencies-storage-api>`.

To access storage api methods, use `api.Storage` namespace.

As in the server documentation in `ambra-sdk`, all api requests to storage are organized by `Study` and `Image` commands.


image_json method
^^^^^^^^^^^^^^^^^

This method by default returns `ImageJsonBox`.
One can filter results by DICOM tags or by getting tags by name::

  image_json = api.Storage.Study.image_json(
      engine_fqdn=engine_fqdn,
      namespace=storage_namespace,
      study_uid=study_uid,
      image_uid=image['id'],
      image_version=image['version'],
  )
  
  # get_tags return generator
  for tag in image_json.get_tags(filter_dict={'group': 2}):
      print(tag.name)
  
  # tag_by_name return first existing tag or None
  tag = image_json.tag_by_name('Manufacturer')
  print(tag.value)


json method
^^^^^^^^^^^

This method by default returns `JsonBox`.
One can filter results by DICOM tags or by getting tags by name::

  json = api.Storage.Study.json(
      engine_fqdn=engine_fqdn,
      namespace=storage_namespace,
      study_uid=study_uid,
  )
  
  image_json = json[0] # get first image element
  
  # get_tags return generator
  for tag in image_json.get_tags(filter_dict={'group': 2}):
      print(tag.name)
  
  # tag_by_name return first existing tag or None
  tag = image_json.tag_by_name('Manufacturer')
  print(tag.value)

Box result
^^^^^^^^^^

All `Storage` methods return `Response`, `PreparedRequest` or `Box`_ objects.

To select return type `Box`, use the `use_box` method argument.
By default all methods return box objects.

for example::

  # Returns box
  schema = api.Storage.Study.schema(
      engine_fqdn=engine_fqdn,
      namespace=storage_namespace,
      study_uid=study_uid,
  )
  assert type(schema) == Box
  
  # Returns Response
  schema = api.Storage.Study.schema(
      engine_fqdn=engine_fqdn,
      namespace=storage_namespace,
      study_uid=study_uid,
      use_box=False
  )
  assert type(schema) == Response


PreparedRequest
^^^^^^^^^^^^^^^

To select returns type  `PreparedRequest`, use `only_prepare` argument.
 
for example:

.. testsetup::

        engine_fqdn='engine_fqdn'
        storage_namespace='storage_namespace'
        study_uid='study_uid'
	
.. doctest::

    >>> from ambra_sdk.storage.request import PreparedRequest
    >>> 
    >>> study_schema = api.Storage.Study.schema(
    ...     engine_fqdn=engine_fqdn,
    ...     namespace=storage_namespace,
    ...     study_uid=study_uid,
    ...     only_prepare=True,
    ...  )
    >>> 
    >>> assert type(study_schema) == PreparedRequest
    >>> study_schema.url
    'https://engine_fqdn/api/v3/storage/study/storage_namespace/study_uid/schema'
    >>> study_schema.method.value
    'GET'


Retries
^^^^^^^

`ambra-sdk.Storage` namespace supports retry mechanism.

By default, `sdk` sets specific retry settings.
In some cases, user-defined Retry mechanisms can be set for specific methods.
The example below shows how to do this::
  
  from requests.adapters import HTTPAdapter
  from requests.packages.urllib3.util import Retry
  
  max_retries = Retry(
      total=10,
      backoff_factor=0.2,
      method_whitelist=['GET', 'DELETE', 'POST'],
   )
  
  adapter = HTTPAdapter(max_retries=max_retries)
  
  some_method_url = api.Storage.Study.schema(
      engine_fqdn=engine_fqdn,
      namespace=storage_namespace,
      study_uid=study_uid,
      only_prepare=True,
   ).url
  
  api.storage_session.mount(some_method_url, adapter)


Headers
^^^^^^^

You can setup some default headers for storage session
(using `storage_default_headers` property) or for both service and storage sessions
(using `default_headers` property)::

  api.default_headers['Golbal-header'] = 'value'
  api.storage_default_headers['Storage-specific-header'] = 'value'


.. _`AmbraHealth storage API`: https://uat.dicomgrid.com/api/v3/storage/storage_api.html

.. _`Box`: https://github.com/cdgriffith/Box
