#!/usr/bin/env python3

'''Convert text from Alberto Elli's transliteration scheme
to unicode Coptic text for machine-assisted comparison with
other versions.

He published a version of ⲡⲃⲟⲓⲥ ⲛⲧⲙⲁⲕⲁⲣⲓⲁ ϩⲗⲗⲁⲣⲓⲁ as a free
PDF, along with a translation and glosses in Italian. Unfortunately
the Coptic and Egyptian transliteration are encoded in laten
letters, with a special font used to present the correct letter
forms. This script converts the Coptic transliteration scheme
to a standard encoding.

See https://mediterraneoantico.it/wp-content/uploads/2020/05/La-vita-di-Ilaria.pdf
'''

def convert(c):
    '''Map Latin transliteration to Coptic characters'''
    if c == 'a':
        return 'ⲁ'
    elif c == 'b':
        return 'ⲃ'
    elif c == 'g':
        return 'ⲅ'
    elif c == 'd':
        return 'ⲇ'
    elif c == 'e':
        return 'ⲉ'
    elif c == 'z':
        return 'ⲍ'
    elif c == 'H':
        return 'ⲏ'
    elif c == 'q':
        return 'ⲑ'
    elif c == 'i':
        return 'ⲓ'
    elif c == 'k':
        return 'ⲕ'
    elif c == 'l':
        return 'ⲗ'
    elif c == 'm':
        return 'ⲙ'
    elif c == 'n':
        return 'ⲛ'
    elif c == 'x':
        return 'ⲝ'
    elif c == 'o':
        return 'ⲟ'
    elif c == 'p':
        return 'ⲡ'
    elif c == 'r':
        return 'ⲣ'
    elif c == 's':
        return 'ⲥ'
    elif c == 't':
        return 'ⲧ'
    elif c == 'u':
        return 'ⲩ'
    elif c == 'P':
        return 'ⲫ'
    elif c == 'C':
        return 'ⲭ'
    elif c == 'T':
        return 'ⲯ'
    elif c == 'w':
        return 'ⲱ'
    elif c == 'y':
        return 'ϣ'
    elif c == 'f':
        return 'ϥ'
    elif c == 'h':
        return 'ϩ'
    elif c == 'j':
        return 'ϫ'
    elif c == 'c':
        return 'ϭ'
    elif c == 'Y':
        return 'ϯ'
    # punctuation
    elif c == '+':
        return '\u0304' # combining macron
    elif c == '.':
        return '·'
    # ligatures
    elif c == 'E':
        return 'ⲓ︤ⲥ︥'
    elif c == 'F':
        return 'ⲭ︤ⲥ︥'
    elif c == 'D':
        return 'ⲡ︤ⲛ︦ⲁ︥'
    # pass everthing else unchanged
    return c


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print(f'usage: {sys.argv[0]} <transliterated.txt>')
        sys.exit(1)

    with open(sys.argv[1]) as f:
        # Don't convert parenthetical annotations
        parenthetical = False
        for line in f.readlines():
            if line.startswith('#'):
                # skip headers/comments
                print(line)
                continue
            coptic = []
            for char in line:
                if char == '(':
                    parenthetical = True
                    coptic.append(char)
                elif char == ')':
                    parenthetical = False
                    coptic.append(char)
                elif char == '\n':
                    continue
                elif parenthetical:
                    coptic.append(char)
                else:
                    coptic.append(convert(char))
            coptic = ''.join(coptic)
            print(coptic)
