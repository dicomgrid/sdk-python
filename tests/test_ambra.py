from ambra_sdk import API_VERSION, MODELS_VERSION, STORAGE_VERSION


def test_api_version():
    assert API_VERSION == 'LBL0022 v37.0 2020-04-15'


def test_models_version():
    assert MODELS_VERSION == 'LBL0022 v37.0 2020-04-15'


def test_storage_version():
    assert STORAGE_VERSION == 'LBL0038 v8.0 2019-07-17'
