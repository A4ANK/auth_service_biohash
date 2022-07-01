import sqlite3 as lite
import hmac
from app_utils import MONGODB_COLLECTION_NAME, MONGODB_NAME, MONGODB_URI_ADMIN, MONGODB_URI_USER
from bio_auth.constants import DB_NAME, HMAC_KEY 
from secrets import choice
from string import ascii_letters, digits
from logging import raiseExceptions
from PIL import Image
from os import urandom
from random import random
from io import BytesIO
from pymongo import MongoClient


dbname = DB_NAME

def randomPassGen(n: int) -> str:
    '''
    Generate a n-character alphanumeric password with 
    at least one lowercase character, 
    at least one uppercase character, 
    and at least three digits:

    args: integer n
    return: n-character long string.
    '''
    alphabet = ascii_letters + digits
    while True:
        password = ''.join(choice(alphabet) for i in range(n))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3):
            break
    return password


def randomImageGen(size: tuple) -> bytes:
    '''
    Generates a random RGB image of size (input1, input2)
    args: tuple(input1, input2) # Dimension of the required image.
    return: <io.BytesIO Object> Image
    '''
    img = Image.new('RGB', size)
    def randomGen(size):
        return urandom(size[0]*size[1])
    
    pixels = zip(randomGen(size), randomGen(size), randomGen(size))
    img.putdata(list(pixels))
    img.rotate(angle=random()%float(360))
    buffer = BytesIO()
    try:
        img.save(buffer, format='JPEG')
        # imggg = Image.open(buffer)
        # imggg.show()
        return buffer.getvalue()
    except Exception as err:
        raiseExceptions(err)
    finally:
        img.close()
        buffer.close()

def fetchAllowedServersAdmin():
    '''
    Fetch Allowed Servers by Admin.

    args: userid

    return: tuple<CREATE Bool, READ Bool, UPDATE Bool, DELETE Bool> 
            or
            tuple<>
    '''
    # MongoDB

    # user has read only permissions in the DB
    client = MongoClient(MONGODB_URI_USER) 
    db = client[MONGODB_NAME]

    collection_list = db.list_collection_names()
    if MONGODB_COLLECTION_NAME in collection_list:
        collection = db[MONGODB_COLLECTION_NAME]
        links = collection.find({},{'_id': 0})
        
        if links:
            userList = list()
            for link in links:
                userLinks = link['links']
                for eachLink in userLinks:
                    userList.append([link['userid'], eachLink])
            return userList
        else:
            return []
    else:
        return []


def fetchAllowedServersUsers(userid):
    '''
    Fetch Allowed Servers of a registered user with given userid.

    args: userid

    return: tuple<CREATE Bool, READ Bool, UPDATE Bool, DELETE Bool> 
            or
            tuple<>
    '''
    # MongoDB

    # user has read only permissions in the DB
    client = MongoClient(MONGODB_URI_USER) 
    db = client[MONGODB_NAME]

    collection_list = db.list_collection_names()
    if MONGODB_COLLECTION_NAME in collection_list:
        collection = db[MONGODB_COLLECTION_NAME]
        links = collection.find({ "userid" : f"{userid}"},{ "_id": 0, f"{userid}": 1, f"{MONGODB_COLLECTION_NAME}": 1})
        if links[0]['links']:
            userLinks = [link for link in links[0]['links']]
            return userLinks
        else:
            return []
    else:
        return []

def fetchAllUserPermissions() -> dict:
    '''
    Fetch permissions of all registered users.

    args: None

    return: Dict<userid str : List<CREATE Bool, READ Bool, UPDATE Bool, DELETE Bool >> 
            or
            Dict<>
    '''
    conn = lite.connect(dbname)
    csor = conn.cursor()
    csor.execute(f"SELECT userid, c, r, u, d FROM userPermissions",)
    check = csor.fetchall()
    conn.commit()
    conn.close()

    if( len(check) != 0 ):
        permsDict = {}
        for perms in check:
            permsDict[perms[0]] = [perms[1], perms[2], perms[3], perms[4]]
        return permsDict
    else:
        return {}


