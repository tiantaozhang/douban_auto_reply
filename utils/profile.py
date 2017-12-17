"""
性能分析工具cprofile
"""


import time
from functools import wraps


def fn_timer(function):
    @wraps(function)
    def function_timer(*args, **kwargs):
        t1 = time.time()
        result = function(*args, **kwargs)
        t2 = time.time()
        print "Total time running %s: %s seconds" % \
               (function.func_name, str(t2-t1))

        return result

    return function_timer


@fn_timer
def random_sort(n):
    import random
    return sorted([random.random() for i in range(n)])


# @profile
def random_sort2(n):
    import random
    l = [random.random() for i in range(n)]
    l.sort()
    return l

if __name__ == '__main__':
    import cProfile
    cProfile.run("random_sort2(2000000)", filename='../tmp/result.out', sort="cumulative")

