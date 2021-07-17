#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Hook definition for Nessie."""
from typing import Any, Dict, Optional

from airflow.hooks.base import BaseHook
from pynessie import init
from pynessie import NessieClient
from pynessie._endpoints import commit
from pynessie.model import CommitMeta
from pynessie.model import Contents
from pynessie.model import ContentsKey
from pynessie.model import Delete
from pynessie.model import MultiContents
from pynessie.model import MultiContentsSchema
from pynessie.model import Operation
from pynessie.model import Put


class NessieHook(BaseHook):
    """Nessie Hook.

    Exposes a Nessie client for actions against a Nessie server.

    :param conn_id: Nessie connection name

    """

    conn_name_attr = "conn_id"
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

    def __init__(self: "NessieHook", conn_id: str = default_conn_name) -> None:
        """Nessie Hook.

        Exposes a Nessie client for actions against a Nessie server.

        :param conn_id: Nessie connection name

        """
        super().__init__()
        self.conn_id = conn_id

    def get_conn(self: "NessieHook") -> NessieClient:
        """Returns a Nessie Client."""
        conn = self.get_connection(self.conn_id)

        return init(config_dict={"endpoint": conn.host, "default_branch": conn.schema})

    def create_reference(self: "NessieHook", name: str, source_ref: str = "main", is_tag: bool = False) -> str:
        """Create a Reference on this Nessie server.

        :param name: name of reference to create
        :param source_ref: optionally which ref to use as base
        :param is_tag: create a Tag rather than a Branch
        """
        hash_ = self.get_conn().get_reference(source_ref).hash_
        return self.get_conn().create_tag(name, hash_).name if is_tag else self.get_conn().create_branch(name, hash_).name

    def delete_reference(self: "NessieHook", name: str, is_tag: bool = False) -> None:
        """Delete a Reference on this Nessie server.

        :param name: name of reference to delete
        :param is_tag: create a Tag rather than a Branch
        """
        hash_ = self.get_conn().get_reference(name).hash_
        self.get_conn().delete_tag(name, hash_) if is_tag else self.get_conn().delete_branch(name, hash_)

    def commit(
        self: "NessieHook",
        branch: str,
        old_hash: str,
        reason: Optional[str] = None,
        author: Optional[str] = None,
        *ops: Operation,
        **properties: Any
    ) -> None:
        """Commit a set of operations to a branch.

        :param branch: name of branch to commit onto
        :param ops: list of operations
        :param old_hash: expected hash of HEAD of branch
        :param reason: commit message
        :param author: commit author
        """
        # todo the ability to fully specify commit meta should be added to Nessie Client
        meta = CommitMeta(message=reason if reason else "", properties=properties)
        if author:
            meta.author = author
        commit(self.get_conn()._base_url, branch, MultiContentsSchema().dumps(MultiContents(meta, list(ops))), old_hash)

    def put(
        self: "NessieHook",
        branch: str,
        old_hash: str,
        key: ContentsKey,
        contents: Contents,
        reason: Optional[str] = None,
        author: Optional[str] = None,
    ) -> None:
        """Add or modify a key on a branch.

        :param branch: name of branch to commit onto
        :param key: key to commit onto
        :param contents: contents to put into this key
        :param old_hash: expected hash of HEAD of branch
        :param reason: commit message
        :param author: commit author
        """
        self.commit(branch, old_hash, reason, author, Put(key, contents))

    def delete(
        self: "NessieHook",
        branch: str,
        old_hash: str,
        key: ContentsKey,
        reason: Optional[str] = None,
        author: Optional[str] = None,
    ) -> None:
        """Delete a key on a branch.

        :param branch: name of branch to commit onto
        :param key: key to commit onto
        :param old_hash: expected hash of HEAD of branch
        :param reason: commit message
        :param author: commit author
        """
        self.commit(branch, old_hash, reason, author, Delete(key))

    def merge(self: "NessieHook", from_branch: str, onto_branch: str) -> None:
        """Perform a merge on a nessie branch.

        The end result of this operation will be that all commits from 'from_branch' are transplanted on to 'onto_branch'

        :param from_branch: ref to move commits from
        :param onto_branch: branch to move commits to
        """
        self.get_conn().merge(from_branch, onto_branch)
