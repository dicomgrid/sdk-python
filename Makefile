.PHONY: flake mypy pytest check html tox

flake:
	-poetry run flake8 || true

mypy:
	-poetry run mypy ambra_sdk || true

pytest:
	-poetry run pytest || true

check: flake mypy pytest

html:
	-poetry run sphinx-build -b html docs/source docs/build || true
doctest:
	-poetry run sphinx-build -b doctest docs/source docs/build || true
gh:
	-poetry run sphinx-build -b html docs/source ../sdk-python-doc || true
	-touch ../sdk-python-doc/.nojekyll
tox:
	-poetry run tox || true
