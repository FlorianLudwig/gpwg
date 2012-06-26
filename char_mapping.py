
chars = [chr(i) for i in xrange(97, 122)] # a-z
chars+= [chr(i) for i in xrange(33, 90)]
print len(chars)

chars_count = {}
for i in xrange(256):
    char = int(i / 255.5 * len(chars))
    chars_count.setdefault(char, 0)
    chars_count[char] += 1
assert sorted(chars_count.keys()) == range(len(chars))

print '8 bit'
print min(chars_count.values())
print max(chars_count.values())
print

chars_count = {}
for i in xrange(2**16):
    char = int(i / (2**16-0.5) * len(chars))
    chars_count.setdefault(char, 0)
    chars_count[char] += 1
assert sorted(chars_count.keys()) == range(len(chars))

print '16 bit'
print min(chars_count.values())
print max(chars_count.values())
print
