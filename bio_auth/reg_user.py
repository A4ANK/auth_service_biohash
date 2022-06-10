import sqlite3 as lite
from bio_auth.common import genMessageHexDigest
from bio_auth.constants import DB_NAME

dbname = DB_NAME
        
def storeUserRegisterInDB(userEntry):
    '''
    Store tuple <maskedid, maskedPasswd, masterSecretKey, timestamp> 
    in userRegister table.

    args: tuple <maskedid, maskedPasswd, masterSecretKey, timestamp> 

    return: None
    '''
    tableName = "userRegister"

    conn = lite.connect(dbname)
    csor = conn.cursor()

    ftList = userEntry
    maskedid = str(userEntry[0])

    conn = lite.connect(dbname)
    csor = conn.cursor()
    stmt = "create table if not exists " + tableName + "(maskedid varchar PRIMARY KEY, maskedPasswd varchar, masterSecretKey varchar, timestamp TIMESTAMP NOT NULL)"
    csor.execute(stmt)
    conn.commit()

    csor.execute(f"SELECT maskedid FROM {tableName} where maskedid = ?",(maskedid,))
    
    resCheck = csor.fetchall()
    conn.commit()
    conn.close()

    if len(resCheck) != 0:
        print(f"Masked ID:{maskedid}: Already Registered.")
        return
        
    conn = lite.connect(dbname)
    csor = conn.cursor()
    stmt = "insert into " + tableName + " values (?, ?, ?, ?)"
    csor.execute(stmt, ftList)
    conn.commit()
    conn.close()
    print(f"User with Masked ID:{maskedid}: registered successfully.")


def registerUserInStore(maskedid, maskedPasswd, timestamp):
    '''
    Generate <maskedid, maskedPasswd, masterSecretKey, timestamp> for generating userEntry, 
    and store the userEntry in userRegister Table.

    args: maskedid (str), maskedPasswd (str), timestamp (str)

    return: None
    '''    
    masterSecretKey = genMessageHexDigest(maskedid, maskedPasswd, algo = "sha512")
    userEntry = [maskedid, maskedPasswd, masterSecretKey, timestamp]
    storeUserRegisterInDB(userEntry)


