#!/usr/bin/env python3

from roop import core

if __name__ == '__main__':
    import roop
    print("roop.globals.skip_nonswap_frame is %s" % roop.globals.skip_nonswap_frame)
    core.run()
