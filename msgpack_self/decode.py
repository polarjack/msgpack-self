import io
import struct

from .float_ieee import ieee_754_32bit_to_float, ieee_754_64bit_to_float

TYPE_NONE_BIN = 0b11000000
TYPE_FALSE_BIN = 0b11000010
TYPE_TRUE_BIN = 0b11000011
TYPE_FLOAT_BIN = 0b11001010
TYPE_STR_BIN = 0b10100000
TYPE_STR_BIN_MASK = 0b10100000

TYPE_POSITIVE_FIXINT_BIN = 0b00000000
TYPE_POSITIVE_FIXINT_BIN_MASK = 0b10000000

TYPE_NEGATIVE_FIXINT_BIN = 0b11100000
TYPE_NEGATIVE_FIXINT_BIN_MASK = 0b11100000

TYPE_LIST_BIN = 0b10010000
TYPE_LIST_BIN_MASK = 0b11110000
TYPE_DICT_BIN = 0b10000000
TYPE_DICT_BIN_MASK = 0b11110000


class Decoder:
    def __init__(
        self,
    ):
        self.result = io.BytesIO()
        self.target = b'\xc0'  # None

    def _byte_to_int(self, byte) -> int:
        # convert to binary
        byte = ''.join(f'{byte:08b}' for byte in byte)
        # convert to int
        return int(byte, 2)

    def _fetch_byte(self, length=1):
        output = self.target[:length]
        self.target = self.target[length:]

        return output

    def _parse_int(self, length):
        int_byte = self._fetch_byte(length=length)
        # convert to binary
        int_bin = ''.join(f'{byte:08b}' for byte in int_byte)
        # convert to int
        return int(int_bin, 2)

    def _parse_list(self, length):
        output = []
        for i in range(length):
            _, result_value = self._parse()
            output.append(result_value)

        return output

    def _parse_dict(self, length):
        output = {}
        for i in range(length):
            key_type, key_value = self._parse()
            value_type, value_value = self._parse()
            output[key_value] = value_value

        return output

    def _parse(self):
        # first byte
        s = self._fetch_byte(length=1)

        # conver first byte to binary
        s_bin = ''.join(f'{byte:08b}' for byte in s)
        s_bin = int(s_bin, 2)

        # type parsing
        if s == b'\xc0':
            return type(None), None
        elif s == b'\xc2':
            return bool, False
        elif s == b'\xc3':
            return bool, True

        if not s_bin & TYPE_POSITIVE_FIXINT_BIN_MASK:
            return int, struct.unpack('B', s)[0]

        if s_bin & TYPE_NEGATIVE_FIXINT_BIN_MASK == TYPE_NEGATIVE_FIXINT_BIN_MASK:
            return int, struct.unpack('b', s)[0]

        if s == b'\xd0':
            target_byte = self._fetch_byte(length=1)
            return int, struct.unpack('>b', target_byte)[0]
        elif s == b'\xd1':
            target_byte = self._fetch_byte(length=2)
            return int, struct.unpack('>h', target_byte)[0]
        elif s == b'\xd2':
            target_byte = self._fetch_byte(length=4)
            return int, struct.unpack('>i', target_byte)[0]
        elif s == b'\xd3':
            target_byte = self._fetch_byte(length=8)
            return int, struct.unpack('>q', target_byte)[0]

        if s == b'\xcc':
            return int, struct.unpack('>B', self._fetch_byte(length=1))[0]
        elif s == b'\xcd':
            return int, struct.unpack('>H', self._fetch_byte(length=2))[0]
        elif s == b'\xce':
            return int, struct.unpack('>I', self._fetch_byte(length=4))[0]
        elif s == b'\xcf':
            return int, struct.unpack('>Q', self._fetch_byte(length=8))[0]

        # float parsing
        if s == b'\xca':  # float 32
            result = self._fetch_byte(length=4)
            # convert to binary
            result = ''.join(f'{byte:08b}' for byte in result)
            # convert to float
            result = ieee_754_32bit_to_float(result)
            return float, result
        elif s == b'\xcb':  # double
            result = self._fetch_byte(length=8)
            # convert to binary
            result = ''.join(f'{byte:08b}' for byte in result)
            # convert to float
            result = ieee_754_64bit_to_float(result)
            return float, result

        # str parsing
        if s_bin & TYPE_STR_BIN == TYPE_STR_BIN:
            length = s_bin - 0b10100000
            return str, self._fetch_byte(length=length).decode('utf-8')
        elif s == b'\xd9':  # str 8
            length = self._fetch_byte(length=1)
            return str, self._fetch_byte(length=self._byte_to_int(length)).decode(
                'utf-8'
            )
        elif s == b'\xda':  # str 16
            length = self._fetch_byte(length=2)
            return str, self._fetch_byte(length=self._byte_to_int(length)).decode(
                'utf-8'
            )
        elif s == b'\xdb':  # str 32
            length = self._fetch_byte(length=4)
            return str, self._fetch_byte(length=self._byte_to_int(length)).decode(
                'utf-8'
            )

        # list parsing
        if s_bin & TYPE_LIST_BIN_MASK == TYPE_LIST_BIN:
            length = s_bin - 0b10010000
            return list, self._parse_list(length)
        elif s == b'\xdc':  # list 16
            length = self._fetch_byte(length=2)
            return list, self._parse_list(length)
        elif s == b'\xdd':  # list 32
            length = self._fetch_byte(length=4)
            return list, self._parse_list(length)

        # dict parsing
        if s_bin & TYPE_DICT_BIN_MASK == TYPE_DICT_BIN:
            length = s_bin - 0b10000000
            return dict, self._parse_dict(length=length)
        elif s == b'\xde':  # dict 16
            length = self._fetch_byte(length=2)
            length = struct.unpack('>H', length)[0]
            return dict, self._parse_dict(length=length)
        elif s == b'\xdf':  # dict 32
            length = self._fetch_byte(length=4)
            length = struct.unpack('>I', length)[0]
            return dict, self._fetch_byte(length=length)

        # bin parsing
        if s == b'\xc4':  # bin 8
            length = self._fetch_byte(length=1)
            return bytes, self._fetch_byte(length=length)
        elif s == b'\xc5':  # bin 16
            length = self._fetch_byte(length=2)
            return bytes, self._fetch_byte(length=length)
        elif s == b'\xc6':  # bin 32
            length = self._fetch_byte(length=4)
            return bytes, self._fetch_byte(length=length)

        raise Exception('not implemented')

    def decode(self, target):
        pass

    def decode_byte(self, target: bytearray):
        self.target = target

        result_type, result_value = self._parse()

        return result_type, result_value
