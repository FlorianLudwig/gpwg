import hashlib

def sha256(data, times=1):
    """Use sha256 repeatedly and return hash object

    sha256("foo", 2) == sha256(sha256("foo") + "foo") """
    orginal = data
    for _ in xrange(times):
        h = hashlib.sha256(data)
        data = h.digest() + orginal
    return h


def sha256_1(data, times=1):
    """Use sha256 repeatedly and return hash object

    sha256("foo", 2) == sha256("foo" + sha256("foo")) """
    orginal = data
    for _ in xrange(times):
        h = hashlib.sha256(data)
        data = orginal + h.digest()
    return h


def sha256_2(data, times=1):
    """Use sha256 repeatedly and return hash object

    sha256("foo", 2) == sha256("foo" + sha256("foo")) """
    h = hashlib.sha256(data)
    base = h.copy
    for _ in xrange(times-1):
        next = base()
        next.update(h.digest())
        h = next
    return h

import time
t = time.time()
master_pw_ = sha256(master_pw, 10000)
print time.time() - t

t = time.time()
a = sha256_1(master_pw, 100000).hexdigest()
print time.time() - t

t = time.time()
b = sha256_2(master_pw, 100000).hexdigest()
print time.time() - t

assert a == b