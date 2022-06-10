import imagehash
import datetime
import random
import io
from PIL import Image
import sqlite3 as lite
from bio_auth.constants import DB_NAME
from bio_auth.reg_user import registerUserInStore
from bio_auth.common import genMessageHexDigest
from bio_auth.crypt import encryptImage

dbname = DB_NAME

def storeUserCredInDB(userEntry):
    '''
    Store tuple <userid, maskedUserid, bioHash, email, maskedPasswd, timestamp>
    in userCredential table.

    args: tuple <userid, maskedUserid, bioHash, email, maskedPasswd, timestamp>

    return: None
    '''
    tableName = "userCredential"

    conn = lite.connect(dbname)
    csor = conn.cursor()

    ftList = userEntry
    userid = str(userEntry[0])

    conn = lite.connect(dbname)
    csor = conn.cursor()
    stmt = "create table if not exists " + tableName + "(userid varchar PRIMARY KEY, maskedUserid varchar, bioHash varchar, email varchar, maskedPasswd varchar, timestamp TIMESTAMP NOT NULL)"
    csor.execute(stmt)
    conn.commit()

    csor.execute(f"SELECT userid FROM {tableName} where userid = ?",(userid,))
    
    resCheck = csor.fetchall()
    conn.commit()
    conn.close()

    if len(resCheck) != 0:
        print(f"User Credential Already Registered: {userid}")
        return
        
    conn = lite.connect(dbname)
    csor = conn.cursor()
    stmt = "insert into " + tableName + " values (?, ?, ?, ?, ?, ?)"
    csor.execute(stmt, ftList)
    conn.commit()
    conn.close()
    print(f"User: {userid} Credential generated")


def bioHashGen(imageFileObj):
    '''
    Returns a generated bioHash (ImageHash) string from an image file object.

    args: imageFileObj (Byte)

    return: bioHash (str)
    '''
    imageStream = io.BytesIO(imageFileObj)
    imageFile = Image.open(imageStream)
    bioHash = imagehash.average_hash(imageFile)
    imageFile.close()
    return str(bioHash)


def storeEncryptedImage(userEncImageEntry):
    '''
    Store tuple <userid, bioImage> in userBioImage table.

    args: tuple <userid, bioImage> 

    return: None
    '''

    tableName = "userBioImage"
    userid = userEncImageEntry[0]
    ftList = userEncImageEntry
    conn = lite.connect(dbname)
    csor = conn.cursor()
    stmt = "create table if not exists " + tableName + "(userid varchar PRIMARY KEY, bioImage BLOB NOT NULL)"
    csor.execute(stmt)
    conn.commit()

    csor.execute(f"SELECT userid FROM {tableName} where userid = ?",(userid,))
    
    resCheck = csor.fetchall()
    conn.commit()
    conn.close()

    if len(resCheck) != 0:
        print(f"User: {userid}'s BioImage Already Stored.")
        return

    conn = lite.connect(dbname)
    csor = conn.cursor()
    stmt = "insert into " + tableName + " values (?, ?)"
    csor.execute(stmt, ftList)
    conn.commit()
    conn.close()
    print(f"User: {userid}'s BioImage is stored successfully.")

def generateUserCredential(userid, passwd, email, bioImage, timestamp):
    '''
    Send <userid, passwd, email, bioImage> for generating User Credentials, 
    and store the User Credentials in UserRegister Table.

    args: userid, passwd, email, bioImage(Bytes)

    return: None
    '''
    random_number = random.randint(2, 10000)
    randomStr = str(random_number) + str(timestamp)
    maskedUserid = genMessageHexDigest(userid, randomStr, "sha512")

    
    bioHash = bioHashGen(bioImage) 

    maskedPasswd = genMessageHexDigest(passwd, bioHash, "sha512")

    userEntry = [userid, maskedUserid, str(bioHash), email, maskedPasswd, timestamp]
    storeUserCredInDB(userEntry)

    ############
    # Now encrypt the image and store in DB
    encryptImageFile = encryptImage(bioImage)

    userEncImageEntry = [userid, encryptImageFile]
    # Add encrypted Image in DB
    storeEncryptedImage(userEncImageEntry)
    #############


def sendCredentialToStore(userid, passwd, email, bioImage):
    '''
    Send <userid, passwd, email, bioImage> for generating User Credentials, 
    and store the User Credentials in UserRegister Table.

    args: userid, passwd, email, bioImage(Bytes)

    return: None
    '''
    
    tableName = "userCredential"

    conn = lite.connect(dbname)
    csor = conn.cursor()
    stmt = "create table if not exists " + tableName + "(userid varchar PRIMARY KEY, maskedUserid varchar, bioHash varchar, email varchar, maskedPasswd varchar, timestamp TIMESTAMP NOT NULL)"
    csor.execute(stmt)
    conn.commit()


    csor.execute("SELECT maskedUserid FROM userCredential WHERE userid = ?", (userid,))
    
    resCheck = csor.fetchall()
    conn.commit()
    conn.close()

    if len(resCheck) != 0:
        maskedUserid = resCheck[0][0]
        print(f"User ID:{userid} with Masked ID:{maskedUserid}: Already Registered.")
        return

    timestamp = datetime.datetime.now()
    generateUserCredential(userid, passwd, email, bioImage, timestamp)
    conn = lite.connect(dbname)
    csor = conn.cursor()
    csor.execute("SELECT maskedUserid, maskedPasswd FROM userCredential WHERE userid = ?", (userid,))
    data = csor.fetchall()
    maskedUserid = data[0][0]
    maskedPasswd = data[0][1]
    
    conn.commit()
    conn.close()
    registerUserInStore(maskedUserid, maskedPasswd, timestamp)
