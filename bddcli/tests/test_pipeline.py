import pytest

from bddcli import given, when


def test_basic_pipeline():
    with given(Main):
        # Without any parameters
        when()
        assert output == 'output'

