import msgpack_self


def in_and_out(target, expected, skip_value_compare=False):
    result = msgpack_self.encode(target)
    assert result.getvalue() == expected

    result_type, result_value = msgpack_self.decode_byte(result.getvalue())
    assert result_type == type(target)
    if not skip_value_compare:  # workaround for float
        assert result_value == target
