Quick Start
===========


Init API
--------

Before we begin, to use sdk you need to know `url` of ambrahealth api and user credentials (`username` and `password`).

For accessing to api functions you need to `sid` - session identificator.

If you already have this, you can init api instance:

.. testsetup::

        from dynaconf import settings
	url = settings.API['url']
	username = settings.API['username']
	password = settings.API['password']
	sid = 'SOME BAD SID'

.. doctest::

    >>> from ambra_sdk.api import Api
    >>> api = Api.with_sid(url, sid)

Or, you can use your user credentials and `SDK` automatically get new sid for you:

.. doctest::

    >>> from ambra_sdk.api import Api
    >>> api = Api.with_creds(url, username, password)

Service API
-----------

This section describes the interaction of ambra-sdk with service api.
This api describes in  `Service API`_ document or in some other
ambra health instance `ambra_url/api/v3/api.html`.

.. _`Service API`: https://uat.dicomgrid.com/api/v3/api.html

At the footer of this document you can find current version sting.
Make sure the current version of `ambra-sdk` is not lower than the api version.

.. doctest::

   >>> from ambra_sdk import API_VERSION
   >>> print(API_VERSION)
   LBL0022 v38.0 2020-05-27

Service api is divided by type of command.
From `ambra-sdk` view all request have a form
`api.TypeOfCommand.command.{get() or all()}`.

Description of all existing methods and you can find in :ref:`Service API reference<referencies-service-api>`. 

Lets get some your user inforametion:

.. doctest::

    >>> from ambra_sdk.api import Api
    >>> api = Api.with_creds(url, username, password)
    >>> user_info = api.Session.user().get()
    >>> print(user_info.email)
    user@ambrahealth.com


You can access to some fields using `dot` notation:

.. doctest::

    >>> assert user_info['namespace_id'] == user_info.namespace_id

Now, lets get your permissions:

.. doctest::

    >>> namespace_id = user_info.namespace_id
    >>> permissions = api.Session \
    ...                  .permissions(
    ...                      namespace_id=namespace_id,
    ...                  ).get()

As you can see this is big dictionary.
Using `only` method, we can  request only some interesting fields:


.. doctest::

    >>> permissions = api.Session \
    ...                  .permissions(namespace_id=namespace_id) \
    ...  		 .only(['study_download', 'study_upload']) \
    ...                  .get()
    >>> assert permissions.to_dict() == {'study_download': 1, 'study_upload': 0}

In `ambra-sdk` we use `get()` method for get some results from api.
Usually this is some dict results. But some api methods return iterable data.
For get this kind of data we use `all()` of `first()` methods.
Lets get list of your accounts. This is iterable response:


.. doctest::

    >>> accounts = api.Account.list().all()

This is iterable object:

.. doctest::

    >>> for account in accounts:
    ...     account_name = account.name


Also, you can use slices:

.. doctest::

    >>> for account in accounts[5:12]:
    ...     account_name, account_uuid = (account.name, account.uuid)


Sometimes you need only first element:

.. doctest::

    >>> account = api.Account.list().first()
    >>> # Get second result
    >>> account = api.Account.list().all()[1:].first()

With `Ambra-SDK` you can use filtering (only for methods that support this):

.. doctest::

    >>> from ambra_sdk.service.filtering import Filter
    >>> from ambra_sdk.service.filtering import FilterCondition
    >>> 
    >>> account = api.Account \
    ...              .list() \
    ...              .filter_by(
    ...                  Filter(
    ...                      'name',
    ...                       FilterCondition.equals,
    ...                      account_name,
    ...                  )
    ...              ).first()
    >>> assert account.name == account_name 

Or you can use `models` system for do the same thing easy:

.. doctest::

    >>> from ambra_sdk.models import Account
    >>> 
    >>> account = api.Account \
    ...              .list() \
    ...              .filter_by(Account.name=='Some Account name') \
    ...              .first()


Set of existing models and fields you can find in :ref:`Models reference<referencies-models>`.

If you remember, we can use `only` method and combine it with filtering:

.. doctest::

    >>> account = api.Account \
    ...              .list() \
    ...              .only({'account': ['name']}) \
    ...              .filter_by(Account.name=='Some Account name') \
    ...              .first()


Using `models` for `only` can also simplify usage:

.. doctest::

    >>> account = api.Account \
    ...              .list() \
    ...              .only([Account.name, Account.uuid]) \
    ...              .filter_by(Account.name=='Some Account name') \
    ...              .first()

The next thing, what you can do is sorting.
Lets sort our accounts by name:

.. doctest::

    >>> from ambra_sdk.service.sorting import Sorter, SortingOrder
    >>> 
    >>> accounts = api.Account.list() \
    ...               .sort_by(Sorter('name', SortingOrder.ascending)) \
    ...               .all()[3:5]

You can use `models` for this case too:

.. doctest::

    >>> accounts = api.Account.list() \
    ...               .sort_by(Account.name.asc()) \
    ...               .all()[3:5]

You can combine filtering sorting and `only` methods as you wish.

Some of API methods have special parameters. For example, `study/add` have a `customfield-{UUID}` argument. For usage this arguments, you can execute `Study.add()` method with `customfield_param` argument, where `customfield_param` is a dict of {UUID: value}.


Storage API
-----------

This section describes ambra-sdk storage api part.
You can find this description in  `Storage API`_ document or in some other ambra health instance `api/v3/storage/storage_api.html`.

.. _`Storage API`: https://uat.dicomgrid.com/api/v3/storage/storage_api.html

At the footer of this document you can find current version sting.
Make sure the current version of `ambra-sdk` is not lower than the api version.

.. doctest::

    >>> from ambra_sdk import STORAGE_VERSION
    >>> print(STORAGE_VERSION)
    LBL0038 v9.0 2020-06-03


Description of all existing methods and you can find in :ref:`Storage API reference<referencies-storage-api>`. 

For accessing storage api commands you can use `api.Storage` namespace.

As in the server documentation in `ambra-sdk` all api requests to storage splitted on `Study` and `Image` commands.

For example, lets try to upload dicom file to your namespace.

First af all, you need get your `namespace_id` and `engine_fqdn`:

.. doctest::

    >>> user = api.User.get().get()
    >>> namespace_id = user.namespace_id
    >>> fqdn = api.Namespace.engine_fqdn(namespace_id=namespace_id).get()
    >>> engine_fqdn = fqdn.engine_fqdn

Now, lets upload dicom file to the storage:


.. doctest::
    :options: +SKIP

    >>> dicom_path = 'PATH_TO_DICOM'
    >>> with open(dicom_path, 'rb') as dicom_file:
    ...     uploaded_image = api.Storage.Image.upload(
    ...         engine_fqdn=fqdn.engine_fqdn,
    ...         namespace=namespace_id,
    ...         opened_file=dicom_file,
    ...     )
 


Addon methods
-------------

This section describes ambra-sdk addon namespace part.
Reference of all existing methods and you can find in :ref:`Addon reference<referencies-addon>`. 

Lets upload some `study` to storage.
First of all you need to upload dicoms to storage.
Than you should wait for study readiness in `v3services`.

Actually, it's a little more complicated..
You can use `api.Addon.Study.upload_and_get` method for doing this:

.. doctest::
    :options: +SKIP

    >>> from pathlib import Path
    >>> study_dir = Path('/path_to_study_dir')
    >>> 
    >>> new_study = api.Addon.Study.upload_and_get(
    ...     study_dir=study_dir,
    ...     namespace_id=user_info.namespace_id
    ... )
    >>> print(new_study.uuid)
