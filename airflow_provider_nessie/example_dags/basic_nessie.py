# -*- coding: utf-8 -*-

from airflow.models import DAG
from airflow.operators.dummy import DummyOperator
from airflow.utils.dates import days_ago
from pynessie.model import ContentsKey
from pynessie.model import DeltaLakeTable
from pynessie.model import IcebergTable
from pynessie.model import Put
from pynessie.model import SqlView

from airflow_provider_nessie.operators.commit_operator import CommitOperator
from airflow_provider_nessie.operators.create_branch_operator import CreateBranchOperator
from airflow_provider_nessie.operators.delete_branch_operator import DeleteBranchOperator
from airflow_provider_nessie.operators.merge_branch_operator import MergeOperator

default_args = {
    "owner": "airflow",
}
with DAG(
    dag_id="example_nessie_operator",
    default_args=default_args,
    schedule_interval=None,
    start_date=days_ago(2),
    tags=["example", "nessie"],
) as dag:

    op1 = [Put(ContentsKey(["prod", "sales", "customers"]), IcebergTable("uuid", "/path/to/tableA"))]
    op2 = [Put(ContentsKey(["prod", "sales", "orders"]), IcebergTable("uuid", "/path/to/tableB"))]
    op3 = [Put(ContentsKey(["prod", "sales", "lineitems"]), IcebergTable("uuid", "/path/to/tableC"))]
    op4 = [Put(ContentsKey(["prod", "sales", "all_orders"]), IcebergTable("uuid", "/path/to/tableD"))]
    op5 = [Put(ContentsKey(["prod", "marketing", "campaigns"]), DeltaLakeTable("uuid", "100", ["99", "98"], ["97"]))]
    op6 = [Put(ContentsKey(["prod", "marketing", "clean_campaigns"]), DeltaLakeTable("uuid", "100", ["99", "98"], ["97"]))]
    op7 = [Put(ContentsKey(["prod", "reports", "campaign_performance"]), IcebergTable("uuid", "/path/to/tableE"))]
    op8 = [
        Put(
            ContentsKey(["prod", "reports", "campaign_performance_bi"]),
            SqlView("uuid", "HIVE", "SELECT * from nessie.prod.reports.campaign_performance"),
        )
    ]

    iceberg_task_1 = CommitOperator(conn_id="nessie-default", branch="test", reason="Iceberg Append 1", ops=op1, task_id="IcebergCommit1")
    iceberg_task_2 = CommitOperator(conn_id="nessie-default", branch="test", reason="Iceberg Append 2", ops=op2, task_id="IcebergCommit2")
    iceberg_task_3 = CommitOperator(conn_id="nessie-default", branch="test", reason="Iceberg Append 3", ops=op3, task_id="IcebergCommit3")
    transform_task_1 = CommitOperator(
        conn_id="nessie-default", branch="test", reason="Transform Task 1", ops=op4, task_id="IcebergTransform"
    )
    delta_task_1 = CommitOperator(conn_id="nessie-default", branch="test", reason="Delta Commit 1", ops=op5, task_id="DeltaCommit1")
    transform_task_2 = CommitOperator(conn_id="nessie-default", branch="test", reason="Transform Task 2", ops=op6, task_id="DeltaTransform")
    materialization_task_1 = CommitOperator(
        conn_id="nessie-default", branch="test", reason="Materialization Task 1", ops=op7, task_id="Materialization"
    )
    sql_view_task_1 = CommitOperator(conn_id="nessie-default", branch="test", reason="SqlView Task 1", ops=op8, task_id="UpdateSqlView")
    data_quality_check = DummyOperator(task_id="DataQualityCheck")

    create_branch = CreateBranchOperator(conn_id="nessie-default", branch="test", task_id="CreateEtlBranch")
    merge_branch = MergeOperator(conn_id="nessie-default", from_branch="test", task_id="MergeEtlBranch")
    delete_branch = DeleteBranchOperator(conn_id="nessie-default", branch="test", task_id="DeleteEtlBranch")
    create_branch >> [iceberg_task_1, iceberg_task_2, iceberg_task_3] >> transform_task_1 >> materialization_task_1
    transform_task_1 >> sql_view_task_1
    create_branch >> delta_task_1 >> transform_task_2 >> materialization_task_1
    transform_task_2 >> sql_view_task_1
    materialization_task_1 >> [data_quality_check, sql_view_task_1] >> merge_branch >> delete_branch
