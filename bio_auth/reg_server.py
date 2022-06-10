import base64
import hashlib
import sqlite3 as lite
from bio_auth.constants import DB_NAME

dbname = DB_NAME

def registerServerInDB(registerServerData):
    '''
    Store tuple <serverid, regServerCode, serverMask> in serverRegister table.

    args: tuple <serverid, regServerCode, serverMask> 

    return: None
    '''

    tableName = "serverRegister"

    conn = lite.connect(dbname)
    csor = conn.cursor()
    stmt = "create table if not exists " + tableName + "(serverid varchar PRIMARY KEY, regServerCode varchar, serverMask varchar)"
    csor.execute(stmt)
    conn.commit()
    conn.close()


    conn = lite.connect(dbname)
    csor = conn.cursor()
    ftList = registerServerData
    serverid = str(registerServerData[0])
    csor.execute(f"SELECT serverid FROM {tableName} where serverid = ?",(serverid,))
    
    resCheck = csor.fetchall()
    conn.commit()
    conn.close()

    if len(resCheck) != 0:
        print(f"Server Already Registered: {serverid}")
        return
        
    conn = lite.connect(dbname)
    csor = conn.cursor()
    stmt = "insert into " + tableName + " values (?, ?, ?)"
    csor.execute(stmt, ftList)
    conn.commit()
    conn.close()
    print(f"Server:{serverid}: registered successfully.")


def getHash(inputStr, algo = "sha512"):
    '''
    Returns a Hex Message Digest of an string object using hashlib.
    Algo:- ["md5", "sha1", "sha256", "sha512"]

    args: inputStr (str), algo = "sha512" (default)

    return: hash (str)
    '''
    if algo == "md5":
        hasher = hashlib.md5() # creates 128 bit hash value
    elif algo == "sha1":
        hasher = hashlib.sha1() # creates 160 bit hash value
    elif algo == "sha256":
        hasher = hashlib.sha256() # creates 160 bit hash value
    else:
        hasher = hashlib.sha512() # creates 512 bit hash value
    hasher.update(inputStr.encode())
    hashHexDigest = hasher.hexdigest()
    return hashHexDigest

def registerServerInStore(serverid):
    '''
    Generate <serverid , regServerCode , serverMask> for generating serverEntry, 
    and store the serverEntry in serverRegister Table.

    args: serverid (str)

    return: None
    '''
    serverid = str(serverid)
    regServerCode = "" # unique server string
    regServerCodeBytes = base64.b64encode(serverid.encode("utf-8"))
    regServerCode = str(regServerCodeBytes, "utf-8")
    inputStr = serverid + regServerCode
    serverMask = getHash(inputStr, algo = "sha512")
    serverEntry = [serverid , regServerCode , serverMask]
    registerServerInDB(serverEntry)


