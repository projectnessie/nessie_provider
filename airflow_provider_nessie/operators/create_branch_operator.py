# -*- coding: utf-8 -*-
"""Create branch operator module."""
from typing import Any
from typing import Dict

from airflow.models import BaseOperator

from ..hooks.nessie_hook import NessieHook


class CreateBranchOperator(BaseOperator):
    """Operator to create a branch in Nessie."""

    def __init__(self: "CreateBranchOperator", nessie_conn_id: str, branch: str, source_branch: str = "main", **kwargs: Any) -> None:
        """Create a branch on nessie server given by nessie_conn_id.

        :param nessie_conn_id: conn id of a nessie server
        :param branch: name of branch to create
        :param source_branch: source to base branch off of
        :param kwargs: extra args for BaseOperator
        """
        super().__init__(**kwargs)
        self.nessie_conn_id = nessie_conn_id
        self.branch = branch
        self.source_branch = source_branch

    def execute(self: "CreateBranchOperator", context: Dict[str, Any]) -> Any:
        """Perform actual create branch operation.

        :param context: unused
        :return: created reference
        """
        hook = NessieHook(nessie_conn_id=self.nessie_conn_id)

        ref = hook.create_reference(self.branch, self.source_branch)

        return ref
