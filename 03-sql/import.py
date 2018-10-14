import sys
import sqlite3
import scorelib as module

def initDb(datFile, schemaFile):
    schema = open(schemaFile, "r").read()
    
    db = sqlite3.connect(datFile)
    cursor = db.cursor()
    cursor.executescript(schema)
    db.commit()

    return db

def insertData(prints, db):
    for p in prints:
        print(p)


if __name__ == "__main__":
    db = initDb(sys.argv[2], "scorelib.sql")
    insertData(module.load(sys.argv[1]), db)
    db.close()
