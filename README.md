# Nessie Airflow Provider

<p align="center">
    <em></em>
</p>

[![build](https://github.com/projectnessie/nessie_provider/workflows/Build/badge.svg)](https://github.com/projectnessie/nessie_provider/actions)
[![codecov](https://codecov.io/gh/projectnessie/nessie_provider/branch/master/graph/badge.svg)](https://codecov.io/gh/projectnessie/nessie_provider)
[![Dependabot Status](https://api.dependabot.com/badges/status?host=github&repo=projectnessie/nessie_provider)](https://dependabot.com)
[![PyPI version](https://badge.fury.io/py/airflow-provider-nessie.svg)](https://badge.fury.io/py/airflow-provider-nessie)

---

**Documentation**: <a href="https://projectnessie.github.io/nessie_provider" target="_blank">https://projectnessie.github.io/nessie_provider</a>

**Source Code**: <a href="https://github.com/projectnessie/nessie_provider" target="_blank">https://github.com/projectnessie/nessie_provider</a>

---

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
