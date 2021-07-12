import pytest


class TestCustomCode:
    """Test custom code methods."""

    @pytest.fixture
    def custom_code(self, api, account):
        """Custom code fixture."""
        query = api.Customcode.add(
            account_id=account.account.uuid,
            code='test_code',
            language='PYTHON',
            name='test_custome_code',
            type='AI_CUSTOM_VALIDATION_CODE',
            zip=b'some_zip',
        )
        # TODO: remove after fixing v3services api
        # account_id argument not in CustomCode.add function
        query.request_args.data['account_id'] = account.account.uuid
        custom_code_uuid = query.get().uuid
        yield custom_code_uuid
        api.Customcode.delete(uuid=custom_code_uuid).get()

    def test_zip(self, api, custom_code):
        """Test zip.

        This method return response instead of json box object
        """
        zip_response = api.Customcode.zip(uuid=custom_code).get()
        assert zip_response.headers['Content-Type'] == \
            'application/zip; charset=ISO-8859-1'
        assert zip_response.content
