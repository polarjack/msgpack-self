import pytest

import msgpack_self

BASE = 'hello world!'
BASE_30 = BASE * 30
BASE_5500 = BASE * 5500


@pytest.mark.parametrize(
    'target, expected',
    [
        (bytearray(BASE.encode('utf-8')), b'\xc4\x0c' + BASE.encode('utf-8')),
        (bytearray(BASE_30.encode('utf-8')), b'\xc5\x01h' + BASE_30.encode('utf-8')),
        (
            bytearray(BASE_5500.encode('utf-8')),
            b'\xc6\x00\x01\x01\xd0' + BASE_5500.encode('utf-8'),
        ),
    ],
)
def test_bytes(target, expected):
    result = msgpack_self.encode(target)
    assert result.getvalue() == expected

    result_type, result_value = msgpack_self.decode_byte(expected)
    assert result_type == bytes
    assert result_value == target
