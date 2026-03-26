import os
import sys
import stat
import shutil
import tempfile
import contextlib


def _which(name):
    for directory in sys.path:
        path = os.path.join(directory, name)
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path

    return None


@contextlib.contextmanager
def bootstrapper_patch(pycode):
    tmp = tempfile.mkdtemp()
    bindir = os.path.abspath(os.path.dirname(sys.executable))
    if bindir not in sys.path:
        sys.path.insert(0, bindir)

    bsfile = _which('bddcli-bootstrapper')
    assert os.path.exists(bsfile)
    newname = os.path.join(tmp, 'backup')
    os.rename(bsfile, os.path.join(tmp, 'backup'))

    with open(newname) as infile, open(bsfile, 'w') as outfile:
        outfile.write(infile.readline())
        outfile.write(infile.readline())
        outfile.write(pycode)
        outfile.write('\n')
        outfile.write(infile.read())

        # set the execution bit
        mode = os.fstat(outfile.fileno()).st_mode
        mode |= stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
        os.fchmod(outfile.fileno(), stat.S_IMODE(mode))

    try:
        yield
    finally:
        os.rename(newname, bsfile)
        shutil.rmtree(tmp)
