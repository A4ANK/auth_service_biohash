from Crypto.Cipher import AES
from bio_auth.constants import AES_KEY, AES_IV

# key size in AES-128 is 128 bit/ 16 Byte.  
# key size in AES-192 is 192 bit/ 24 Byte.
# key size in AES-256 is 256 bit/ 32 Byte.
# Initialization Vector must be 128 bit / 16 Bytes long.

key = AES_KEY 
iv = AES_IV
# def encryptImage(input_file):
def encryptImage(inputImage):
    '''
    AES Encryption.

    args: inputImage (Byte Object)

    return: encryptedData (Byte Object)
    '''
    global key,iv
    
    CFBCipher = AES.new(key, AES.MODE_CFB, iv)
    encryptedData = CFBCipher.encrypt(inputImage)
    return encryptedData

def decryptImage(encryptedData):
    '''
    AES Decryption.

    args: encryptedData (Byte Object)

    return: decryptedData (Byte Object)
    '''
    global key,iv

    CFBDecipher = AES.new(key, AES.MODE_CFB, iv)
    decryptedData = (CFBDecipher.decrypt(encryptedData))
    return decryptedData
