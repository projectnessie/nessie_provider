#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Hook definition for Nessie."""
from typing import Dict

from airflow.hooks.base import BaseHook
from pynessie import init
from pynessie import NessieClient


class NessieHook(BaseHook):
    """Nessie Hook.

    Exposes a Nessie client for actions against a Nessie server.

    :param nessie_conn_id: Nessie connection name

    """

    conn_name_attr = "nessie_conn_id"
    default_conn_name = "nessie_default"
    conn_type = "nessie"
    hook_name = "Nessie"

    @staticmethod
    def get_ui_field_behaviour() -> Dict:
        """Returns custom field behaviour."""
        return {
            "hidden_fields": ["port"],
            "relabeling": {"schema": "Branch", "host": "Nessie URI"},
        }

    def __init__(self: "NessieHook", nessie_conn_id: str = default_conn_name) -> None:
        """Nessie Hook.

        Exposes a Nessie client for actions against a Nessie server.

        :param nessie_conn_id: Nessie connection name

        """
        super().__init__()
        self.nessie_conn_id = nessie_conn_id

    def get_conn(self: "NessieHook") -> NessieClient:
        """Returns a Nessie Client."""
        conn = self.get_connection(self.nessie_conn_id)

        return init(config_dict={"endpoint": conn.host, "default_branch": conn.schema})

    def create_reference(self: "NessieHook", name: str, source_ref: str = "main", is_tag: bool = False) -> str:
        """Create a Reference on this Nessie server.

        :param name: name of reference to create
        :param source_ref: optionally which ref to use as base
        :param is_tag: create a Tag rather than a Branch
        """
        hash_ = self.get_conn().get_reference(source_ref).hash_
        return self.get_conn().create_branch(name, hash_).name

    def merge(self: "NessieHook", from_branch: str, onto_branch: str) -> None:
        """Perform a merge on a nessie branch.

        The end result of this operation will be that all commits from 'from_branch' are transplanted on to 'onto_branch'

        :param from_branch: ref to move commits from
        :param onto_branch: branch to move commits to
        """
        self.get_conn().merge(from_branch, onto_branch)
