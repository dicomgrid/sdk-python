import pytest

from ambra_sdk.models.base import FK, BaseModel
from ambra_sdk.models.fields import Integer
from ambra_sdk.service.filtering import Filter, FilterCondition
from ambra_sdk.service.sorting import Sorter, SortingOrder


class TestBaseModel:
    """Test Base model and fields."""

    @pytest.fixture
    def models(self):
        """Two models fixture."""
        class A(BaseModel):
            f = Integer(description='This is field')

            def __init__(self, *, f=None):
                self.f = f  # NOQA WPS601

        class B(BaseModel):
            a = FK('A', description='This is A model')

            def __init__(self, *, a=None):
                self.a = a  # NOQA WPS601

        B.__dict__['a']._from_model = A  # NOQA:WPS609
        B.__dict__['a']._parent = B  # NOQA:WPS609
        return A, B

    def test_base_model_parent(self, models):
        """Test model parent."""
        A, B = models
        assert A.f._parent == A

    def test_field_name(self, models):
        """Test field name."""
        A, B = models
        assert A.f._name == 'f'

    def test_full_name(self, models):
        """Test full name."""
        A, B = models
        assert B.a.f._full_name == 'B.a.f'

    def test_base_model_descriptor(self, models):
        """Test full name."""
        A, B = models
        instance = A(f=3)
        assert instance.f == 3

    def test_fk(self, models):
        """Test fk."""
        A, B = models
        assert B.a._name == 'a'
        assert B.a._parent == B
        # New instance of model
        assert B.a.f._parent != A
        assert B.a.f._parent.__name__ == 'A'

    def test_fk_descriptor(self, models):
        """Test fk descriptor."""
        A, B = models
        a = A(f=3)
        b = B(a=a)
        assert b.a.f == 3

    def test_fk_descriptor_validate(self, models):
        """Test fk descriptor validation."""
        A, B = models
        with pytest.raises(ValueError):
            a = A(f='test')

        with pytest.raises(ValueError):
            B(a=3)

        a = A(f=3)
        b = B(a=a)
        assert b.a.f == 3

        b.a.f = 4
        assert b.a.f == 4

        with pytest.raises(ValueError):
            a.f = 'test'

        with pytest.raises(ValueError):
            b.a = 'test'

        with pytest.raises(ValueError):
            b.a.f = 'test'

    def test_standart_filtering(self, models):
        """Test standart filtering."""
        A, B = models

        assert B.a.f.equals(10, full_name=True) == Filter(
            field_name='B.a.f',
            condition=FilterCondition.equals,
            value=10,
        )
        assert B.a.f.equals_or_null(10, full_name=True) == Filter(
            field_name='B.a.f',
            condition=FilterCondition.equals_or_null,
            value=10,
        )

        assert B.a.f.not_equals(10, full_name=True) == Filter(
            field_name='B.a.f',
            condition=FilterCondition.not_equals,
            value=10,
        )
        assert B.a.f.gt(10, full_name=True) == Filter(
            field_name='B.a.f',
            condition=FilterCondition.gt,
            value=10,
        )

        assert B.a.f.ge(10, full_name=True) == Filter(
            field_name='B.a.f',
            condition=FilterCondition.ge,
            value=10,
        )

        assert B.a.f.lt(10, full_name=True) == Filter(
            field_name='B.a.f',
            condition=FilterCondition.lt,
            value=10,
        )

        assert B.a.f.le(10, full_name=True) == Filter(
            field_name='B.a.f',
            condition=FilterCondition.le,
            value=10,
        )

    def test_filter_with_seq(self, models):
        """Test seq filtering."""
        A, B = models
        assert B.a.f.in_condition([1, 2], full_name=True) == Filter(
            field_name='B.a.f',
            condition=FilterCondition.in_condition,
            value='[1, 2]',
        )
        assert B.a.f.in_or_null([1, 2], full_name=True) == Filter(
            field_name='B.a.f',
            condition=FilterCondition.in_or_null,
            value='[1, 2]',
        )

    def test_filter_with_seq_validation(self, models):
        """Test seq filtering validation."""
        A, B = models
        with pytest.raises(ValueError):
            B.a.f.in_condition(1)

    def test_filtering_short_name(self, models):
        """Test filtering short name."""
        A, B = models
        assert B.a.f.equals(10, full_name=False) == Filter(
            field_name='f',
            condition=FilterCondition.equals,
            value=10,
        )

    def test_filtering_validation(self, models):
        """Test filtering validation."""
        A, B = models
        with pytest.raises(ValueError):
            B.a.f.equals('test')

    def test_filtering_magic(self, models):
        """Test filtering magic."""
        A, B = models

        assert (B.a.f == 10) == Filter(  # NOQA: WPS309
            field_name='f',
            condition=FilterCondition.equals,
            value=10,
        )

        assert (B.a.f != 10) == Filter(  # NOQA: WPS309
            field_name='f',
            condition=FilterCondition.not_equals,
            value=10,
        )

        assert (B.a.f > 10) == Filter(  # NOQA: WPS309
            field_name='f',
            condition=FilterCondition.gt,
            value=10,
        )
        assert (B.a.f >= 10) == Filter(  # NOQA: WPS309
            field_name='f',
            condition=FilterCondition.ge,
            value=10,
        )

        assert (B.a.f < 10) == Filter(  # NOQA: WPS309
            field_name='f',
            condition=FilterCondition.lt,
            value=10,
        )

        assert (B.a.f <= 10) == Filter(  # NOQA: WPS309
            field_name='f',
            condition=FilterCondition.le,
            value=10,
        )

    def test_sorter(self, models):
        """Test sorter."""
        A, B = models

        assert B.a.f.asc(full_name=True) == Sorter(
            field_name='B.a.f',
            order=SortingOrder.ascending,
        )

        assert B.a.f.desc(full_name=True) == Sorter(
            field_name='B.a.f',
            order=SortingOrder.descending,
        )

        assert B.a.f.asc() == Sorter(
            field_name='f',
            order=SortingOrder.ascending,
        )
