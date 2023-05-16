import sys


def clear():
    sys.stdout.write("\x1b[1A")
    sys.stdout.write("\x1b[2K")
