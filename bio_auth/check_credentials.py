from bio_auth.common import fetch_MaskedID_BioHash, fetch_emailID, fetchBioImage, fetchMaskedPasswd, genMessageHexDigest
from bio_auth.crypt import decryptImage
import io
from PIL import Image, ImageChops

from bio_auth.reg_biohash import bioHashGen

def checkUseronly(userid):
    '''
    Check if a userid is present in the DB or not.
    
    args: userid 

    return: bool
    '''
    if( fetch_MaskedID_BioHash(userid)[0]):
        print(f"User: {userid} is already registered.")
        return True
    else:
        print(f"Userid: {userid} is Not Registered.")
        return False

def checkEmailonly(email):
    '''
    Check if a email is present in the DB or not.
    
    args: email 

    return: bool
    '''
    if( fetch_emailID(email)[0]):
        print(f"Email: {email} is already registered.")
        return True
    else:
        print(f"Email: {email} is Not Registered.")
        return False

def checkUserRegisterInDB(userid, passwd):
    '''
    Check for login using userid and passwd in the DB.
    
    args: userid , passwd

    return: bool
    '''
    if( checkUseronly(userid) ):
        _ , data = fetch_MaskedID_BioHash(userid)
        
        maskedid = data[0] 
        bioHash  = data[1]

        res , maskedPasswd = fetchMaskedPasswd(maskedid)

        if( res ):
            maskedPasswdFetched = maskedPasswd

            maskedPasswdProvided = genMessageHexDigest(passwd, bioHash)
            if(maskedPasswdProvided == maskedPasswdFetched):
                print(f"Userid and Password verified successfully.")
                return True
            else:
                print(f"Userid and Password Not Verified.")
                return False

def checkBioImage(userid, bioImage):
    '''
    Check if Correct bioImage is Uploaded or not by comparing pre-stored  
    bioImage from the DB with the uploaded bioImage.
    
    args: userid (str), bioImage (bytes)

    return: bool
    '''
    imageStream1 = io.BytesIO(bioImage)
    bioImageProvided = Image.open(imageStream1)
    if(fetchBioImage(userid)[0]):
        encryptImageFile = fetchBioImage(userid)[1]
        decryptImageFile = decryptImage(encryptImageFile)
        imageStream2 = io.BytesIO(decryptImageFile)
        bioImageFetched = Image.open(imageStream2)
        try:
            diff = ImageChops.difference(bioImageProvided, bioImageFetched)
            bioImageFetched.close()
            bioImageProvided.close()
            bioHashProvided = bioHashGen(bioImage)
            bioHashFetched= bioHashGen(decryptImageFile)

            if (diff.getbbox() is None and 
                bioHashFetched == bioHashProvided
                ):
                print(f"BioHash Is Correct.")
                return True
            else:
                print(f"Userid: {userid} Is Registered But Wrong Image Uploaded.")
                print(f"BioHash Is Incorrect.")
                return False
        except ValueError as err:
            return False
    else:
        print("Error in fetching bioImage.")
        return False

