import os
import sys
import importlib


def main():
    prog = sys.argv.pop(1)
    address = sys.argv.pop(1)
    working_directory = sys.argv.pop(1) if len(sys.argv) > 1 else '.'
    os.chdir(working_directory)
    sys.argv[0] = prog

    module, func = address.split(':')
    module = __import__(module, globals={'__name__': __name__}, fromlist=[func])
    func = getattr(module, func)
    return func()

