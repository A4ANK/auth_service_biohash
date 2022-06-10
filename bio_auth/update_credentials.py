import sqlite3 as lite
from bio_auth.check_credentials import checkUseronly
from bio_auth.constants import DB_NAME
from bio_auth.reg_biohash import bioHashGen
from bio_auth.update_db import updatePasswdRC

dbname = DB_NAME

def updateUserCredentials(userid, newPasswd):
    '''
    Utility function for "forgot password" which updates (New Password) in the DB.

    args: userid (str), newPasswd(str)

    return: bool
    '''
    if checkUseronly(userid):
        conn = lite.connect(dbname)
        csor = conn.cursor()
        csor.execute(f"SELECT maskedUserid, bioHash FROM userCredential where userid = ?",(userid,))
        check1 = csor.fetchall()
        conn.commit()
        conn.close()


        if( len(check1) != 0 ):
            maskedid = check1[0][0]
            bioHash = check1[0][1]

            if(updatePasswdRC(userid, maskedid, newPasswd, bioHash)):
                print(f"Userid: {userid}'s password updated successfully.")
                return True
            else:
                print(f"Server is not able to update the password.")
                print(f"Internal Server Error.")
                return False
        else:
            print(f"Userid: {userid} Is Registered But Wrong Image Uploaded.")
            print(f"BioHash Is Incorrect.")
            return False

            
    else:
        print(f"Userid: {userid} is Not Registered.")
        return False
