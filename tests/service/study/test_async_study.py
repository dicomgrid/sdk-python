import pytest

from ambra_sdk.service.filtering import Filter, FilterCondition
from ambra_sdk.service.sorting import Sorter, SortingOrder


@pytest.mark.asyncio
class TestAsyncStudy:
    """Test Study."""

    async def test_study_list(
        self,
        async_api,
        async_account,
        async_readonly_study,
    ):
        """Test study list."""
        query = async_api \
            .Study \
            .list() \
            .set_rows_in_page(5000) \
            .filter_by(
                Filter(
                    'phi_namespace',
                    FilterCondition.equals,
                    async_account.account.namespace_id,
                ),
            ) \
            .all()
        studies = []
        async for study in query:
            studies.append(study)
        assert len(studies) == 1

        studies = []
        async for study in query[:3]:  # NOQA:WPS440
            studies.append(study)
        assert len(studies) == 1

        studies = []
        async for study in query[1:4]:  # NOQA:WPS440
            studies.append(study)
        assert len(studies) == 0  # NOQA:WPS507

    async def test_study_list_only(
        self,
        async_api,
        async_account,
        async_readonly_study,
    ):
        """Test study list sorting."""
        studies_query = async_api \
            .Study \
            .list() \
            .filter_by(
                Filter(
                    'phi_namespace',
                    FilterCondition.equals,
                    async_account.account.namespace_id,
                ),
            ) \
            .only({'study': ['uuid']}) \
            .all()
        studies = []
        async for study_obj in studies_query:
            studies.append(study_obj)
        assert len(list(studies)) == 1
        study = await studies_query.first()
        assert 'uuid' in study
        assert len(study) == 1

    async def test_study_filtering(
        self,
        async_api,
        async_account,
        async_readonly_study,
        async_readonly_study2,
    ):
        """Test study list filtering."""
        # name in study2
        patient_name = 'AAAA'
        filt = Filter(
            field_name='patient_name',
            condition=FilterCondition.equals,
            value=patient_name,
        )
        studies_iterator = async_api \
            .Study \
            .list() \
            .only({'study': ['patient_name']}) \
            .filter_by(
                Filter(
                    'phi_namespace',
                    FilterCondition.equals,
                    async_account.account.namespace_id,
                ),
            ) \
            .filter_by(filt) \
            .all()
        studies = []
        async for study in studies_iterator[:3]:
            studies.append(study)
        assert len(study) == 1
        assert (await studies_iterator.first()).patient_name == patient_name

    async def test_study_sorting(
        self,
        async_api,
        async_account,
        async_readonly_study,
        async_readonly_study2,
    ):
        """Test study list sorting."""
        sorter = Sorter(
            field_name='patient_name',
            order=SortingOrder.ascending,
        )
        studies_geneartor = async_api \
            .Study \
            .list() \
            .only({'study': ['uuid']}) \
            .filter_by(
                Filter(
                    'phi_namespace',
                    FilterCondition.equals,
                    async_account.account.namespace_id,
                ),
            ) \
            .sort_by(sorter) \
            .all()
        studies = []
        async for study in studies_geneartor:
            studies.append(study.uuid)

        r_sorter = Sorter(
            field_name='patient_name',
            order=SortingOrder.descending,
        )

        r_studies_geneartor = async_api \
            .Study \
            .list() \
            .only({'study': ['uuid']}) \
            .filter_by(
                Filter(
                    'phi_namespace',
                    FilterCondition.equals,
                    async_account.account.namespace_id,
                ),
            ) \
            .sort_by(r_sorter) \
            .all()

        r_studies = []
        async for study in r_studies_geneartor:  # NOQA:WPS440
            r_studies.append(study.uuid)

        assert list(reversed(studies)) == r_studies

    async def test_study_list_get(
        self,
        async_api,
        async_account,
        async_readonly_study,
    ):
        """Test study list get."""
        get_result = await async_api \
            .Study \
            .list() \
            .set_rows_in_page(5000) \
            .filter_by(
                Filter(
                    'phi_namespace',
                    FilterCondition.equals,
                    async_account.account.namespace_id,
                ),
            ) \
            .get()
        assert 'more' in get_result
        assert 'studies' in get_result
        assert 'page' in get_result
