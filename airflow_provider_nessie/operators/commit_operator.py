# -*- coding: utf-8 -*-
"""Create branch operator module."""
from typing import Any, Dict, List

from airflow.models import BaseOperator
from airflow.sensors.base import apply_defaults
from pynessie.model import Operation

from ..hooks.nessie_hook import NessieHook


class CommitOperator(BaseOperator):
    """Operator to create a branch in Nessie."""

    @apply_defaults
    def __init__(
        self: "CommitOperator",
        conn_id: str = "nessie_default",
        branch: str = None,
        reason: str = "",
        ops: List[Operation] = None,
        *args: Any,
        **kwargs: Any
    ) -> None:
        """Create a branch on nessie server given by conn_id.

        :param conn_id: conn id of a nessie server
        :param branch: name of branch to create
        :param reason: Commit message
        :param args: extra args for BaseOperator
        :param kwargs: extra args for BaseOperator
        """
        super().__init__(*args, **kwargs)
        self.conn_id = conn_id
        if branch is None:
            raise Exception("Cannot have a null branch for commit operations")
        self.branch = branch
        self.reason = reason
        if ops is None:
            raise Exception("Ops argument cannot be None. Must commit some operations.")
        self.ops = ops

    def execute(self: "CommitOperator", context: Dict[str, Any]) -> Any:
        """Perform actual create branch operation.

        :param context: airflow context
        :return: created reference
        """
        task_id = context["task"].task_id
        run_id = context["run_id"]
        author = context["task"].owner
        hook = NessieHook(conn_id=self.conn_id)

        hook.commit(
            self.branch,
            hook.get_conn().get_reference(self.branch).hash_,
            self.reason,
            author,
            *self.ops,
            task_id=task_id,
            run_id=run_id,
            application_type="airflow"
        )
