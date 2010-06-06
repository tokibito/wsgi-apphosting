from wsgiref.simple_server import make_server

from StringIO import StringIO
import os
from apphosting.handler import Handler
from apphosting.config import Config

def start():
    handler = Handler(Config({
        'pool_max_runners': 5,
        'provider_appdir': os.path.join(os.path.dirname(__file__), '../../tests'),
        'router_domain': 'example.com'
    }))

    httpd = make_server('0.0.0.0', 8080, handler)
    httpd.serve_forever()

    hadnler.free()

if __name__=="__main__":
    start()
