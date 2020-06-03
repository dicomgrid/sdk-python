.. _referencies-storage-api:

Storage namespace
-----------------

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

All `Storage` methods returns `Response` or `Box`_ objects.

.. _`Box`: https://github.com/cdgriffith/Box

To select returns type you can use `use_box` method argument.
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




This entrypoints for using storage API methods.

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
