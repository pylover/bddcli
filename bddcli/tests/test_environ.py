import os

from bddcli import Command, stdout, Application, when, given


def foo():
    e = os.environ.copy()
    del e['PWD']
    print(' '.join(f'{k}: {v}' for k, v in e.items()))


app = Application('foo', 'bddcli.tests.test_environ:foo')


def test_environ():
    with Command(app, 'Environment variables', environ={'bar': 'baz'}):
        assert stdout == 'bar: baz\n'

        when('Without any variable', environ=given - 'bar')
        assert stdout == '\n'

        when('Add another variables', environ=given + {'qux': 'quux'})
        assert stdout == 'bar: baz qux: quux\n'
