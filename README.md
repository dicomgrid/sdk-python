# Ambra-SDK

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPI version](https://badge.fury.io/py/ambra-sdk.svg)](https://badge.fury.io/py/ambra-sdk)



---

Welcome to ambra-sdk library for intract with ambrahealth service and storage api. 


## Quickstart

```bash
pip install ambra-sdk
```

## Running

```python
from ambra_sdk.api import Api
from ambra_sdk.models import Study
from ambra_sdk.service.filtering import Filter, FilterCondition
from ambra_sdk.service.sorting import Sorter, SortingOrder

api = Api.with_creds(url, username, password)
user_info = api.Session.user().get()

studies = api \
    .Study \
    .list() \
    .filter_by(
        Filter(
            'phi_namespace',
            FilterCondition.equals,
            user_info.namespace_id,
        ),
    ) \
    .only([Study.study_uid, Study.image_count]) \
    .sort_by(
        Sorter(
            'created',
            SortingOrder.ascending,
        ),
    ) \
    .all()

for study in studies:
    print(study.study_uid, study.image_count)
 
```

## License

Ambra-SDK is licensed under the terms of the Apache-2.0 License (see the file LICENSE).

## Read the docs

Documentation: https://dicomgrid.github.io/sdk-python/index.html
