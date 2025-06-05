import string
import random


def get_code():
    return ''.join(random.sample(string.ascii_letters + string.digits + string.punctuation, 32))

print(get_code())

