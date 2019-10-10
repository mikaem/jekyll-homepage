import sys
import os
import re
from copy import copy

book_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

files = list(os.walk('_site/research'))[0][2]

def main():
    os.chdir(book_root)

    for f in files:
        b = open('_site/research/{}'.format(f))
        bs = b.read()
        b.close()
        bss = bs[bs.find('#References'):]

        for ref in re.findall('(https://doi.org/10[.][0-9]{4,}[^\s"/<>]*/[^\s"<>]+)', bss):
            print(ref)
            bss = re.sub(ref, '<a href="{0}">{1}</a>'.format(ref, ref[16:]), bss)

        for ref in re.findall('https://arxiv.org/abs/[0-9]{4,}.[0-9]{5,}', bss):
            print(ref)
            bss = re.sub(ref, '<a href="{0}">{0}</a>'.format(ref), bss)

        for ref in re.findall('https://folk.uio.no/mikaem/preprints/[\w\d]*.pdf', bss):
            print(ref)
            bss = re.sub(ref, '<a href="{0}">{1}</a>'.format(ref, ref[37:]), bss)

        b = open('_site/research/{}'.format(f), 'w')
        bs = bs[:bs.find('#References')] + bss
        b.write(bs)
        b.close()


if __name__ == '__main__':
    main()
