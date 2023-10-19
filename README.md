# MsgPack Self Implementation

Msgpack Official [Spec](https://github.com/msgpack/msgpack/blob/master/spec.md)


- [MsgPack Self Implementation](#msgpack-self-implementation)
  - [Usage](#usage)
  - [Unit Test](#unit-test)
    - [Basic Type](#basic-type)
    - [int Family](#int-family)
    - [float Family](#float-family)
    - [str Family](#str-family)
    - [bin Family](#bin-family)
    - [list Family](#list-family)
    - [map Family](#map-family)


## Usage

recommend to use `virtualenv` to run this project
support python 3.9+

1. clone this repo
2. run the `sample.py`
```bash
python sample.py
```

`sample.py`
```python
import msgpack_self

if __name__ == "__main__":
    target = {
        "a": 1,
        "b": True,
        "c": [1, 2, 3],
    }

    result = msgpack_self.encode(target)
    print(result.getvalue()) # this is bytes

    result_type, result_value = msgpack_self.decode_byte(result.getvalue())
    print(result_type) # this is type
    print(result_value) # should be same as target
```

## Unit Test

- make sure you have `pytest` install, or you can install with `pip install pytest`
- Alternatively, you can use poetry to install the dev dependencies

```bash
poetry install
```

Run The Unit Test
```bash
pytest
```

### Basic Type

Parsing None, True, False [test_basic](./tests/test_basic.py#L16)

### int Family

Parsing int family include [test_int_family](./tests/test_basic.py#L35)

- positive fixint
- negative fixint
- int 8
- int 16
- int 32
- int 64
- uint 8
- uint 16
- uint 32
- uint 64

### float Family

Parsing float family include [test_float_family](./tests/test_basic.py#L49)

*NOTE: will skip value compare since float is not accurate*

### str Family

Parsing str family include [test_str_family](./tests/test_basic.py#L64)

- str length under 8
- str 8
- str 16
- str 32

### bin Family

Prasing bin family include [test_bin_family](./tests/test_bin.py#L18)
- bytes 8
- bytes 16
- bytes 32

### list Family

Parsing list family include [test_list_family](./tests/test_basic.py#L77)

- pure list with int
- list mix with int and str
- list mix with int, str, bool

### map Family

Parsing map (dict) family include [test_dict](./tests/test_dict.py#L69)

- basic dict
- dict with bool
- dict with int
- dict with str
- dict with list
- dict with item more than 15
- nested dict
