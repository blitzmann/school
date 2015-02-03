'''
Exercise 5.4 - multiproc

Write a program that finds a message M (a pre-image) that hashes to the
following value under SHA-512-8 (in hex):
    A9
Write a program that finds a message M that hashes to the following value under
SHA-512-16 (in hex):
    3D 4B
Write a program that finds a message M that hashes to the following value under
SHA-512-24 (in hex):
    3A  7F  27
Write a program that finds a message M that hashes to the following value under
SHA-512-32 (in hex):
    C3  C0  35 7C

Time how long your programs take when n is 8, 16, 24, and 32, averaged over five
runs each. Your programs may use an existing cryptography library. How long
would you expect a similar program to take for SHA-512-256? For SHA-512-384?
For SHA-512 itself?

'''

import hashlib
import math
import random
from timer import Timer
import multiprocessing

output = multiprocessing.Queue()

tests = {
    8: "A9",
    16: "3D4B",
    24: "3A7F27",
    32: "C3C0357C"
}

max_pool = int(math.pow(2, 256))

def doTest(n, m, x, output):
    """
    n: number of bits to truncate to
    m: message to match
    """
    i = 0
    with Timer() as t:
        while True:
            i += 1
            test = str(random.randint(1, max_pool))
            hash = hashlib.sha512(test).hexdigest().upper()[:n/4]
            print "testing: %s-%s %s %s" % (n, x, hash, test)
            if hash == m:
                break
    output.put((n, x, t.msecs, test, i))

if __name__ == '__main__':
    runs = {}
    jobs = []
    with Timer() as c:
        for n, m in tests.items():
            runs[n] = []
            for _ in xrange(5):
                p = multiprocessing.Process(target=doTest, args=(n, m, _, output))
                jobs.append(p)

        for p in jobs:
            p.start()
        for p in jobs:
            p.join()

    results = [output.get() for p in jobs]
    for run in results:
        runs[run[0]].append(run[1:])

    for bits, run in runs.items():
        time = [v[1] for v in run]
        iterations = [v[3] for v in run]

        print "\nInfo for %d (finding %s)"%(bits, tests[bits])
        print "\tAverage ms:\t%fms (%f / %f)"% (sum(time) / len(time), min(time), max(time))
        print "\tAverage s:\t%fs (%f / %f)"%(((sum(time) / len(run))/1000), min(time)/1000,  max(time)/1000)
        print "\tAverage iterations:\t%d (%d / %d)"%(sum(iterations) / len(iterations), min(iterations), max(iterations))

    print "\nTotal time: %ss" % (c.secs)

