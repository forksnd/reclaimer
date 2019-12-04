COMPRESSION_UNKNOWN = -1
COMPRESSION_NONE  = 0  # 16bit pcm
COMPRESSION_ADPCM = 1
COMPRESSION_OGG   = 2  # halo pc only
COMPRESSION_WMA   = 3  # halo 2 only

ENCODING_UNKNOWN = -1
ENCODING_MONO   = 0
ENCODING_STEREO = 1
ENCODING_CODEC  = 2

SAMPLE_RATE_22K = 22050
SAMPLE_RATE_32K = 32000  # halo 2 only
SAMPLE_RATE_44K = 44100

DEF_SAMPLE_CHUNK_SIZE = 0x10000
MAX_SAMPLE_CHUNK_SIZE = 0x400000
MAX_MOUTH_DATA        = 0x2000

ADPCM_COMPRESSED_BLOCKSIZE   = 36
ADPCM_DECOMPRESSED_BLOCKSIZE = 128
