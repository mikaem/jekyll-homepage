.PHONY: help homepage clean serve

help:
	@echo "Please use 'make <target>' where <target> is one of:"
	@echo "  install     to install the necessary dependencies for jupyter-book to build"
	@echo "  homepage    to convert the `content/` folder into Jekyll markdown in `_build/`"
	@echo "  clean       to clean out site build files"
	@echo "  runall      to run all notebooks in-place, capturing outputs with the notebook"
	@echo "  serve       to serve the repository locally with Jekyll"
	@echo "  build       to build the site HTML locally with Jekyll and store in _site/"


install:
	gem install bundler
	bundle install

homepage:
	jupyter-book build --overwrite ./
	#python scripts/preprocess.py

bookex:
	jupyter-book build --execute --overwrite ./
	#python scripts/preprocess.py

runall:
	jupyter-book run ./content

clean:
	python scripts/clean.py

serve:
	bundle exec guard

build:
	bundle exec jekyll build
	touch _site/.nojekyll
	cp -r _site/. ../docs/

pdf:
	python scripts/create_pdf.py
