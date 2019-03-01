import os

from bddcli import Given, stdout, Application, when, given


def foo():  # pragma: no cover
    e = os.environ.copy()
    del e['PWD']
    print(' '.join(f'{k}: {v}' for k, v in e.items()))


app = Application('foo', 'bddcli.tests.test_environ:foo')


def test_environ():
    with Given(app, environ={'bar': 'baz'}):
        assert stdout == 'bar: baz\n'

        when(environ=given - 'bar')
        assert stdout == '\n'

        when(environ=given + {'qux': 'quux'})
        assert stdout == 'bar: baz qux: quux\n'

        when(environ=given | {'bar': 'quux'})
        assert stdout == 'bar: quux\n'
