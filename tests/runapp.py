#coding:utf-8
import os
from unittest import TestCase

from apphosting.pool import Pool
from apphosting.config import Config

SAMPLEAPP = 'simpleapp'
SAMPLEAPP2 = 'simpleapp2'
SAMPLEAPP3 = 'simpleapp3'

__all__ = ('SampleAppTestCase',)

class SampleAppTestCase(TestCase):
    def setUp(self):
        self.pool = Pool('apphosting.sandbox.providers.filesystem', Config({
            'app_dir': os.path.dirname(__file__),
        }))

    def tearDown(self):
        self.pool.delete_all_runner()
        self.pool = None

    def get_environ(self):
        return {
            'SERVER_NAME': 'localhost',
            'SERVER_PORT': '80',
            'REQUEST_METHOD': 'GET',
            'wsgi.url_scheme': 'http',
        }

    def test_runwsgiapp(self):
        """
        シンプルなWSGIアプリケーションのテスト
        """
        start_info = {}
        def _start_response(status, headers, exc_info=None):
            start_info['status'] = status
            start_info['headers'] = headers
        for i in range(3):
            resp = self.pool.process(SAMPLEAPP, {}, _start_response)
            self.assertEqual(start_info['status'], '200 OK')
            self.assertEqual(resp, 'It works!\r\n')

    def test_flaskapp(self):
        """
        Flaskアプリケーションのテスト
        """
        start_info = {}
        def _start_response(status, headers, exc_info=None):
            start_info['status'] = status
            start_info['headers'] = headers
        for i in range(3):
            resp = self.pool.process(SAMPLEAPP2, self.get_environ(), _start_response)
            self.assertEqual(start_info['status'], '200 OK')
            self.assertEqual(resp, 'Hello Flask!')

    def test_djangoapp(self):
        """
        Djangoアプリケーションのテスト
        """
        start_info = {}
        def _start_response(status, headers, exc_info=None):
            start_info['status'] = status
            start_info['headers'] = headers
        for i in range(3):
            resp = self.pool.process(SAMPLEAPP3, self.get_environ(), _start_response)
            self.assertEqual(start_info['status'], '200 OK')
            self.assertEqual(resp, 'Hello Django!')

    def test_multihost(self):
        """
        複数アプリケーションのホスト
        """
        start_info = {}
        def _start_response(status, headers, exc_info=None):
            start_info['status'] = status
            start_info['headers'] = headers
        for i in range(3):
            resp = self.pool.process(SAMPLEAPP, {}, _start_response)
            self.assertEqual(start_info['status'], '200 OK')
            self.assertEqual(resp, 'It works!\r\n')
        for i in range(4):
            resp = self.pool.process(SAMPLEAPP2, self.get_environ(), _start_response)
            self.assertEqual(start_info['status'], '200 OK')
            self.assertEqual(resp, 'Hello Flask!')
        for i in range(5):
            resp = self.pool.process(SAMPLEAPP3, self.get_environ(), _start_response)
            self.assertEqual(start_info['status'], '200 OK')
            self.assertEqual(resp, 'Hello Django!')
        self.assertEqual(self.pool.process_info(SAMPLEAPP)['processed'], 3)
        self.assertEqual(self.pool.process_info(SAMPLEAPP2)['processed'], 4)
        self.assertEqual(self.pool.process_info(SAMPLEAPP3)['processed'], 5)
