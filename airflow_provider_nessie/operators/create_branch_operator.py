# -*- coding: utf-8 -*-
"""Create branch operator module."""
from typing import Any, Dict

from airflow.models import BaseOperator
from airflow.sensors.base import apply_defaults

from ..hooks.nessie_hook import NessieHook


class CreateBranchOperator(BaseOperator):
    """Operator to create a branch in Nessie."""

    @apply_defaults
    def __init__(
        self: "CreateBranchOperator",
        conn_id: str = "nessie_default",
        branch: str = None,
        source_branch: str = "main",
        *args: Any,
        **kwargs: Any
    ) -> None:
        """Create a branch on nessie server given by conn_id.

        :param conn_id: conn id of a nessie server
        :param branch: name of branch to create
        :param source_branch: source to base branch off of
        :param args: extra args for BaseOperator
        :param kwargs: extra args for BaseOperator
        """
        super().__init__(*args, **kwargs)
        self.conn_id = conn_id
        if branch is None:
            raise Exception("Cannot have a null branch for commit operations")
        self.branch = branch
        self.source_branch = source_branch

    def execute(self: "CreateBranchOperator", context: Dict[str, Any]) -> Any:
        """Perform actual create branch operation.

        :param context: unused
        :return: created reference
        """
        hook = NessieHook(conn_id=self.conn_id)

        ref = hook.create_reference(self.branch, self.source_branch)

        return ref
