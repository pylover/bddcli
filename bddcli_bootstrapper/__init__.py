import sys
import importlib
import time


def main():
    prog = sys.argv.pop(1)
    address = sys.argv.pop(1)
    sys.argv[0] = prog

    module, func = address.split(':')
    module = __import__(
        module,
        globals={'__name__': __name__},
        fromlist=[func]
    )
    func = getattr(module, func)
    return func()

