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


class Line:
    '''Represent a line of coptic text with associated reference and notes.'''
    def __init__(self, ref, coptic, note):
        self.ref = ref
        self.coptic = coptic
        self.note = note

    def __str__(self):
        return f'{str(self.ref): ^5} : {self.coptic: <62} : {self.note}'


def read_text(infilename):
    text = []
    with open(infilename, newline='') as infile:
        ref = None
        longest = 0

        reader = csv.reader(infile)
        # first row has the column headings
        header = reader.__next__()

        for row in reader:
            coptic = row[2]
            note = row[7]
            # Parse the page and line reference.
            try:
                newref = LineRef.from_str(row[0])
                if ref and newref.page == ref.page and newref.line != ref.line + 1:
                    print(f'Warning: Line numbering off: Found {newref} following {ref}')
                ref = newref
            except ValueError:
                # Otherwise calculate the next expected line number.
                ref.increment()

            longest = max(longest, len(coptic))

            # Must construct a new LineRef for eac each lime, otherwise
            # the Line object will hold a refence which updates at the
            # same time as our local instance.
            lineref = LineRef(ref.page, ref.line)
            line = Line(lineref, coptic, note)
            text.append(line)
            print(line)

    print(f'Longest Coptic line is {longest}')
    return text


def analyse_chars(text):
    '''Report a list of unicode characters used in the text.'''

    chars = set()
    for line in text:
        chars.update(set(line.coptic))

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
        if unicodedata.combining(key):
            label = '\u25CC' + key
        elif key.isprintable():
            label = key
        else:
            label = ' '
        print(f'  {label}\t{ord(key):04X}\t{name}')


def check_macrons(text):
    '''Report issues with combining marks.'''
    for line in text:
        if '\u0305' in line.coptic:
            print(f'Error: line {line.ref} contains U+0305 Combining Overbar.')
            offset = line.coptic.find('\u0305')
            print(f'  {line.coptic}')
            print(f'  {" " * offset}^')
            print('Consider U+0304 Combining Macron instead.\n')
        if '\u2CEF' in line.coptic:
            print(f'Error: line {line.ref} contains U+2CEF Combining Ni.')
            offset = line.coptic.find('\u2CEF')
            print(f'  {line.coptic}')
            print(f'  {" " * offset}^')
            print('Consider U+0304 Combining Macron instead.\n')


def check_punctuation(text):
    '''Report issues with punctuation marks.'''
    for line in text:
        if '.' in line.coptic:
            print(f'Error: line {line.ref} contains a period.')
            offset = line.coptic.find('.')
            print(f'  {line.coptic}')
            print(f'  {" " * offset}^')
            print('Consider U+00B7 Middle Dot instead.\n')
        elif ',' in line.coptic:
            print(f'Error: line {line.ref} contains a comma.')
            offset = line.coptic.find('.')
            print(f'  {line.coptic}')
            print(f'  {" " * offset}^')
            print('This is not native Coptic punctuation.\n')


def check_whitespace(text):
    '''Report issues with leading/trailing whitespace.'''
    for line in text:
        if line.coptic != str.strip(line.coptic):
            leading = line.coptic[0].isspace()
            trailing = line.coptic[:1].isspace()
            if line.coptic.endswith('\n'):
                print(f'Warning: line {line.ref} contains an extra newline.')
                print(f'  "...{line.coptic[-10:-1]}\\n"')
            elif leading and trailing:
                print(f'Warning: line {line.ref} contains both leading and trailing whitespace.')
                print(f'  "{line.coptic[:5]}...{line.coptic[-5:]}"')
            elif leading:
                print(f'Warning: line {line.ref} contains leading whitespace.')
                print(f'  "{line.coptic[:10]}..."')
            else:
                print(f'Warning: line {line.ref} contains trailing whitespace.')
                print(f'  "...{line.coptic[-10:]}"')


def construct_markdown(text):
    '''Construct a markdown version of the text.'''

    # format lines in a table, since markdown doesn't support <ol> with
    # our multilevel reference line numbers.
    headings = ('ref', 'coptic text')
    headings = map(lambda head: ' ' + head + ' ', headings)
    md = '|'.join(headings) + '\n'
    dividers = map(lambda head: '-' * len(head), headings)
    md += '|'.join(dividers) + '\n'

    for line in text:
        md += f'{line.ref}|{line.coptic}\n'

    return md


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <filename.csv>')
        print()
        print('Parse the text of Hillaria out of a csv export.')
        exit(1)

    text = read_text(sys.argv[1])
    analyse_chars(text)
    check_macrons(text)
    check_punctuation(text)
    check_whitespace(text)

    md = construct_markdown(text)
    print(md)
