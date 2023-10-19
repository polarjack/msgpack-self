import struct


def float_to_ieee_754_32bit(num):
    # Pack the float into its 32-bit IEEE 754 representation
    ieee_754_bytes = struct.pack('>f', num)

    # Convert the bytes to binary representation
    ieee_754_binary = ''.join(f'{byte:08b}' for byte in ieee_754_bytes)

    return ieee_754_binary


def ieee_754_32bit_to_float(binary):
    # Convert the binary representation to bytes
    ieee_754_bytes = bytes(int(binary[i : i + 8], 2) for i in range(0, len(binary), 8))

    # Unpack the bytes into a float
    num = struct.unpack('>f', ieee_754_bytes)[0]

    return num


def float_to_ieee_754_64bit(num):
    # Pack the float into its 64-bit IEEE 754 representation
    ieee_754_bytes = struct.pack('>d', num)

    # Convert the bytes to binary representation
    ieee_754_binary = ''.join(f'{byte:08b}' for byte in ieee_754_bytes)

    return ieee_754_binary


def ieee_754_64bit_to_float(binary):
    # Convert the binary representation to bytes
    ieee_754_bytes = bytes(int(binary[i : i + 8], 2) for i in range(0, len(binary), 8))

    # Unpack the bytes into a float
    num = struct.unpack('>d', ieee_754_bytes)[0]

    return num
