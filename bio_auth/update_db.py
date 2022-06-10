import datetime
import sqlite3 as lite
from bio_auth.common import genMessageHexDigest
from bio_auth.constants import DB_NAME

dbname = DB_NAME

def updatePasswdRC(userid, maskedid, newPasswd, bioHash):
    '''
    Update (newPasswd,updated timestamp) only in userCredendial table.
    Update newPasswd only in userRegister table. 
    Updated timestamp can be used to know Last password change timestamp.

    args: userid (str), maskedid (str), newPasswd (str), bioHash (str)

    return: bool
    '''
    try:
        newMaskedPasswd = genMessageHexDigest(newPasswd, bioHash, "sha512")
        newTimestamp = datetime.datetime.now() 
        print("newMaskedPasswd", newMaskedPasswd)
        conn = lite.connect(dbname)
        csor = conn.cursor()
        csor.execute(f"UPDATE userCredential SET maskedPasswd = ?, timestamp = ? where userid = ?",(newMaskedPasswd, newTimestamp, userid,))
        conn.commit()

        csor = conn.cursor()
        csor.execute(f"UPDATE userRegister SET maskedPasswd = ? where maskedid = ?",(newMaskedPasswd, maskedid,))
        conn.commit()

        conn.close()
        print("Password Changed Successfully.")
        return True
    except:
        return False