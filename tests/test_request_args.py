from datetime import date, datetime

import pytest

from ambra_sdk.request_args import AioHTTPRequestArgs, RequestArgs


class TestRequestArgs:
    """Test request args."""

    @pytest.fixture
    def request_args(self):
        """Request args."""
        yield RequestArgs(
            method='GET',
            url='/some/url',
            full_url='/some/full/url',
            data={
                'd1': 1,
                'd2': 2,
            },
        )

    def test_dict_optional_args(self, request_args):
        """Test dict optional args.

        :param request_args: request args
        """
        args = request_args.dict_optional_args(
            autocast_arguments_to_string=False,
        )
        assert args['data'] == {'d1': 1, 'd2': 2}
        assert 'method' not in args
        assert 'url' not in args
        assert 'full_url' not in args

    def test_dict_optional_args_with_autocast(self, request_args):
        """Test dict optional args with autocast.

        :param request_args: request args
        """
        request_args.data = {
            'string': 'string',
            'int': 3,
            'none': None,
            'datetime': datetime(2000, 1, 2, 3, 4, 5),
            'date': date(2000, 1, 2),
            'list': ['a', 'b', 'c'],
            'dict': {
                'a': 1,
            },
        }
        args = request_args.dict_optional_args(
            autocast_arguments_to_string=True,
        )
        assert args['data'] == {
            'string': 'string',
            'int': 3,
            'none': None,
            'datetime': '2000-01-02 03:04:05',
            'date': '2000-01-02 00:00:00',
            'list': '["a", "b", "c"]',
            'dict': '{"a": 1}',
        }


class TestAioHTTPRequestArgs:
    """Test aiohttp request args."""

    @pytest.fixture
    def request_args(self):
        """Request args."""
        yield AioHTTPRequestArgs(
            method='GET',
            url='/some/url',
            full_url='/some/full/url',
            data={
                'd1': 1,
                'd2': 2,
            },
        )

    def test_dict_optional_args(self, request_args):
        """Test dict optional args.

        :param request_args: request args
        """
        args = request_args.dict_optional_args(
            autocast_arguments_to_string=False,
        )
        assert args['data'] == {'d1': 1, 'd2': 2}
        assert 'method' not in args
        assert 'url' not in args
        assert 'full_url' not in args

    def test_dict_optional_args_with_autocast(self, request_args):
        """Test dict optional args with autocast.

        :param request_args: request args
        """
        request_args.data = {
            'string': 'string',
            'int': 3,
            'none': None,
            'datetime': datetime(2000, 1, 2, 3, 4, 5),
            'date': date(2000, 1, 2),
            'list': ['a', 'b', 'c'],
            'dict': {
                'a': 1,
            },
        }
        args = request_args.dict_optional_args(
            autocast_arguments_to_string=True,
        )
        assert args['data'] == {
            'string': 'string',
            'int': 3,
            'none': None,
            'datetime': '2000-01-02 03:04:05',
            'date': '2000-01-02 00:00:00',
            'list': '["a", "b", "c"]',
            'dict': '{"a": 1}',
        }
