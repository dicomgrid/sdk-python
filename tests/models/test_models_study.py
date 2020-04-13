from ambra_sdk.models import Study
from ambra_sdk.service.filtering import Filter, FilterCondition


class TestModelsStudyFilteringSorting:
    """Test Study model.

    Test filtering and sorting.
    """

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
        studies = api \
            .Study \
            .list() \
            .filter_by(Study.patient_name == patient_name) \
            .filter_by(
                Filter(
                    'phi_namespace',
                    FilterCondition.equals,
                    account.account.namespace_id,
                ),
            ) \
            .only({'study': ['patient_name']}) \
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
            .sort_by(Study.patient_name.asc()) \
            .all()
        studies = [study.uuid for study in studies]

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
            .sort_by(Study.patient_name.desc()) \
            .all()

        r_studies = [study.uuid for study in r_studies]
        assert list(reversed(studies)) == r_studies


# this tests not in TestModelsStudyFilteringSorting bacause
# readonly fixture created for one class.
# so in next tests we would 2 study

class TestModelsStudyOnly:
    """Test Study model.

    Test only behaviour.
    """

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
            .only(Study.uuid) \
            .all()
        assert len(list(studies)) == 1
        study = studies.first()
        assert 'uuid' in study
        assert len(study) == 1

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
            .only(
                [
                    Study.uuid,
                    Study.patient_name,
                ],
            ) \
            .all()
        assert len(list(studies)) == 1
        study = studies.first()
        assert 'uuid' in study
        assert 'patient_name' in study
        assert len(study) == 2
