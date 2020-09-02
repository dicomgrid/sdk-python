.. _quick-start:

.. testsetup::

        from dynaconf import settings
	url = settings.API['url']
	username = settings.API['username']
	password = settings.API['password']
	sid = 'SOME BAD SID'
	client_name = 'SOME_CLIENT_NAME'


Quick Start
===========

This page gives an introduction on how to get started with the `ambra-sdk` library.
First, make sure that `ambra-sdk` is installed and up-to-date.
Let’s get started with some simple examples.


Init API
--------

Begin by importing the `ambra-sdk` module::

  from ambra_sdk.api import Api

To use `ambra-sdk` one needs to know the `url` of `AmbraHealth API` and `SID`.

::

  api = Api.with_sid(url, sid)  # Init API with sid

Another option is to use user credentials (`username` and `password`) and `ambra-sdk` takes care of using  the `sid` for the session::

  api = Api.with_creds(url, username, password)
  
`client_name` to `ambra-sdk` constructors can be used.
This value will be added to the `SDK` request headers.
Thus, `AmbraHealth` will be able to understand and log who exactly is making requests to help troubleshoot issues.

::

  api = Api.with_creds(url, username, password, client_name)


Service API
-----------

All `ambra-sdk` service API methods are described in the `AmbraHealth Service API`_ document and all of them are divided by namespaces.
In `ambra-sdk` we have the same separation of methods by namespaces.


All methods in `AmbraHealth service API` can be divided on two groups:

- Methods with one result
- Methods with multiple results

In order to deal with the first group, use `get()` method for getting results from a prepared request.
Alternatively, multiple results can be retrieved by using `first()` or `all()` methods to get the first row of results or getting an iterator over all results.

For example, let's request your user information.
This is `user method in session namespace`_, so we should use an `api.Session.user` method of `ambra-sdk`.

This is a simple method with only one result, so for fetching data from the service,  use the `get()` method::

    from ambra_sdk.api import Api
    api = Api.with_creds(url, username, password)
    user_info = api.Session.user().get()
    print(user_info.email)

Let's look at another example where we are using methods that return multiple results.
One of these methods is the `account list method`_.

Let's get a first object in results::

  account = api.Account.list().first()

`all()` method returns an iterator over all elements::

  # Get all accounts
  accounts = api.Account.list().all()

One can use slices for skipping and taking some number of results::

  # Get 7 results after skipping the first 5 rows.
  accounts = api.Account.list().all()[5:12]

Now, iterate over all accounts::

  for account in accounts:
      account_name = account.name

.. note::

   *ambra-sdk* `all()` method returns a lazy iterator.
   It means that we request new data from `AmbraHealth API` only when we actually need it.



Storage API
-----------

All `ambra-sdk` storage API methods are described in the `AmbraHealth Storage API`_ document .

As in the server documentation in `ambra-sdk`, all api requests to storage are divided into `Study` and `Image` namespaces.

For accessing storage api methods, use the  ambra-sdk `api.Storage` namespace.

For example, let's try to upload a `dicom` file to your user namespace.

Let’s get your user `namespace_id` and `engine_fqdn` using `ambra-sdk` service api `User.get` and `Namespaces.engine_fqdn` methods::

  user = api.User.get().get()
  namespace_id = user.namespace_id
  fqdn = api.Namespace.engine_fqdn(namespace_id=namespace_id).get()
  engine_fqdn = fqdn.engine_fqdn

Then, upload `dicom` file to the storage::

  dicom_path = 'PATH_TO_DICOM'
  with open(dicom_path, 'rb') as dicom_file:
      uploaded_image = api.Storage.Image.upload(
          engine_fqdn=fqdn.engine_fqdn,
          namespace=namespace_id,
          opened_file=dicom_file,
      )
 
.. note::

   Unlike service API methods, storage methods do not use `get()`, `first()` or `all()`.


Addon methods
-------------

All service and storage api methods are  described in the `AmbraHealth` specification documents.
In `ambra-sdk`, all methods outside of this specifications are placed in the `Addon` namespace.

For example, one common task is to upload a new study in `AmbraHealth`, upload `dicom` files to storage, and wait for a new study object in service.
Use `api.Addon.Study.upload_and_get` method::

  from pathlib import Path
  study_dir = Path('/path_to_study_dir')
  
  new_study = api.Addon.Study.upload_and_get(
      study_dir=study_dir,
      namespace_id=user_info.namespace_id
  )


.. _`AmbraHealth service API`: https://uat.dicomgrid.com/api/v3/api.html
.. _`AmbraHealth storage API`: https://uat.dicomgrid.com/api/v3/storage/storage_api.html
.. _`user method in session namespace`: https://uat.dicomgrid.com/api/v3/api.html#session_user
.. _`account list method`: https://uat.dicomgrid.com/api/v3/api.html#account_list
