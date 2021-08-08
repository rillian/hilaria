#!/usr/bin/env python3

# Script to parse text out of a CSV file exported from Google Docs
# and mark it up for input into the Coptic Scriptorium ingest tooling.

import csv
import unicodedata

def read_text(infilename):
    with open(infilename, newline='') as infile:
        page = line = None
        longest = 0
        chars = set()
        reader = csv.reader(infile)
        # first row has the column headings
        header = reader.__next__()
        for row in reader:
            coptic = row[2]
            note = row[7]
            line_number = row[0]
            # fill in continuous line numbers
            try:
                page, line = map(int, line_number.split('.'))
            except ValueError:
                line += 1
                line_number = f'{page}.{line}'
            print(f'{line_number: ^5} : {coptic: <62} : {note}')
            longest = max(longest, len(coptic))
            chars.update(set(coptic))
    print(f'Longest Coptic line is {longest}')
    print('Characters in the text:')
    keys = list(chars)
    keys.sort()
    for key in keys:
        try:
            name = unicodedata.name(key)
        except ValueError:
            name = f'unnamed character'
        if key == '\n':
            name = 'newline'
        elif key == '\t':
            name = 'tab'
        if key.isprintable():
            label = key
        else:
            label = ' '
        print(f'  {label}\t{ord(key):04X}\t{name}')

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <filename.csv>')
        print()
        print('Parse the text of Hillaria out of a csv export.')
        exit(1)

    read_text(sys.argv[1])
