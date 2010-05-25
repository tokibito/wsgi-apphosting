#coding:utf-8
from unittest import TestCase

from apphosting.pool import Pool

SAMPLEAPP = 'tests.simpleapp.main'
SAMPLEAPP2 = 'tests.simpleapp2.main'

class SampleAppTestCase(TestCase):
    def setUp(self):
        self.pool = Pool()

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

    def test_pool(self):
        """
        Poolの複数回リクエスト
        """
        self.pool.create_runner(SAMPLEAPP)
        start_info = {}
        def _start_response(status, headers, exc_info=None):
            start_info['status'] = status
            start_info['headers'] = headers
        for i in range(3):
            resp = self.pool.process(SAMPLEAPP, {}, _start_response)
            self.assertEqual('200 OK', start_info['status'])
            self.assertEqual('It works!\r\n', resp)

    def test_flaskapp(self):
        """
        Flaskアプリケーションのテスト
        """
        self.pool.create_runner(SAMPLEAPP2)
        start_info = {}
        def _start_response(status, headers, exc_info=None):
            start_info['status'] = status
            start_info['headers'] = headers
        for i in range(3):
            resp = self.pool.process(SAMPLEAPP2, self.get_environ(), _start_response)
            self.assertEqual('200 OK', start_info['status'])
            self.assertEqual('Hello Flask!', resp)

    def test_multihost(self):
        """
        複数アプリケーションのホスト
        """
        self.pool.create_runner(SAMPLEAPP)
        self.pool.create_runner(SAMPLEAPP2)
        start_info = {}
        def _start_response(status, headers, exc_info=None):
            start_info['status'] = status
            start_info['headers'] = headers
        for i in range(3):
            resp = self.pool.process(SAMPLEAPP, {}, _start_response)
            self.assertEqual('200 OK', start_info['status'])
            self.assertEqual('It works!\r\n', resp)
        for i in range(3):
            resp = self.pool.process(SAMPLEAPP2, self.get_environ(), _start_response)
            self.assertEqual('200 OK', start_info['status'])
            self.assertEqual('Hello Flask!', resp)
