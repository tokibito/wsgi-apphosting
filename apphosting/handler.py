# coding:utf-8
# WSGIハンドラ
from apphosting.pool import Pool
from apphosting.router import DomainRouter, UserDomainRouter

class NotFoundApplication(object):
    page = """<html><head>
<title>404 Not Found</title>
</head><body>
<h1>404 Not Found</h1>
</body></html>"""

    def __call__(self, environ, start_response):
        start_response('404 Not Found', [('Content-type', 'text/html')])
        return self.page

class Handler(object):
    pool_class = Pool
    router_class = DomainRouter
    app_provider = 'apphosting.sandbox.providers.filesystem'
    runner_auto_create = True
    app404 = NotFoundApplication()

    def __init__(self, config):
        self.config = config
        self.router = self.router_class(self.get_domain())
        self.pool = self.pool_class(
            self.app_provider,
            config,
            self.runner_auto_create
        )

    def __call__(self, environ, start_response):
        app_name = self.get_app_name(environ)
        if not app_name or not self.pool.has_application(app_name):
            return self.handler404(environ, start_response)
        response = self.pool.process(app_name, environ, start_response)
        return response

    def free(self):
        self.pool.delete_all_runner()
        self.pool = None

    def get_domain(self):
        return self.config.get('router_domain')

    def get_app_name(self, environ):
        return self.router.get_route(environ)

    def handler404(self, environ, start_response):
        return self.app404(environ, start_response)
