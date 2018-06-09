import random
import string

from CDO.vars import *


def get(request, name):
    if contain(request, name):
        return request.session[name]
    return None


def write(request, name, value):
    print('At %s write %s' % (name, str(value)))
    request.session[name] = value


def remove(request, name):
    request.session[name] = None


def contain(request, name):
    return name in request.session and request.session[name] is not None


def string_generator(size=6, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
