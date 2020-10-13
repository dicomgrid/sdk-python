from ambra_sdk import API_VERSION, MODELS_VERSION, STORAGE_VERSION


def test_api_version():
    assert API_VERSION == 'LBL0022 v41.0 2020-10-07'


def test_models_version():
    assert MODELS_VERSION == 'LBL0022 v41.0 2020-10-07'


def test_storage_version():
    assert STORAGE_VERSION == 'LBL0038 v11.0 2020-10-07'
