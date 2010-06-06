import fapws._evwsgi as evwsgi
import time
import sys
sys.setcheckinterval(100000) # since we don't use threads, internal checks are no more required

import os
from apphosting.handler import Handler
from apphosting.config import Config

import custom_base

handler = Handler(Config({
    'pool_max_runners': 5,
    'provider_appdir': os.path.join(os.path.dirname(__file__), '../../tests'),
    'router_domain': 'example.com'
}))

def start():
    evwsgi.start("0.0.0.0", "8080")

    evwsgi.set_base_module(fapws_base)

    evwsgi.wsgi_cb(('', handler))

    evwsgi.set_debug(0)
    evwsgi.run()

    handler.free()

if __name__=="__main__":
    start()