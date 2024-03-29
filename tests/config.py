#coding:utf-8
# コンフィグのテスト
import os
from unittest import TestCase

from apphosting.config import FileConfig

BASEDIR = os.path.dirname(os.path.abspath(__file__))

__all__ = ('ConfigTestCase',)

class ConfigTestCase(TestCase):
    def setUp(self):
        self.config = FileConfig(os.path.join(BASEDIR, 'test.yaml'))

    def test_get(self):
        self.assertEqual(BASEDIR, self.config.get('provider_appdir'))
        self.assertEqual(self.config.get('foo_bar'), 12345)
        self.assertEqual(self.config.get('foo_fizz_buzz'), 'test')
