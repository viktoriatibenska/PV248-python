import sys
import sqlite3
import json

def main(datFile, author):
    author = "%" + author + "%"
    db = sqlite3.connect(datFile)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM person AS p " +
                    "JOIN score_author AS sa ON p.id = sa.composer " + 
                    "JOIN score AS s ON sa.score = s.id " +
                    "JOIN edition AS e ON e.score = s.id " + 
                    "JOIN print AS pr ON pr.edition = e.id " + 
                    "WHERE p.name LIKE ? " + 
                    "ORDER BY p.name, pr.id", (author,))
    authorsMatch = cursor.fetchall()
    if authorsMatch is not None:
        res = {}
        authorPrints = []
        printItem = {}
        currentComposer = authorsMatch[0][3]
        for a in authorsMatch:
            if currentComposer != a[3]:
                res[currentComposer] = authorPrints
                authorPrints = []
                currentComposer = a[3]
            
            printItem["Print Number"] = a[17]
            printItem["Composer"] = getComposers(a[7], cursor)
            if a[8] != None:
                printItem["Title"] = a[8]
            if a[9] != None:
                printItem["Genre"] = a[9]
            if a[10] != None:
                printItem["Key"] = a[10]
            if a[12] != None:
                printItem["Composition Year"] = a[12]
            if a[15] != None:
                printItem["Edition"] = a[15]
            printItem["Editor"] = getEditors(a[13], cursor)
            printItem["Voices"] = getVoices(a[7], cursor)
            if a[18] == "Y":
                printItem["Partiture"] = True
            else:
                printItem["Partiture"] = False

            if a[11] != None:
                printItem["Incipit"] = a[11]

            authorPrints.append(printItem)
            printItem = {}

        res[currentComposer] = authorPrints
        print(json.dumps(res, ensure_ascii=False, indent=4))
                
def getComposers(scoreId, cursor):
    res = []
    cursor.execute("select * from score_author as s join person as p on s.composer = p.id WHERE s.score = ?", (scoreId,))
    match = cursor.fetchall()
    if match is not None:
        for m in match:
            author = {}
            if m[6] is not None:
                author["Name"] = m[6]
            if m[4] is not None:
                author["Born"] = m[4]
            if m[5] is not None:
                author["Died"] = m[5]
            res.append(author)
    return res

def getEditors(editionId, cursor):
    res = []
    cursor.execute("select * from edition_author as e join person as p on e.editor = p.id WHERE e.edition = ?", (editionId,))
    match = cursor.fetchall()
    if match is not None:
        for m in match:
            author = {}
            if m[6] is not None:
                author["Name"] = m[6]
            if m[4] is not None:
                author["Born"] = m[4]
            if m[5] is not None:
                author["Died"] = m[5]
            res.append(author)
    return res

def getVoices(scoreId, cursor):
    res = {}
    cursor.execute("select * from voice where score = ?", (scoreId,))
    match = cursor.fetchall()
    if match is not None:
        for m in match:
            voice = {}
            if m[4] is not None:
                voice["Name"] = m[4]
            if m[3] is not None:
                voice["Range"] = m[3]
            res[m[1]] = voice

    return res


if __name__ == "__main__":
    main("scorelib.dat", sys.argv[1])
