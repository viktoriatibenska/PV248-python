import sys
import re
from collections import Counter

f = open(sys.argv[1], 'r', encoding='utf8')

command = sys.argv[2]

if command == 'composer':
    composers = []
    for line in f:
        r = re.compile( r"Composer: (.*)" )
        m = r.match(line)
        
        if m is None: continue

        clean = re.sub( r"\(.*\)", '', m.group(1) )
        clean = clean.split(';')
        clean = map(str.strip, clean)
        clean = list(filter(None, clean))
        composers.extend(clean)

    for composer, count in Counter(composers).most_common():
        print(composer + ': ' + str(count))
elif command == 'century':
    centuries = []
    for line in f:
        r = re.compile( r"Composition Year: (.*)" )
        m = r.match(line)

        if m is None or m.group(1) == '': continue

        clean = m.group(1).strip()
        
        # handle centuries specified as XXth century
        centuryRegexMatch = re.compile( r"[0-9]{2}th century" ).match(clean)
        if centuryRegexMatch is not None:
            centuries.append(int(centuryRegexMatch.group()[:2]))
            continue

        # handle dates in format nn. nn. nnnn
        datesRegexMatch = re.compile( r"[0-9]{1,2}. [0-9]{1,2}. [0-9]{4}" ).match(clean)
        if datesRegexMatch is not None:
            clean = datesRegexMatch.group()[-4:]

        # handle ranges such as 0000--0000
        rangeRegexMatch = re.compile( r"[0-9]{4}--[0-9]{4}" ).match(clean)
        if rangeRegexMatch is not None:
            clean = rangeRegexMatch.group()[:4]

        # remove all non digit characters
        clean = re.sub(r"\D", '', clean)
        if clean != '':
            centuries.append(int(clean[:2])+1)

    for century, count in Counter(centuries).most_common():
        print(str(century) + 'th century: ' + str(count))
