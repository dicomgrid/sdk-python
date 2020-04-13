
class TestStorageStudy:
    """Test Study namespace of Storage api."""

    def test_schema(self, api, readonly_study):
        """Test schema method."""
        engine_fqdn = readonly_study.engine_fqdn
        storage_namespace = readonly_study.storage_namespace
        study_uid = readonly_study.study_uid

        st = api.Storage.Study.schema(
            engine_fqdn=engine_fqdn,
            namespace=storage_namespace,
            study_uid=study_uid,
        )
        assert st
