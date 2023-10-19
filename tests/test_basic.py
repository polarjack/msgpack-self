import pytest

from .share import in_and_out


# None, True, False
@pytest.mark.parametrize(
    'target, expected',
    [
        (None, b'\xc0'),
        (True, b'\xc3'),
        (False, b'\xc2'),
    ],
)
def test_basic(target, expected):
    in_and_out(target, expected)


# int
@pytest.mark.parametrize(
    'target, expected',
    [
        (1, b'\x01'),
        (-2, b'\xfe'),
        (123, b'{'),
        (-15, b'\xf1'),
        (300, b'\xcd\x01,'),
        (-321, b'\xd1\xfe\xbf'),
        (65540, b'\xce\x00\x01\x00\x04'),
        (-32770, b'\xd2\xff\xff\x7f\xfe'),
        (4294967299, b'\xcf\x00\x00\x00\x01\x00\x00\x00\x03'),
        (-2147483650, b'\xd3\xff\xff\xff\xff\x7f\xff\xff\xfe'),
    ],
)
def test_int_family(target, expected):
    in_and_out(target, expected)


# float
@pytest.mark.parametrize(
    'target, expected',
    [
        (1.1, b'\xca?\x8c\xcc\xcd'),
        (-1.1, b'\xca\xbf\x8c\xcc\xcd'),
        (1234.1234, b'\xcaD\x9aC\xf3'),
        (-1234.1234, b'\xca\xc4\x9aC\xf3'),
    ],
)
def test_float_family(target, expected):
    in_and_out(target, expected, skip_value_compare=True)


# str
@pytest.mark.parametrize(
    'target, expected',
    [
        ('a', b'\xa1a'),
        ('hello world!', b'\xachello world!'),
        ('hello world!' * 3, b'\xd9$' + b'hello world!' * 3),
        ('hello world!' * 30, b'\xda\x01h' + b'hello world!' * 30),
        ('hello world!' * 5500, b'\xdb\x00\x01\x01\xd0' + b'hello world!' * 5500),
    ],
)
def test_str(target, expected):
    in_and_out(target, expected)


# list
@pytest.mark.parametrize(
    'target, expected',
    [
        ([1, 2, 3], b'\x93\x01\x02\x03'),
        ([1, 2, True], b'\x93\x01\x02\xc3'),
        ([1, 'a', True], b'\x93\x01\xa1a\xc3'),
    ],
)
def test_list(target, expected):
    in_and_out(target, expected)
