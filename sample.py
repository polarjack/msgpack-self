import msgpack_self

if __name__ == '__main__':
    target = {
        'a': 1,
        'b': True,
        'c': [1, 2, 3],
    }

    result = msgpack_self.encode(target)
    print(result.getvalue())

    result_type, result_value = msgpack_self.decode_byte(result.getvalue())
    print(result_type)
    print(result_value)
