import sys
import os
from shadowsocks.daemon import freopen
from collections import defaultdict


def f1():
    print __file__
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../'))
    print sys.path


def f2():
    freopen("/Users/Len/Downloads/txt", 'a', sys.stdout)
    print "test1..."
    print "test2..."
    print "cat file"


def f3():
    if 0:
        print "0"
    else:
        print "not 0"


def f4():
    try:
        with open("/Users/Len/Downloads/txt") as f:
            print int(f.read())
    except Exception, e:
        print e

    print "f is closed", f.closed


def f5():
    POLL_NULL = 0x00
    POLL_IN = 999
    POLL_OUT = 888
    POLL_ERR = 777
    results = defaultdict(lambda: POLL_NULL)
    for p in [(1, POLL_IN), (2, POLL_OUT), (3, POLL_ERR)]:
        for fd in range(1, 3):
            results[fd] |= p[1]
    return results.items()


def f6():
    rs = defaultdict(lambda: 'abc')
    rs[0] = "x"
    rs[1] = "y"

    print rs.items()


if __name__ == "__main__":
    # f1()
    #f2()
    #f3()
    #f4()
    #print f5()
    f6()
