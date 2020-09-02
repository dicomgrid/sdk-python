FAQ
===

.. contents::
   :local:

How can I get the nth element of results in service api methods?
----------------------------------------------------------------

Use slices::

    # Get second result
    account = api.Account.list().all()[1:].first()


How can I execute a large number of queries?
--------------------------------------------

Today `ambra-sdk` does not support `bundled calls` where multiple queries can be run in one request. The following is possible, however:

This `gist <https://gist.github.com/dyens/488a9c0e2f150865e1658e393121bc52>`_ shows some example of using `bundled calls` api with multithreading

If `bundled calls` opportunity is important for you feel free to create an issue in `GitHub <https://github.com/dicomgrid/sdk-python/issue>`_.


What is the difference between :py:meth:`api.Study.duplicate` and :py:meth:`api.Addon.Study.duplicate_and_get` methods ?
------------------------------------------------------------------------------------------------------------------------

The first method is `AmbraHealth API` async method.
It gets your task and starts the study duplication in the background.

The second method creates a study duplication task and waits for a new duplicated study.
This is async method.
