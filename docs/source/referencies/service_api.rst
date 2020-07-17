.. _referencies-service-api:

Service namespace
-----------------

.. testsetup::

        from dynaconf import settings
	from ambra_sdk.api import Api
	class Account:
	    namespace_id = 3
	account = Account()
	url = settings.API['url']
	username = settings.API['username']
	password = settings.API['password']
	api = Api.with_creds(url, username, password)



This entrypoints for using service API methods.

Query objects
^^^^^^^^^^^^^


All `Service` methods returns `Query` object for preparing request data.
For example:

.. doctest::

    >>> print(type(api.Study.list()))
    <class 'ambra_sdk.service.query.QueryOPSF'>

`OSF` in query name means that you can use `only`, `sort_by`, `filter_by` methods. `P` means that this is a query for results with pagination. So you can use `all` or `first` method on this object.

Full usage example:

.. doctest::

    >>> from ambra_sdk.models import Study
    >>> 
    >>> studies_query = api \
    ...     .Study \
    ...     .list() \
    ...     .only([Study.uuid, Study.patient_name, Study.created]) \
    ...     .filter_by(Study.phi_namespace == account.namespace_id) \
    ...     .sort_by(Study.patient_name.asc())
    >>> 
    >>> studies = studies_query.all()
    >>> 
    >>> for study in studies:
    ...     study.patient_name
    >>> 

Query object have `full_url`, `url` and `request_data` attributes:

.. doctest::

    >>> full_url = studies_query.full_url
    >>> request_data = studies_query.request_data
    >>> url = studies_query.url

This data can be very useful in some cases.


Retries
^^^^^^^

`SDK` service namespace supports retry mechanism. By default, `sdk` sets some retry settings.
In some cases, you may need to define your settings for some methods.
The example below shows how to do this:


.. doctest::

    >>> from requests.adapters import HTTPAdapter
    >>> from requests.packages.urllib3.util import Retry
    >>> 
    >>> max_retries = Retry(
    ...     total=10,
    ...     backoff_factor=0.2,
    ...     method_whitelist=['GET', 'POST'],
    ...  )
    >>> 
    >>> adapter = HTTPAdapter(max_retries=max_retries)
    >>> 
    >>> some_method_url = api.Study.list().full_url
    >>> api.service_session.mount(some_method_url, adapter)


Study customfields filtering
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`api.Study.get` and `api.Study.list` methods returns study data. If study have `customfields` attribute you can use filtering on it. For example:

.. doctest::
    :options: +SKIP

    >>> study = api \
    ...     .Study \
    ...     .get(uuid=uuid) \
    ...     .get()
    >>> 
    >>> # Or
    >>> 
    >>> study = api \
    ...     .Study \
    ...     .list() \
    ...     .first()
    >>> 
    >>> filtered_customfields = study \
    ...     .customfields \
    ...     .filter_by({'name': 'some_name'})
    >>> 
    >>> for customfield in filtered_customfields:
    ...     print(customfield)

You can use `get_by_name` or `get_by_uuid` functions for get only first filtered result.

.. doctest::
    :options: +SKIP

    >>> customfield = study.customfields.get_by_name('some_name')
    >>> customfield = study.customfields.get_by_uuid('some_uuid')


.. automodule:: ambra_sdk.service.entrypoints
   :members:
   :undoc-members:
   :inherited-members:
