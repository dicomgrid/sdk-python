.. _service-api:

.. testsetup::

        from dynaconf import settings
	from ambra_sdk.api import Api
	url = settings.API['url']
	username = settings.API['username']
	password = settings.API['password']
	api = Api.with_creds(url, username, password)
	sid = 'SOME BAD SID'
	client_name = 'SOME_CLIENT_NAME'

Service API
-----------

This section describes the interaction with `AmbraHealth service API`_ .

At the footer of this document, the current version of the `AmbraHealth API` is specified.
Make sure that the current version of `ambra-sdk` is not lower.

.. doctest::

   >>> from ambra_sdk import API_VERSION
   >>> print(API_VERSION)
   LBL0022 v45.0 2021-04-07

In `ambra-sdk` all service api methods have the form
`api.CommandNamespace.command.{get(),all() or first()}`.

You can find a description of all existing methods in the :ref:`Service API reference<referencies-service-api>`.


Query objects
^^^^^^^^^^^^^

All `Service` methods returns `Query` object for preparing data request.
For example:

.. doctest::

    >>> query_object = api.Study.list()
    >>> print(type(query_object))
    <class 'ambra_sdk.service.query.QueryOPSF'>

`OSF` in query type name means that you can use `only`, `sort_by`, and `filter_by` methods. `P` means that this is a query for results with pagination. So you can use `all` or `first` method on this object.

Inspect your `query` object to get information about request::

  query_object.url
  query_object.full_url
  query_object.request_args

Execute this query using `first()` or `all()` method (`api.Study.list()` is query for request multiple results)::

  some_study = query_object.first()
  for study in query_object.all():
      do_somethingwith(study)

Another example is a query for requesting one result::

  study_get_query = api \
      .Study \
      .get(uuid=uuid)
 
For requesting study data using this query, we use `get()` method::

  some_study = study_get_query.get()

Only
^^^^

All `ambra-sdk` service api methods support the `only` method to limit the set of requested fields.
Using this method is slightly different for different types of requests.

For example, let's imagine that we are using a method for requesting only one Field in the result.
In this case, we pass to the :py:meth:`query.only` function to specify the required field or list of required fields::

  user_query = api.User.get().only(['email', 'name'])

  # for request only one field
  user_query = api.User.get().only('email')
  user = user_query.get()
  assert list(user.keys()) == ['email']

Another use case: When preparing a request to get multiple results, pass a dict in the :py:meth:`query.only` function where the key is the request object name and the value is a list of requested fields. For example::
 
  account_request = api.Account \
      .list() \
      .only({'account': ['name', 'uuid']})
  account = account_request.first()
  assert set(account.keys()) == set(['name', 'uuid'])

An easier way to do this is using models::

 from ambra_sdk.models import Account

 account_request = api.Account \
      .list() \
      .only([Account.name, Account.uuid])
  account = account_request.first()
  
  
Pagination
^^^^^^^^^^

When querying methods that return multiple results, `ambra-sdk` supports an automatic pagination of server requests.

Suppose we have a study list query::

  study_list_query = api.Study.list()

Then let's create study list iterator using the `all()` method::

  study_list_iterator = study_list_query.all()

In code::

  for study in study_list_iterator:
       do_something_with(study)

`study_list_iterator` requests the 100 studies from `AmbraHalth API`, yields the results in the loop, and then requests the next 100 results.

In the query level, one can change the number of rows in one pagination page::

  study_list_query = api.Study.list().set_rows_in_page(20)

Set a range of requested results: For example, to skip the first 5 results and take the next 10 items::

  for study in study_list_iterator \
      .set_range(min_row=5, max_row=15):
      do_something_with(study)

Slices can also be used to achieve the same result::

  for study in study_list_iterator[5:15]:
      do_something_with(study)

.. note::

   At this moment, `ambra-sdk` does not support stepping or reverse stepping through multiple results::

     # This code is invalid
     for study in study_list_iterator[5:15:2]:
          do_something_with(study)


