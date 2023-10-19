import io
import struct

TYPE_NONE = 0xC0
TYPE_FALSE = 0xC2
TYPE_TRUE = 0xC3


class Encoder:
    def __init__(self, float_precision=32):
        self.result = io.BytesIO()
        self.float_precision = float_precision

    def _dict_length(self, length):
        # 1, 3, 5 bytes
        # 1 => 1000XXXX + length
        # 3 => 0xde, length
        # 5 => 0xdf, length
        if length <= 0x0F:
            self.result.write(bytes([0x80 | length]))
        elif length <= 0xFFFF:
            self.result.write(b'\xde' + struct.pack('>H', length))
        elif length <= 0xFFFFFFFF:
            self.result.write(b'\xdf' + struct.pack('>I', length))
        else:
            raise ValueError('dict length out of range')

    def _str_length_encode(self, length):
        # 1, 2, 3, 5 bytes
        # 1 => 101XXXXX + length
        # 2 => 0xd9, length
        # 3 => 0xda, length
        # 5 => 0xdb, length
        if length <= 0x1F:
            self.result.write(bytes([0xA0 | length]))
        elif length <= 0xFF:
            length = struct.pack('>B', length)
            self.result.write(b'\xd9' + length)
        elif length <= 0xFFFF:
            length = struct.pack('>H', length)
            self.result.write(b'\xda' + length)
        elif length <= 0xFFFFFFFF:
            length = struct.pack('>I', length)
            self.result.write(b'\xdb' + length)
        else:
            raise ValueError('str length out of range')

    def _encode(self, target):
        if isinstance(target, type(None)):
            return self.result.write(bytes([TYPE_NONE]))
        elif isinstance(target, bool):
            if target:
                return self.result.write(bytes([TYPE_TRUE]))
            else:
                return self.result.write(bytes([TYPE_FALSE]))
        elif isinstance(target, int):
            # positive fixint 0xxxxxxx
            if 0 <= target <= 0x7F:
                return self.result.write(target.to_bytes(1, 'big'))

            # negative fixint 111YYYYY
            if -0x20 <= target < 0:
                return self.result.write(bytes([0xE0 | (target & 0x1F)]))

            # uint 8 0xcc | ZZZZZZZZ
            if 0x80 <= target <= 0xFF:
                return self.result.write(bytes([0xCC, target & 0xFF]))

            # int 8 0xd0 | ZZZZZZZZ
            if -0x80 <= target < 0:
                return self.result.write(bytes([0xD0, target & 0xFF]))

            # uint 16 0xcd |ZZZZZZZZ|ZZZZZZZZ
            if 0x100 <= target <= 0xFFFF:
                return self.result.write(b'\xcd' + struct.pack('>H', target))

            # int 16 0xd1 |ZZZZZZZZ|ZZZZZZZZ
            if -0x8000 <= target < -0x80:
                return self.result.write(b'\xd1' + struct.pack('>h', target))

            # uint 32 0xce |ZZZZZZZZ|ZZZZZZZZ|ZZZZZZZZ|ZZZZZZZZ
            if 0x10000 <= target <= 0xFFFFFFFF:
                return self.result.write(b'\xce' + struct.pack('>I', target))

            # int 32 0xd2 |ZZZZZZZZ|ZZZZZZZZ|ZZZZZZZZ|ZZZZZZZZ
            if -0x80000000 <= target < -0x8000:
                return self.result.write(b'\xd2' + struct.pack('>i', target))

            # uint 64 0xcf
            if 0x100000000 <= target <= 0xFFFFFFFFFFFFFFFF:
                return self.result.write(b'\xcf' + struct.pack('>Q', target))

            # int 64  0xd3  |ZZZZZZZZ|ZZZZZZZZ|ZZZZZZZZ|ZZZZZZZZ|ZZZZZZZZ|ZZZZZZZZ|ZZZZZZZZ|ZZZZZZZZ
            if -0x8000000000000000 <= target < -0x80000000:
                return self.result.write(b'\xd3' + struct.pack('>q', target))

            raise ValueError('int out of range')

        elif isinstance(target, float):
            # 5, 9 bytes
            # 5 => 0xca, float -> sign(1) + exponent(8) + fraction(23)
            # 9 => 0xcb, double

            if self.float_precision == 32:
                return self.result.write(b'\xca' + struct.pack('>f', target))
            else:
                return self.result.write(b'\xcb' + struct.pack('>d', target))

        elif isinstance(target, str):
            target = target.encode('utf-8')
            length = len(target)

            self._str_length_encode(length)
            self.result.write(target)
            return
        elif isinstance(target, (bytes, bytearray)):
            # 2, 3, or 5 bytes
            # 2 => 0xc4, length
            # 3 => 0xc5, length
            # 5 => 0xc6, length
            length = len(target)

            if length <= 0xFF:
                self.result.write(bytes([0xC4, length]))
            elif length <= 0xFFFF:
                self.result.write(bytes([0xC5, length]))
            elif length <= 0xFFFFFFFF:
                self.result.write(bytes([0xC6, length]))

            self.result.write(target)
            return
        elif isinstance(target, list):
            # 1, 3, 5 bytes
            # 1 => 1001XXXX + length
            # 3 => 0xdc, length
            # 5 => 0xdd, length
            if len(target) <= 0x0F:
                self.result.write(bytes([0x90 | len(target)]))
            elif len(target) <= 0xFFFF:
                self.result.write(bytes([0xDC, len(target)]))
            elif len(target) <= 0xFFFFFFFF:
                self.result.write(bytes([0xDD, len(target)]))

            for item in target:
                self._encode(item)
            return

        elif isinstance(target, dict):
            self._dict_length(len(target))
            for k, v in target.items():
                self._encode(k)
                self._encode(v)
            return
        else:
            raise TypeError('Unknown type: {}'.format(type(target)))

    def encode(self, target: dict):
        self._encode(target)
        return self.result
