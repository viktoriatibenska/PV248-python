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
    cursor = db.cursor()
    composerIds = []
    editorIds = []

    for p in prints:
        for composer in p.composition().authors:
            composerIds.append(insertPerson(composer, cursor))
        for editor in p.edition.authors:
            editorIds.append(insertPerson(editor, cursor))

        scoreId = insertScore(p.composition(), cursor)
        for i, voice in enumerate(p.composition().voices):
            insertVoice(voice, scoreId, i+1, cursor)
        for composerId in composerIds:
            insertScoreAuthor(scoreId, composerId, cursor)

        editionId = insertEdition(p.edition, scoreId, cursor)
        for editorId in editorIds:
            insertEditionAuthor(editionId, editorId, cursor)

        insertPrint(p, editionId, cursor)
        composerIds = []
        editorIds = []

def insertPerson(person, cursor):
    cursor.execute("SELECT * FROM person WHERE name IS ?", (person.name,))
    match = cursor.fetchone()

    if match is None:
        cursor.execute("INSERT INTO person(name, born, died) VALUES(?, ?, ?)", (person.name, person.born, person.died))
        return cursor.lastrowid
    else:
        born = match[1]
        died = match[2]

        if born is None:
            born = person.born
        if died is None:
            died = person.died
        
        cursor.execute("UPDATE person SET born=?, died=? WHERE name=?", (born, died, person.name))
        return match[0]

def insertScore(composition, cursor):
    res = -1
    cursor.execute("SELECT * FROM score WHERE name IS ? AND genre IS ? AND key IS ? AND incipit IS ? AND year IS ?", 
                    (composition.name, composition.genre, composition.key, composition.incipit, composition.year,))
    match = cursor.fetchall()

    if match is not None:
        for m in match:
            cursor.execute("SELECT * FROM score_author as s JOIN person AS p ON p.id = s.composer WHERE s.score = ?", (m[0],))
            composers = cursor.fetchall()
            cursor.execute("SELECT * FROM voice WHERE score = ?", (m[0],))
            voices = cursor.fetchall()
            if compareAuthors(composers, composition.authors, 6) and compareVoices(voices, composition.voices):
                res = m[0]
                break
    if match is None or res == -1:
        cursor.execute("INSERT INTO score(name, genre, key, incipit, year) VALUES (?, ?, ?, ?, ?)",
                        (composition.name, composition.genre, composition.key, composition.incipit, composition.year))
        res = cursor.lastrowid
    
    return res

def insertEdition(edition, scoreId, cursor):
    res = -1
    cursor.execute("SELECT * FROM edition WHERE score IS ? AND name IS ?", (scoreId, edition.name,))
    match = cursor.fetchall()

    if match is not None:
        for m in match:
            cursor.execute("SELECT * FROM edition_author as e JOIN person AS p ON p.id = e.editor WHERE e.edition = ?", (m[0],))
            editors = cursor.fetchall()
            if compareAuthors(editors, edition.authors, 6):
                res = m[0]
                break
    if match is None or res == -1:
        cursor.execute("INSERT INTO edition(score, name, year) VALUES(?, ?, ?)", (scoreId, edition.name, None))
        res = cursor.lastrowid
    
    return res

def compareVoices(dbVoices, localVoices):
    if len(dbVoices) != len(localVoices):
        return False
    for dv in dbVoices:
        found = False
        index = 1
        for lv in localVoices:
            if dv[1] == index and ((lv is None and dv[3] is None and dv[4] is None) or (dv[3] == lv.range and dv[4] == lv.name)):
                found = True
            index += 1
        if not found:
            return False
    return True

def compareAuthors(dbAuthors, localAuthors, colIndex):
    if len(dbAuthors) != len(localAuthors):
        return False
    for de in dbAuthors:
        found = False
        for le in localAuthors:
            if de[colIndex] == le.name:
                found = True
        if not found:
            return False
    return True

def insertVoice(voice, scoreId, number, cursor):
    cursor.execute("SELECT * FROM voice WHERE number IS ? AND score IS ? AND range IS ? AND name IS ?",
                    (number, scoreId, (voice.range if voice is not None else None), (voice.name if voice is not None else None)))
    match = cursor.fetchone()

    if match is None:
        cursor.execute("INSERT INTO voice(number, score, range, name) VALUES(?, ?, ?, ?)", 
                        (number, scoreId, (voice.range if voice is not None else None), (voice.name if voice is not None else None)))

def insertEditionAuthor(editionId, editorId, cursor):
    cursor.execute("SELECT * FROM edition_author WHERE edition IS ? AND editor IS ?", (editionId, editorId,))
    match = cursor.fetchone()

    if match is None:
        cursor.execute("INSERT INTO edition_author(edition, editor) VALUES(?, ?)", (editionId, editorId))

def insertScoreAuthor(scoreId, composerId, cursor):
    cursor.execute("SELECT * FROM score_author WHERE score IS ? AND composer IS ?", (scoreId, composerId,))
    match = cursor.fetchone()

    if match is None:
        cursor.execute("INSERT INTO score_author(score, composer) VALUES(?, ?)", (scoreId, composerId))

def insertPrint(print, editionId, cursor):
    cursor.execute("SELECT * FROM print WHERE id IS ? AND partiture IS ? AND edition IS ?", (print.print_id, print.partiture, editionId))
    match = cursor.fetchone()

    if match is None:
        cursor.execute("INSERT INTO print(id, partiture, edition) VALUES(?, ?, ?)", (print.print_id, print.partiture, editionId))

def main():
    db = initDb(sys.argv[2], "scorelib.sql")
    insertData(module.load(sys.argv[1]), db)
    db.commit()
    db.close()

if __name__ == "__main__":
    main()
