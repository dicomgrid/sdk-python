from ambra_sdk.service.filtering import Filter, FilterCondition
from ambra_sdk.service.sorting import Sorter, SortingOrder


class TestStudy:
    """Test Study."""

    def test_study_list(
        self,
        api,
        account,
        readonly_study,
    ):
        """Test study list."""
        studies = api \
            .Study \
            .list() \
            .set_rows_in_page(5000) \
            .filter_by(
                Filter(
                    'phi_namespace',
                    FilterCondition.equals,
                    account.account.namespace_id,
                ),
            ) \
            .all()
        assert len(list(studies)) == 1
        assert len(list(studies[:3])) == 1
        assert len(list(studies[1:4])) == 0  # NOQA:WPS507

    def test_study_list_only(self, api, account, readonly_study):
        """Test study list sorting."""
        studies = api \
            .Study \
            .list() \
            .filter_by(
                Filter(
                    'phi_namespace',
                    FilterCondition.equals,
                    account.account.namespace_id,
                ),
            ) \
            .only({'study': ['uuid']}) \
            .all()
        assert len(list(studies)) == 1
        study = studies.first()
        assert 'uuid' in study
        assert len(study) == 1

    def test_study_filtering(
        self,
        api,
        account,
        readonly_study,
        readonly_study2,
    ):
        """Test study list filtering."""
        # name in stady2
        patient_name = 'AAAA'
        filt = Filter(
            field_name='patient_name',
            condition=FilterCondition.equals,
            value=patient_name,
        )
        studies = api \
            .Study \
            .list() \
            .only({'study': ['patient_name']}) \
            .filter_by(
                Filter(
                    'phi_namespace',
                    FilterCondition.equals,
                    account.account.namespace_id,
                ),
            ) \
            .filter_by(filt) \
            .all()
        assert len(list(studies[:3])) == 1
        assert studies.first().patient_name == patient_name

    def test_study_sorting(
        self,
        api,
        account,
        readonly_study,
        readonly_study2,
    ):
        """Test study list sorting."""
        sorter = Sorter(
            field_name='patient_name',
            order=SortingOrder.ascending,
        )
        studies = api \
            .Study \
            .list() \
            .only({'study': ['uuid']}) \
            .filter_by(
                Filter(
                    'phi_namespace',
                    FilterCondition.equals,
                    account.account.namespace_id,
                ),
            ) \
            .sort_by(sorter) \
            .all()
        studies = [study.uuid for study in studies]

        r_sorter = Sorter(
            field_name='patient_name',
            order=SortingOrder.descending,
        )

        r_studies = api \
            .Study \
            .list() \
            .only({'study': ['uuid']}) \
            .filter_by(
                Filter(
                    'phi_namespace',
                    FilterCondition.equals,
                    account.account.namespace_id,
                ),
            ) \
            .sort_by(r_sorter) \
            .all()

        r_studies = [study.uuid for study in r_studies]
        assert list(reversed(studies)) == r_studies
