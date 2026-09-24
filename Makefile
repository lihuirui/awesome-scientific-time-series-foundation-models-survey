.PHONY: all search screen bib figures readme paper check clean

all: search screen bib figures readme paper check

search:
	python3 scripts/search.py

screen:
	python3 scripts/screen.py

bib:
	python3 scripts/generate_bib.py

figures:
	python3 scripts/generate_figures.py

readme:
	python3 scripts/generate_readme.py

paper: bib figures
	cd paper && tectonic main.tex

check:
	python3 scripts/check.py

clean:
	rm -f paper/*.aux paper/*.bbl paper/*.blg paper/*.log paper/*.out paper/*.xdv
