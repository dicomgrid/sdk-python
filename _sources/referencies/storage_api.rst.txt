.. _referencies-storage-api:

Storage namespace
-----------------

.. testsetup::

        from dynaconf import settings
	from ambra_sdk.api import Api
	url = settings.API['url']
	username = settings.API['username']
	password = settings.API['password']
	api = Api.with_creds(url, username, password)


Namespace for using `ambra-sdk` with `v3storage`.

For example:

.. doctest::
    :options: +SKIP

    >>> # get study schema:
    >>> api.Storage.Study.schema(
    >>>     engine_fqdn=engine_fqdn,
    >>>     namespace=storage_namespace,
    >>>     study_uid=study_uid,
    >>> )

Using boxes
^^^^^^^^^^^

All `Storage` methods returns `Response`, `PreparedRequest` or `Box`_ objects.

.. _`Box`: https://github.com/cdgriffith/Box

To select returns type `Box` you can use `use_box` method argument.
By default all methods prefer to return box objects.

for example:

.. doctest::
    :options: +SKIP

    >>> # Returns box
    >>> schema = api.Storage.Study.schema(
    ...     engine_fqdn=engine_fqdn,
    ...     namespace=storage_namespace,
    ...     study_uid=study_uid,
    >>> )
    >>> assert type(schema) == Box
    >>> 
    >>> # Returns Response
    >>> schema = api.Storage.Study.schema(
    ...     engine_fqdn=engine_fqdn,
    ...     namespace=storage_namespace,
    ...     study_uid=study_uid,
    ...     use_box=False
    >>> )
    >>> assert type(schema) == Response

image_json method
^^^^^^^^^^^^^^^^^

This method by default return `ImageJsonBox`.
You can filter tags in json or get tag by name:

.. doctest::
    :options: +SKIP

    >>> image_json = api.Storage.Study.image_json(
    ...     engine_fqdn=engine_fqdn,
    ...     namespace=storage_namespace,
    ...     study_uid=study_uid,
    ...     image_uid=image['id'],
    ...     image_version=image['version'],
    >>> )
    >>> 
    >>> # get_tags return generator
    >>> for tag in image_json.get_tags(filter_dict={'group': 2}):
    ...     print(tag.name)
    >>> 
    >>> # tag_by_name return first existing tag or None
    >>> tag = image_json.tag_by_name('Manufacturer')
    >>> print(tag.value)


json method
^^^^^^^^^^^

This method by default return `JsonBox`.
For all elements in response you can filter tags or get tag by name:

.. doctest::
    :options: +SKIP

    >>> json = api.Storage.Study.json(
    ...     engine_fqdn=engine_fqdn,
    ...     namespace=storage_namespace,
    ...     study_uid=study_uid,
    >>> )
    >>> 
    >>> image_json = json[0] # get first image element
    >>> 
    >>> # get_tags return generator
    >>> for tag in image_json.get_tags(filter_dict={'group': 2}):
    ...     print(tag.name)
    >>> 
    >>> # tag_by_name return first existing tag or None
    >>> tag = image_json.tag_by_name('Manufacturer')
    >>> print(tag.value)


PreparedRequest
^^^^^^^^^^^^^^^

To select returns type  `PreparedRequest` you can use `only_prepare` argument.

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

`SDK` storage namespace supports retry mechanism. By default, `sdk` sets some retry settings.
In some cases, you may need to define your settings for some methods.
The example below shows how to do this:


.. doctest::

    >>> from requests.adapters import HTTPAdapter
    >>> from requests.packages.urllib3.util import Retry
    >>> 
    >>> max_retries = Retry(
    ...     total=10,
    ...     backoff_factor=0.2,
    ...     method_whitelist=['GET', 'DELETE', 'POST'],
    ...  )
    >>> 
    >>> adapter = HTTPAdapter(max_retries=max_retries)
    >>> 
    >>> some_method_url = api.Storage.Study.schema(
    ...     engine_fqdn=engine_fqdn,
    ...     namespace=storage_namespace,
    ...     study_uid=study_uid,
    ...     only_prepare=True,
    ...  ).url
    >>> 
    >>> api.storage_session.mount(some_method_url, adapter)



Image namespace
^^^^^^^^^^^^^^^
.. autoclass:: ambra_sdk.storage.image.Image
   :members:
   :undoc-members:
   :inherited-members:

Study namespace
^^^^^^^^^^^^^^^
.. autoclass:: ambra_sdk.storage.study.Study
   :members:
   :undoc-members:
   :inherited-members:
