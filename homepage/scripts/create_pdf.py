import os
import re

book_root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
os.chdir(book_root)
os.system("mkdir _buildpdf")
os.chdir("_buildpdf")

fl = ''
href = {}
qref = {}
hcite = {}
aref = {}
for f in ('chapter3/intro',
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
          'solutions/poiseuille'):
    name = ''.join(f.split('/'))
    os.system("cp ../content/{0}.ipynb {1}.ipynb".format(f, name))
    os.system("jupyter nbconvert --to notebook --execute --inplace {0}.ipynb".format(name))
    b = open('{}.ipynb'.format(name))
    bs = b.read()
    b.close()
    for ref in set(re.findall(r'{% cite (\w*) %}', bs)):
        hh = hash(ref)
        hcite[hh] = ref
        bs = re.sub(r'{{% cite {0} %}}'.format(ref), str(hh), bs)

    for ref in set(re.findall(r'\[([\w\d\s]*)\]\(([\w\d\s/.]*).ipynb#mjx-eqn-([\w\d:-]*)\)', bs)):
        hh = hash(ref)
        qref[hh] = ref
        bs = re.sub(r'\[%s\]\(%s.ipynb#mjx-eqn-%s\)'%(ref), str(hh), bs)

    for ref in set(re.findall(r'\[([\w\d\s]*)\]\(([\w\d\s/..]*).ipynb#([\w\d-]*)\)', bs)):
        hh = hash(ref)
        href[hh] = ref
        bs = re.sub(r'\[%s\]\(%s.ipynb#%s\)'%(ref), str(hh), bs)

    for ref in set(re.findall(r'@anchor{([^{}]*)}', bs)):
        hh = hash(ref)
        aref[hh] = ref
        bs = re.sub("@anchor{%s}"%(ref), str(hh), bs)

    bs = re.sub(r'\$\\\\setCounter\{0\}\$', '', bs)
    bs = re.sub(r'\{:start.*\}', '', bs)
    bs = re.sub(r'{% bibliography --cited %}', '', bs)
    bs = re.sub(r'## References', '', bs)
    bs = re.sub(r'\$\$\\n', '', bs)
    b = open('{}.ipynb'.format(name), 'w')
    b.write(bs)
    b.close()

    os.system("jupyter nbconvert %s.ipynb --to latex --template=../scripts/mytmpl.tplx"%(name))

    h = open("%s.tex"%(name)).read()
    f0 = h.find('maketitle')+11
    f1 = h.find('end{document}')-1
    fl += h[f0:f1]

preamble = h[:h.find(r'\maketitle')+12]
title = r"""title{MEK4300 - Lecture Notes}
\\author{Prof. Mikael Mortensen}
"""
preamble = re.sub(r'title{%s}'%(name), title, preamble)
preamble += fl
preamble += r"""
\bibliographystyle{plain}
\bibliography{../_bibliography/references.bib}
\end{document}"""
b = open('book.tex', 'w')
for hh, ref in hcite.items():
    preamble = re.sub(r'%d'%(hh), r'\\cite{'+ref+r'}', preamble)
for hh, ref in href.items():
    if 'problem' in ref[0].lower():
        preamble = re.sub(r'%d'%(hh), r'Problem \\ref{'+ref[2].lower()+r'}', preamble)
    else:
        preamble = re.sub(r'%d'%(hh), r'Sec. \\ref{'+ref[2].lower()+r'}', preamble)
for hh, ref in qref.items():
    preamble = re.sub(r'%d'%(hh), r'Eq. \\eqref{'+ref[2]+r'}', preamble)
for hh, ref in aref.items():
    preamble = re.sub(r'%d'%(hh), r'\\label{'+ref+r'}', preamble)
b.write(preamble)
b.close()

os.system('latexmk -shell-escape -pdf book.tex')
os.chdir('../')
os.system('cp _buildpdf/book.pdf .')
