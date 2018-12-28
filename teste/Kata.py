def in_array(array1, array2):
    r = set( a for a in array1 if any(a in b for b in array2))
    r = list(r)
    # your code
    r.sort()
    return r

a1 = ["live", "arp", "live", "strong"]
a2 = ["lively", "alive", "harp", "sharp", "armstrong"]
r = ['arp', 'live', 'strong']

assert in_array(a1, a2) == r