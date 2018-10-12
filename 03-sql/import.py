import sys
import sqlite3

txtFile = sys.argv[1]
datFile = sys.argv[2]

print(txtFile)
print(datFile)

try:
    db = sqlite3.connect(datFile)
    cursor = db.cursor()
    print(sqlite3.version)
except Exception as e:
    db.rollback()
    raise e
finally:
    db.close()