import os

from bddcli import Given, stdout, Application, when


def foo():  # pragma: no cover
    print(os.getcwd(), flush=True)


app = Application('foo', 'tests.test_workingdirectory:foo')


def test_working_directory():
    with Given(app):
        assert f'{os.getcwd()}\n' == stdout
        if os.name == "nt":
            tmp_dir = os.getenv('TEMP')
        else:
            tmp_dir = '/tmp'
        when(working_directory=tmp_dir)
        assert stdout == tmp_dir + '\n'
