import sys
import sqlite3
import json

def main(datFile):
    printNo = sys.argv[1]
    try:
        printNo = int(printNo)
    except ValueError:
        print("Argument is not a number!")

    db = sqlite3.connect(datFile)
    cursor = db.cursor()
    cursor.execute("SELECT p.name, p.born, p.died FROM person AS p " +
                    "JOIN score_author AS sa ON p.id = sa.composer " + 
                    "JOIN score AS s ON sa.score = s.id " +
                    "JOIN edition AS e ON e.score = s.id " + 
                    "JOIN print ON print.edition = e.id " + 
                    "WHERE print.id = ?", (printNo,))
    match = cursor.fetchall()
    if match is not None:
        item = {}
        res = []
        for m in match:
            if m[0] != None:
                item["name"] = m[0]
            if m[1] != None:
                item["born"] = m[1]
            if m[2] != None:
                item["died"] = m[2]
            res.append(item)
            item = {}
        print(json.dumps(res, ensure_ascii=False, indent=4))

if __name__ == "__main__":
    main("scorelib.dat")
