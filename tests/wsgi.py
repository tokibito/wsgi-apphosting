#coding:utf-8
import os
from unittest import TestCase

from apphosting.handler import Handler
from apphosting.config import Config

class HandlerTestCase(TestCase):
    def setUp(self):
        self.handler = Handler(Config({
          'pool_max_runners': 5,
          'provider_appdir': os.path.dirname(__file__),
          'router_domain': 'example.com'
        }))

    def tearDown(self):
        self.handler.free()

    def get_environ_with_host(self, host):
        return {
            'HTTP_HOST': host,
            'SERVER_NAME': 'localhost',
            'SERVER_PORT': '80',
            'REQUEST_METHOD': 'GET',
            'wsgi.url_scheme': 'http',
        }

    def test_handler_call(self):
        start_info = {}
        def _start_response(status, headers, exc_info=None):
            start_info['status'] = status
            start_info['headers'] = headers
        for i in range(3):
            start_info = {}
            resp = self.handler(self.get_environ_with_host('simpleapp.example.com'), _start_response)
            self.assertEqual(start_info['status'], '200 OK')
        start_info = {}
        resp = self.handler(self.get_environ_with_host('foobar.example.com'), _start_response)
        self.assertEqual(start_info['status'], '404 Not Found')
