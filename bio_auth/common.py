import sqlite3 as lite
import hmac
from bio_auth.constants import DB_NAME, HMAC_KEY 

dbname = DB_NAME

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
    csor.execute(f"SELECT email FROM userCredential where userid = ?",(email,))
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