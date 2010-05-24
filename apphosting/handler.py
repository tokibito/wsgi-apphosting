#coding:utf-8
#wsgiのルーティング用ハンドラ
class Handler(object):
    def __init__(self, router, config):
        self.config = config
        self.router = router

    def __call__(self, environ, start_response):
        pass
