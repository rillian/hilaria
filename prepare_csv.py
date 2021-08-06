#!/usr/bin/env python3

# Script to parse text out of a CSV file exported from Google Docs
# and mark it up for input into the Coptic Scriptorium ingest tooling.

import csv

def read_text(infilename):
    with open(infilename, newline='') as infile:
        longest = 0
        reader = csv.reader(infile)
        for row in reader:
            print(f'{row[0]: ^5} : {row[2]: <62} : {row[7]}')
            longest = max(longest, len(row[2]))
    print(f'Longest Coptic line is {longest}')

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <filename.csv>')
        print()
        print('Parse the text of Hillaria out of a csv export.')
        exit(1)

    read_text(sys.argv[1])
