"""Shared pytest fixtures.

Sets ``WORKSTATION_DB_PATH`` to a temp file *before* any app module
is imported so the backend never touches a developer's real database
during tests. An autouse fixture then resets the table back to the
seed contents between tests so assertions on workload counts stay
stable regardless of execution order.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

# Create the temp DB path first and install it into the environment
# before the app package is imported anywhere.
_TMP_DIR = Path(tempfile.mkdtemp(prefix="workstation-test-"))
os.environ["WORKSTATION_DB_PATH"] = str(_TMP_DIR / "workstation.db")

import pytest  # noqa: E402

from app.data.workloads import WORKLOADS  # noqa: E402
from app.store.workloads import workload_store  # noqa: E402


@pytest.fixture(autouse=True)
def _reset_workload_store() -> None:
    workload_store.reset(WORKLOADS)
    yield