Sorting
^^^^^^^

Some service api methods in `ambra-sdk` support sorting: To top sort, pass `Sorter` object to `sort_by` query method::
  
  from ambra_sdk.service.sorting import Sorter, SortingOrder

  sorter = Sorter(
      field_name='patient_name',
      order=SortingOrder.ascending,
  )
  study_query = api \
      .Study \
      .list() \
      .sort_by(sorter)

Using models::

  from ambra_sdk.models import Study

  study_query = api \
      .Study \
      .list() \
      .sort_by(Study.patient_name.asc())

Filtering
^^^^^^^^^

Some service api methods in `ambra-sdk` support filtering.
To filter results, pass `Filter` object to `filter_by` query method::

  from ambra_sdk.service.filtering import Filter
  from ambra_sdk.service.filtering import FilterCondition
  
  account_name = 'SOME_ACCOUNT_NAME'
  account = api.Account \
               .list() \
               .filter_by(
                   Filter(
                       'name',
                        FilterCondition.equals,
                       account_name,
                   )
               ).first()
  assert account.name == account_name 


Using `models`::

  from ambra_sdk.models import Account

  account = api.Account \
               .list() \
               .filter_by(Account.name==account_name) \
               .first()


Special arguments (customfields)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some of `AmbraHealth API` methods accept special parameters.

For example, `add a method in the study namespace`_ has a `customfield-{UUID}` argument.
To use this argument, execute `Study.add()` method with `customfield_param` argument, where `customfield_param` is a dict of {UUID: value}::

  api.Study.add(
      ...,
      customfield_param={
          customfield_uid1: customfield_value1,
          customfield_uid2: customfield_value2,
      },
  )

Study customfields filtering
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

:py:meth:`api.Study.get` and :py:meth:`api.Study.list` methods return study data.
If a given study has `customfields` attributes, one can use filtering to retrieve specific fields. For example::

  study = api \
      .Study \
      .get(uuid=uuid) \
      .get()
  
  # Or
  
  study = api \
      .Study \
      .list() \
      .first()
  
  filtered_customfields = study \
      .customfields \
      .filter_by({'name': 'some_name'})
  
  for customfield in filtered_customfields:
      print(customfield)


Use `get_by_name` or `get_by_uuid` functions to get only the first filtered result::

  customfield = study.customfields.get_by_name('some_name')
  customfield = study.customfields.get_by_uuid('some_uuid')


Retries
^^^^^^^

`SDK` service namespace supports a retry mechanism.
By default, `ambra-sdk` sets specific retry settings.
In some cases, one can define custom settings for specific methods.
The example below shows how to do this::

  from requests.adapters import HTTPAdapter
  from requests.packages.urllib3.util import Retry
  
  max_retries = Retry(
      total=10,
      backoff_factor=0.2,
      method_whitelist=['GET', 'POST'],
   )
  
  adapter = HTTPAdapter(max_retries=max_retries)
  
  some_method_url = api.Study.list().full_url
  api.service_session.mount(some_method_url, adapter)


Headers
^^^^^^^

You can setup some default headers for service session
(using `service_default_headers` property) or for both service and storage sesssions
(using `default_headers` property)::

  api.default_headers['Golbal-header'] = 'value'
  api.service_default_headers['Service-pecific-header'] = 'value'

You can setup headers for some special requests::

  query = api.User.get()
  query.request_args.headers = {'Special-request-header': 'value'}
  user = query.get()

For setup headers for login call (get new sid) you can use `special_headers_for_login`::

  api = Api.with_creds(
      url,
      username,
      password,
      special_headers_for_login = {
          'Special-header-for-login': 'value',
      },
  )

 

.. _`add a method in the study namespace`: https://uat.dicomgrid.com/api/v3/api.html#study_add

.. _`AmbraHealth service API`: https://uat.dicomgrid.com/api/v3/api.html
