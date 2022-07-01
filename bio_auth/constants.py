from os import getenv 

# Database Name
DB_NAME = "sample.db"

# Key used in HMAC
HMAC_KEY = getenv("HMAC_KEY") or "AnyKeyOfYourChoice"

# AES 
# key size in AES-128 is 128 bit/ 16 Byte.  
# key size in AES-192 is 192 bit/ 24 Byte.
# key size in AES-256 is 256 bit/ 32 Byte.
# Initialization Vector must be 128 bit / 16 Bytes long.

stringNone = lambda keyStr: keyStr.encode if keyStr else None

AES_KEY = stringNone(getenv("AES_KEY")) or b'eyJ0b2tlbiI6ImV5SjBlWEFpT2lKS1Yx' # 32 Byte
AES_IV = stringNone(getenv("AES_IV")) or b'eyJ0b2tlbiI6ImV5'  # 16 Byte
