.PHONY: flake mypy pytest check html tox

flake:
	-poetry run flake8 || true

mypy:
	-poetry run mypy ambra_sdk || true

pytest:
	-poetry run pytest || true

check: flake mypy doctest pytest

html:
	-poetry run sphinx-build -b html docs/source docs/build || true
text:
	-poetry run sphinx-build -b text docs/source docs/build/texts || true
text-unify:
	-cat docs/build/texts/index.txt \
             docs/build/texts/installation.txt \
             docs/build/texts/quickstart.txt \
             docs/build/texts/service_api.txt \
             docs/build/texts/storage_api.txt \
             docs/build/texts/addon.txt \
             docs/build/texts/faq.txt > docs/build/texts/single.txt || true
doctest:
	-poetry run sphinx-build -b doctest docs/source docs/build || true
spelling:
	-poetry run sphinx-build -b spelling docs/source docs/build || true
gh:
	-poetry run sphinx-build -b html docs/source ../sdk-python-doc || true
	-touch ../sdk-python-doc/.nojekyll
tox:
	-poetry run tox || true
