import pytest

from bddcli.fixtures import bootstrapper_patch


@pytest.fixture
def bootpatch():
    return bootstrapper_patch
