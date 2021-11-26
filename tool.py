import random
import string
import cacheout

def randstr(length: int):
    return "".join(random.sample(string.ascii_letters + string.digits, length))

cache = cacheout.cache.Cache(ttl=600)