import os

from bddcli import Command, stdout, Application, when


def foo():
    print(f'bar: {os.environ["bar"]}')


app = Application('foo', 'bddcli.tests.test_environ:foo')


def test_environ():
    with Command(app, 'Environment variables', environ={'bar': 'baz'}):
        assert stdout == 'bar: baz\n'


