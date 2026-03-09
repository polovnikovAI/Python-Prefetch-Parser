import ctypes
import struct
import binascii

class DecompressWin(object):
    def tohex(self, val, nbits):
        return hex((val + (1 << nbits)) % (1 << nbits))

    def decompress(self, infile):
        USHORT = ctypes.c_uint16
        UCHAR = ctypes.c_ubyte
        ULONG = ctypes.c_uint32

        try:
            RtlDecompressBufferEx = ctypes.windll.ntdll.RtlDecompressBufferEx
            RtlGetCompressionWorkSpaceSize = ctypes.windll.ntdll.RtlGetCompressionWorkSpaceSize
        except AttributeError:
            return None

        with open(infile, 'rb') as fin:
            header = fin.read(8)
            compressed = fin.read()
            signature, decompressed_size = struct.unpack('<LL', header)
            calgo = (signature & 0x0F000000) >> 24
            crcck = (signature & 0xF0000000) >> 28
            magic = signature & 0x00FFFFFF

            if magic != 0x004d414d:
                fin.seek(0)
                return fin.read()

            if crcck:
                file_crc = struct.unpack('<L', compressed[:4])[0]
                crc = binascii.crc32(header)
                crc = binascii.crc32(struct.pack('<L', 0), crc)
                compressed = compressed[4:]
                crc = binascii.crc32(compressed, crc)
                if crc != file_crc:
                    return None

            compressed_size = len(compressed)
            ntCompressBufferWorkSpaceSize = ULONG()
            ntCompressFragmentWorkSpaceSize = ULONG()

            RtlGetCompressionWorkSpaceSize(USHORT(calgo),
                                           ctypes.byref(ntCompressBufferWorkSpaceSize),
                                           ctypes.byref(ntCompressFragmentWorkSpaceSize))

            ntCompressed = (UCHAR * compressed_size).from_buffer_copy(compressed)
            ntDecompressed = (UCHAR * decompressed_size)()
            ntFinalUncompressedSize = ULONG()
            ntWorkspace = (UCHAR * ntCompressFragmentWorkSpaceSize.value)()

            ntstatus = RtlDecompressBufferEx(
                USHORT(calgo),
                ctypes.byref(ntDecompressed),
                ULONG(decompressed_size),
                ctypes.byref(ntCompressed),
                ULONG(compressed_size),
                ctypes.byref(ntFinalUncompressedSize),
                ctypes.byref(ntWorkspace))

            if ntstatus:
                return None

        return bytearray(ntDecompressed)