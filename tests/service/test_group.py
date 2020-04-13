
class TestGroup:
    """Test Group."""

    def test_create_group_fixture(
        self,
        create_group,
    ):
        """Test create group fixture."""
        group_name = 'my_sdk_group'
        group = create_group(group_name)
        assert group.namespace_id
        assert group.uuid
        assert group.name == group_name
