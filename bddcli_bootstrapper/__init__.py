import sys
import importlib
import time
import os


def main():
    prog = sys.argv.pop(1)
    address = sys.argv.pop(1)
    workingdirectory = sys.argv.pop(1)

    sys.argv[0] = prog
    module, expression = address.split(':')

    if '' not in sys.path:
        sys.path.insert(0, '')

    module = importlib.import_module(module)
    func = eval(f'{expression}', globals(), module.__dict__)
    if workingdirectory:
        os.chdir(workingdirectory)
    return func()


if __name__ == '__main__':
    sys.exit(main())
