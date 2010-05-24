#coding:utf-8
from unittest import TestCase

from apphosting.pool import Pool

SAMPLEAPP = 'tests.sampleapp.main'

class SampleAppTestCase(TestCase):
    def test_pool(self):
        """
        Poolの複数回リクエスト
        """
        pool = Pool()
        pool.create_runner(SAMPLEAPP)
        start_info = {}
        def _start_response(status, headers, exc_info=None):
            start_info['status'] = status
            start_info['headers'] = headers
        for i in range(3):
            resp = pool.process(SAMPLEAPP, {}, _start_response)
            self.assertEqual('200 OK', start_info['status'])
            self.assertEqual('It works!\r\n', resp)
        pool.delete_runner(SAMPLEAPP)
