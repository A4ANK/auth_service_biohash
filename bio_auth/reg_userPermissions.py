import sqlite3 as lite
from bio_auth.constants import DB_NAME

dbname = DB_NAME

def storeUserPermissionInDB(userid, CREATE, READ, UPDATE, DELETE, timestamp):
    '''
    Store tuple <userid str, CREATE bool, READ bool, UPDATE bool, DELETE bool, timestamp str>
    in userPermissions table.

    args: tuple <userid, CREATE, READ, UPDATE, DELETE, timestamp>

    return: None
    '''
    tableName = "userPermissions"

    conn = lite.connect(dbname)
    csor = conn.cursor()
    userPermissionsEntry = (userid, CREATE, READ, UPDATE, DELETE, timestamp)
    ftList = userPermissionsEntry
    userid = str(userPermissionsEntry[0])

    conn = lite.connect(dbname)
    csor = conn.cursor()
    stmt = "create table if not exists " + tableName + "(userid varchar PRIMARY KEY, c bool, r bool, u bool, d bool, timestamp TIMESTAMP NOT NULL)"
    csor.execute(stmt)
    conn.commit()

    csor.execute(f"SELECT userid FROM {tableName} where userid = ?",(userid,))
    
    resCheck = csor.fetchall()
    conn.commit()
    conn.close()

    if len(resCheck) != 0:
        print(f"User: {userid} Permissions Already Stored.")
        return
        
    conn = lite.connect(dbname)
    csor = conn.cursor()
    stmt = "insert into " + tableName + " values (?, ?, ?, ?, ?, ?)"
    csor.execute(stmt, ftList)
    conn.commit()
    conn.close()
    print(f"User: {userid} Permissions Stored Successfully")

