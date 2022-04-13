.. _async:

Async
=====

``SDK`` has an async version (support asyncio mechanism in python).
For using Async version of SDK you need import::

  from ambra_sdk.api import AsyncApi
  api = AsyncApi.with_creds(...)

For example service `api.User.get` can be performed::

  user = await api.User.get().only(['email', 'name']).get()

We support async versions for all methods in the sync version of sdk (include addon methods).



Async vs Sync difference
------------------------

- In the async version for results with pagination we have an async generator result.
  For example::

    async for study in api.Study.list().all():
        print(study)


  This is pretty the same like in sync version, but now you can not to do something like this::

     studies = list(api.Study.list().all())

- In the async version we have `aiohttp.ClientResponse` instead of `requests.Response` object. There are some differences between this::

    # Sync:
    anonymize_response = api.Storage.Study.anonymize(
        engine_fqdn=engine_fqdn,
        namespace=storage_namespace,
        to_namespace=storage_namespace,
        study_uid=study_uid,
        region=region,
        color='121197149',
    )
    response_status_code = anonymize_response.status_code
    new_study_uid = anonymize_response.text

    # Async:
    anonymize_response = await api.Storage.Study.anonymize(
        engine_fqdn=engine_fqdn,
        namespace=storage_namespace,
        to_namespace=storage_namespace,
        study_uid=study_uid,
        region=region,
        color='121197149',
    )

    # respone.status_code -> response.status
    response_status_code = anonymize_response.status

    # response.text now is coroutine
    new_study_uid = await anonymize_response.text()


- Api has no `sid` property. For get SDK sid use this::

    sid = await api.get_sid()
