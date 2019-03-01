import os

from bddcli import Given, stdout, Application, when


def foo():  # pragma: no cover
    print(os.getcwd())


app = Application('foo', 'bddcli.tests.test_workingdirectory:foo')


def test_working_directory():
    with Given(app):
        assert f'{os.getcwd()}\n' == stdout

        when(working_directory='/tmp')
        assert stdout == '/tmp\n'
