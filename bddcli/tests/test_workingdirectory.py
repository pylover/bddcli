import os

from bddcli import Command, stdout, Application, when


def foo():
    print(os.getcwd())


app = Application('foo', 'bddcli.tests.test_workingdirectory:foo')


def test_working_directory():
    with Command(
        app,
        'Without specifying working directory',
    ):
        assert f'{os.getcwd()}\n' == stdout

        when('Specifying a working directory', working_directory='/tmp')
        assert stdout == '/tmp\n'
