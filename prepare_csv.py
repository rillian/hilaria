#!/usr/bin/env python3

# Script to parse text out of a CSV file exported from Google Docs
# and mark it up for input into the Coptic Scriptorium ingest tooling.

import csv
import unicodedata

class LineRef:
    '''Represent a `page.line` style reference

       This is the scheme used in Drescher's transcription.
       We provide a string representation so it can be printed
       as normal.'''
    def __init__(self, page, line):
        self.page = page
        self.line = line

    def __str__(self):
        return f'{self.page}.{self.line}'

    def increment(self):
        '''Increment the line number'''
        self.line += 1

    @classmethod
    def from_str(cls, string):
        '''Construct a new representation from a str'''
        page, line = map(int, string.split('.'))
        return cls(page, line)



def read_text(infilename):
    with open(infilename, newline='') as infile:
        ref = None
        longest = 0
        chars = set()
        reader = csv.reader(infile)
        # first row has the column headings
        header = reader.__next__()
        for row in reader:
            coptic = row[2]
            note = row[7]
            # Parse the page and line reference.
            try:
                ref = LineRef.from_str(row[0])
            except ValueError:
                # Otherwise calculate the next expected line number.
                ref.increment()
            print(f'{str(ref): ^5} : {coptic: <62} : {note}')
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
