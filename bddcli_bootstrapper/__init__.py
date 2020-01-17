import sys
import importlib
import time


def main():
    prog = sys.argv.pop(1)
    address = sys.argv.pop(1)
    sys.argv[0] = prog
    module, expression = address.split(':')

    if '' not in sys.path:
        sys.path.insert(0, '')

    module = importlib.import_module(module)
    func = eval(f'{expression}', globals(), module.__dict__)
    return func()


if __name__ == '__main__':
    sys.exit(main())
