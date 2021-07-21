# Nessie Airflow Provider

<p align="center">
    <em></em>
</p>

[![build](https://github.com/projectnessie/nessie_provider/workflows/Build/badge.svg)](https://github.com/projectnessie/nessie_provider/actions)
[![codecov](https://codecov.io/gh/projectnessie/nessie_provider/branch/master/graph/badge.svg)](https://codecov.io/gh/projectnessie/nessie_provider)
[![PyPI version](https://badge.fury.io/py/airflow-provider-nessie.svg)](https://badge.fury.io/py/airflow-provider-nessie)

---

**Documentation**: <a href="https://projectnessie.github.io/nessie_provider" target="_blank">https://projectnessie.github.io/nessie_provider</a>

**Source Code**: <a href="https://github.com/projectnessie/nessie_provider" target="_blank">https://github.com/projectnessie/nessie_provider</a>

---

## Usage

To use in airflow install via pip `pip install airflow-provider-nessie`. See [Nessie Documentation](https://projectnessie.org/try) for
instructions on starting and using a Nessie server.

### Operators and Hooks

To interact with Nessie from an airflow DAG you have the following options:

* Nessie Hook: register as a connection w/ Airflow and store your Nessie url and credentials
* Create reference operator: Create a Branch or Tag as part of an airflow DAG
* Delete reference operator: Delete a Branch or Tag as part of an airflow DAG
* Commit operator: commit objects to the Nessie database on a given branch
* Merge operator: merge one branch into another

These can be seen in action by looking at the [Example DAGs](https://github.com/projectnessie/nessie_provider/tree/master/airflow_provider_nessie/example_dags).
The `basic_nessie.py` DAG shows each operator in action and the `spark_nessie_iceberg.py` DAG shows a more complicated example of performing an iceberg
transaction in Nessie from the Spark operator.

## Development

### Setup environement

You should have [Pipenv](https://pipenv.readthedocs.io/en/latest/) installed. Then, you can install the dependencies with:

```bash
pipenv install --dev
```

After that, activate the virtual environment:

```bash
pipenv shell
```

### Run unit tests

You can run all the tests with:

```bash
make test
```

Alternatively, you can run `pytest` yourself:

```bash
pytest
```

### Format the code

Execute the following command to apply `isort` and `black` formatting:

```bash
make format
```

## License

This project is licensed under the terms of the Apache Software License 2.0.
