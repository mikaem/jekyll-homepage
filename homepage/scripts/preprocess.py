import sys
import os
import re
from copy import copy

book_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

files = ('chapter3/intro',
         'chapter3/planeshearflow',
         'chapter3/couette',
         'chapter3/poiseuille',
         'chapter3/similarity',
         'chapter3/stokes',
         'chapter4/intro',
         'fenics/intro',
         'fenics/nonlinear',
         'mandatory/mandatory1',
         'solutions/couette',
         'solutions/poiseuille')

def main():
    os.chdir(book_root)

    for f in files:
        b = open('_build/{}.md'.format(f))
        bs = b.read()
        b.close()

        for ref in set(re.findall(r'\[([\w\d\s]*)\]\(([\w\d\s/.]*).ipynb#mjx-eqn-([\w\d:-]*)\)', bs)):
            print(ref)
            ref1 = ref[1].strip('.').lstrip('/') if '/' in ref[1] else f
            bs = re.sub('\[%s\]\(%s.ipynb#mjx-eqn-%s\)'%(ref), '[%s](%s#mjx-eqn-%s)'%(ref[0], '/MEK4300-lecturenotes/'+ref1+'.html', ref[2]), bs)

        for ref in set(re.findall(r'@anchor{([^{}]*)}', bs)):
            print(ref)
            bs = re.sub('@anchor{%s}'%(ref), '<a id="%s"></a>'%(ref), bs)

        for ref in set(re.findall(r'\[([\w\d\s]*)\]\(([\w\d\s/..]*).ipynb#([\w\d-]*)\)', bs)):
            print(ref)
            ref1 = ref[1].strip('.').lstrip('/') if '/' in ref[1] else f
            bs = re.sub(r'\[%s\]\(%s.ipynb#%s\)'%(ref), r'[%s](%s#%s)'%(ref[0], '/MEK4300-lecturenotes/'+ref1+'.html', ref[2].lower()), bs)

        b = open('_build/{}.md'.format(f), 'w')
        b.write(bs)
        b.close()


if __name__ == '__main__':
    main()
