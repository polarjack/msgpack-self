import pytest

from .share import in_and_out


# dictionary
@pytest.mark.parametrize(
    ['target', 'expected'],
    argvalues=[
        pytest.param(
            {'a': 1, 'b': 2},
            b'\x82\xa1a\x01\xa1b\x02',
            id='simple dict',
        ),
        pytest.param(
            {'a': 1, 'b': True},
            b'\x82\xa1a\x01\xa1b\xc3',
            id='dict with bool',
        ),
        pytest.param(
            {'a': 1, 'b': 'hello world'},
            b'\x82\xa1a\x01\xa1b\xabhello world',
            id='dict with str',
        ),
        pytest.param(
            {'a': 1, 'b': [1, 2, 3]},
            b'\x82\xa1a\x01\xa1b\x93\x01\x02\x03',
            id='dict with list',
        ),
        pytest.param(
            {'a': 1, 'long_key_name': 'long_value'},
            b'\x82\xa1a\x01\xadlong_key_name\xaalong_value',
            id='dict with long key name',
        ),
        pytest.param(
            {
                'a': 97,
                'b': 98,
                'c': 99,
                'd': 100,
                'e': 101,
                'f': 102,
                'g': 103,
                'h': 104,
                'i': 105,
                'j': 106,
                'k': 107,
                'l': 108,
                'm': 109,
                'n': 110,
                'o': 111,
                'p': 112,
                'q': 113,
                'r': 114,
                's': 115,
                't': 116,
                'u': 117,
                'v': 118,
                'w': 119,
                'x': 120,
                'y': 121,
                'z': 122,
            },
            b'\xde\x00\x1a\xa1aa\xa1bb\xa1cc\xa1dd\xa1ee\xa1ff\xa1gg\xa1hh\xa1ii\xa1jj\xa1kk\xa1ll\xa1mm\xa1nn\xa1oo\xa1pp\xa1qq\xa1rr\xa1ss\xa1tt\xa1uu\xa1vv\xa1ww\xa1xx\xa1yy\xa1zz',
            id='dict with item more than 15',
        ),
        pytest.param(
            {'a': 1, 'b': {'c': 2, 'd': 3}},
            b'\x82\xa1a\x01\xa1b\x82\xa1c\x02\xa1d\x03',
            id='nested dict',
        ),
    ],
)
def test_dict(target, expected):
    in_and_out(target, expected)
