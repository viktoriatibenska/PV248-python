import sys
import re

class Print:
    def __init__(self, edition, print_id, partiture):
        self.edition = edition
        self.print_id = print_id
        self.partiture = partiture
    def format(self):
        result = ""

        result += "Print Number:" + putSpace(str(self.print_id)) + "\n"
        result += "Composer:" + putSpace(printPeople(self.composition().authors, ";")) + "\n"
        result += "Title:" + putSpace(checkNone(self.composition().name)) + "\n"
        result += "Genre:" + putSpace(checkNone(self.composition().genre)) + "\n"
        result += "Key:" + putSpace(checkNone(self.composition().key)) + "\n"
        result += "Composition Year:" + putSpace(str(checkNone(self.composition().year))) + "\n"
        result += "Edition:" + putSpace(checkNone(self.edition.name)) + "\n"
        result += "Editor:" + putSpace(printPeople(self.edition.authors, ",")) + "\n"
        result += printVoices(self.composition().voices)
        result += "Partiture:" + putSpace(("yes" if self.partiture else "no")) + "\n"
        result += "Incipit:" + putSpace(checkNone(self.composition().incipit))

        print(result)
    def composition(self):
        return self.edition.composition

class Edition:
    def __init__(self, composition, authors, name):
        self.composition = composition
        self.authors = authors
        self.name = name

class Composition:
    def __init__(self, name, incipit, key, genre, year, voices, authors):
        self.name = name
        self.incipit = incipit
        self.key = key
        self.genre = genre
        self.year = year
        self.voices = voices
        self.authors = authors

class Voice:
    def __init__(self, name, range):
        self.name = name
        self.range = range

class Person:
    def __init__(self, name, born, died):
        self.name = name
        self.born = born
        self.died = died

def checkNone(value):
    if value == None:
        return ""
    else:
        return value

def intNone(value):
    if value is None:
        return None
    else:
        return int(value)

def putSpace(value):
    if value == "":
        return value
    else:
        return " " + value

def printVoices(voices):
    result = ""
    i = 1

    for v in voices:
        result += "Voice " + str(i) + ": "

        if v != None:
            if v.range != None and v.name != None:
                result += v.range + ", " + v.name
            elif v.range != None and v.name == None:
                result += v.range
            elif v.range == None and v.name != None:
                result += v.name

        i += 1
        result += '\n'

    return result

def printPeople(people, separator):
    result = ""
    i = 1

    for p in people:
        if i != 1:
            result += separator + " "

        result += p.name

        if p.born != None or p.died != None:
            result += " (" + str(checkNone(p.born)) + "--" + str(checkNone(p.died)) + ")"

        i = i + 1

    return result

def parsePeople(people, deliminator):
    result = []
    
    if people != None:
        clean = people.split(';')
        clean = map(str.strip, clean)
        clean = list(filter(None, clean))
        
        starR = re.compile( r".*\(\*([0-9]{4})\)" )
        crossR = re.compile( r".*\(\+([0-9]{4})\)" )
        dashR = re.compile( r".*\(([0-9]{4})?(-{1,2})([0-9]{4})?\)" )
        for item in clean:
            name = re.sub( r"\(.*\)", '', item )
            name = name.strip()

            dashM = dashR.match(item)
            starM = starR.match(item)
            crossM = crossR.match(item)

            if dashM is not None:
                result.append(Person(name, intNone(dashM.group(1)), intNone(dashM.group(3))))
            elif starM is not None:
                result.append(Person(name, int(starM.group(1)), None))
            elif crossM is not None:
                result.append(Person(name, None, int(crossM.group(1))))
            else:
                result.append(Person(name, None, None))

    return result

def parseEditors(editors):
    result = []

    clean = re.sub( r"\(.*\)", '', editors )
    clean = clean.split(',')
    clean = map(str.strip, clean)
    clean = list(filter(None, clean))

    name = ""

    for item in clean:
        if name == "":
            name += item
        else:
            if item.find(' ') == -1:
                name += ", " + item
                result.append(Person(name, None, None))
                name = ""
            else:
                result.append(Person(name, None, None))
                result.append(Person(item, None, None))
                name = ""

    if name != "":
        result.append(Person(name, None, None))

    return result

def parseVoices(dict):
    result = []

    index = 1

    rangeR = re.compile ( r"(.*?--.*?)($|\,)(.*)" )
    while 'Voice ' + str(index) in dict:
        voice = dict['Voice ' + str(index)]

        if voice is None:
            result.append(None)
        else:
            voice = voice.replace(';', ',')
            rangeM = rangeR.match(voice)

            if rangeM is not None:
                tmpRange = rangeM.group(1).strip()
                tmpName = rangeM.group(3).strip()

                if tmpName == "":
                    result.append(Voice(None, tmpRange))
                else:
                    result.append(Voice(tmpName, tmpRange))
            else:
                result.append(Voice(voice, None))

        index += 1

    return result

def parsePrintItem(item):
    p = Print(None, None, None)
    
    # Print Number
    p.print_id = int(item['Print Number'])

    # Partiture
    if item['Partiture'] != None and item['Partiture'].find("yes") is not -1:
        p.partiture = True
    else:
        p.partiture = False

    # Edition name
    p.edition = Edition(None, None, item['Edition'])

    # Authors - Editors
    if 'Editor' in item:
        if item['Editor'] is None:
            p.edition.authors = []
        else:
            p.edition.authors = parseEditors(item['Editor'])
    else:
        p.edition.authors = []

    ## Composition
    p.edition.composition = Composition(item['Title'], 
                                        item['Incipit'], 
                                        None, None, None, None, None)
    
    # Genre
    if 'Genre' in item:
        p.edition.composition.genre = item['Genre']
    else:
        p.edition.composition.genre = None

    # Key
    if 'Key' in item:
        p.edition.composition.key = item['Key']
    else:
        p.edition.composition.key = None

    # Composers - authors
    p.edition.composition.authors = parsePeople(item['Composer'], ";")

    # Composition year
    if 'Composition Year' in item and item['Composition Year'] != None:
        yearR = re.compile( r"[0-9]{4}" )
        yearM = yearR.match(item['Composition Year'])
        if yearM is not None:
            p.edition.composition.year = int(yearM.group(0))
        else:
            p.edition.composition.year = None
    else:
        p.edition.composition.year = None

    # Voices
    p.edition.composition.voices = parseVoices(item)

    return p

def load(filename):
    result = []
    f = open(filename, 'r', encoding='utf8')
    printItem = {}

    lineR =  re.compile( r"(.*?): (.*)" )

    for line in f:
        lineM = lineR.match(line)

        if lineM is None:
            continue

        label = lineM.group(1).strip()
        value = lineM.group(2).strip()

        if value != '':
            printItem[label] = value
        else:
            printItem[label] = None

        #print(label + ": " + ("" if printItem[label] == None else printItem[label]))

        if label == 'Incipit':
            result.append(parsePrintItem(printItem))
            printItem = {}

    return sorted(result, key=lambda x: x.print_id)
    