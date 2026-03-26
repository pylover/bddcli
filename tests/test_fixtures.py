from bddcli import Given, stdout, status, stderr, Application


def foo():
    print('foo')


def test_basic_pipeline(bootpatch):
    app = Application('foo', f'{__name__}:foo')
    pycode = 'print("lorem ipsum")'
    with bootpatch(pycode), Given(app):
        assert status == 0
        assert stdout == 'lorem ipsum\nfoo\n'
        assert stderr == ''
