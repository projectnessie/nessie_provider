# -*- coding: utf-8 -*-
"""Entry point for the Nessie Airflow provider.

Contains important descriptions for registering to Airflow
"""

__version__ = "0.1.2"


def get_provider_info() -> dict:
    """Hook for Airflow."""
    return {
        "package-name": "airflow-provider-nessie",
        "name": "Nessie Airflow Provider",
        "description": "An Airflow provider for Project Nessie",
        "hook-class-names": ["airflow_provider_nessie.hooks.nessie_hook.NessieHook"],
        "versions": [__version__],
    }
