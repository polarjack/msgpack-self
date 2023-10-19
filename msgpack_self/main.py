import io

from .decode import Decoder
from .encode import Encoder


def encode(target) -> io.BytesIO:
    encoder = Encoder()
    return encoder.encode(target=target)


def decode_byte(target_byte: bytes):
    decoder = Decoder()
    return decoder.decode_byte(target_byte)
