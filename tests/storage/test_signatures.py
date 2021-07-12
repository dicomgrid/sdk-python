from inspect import signature

from ambra_sdk.storage.image import AsyncImage, Image
from ambra_sdk.storage.image.base_image import BaseImage
from ambra_sdk.storage.study import AsyncStudy, Study
from ambra_sdk.storage.study.base_study import BaseStudy


def test_study_signatures():
    """Test study signatures."""
    for method in dir(Study):
        if method.startswith('_'):
            continue
        method_signature = signature(getattr(Study, method)).parameters
        base_signature = signature(getattr(BaseStudy, f'_{method}')).parameters

        specific_args = {'use_box', 'only_prepare'}

        cleared_signature = {
            i
            for i in method_signature if i not in specific_args
        }

        assert cleared_signature == set(
            base_signature,
        ), f'Method name {method}'


def test_async_study_signatures():
    """Test async study signatures."""
    for method in dir(AsyncStudy):
        if method.startswith('_'):
            continue
        method_signature = signature(getattr(AsyncStudy, method)).parameters
        base_signature = signature(getattr(BaseStudy, f'_{method}')).parameters

        specific_args = {'use_box', 'only_prepare'}

        cleared_signature = {
            i for i in method_signature if i not in specific_args
        }

        assert cleared_signature == set(
            base_signature,
        ), f'Method name {method}'


def test_image_signatures():
    """Test image signatures."""
    for method in dir(Image):
        if method.startswith('_'):
            continue
        method_signature = signature(getattr(Image, method)).parameters
        base_signature = signature(getattr(BaseImage, f'_{method}')).parameters

        specific_args = {'use_box', 'only_prepare'}

        cleared_signature = {
            i for i in method_signature if i not in specific_args
        }

        assert cleared_signature == set(
            base_signature,
        ), f'Method name {method}'


def test_async_image_signatures():
    """Test async image signatures."""
    for method in dir(AsyncImage):
        if method.startswith('_'):
            continue
        method_signature = signature(getattr(AsyncImage, method)).parameters
        base_signature = signature(getattr(BaseImage, f'_{method}')).parameters

        specific_args = {'use_box', 'only_prepare'}

        cleared_signature = {
            i for i in method_signature if i not in specific_args
        }

        assert cleared_signature == set(
            base_signature,
        ), f'Method name {method}'
