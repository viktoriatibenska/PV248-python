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
        #clean = clean.strip()
        clean = list(filter(None, clean))
        composers.extend(clean)

    for composer, count in Counter(composers).most_common():
        print(composer + ': ' + str(count))
elif command == 'century':
    print('century')
