run:
	python -m pipenv run python neuralut/app.py

test:
	python -m pipenv run pytest

raw-test:
	python -m pipenv run python neuralut/rawtest.py
