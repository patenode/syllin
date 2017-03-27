import random
import string
from hashlib import sha512

SIMPLE_CHARS = string.ascii_letters + string.digits

def get_random_string(length=24):
    return ''.join(random.choice(SIMPLE_CHARS) for i in range(length))

def get_random_hash(length=24):
    hash = sha512()
    hash.update(get_random_string())
    return hash.hexdigest()[:length]