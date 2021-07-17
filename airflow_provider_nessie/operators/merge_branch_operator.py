# -*- coding: utf-8 -*-
"""Merge branch operator module."""
from typing import Any, Dict

from airflow.models import BaseOperator
from airflow.sensors.base import apply_defaults

from ..hooks.nessie_hook import NessieHook


class MergeOperator(BaseOperator):
    """Operator to merge a branch in Nessie."""

    @apply_defaults
    def __init__(
        self: "MergeOperator",
        conn_id: str = "nessie_default",
        from_branch: str = None,
        onto_branch: str = "main",
        *args: Any,
        **kwargs: Any
    ) -> None:
        """Merge a branch on nessie server given by conn_id.

        :param conn_id: conn id of a nessie server
        :param from_branch: ref to move commits from
        :param onto_branch: branch to move commits to
        :param args: extra args for BaseOperator
        :param kwargs: extra args for BaseOperator
        """
        super().__init__(*args, **kwargs)
        self.conn_id = conn_id
        if from_branch is None:
            raise Exception("Cannot have a null branch for commit operations")
        self.from_branch = from_branch
        self.onto_branch = onto_branch

    def execute(self: "MergeOperator", context: Dict[str, Any]) -> None:
        """Perform actual create branch operation.

        :param context: unused
        """
        hook = NessieHook(conn_id=self.conn_id)

        hook.merge(self.from_branch, self.onto_branch)
