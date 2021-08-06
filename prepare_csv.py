#!/usr/bin/env python3

# Script to parse text out of a CSV file exported from Google Docs
# and mark it up for input into the Coptic Scriptorium ingest tooling.

import csv

def read_text(infilename):
    with open(infilename, newline='') as infile:
        reader = csv.reader(infile)
        for row in reader:
            print(f'{row[0]: ^5} : {row[2]}')

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <filename.csv>')
        print()
        print('Parse the text of Hillaria out of a csv export.')
        exit(1)

    read_text(sys.argv[1])