def fetchUserPermissions(userid):
    '''
    Fetch permissions of a registered user.

    args: userid

    return: tuple<CREATE Bool, READ Bool, UPDATE Bool, DELETE Bool> 
            or
            tuple<>
    '''
    conn = lite.connect(dbname)
    csor = conn.cursor()
    csor.execute(f"SELECT c, r, u, d FROM userPermissions where userid = ?",(userid,))
    check = csor.fetchall()
    conn.commit()
    conn.close()

    if( len(check) != 0 ):
        CREATE = check[0][0]
        READ = check[0][1]
        UPDATE = check[0][2]
        DELETE = check[0][3]
        return (CREATE, READ, UPDATE, DELETE)
    else:
        return ()


def fetch_MaskedID_BioHash(userid):
    '''
    Fetch MaskedID and BioHash from the DB.

    args: userid

    return: tuple<True, list<maskedid, bioHash> > 
            or
            tuple<False, list<> >
    '''
    conn = lite.connect(dbname)
    csor = conn.cursor()
    csor.execute(f"SELECT maskedUserid, bioHash FROM userCredential where userid = ?",(userid,))
    check = csor.fetchall()
    conn.commit()
    conn.close()

    if( len(check) != 0 ):
        maskedid = check[0][0]
        bioHash = check[0][1]
        return True, [maskedid, bioHash]
    else:
        return False, []

def fetch_emailID(email):
    '''
    Fetch emailID only.

    args: userid

    return: tuple<True, email > 
            or
            tuple<False, <> >
    '''
    conn = lite.connect(dbname)
    csor = conn.cursor()
    csor.execute(f"SELECT email FROM userCredential where email = ?",(email,))
    check = csor.fetchall()
    conn.commit()
    conn.close()

    if( len(check) != 0 ):
        email = check[0][0]
        return True, email
    else:
        return False, None

def fetchMaskedPasswd(maskedid):
    '''
    Fetch MaskedPasswd from the DB.

    args: maskedid

    return: tuple<True, maskedPasswd > 
            or
            tuple<False, <> >
    '''
    conn = lite.connect(dbname)
    csor = conn.cursor()
    csor.execute(f"SELECT maskedPasswd FROM userRegister where maskedid = ?",(maskedid,))
    check = csor.fetchall()
    conn.commit()
    conn.close()
    
    if( len(check) != 0 ):
        maskedPasswd = check[0][0]
        return True, maskedPasswd
    else:
        return False, None

def genMessageHexDigest(inputStr1, inputStr2, algo="sha512"):
    '''
    Returns Hex Message Digest of (inputStr1 + inputStr2) using HMAC.

    args: inputStr1 (str), inputStr2 (str), algo (default = "sha512")
    
    return: hexMessageDigest
    '''
    key1= HMAC_KEY

    maskedPasswdProvided = inputStr1 + inputStr2
    hmac1 = hmac.new(key=key1.encode(), msg=maskedPasswdProvided.encode(), digestmod=algo)
    hexMessageDigest = hmac1.hexdigest()
    return hexMessageDigest

def fetchBioImage(userid):
    '''
    Fetch encrypted bioImage from the DB.

    args: userid

    return: tuple<True, bioImage > 
            or
            tuple<False, <> >
    '''

    conn = lite.connect(dbname)
    csor = conn.cursor()
    csor.execute(f"SELECT maskedUserid, bioHash FROM userCredential where userid = ?",(userid,))
    check1 = csor.fetchall()
    conn.commit()
    conn.close()


    if( len(check1) != 0 ):
        conn = lite.connect(dbname)
        csor = conn.cursor()
        csor.execute(f"SELECT bioImage FROM userBioImage where userid = ?",(userid,))
        check = csor.fetchall()
        conn.commit()
        conn.close()
        
        if( check ):
            bioImage = check[0][0]
            return True, bioImage
        else:
            return False, None
    else:
        return False, None