PIPENV_RUN := pipenv run

flake8:
	$(PIPENV_RUN) flake8 airflow_provider_nessie tests --exclude "airflow_provider_nessie/example_dags/*"

safety:
	$(PIPENV_RUN) safety check

mypy:
	$(PIPENV_RUN) mypy --ignore-missing-imports -p airflow_provider_nessie

isort-src:
	$(PIPENV_RUN) isort ./airflow_provider_nessie

isort-docs:
	$(PIPENV_RUN) isort -rc ./docs/src -o airflow_provider_nessie

format: isort-src isort-docs
	$(PIPENV_RUN) black .

test:
	$(PIPENV_RUN) pytest --cov=airflow_provider_nessie/

check: flake8 mypy test

docs-serve:
	$(PIPENV_RUN) mkdocs serve

docs-publish:
	$(PIPENV_RUN) mkdocs gh-deploy

bumpversion-major:
	$(PIPENV_RUN) bumpversion major

bumpversion-minor:
	$(PIPENV_RUN) bumpversion minor

bumpversion-patch:
	$(PIPENV_RUN) bumpversion patch
