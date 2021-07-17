# -*- coding: utf-8 -*-
"""Merge branch operator module."""
from typing import Any
from typing import Dict

from airflow.models import BaseOperator

from ..hooks.nessie_hook import NessieHook


class MergeOperator(BaseOperator):
    """Operator to merge a branch in Nessie."""

    def __init__(self: "MergeOperator", nessie_conn_id: str, from_branch: str, onto_branch: str = "main", **kwargs: Any) -> None:
        """Merge a branch on nessie server given by nessie_conn_id.

        :param nessie_conn_id: conn id of a nessie server
        :param from_branch: ref to move commits from
        :param onto_branch: branch to move commits to
        :param kwargs: extra args for BaseOperator
        """
        super().__init__(**kwargs)
        self.nessie_conn_id = nessie_conn_id
        self.from_branch = from_branch
        self.onto_branch = onto_branch

    def execute(self: "MergeOperator", context: Dict[str, Any]) -> None:
        """Perform actual create branch operation.

        :param context: unused
        """
        hook = NessieHook(nessie_conn_id=self.nessie_conn_id)

        hook.merge(self.from_branch, self.onto_branch)
