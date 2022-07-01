from logging import raiseExceptions
import sqlite3 as lite
from bio_auth.constants import DB_NAME
import os

def createDB(dbname = DB_NAME):
    '''
    Create DB with DB_NAME and also create 3 tables.
    1. userRegister
    2. userCredential
    3. userBioImage

    args: DB_NAME

    return: None
    '''
    conn = lite.connect(dbname)

    csor = conn.cursor()
    stmt = "create table if not exists " + "userRegister" + "(maskedid varchar PRIMARY KEY, maskedPasswd varchar, masterSecretKey varchar, timestamp TIMESTAMP NOT NULL)"
    csor.execute(stmt)
    conn.commit()

    csor = conn.cursor()
    stmt = "create table if not exists " + "userCredential" + "(userid varchar PRIMARY KEY, maskedUserid varchar, bioHash varchar, email varchar, maskedPasswd varchar, timestamp TIMESTAMP  NOT NULL)"
    csor.execute(stmt)
    conn.commit()

    csor = conn.cursor()
    stmt = "create table if not exists " + "userBioImage" + "(userid varchar PRIMARY KEY, bioImage BLOB NOT NULL)"
    csor.execute(stmt)
    conn.commit()

    conn.close()




def deleteDB(dbname = DB_NAME):
    '''
    DELETE the DATABASE file if already present. 
    args: DB_NAME

    return: None
    '''
    try:
        if(os.path.isfile(dbname)):
            os.remove(dbname)
    except Exception as err:
        raiseExceptions(err)