import StringIO

from fapws.base import *
from fapws.base import Environ as BaseEnviron

class Environ(BaseEnviron):
    def __init__(self, *arg, **kw):
        super(Environ, self).__init__(*arg, **kw)
        self['wsgi.errors'] = StringIO.StringIO()
        self['wsgi.input'] = StringIO.StringIO()
