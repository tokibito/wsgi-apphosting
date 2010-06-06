# coding:utf-8
# WSGIハンドラ
import logging

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
        return [self.page]

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
        # wsgi.input/wsgi.errors はcStringIOのオブジェクトの可能性があるので
        # pickle化できるようにStringIOにする
        from StringIO import StringIO
        original_wsgi_errors = environ.get('wsgi.errors')
        environ['wsgi.errors'] = StringIO()
        try:
            content_length = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError, TypeError):
            content_length = 0
        original_wsgi_input = environ.get('wsgi.input')
        if original_wsgi_input and content_length > 0:
            environ['wsgi.input'] = StringIO(original_wsgi_input.read())
        else:
            environ['wsgi.input'] = StringIO()

        # 残りのpickle化できない項目は潰す
        import pickle
        for k, v in environ.iteritems():
            try:
                pickle.dumps(v)
            except:
                logging.warn('%s: %s does not pickling.' % (k, v))
                environ[k] = None

        app_name = self.get_app_name(environ)
        if not app_name or not self.pool.has_application(app_name):
            return self.handler404(environ, start_response)
        response = self.pool.process(app_name, environ, start_response)

        if original_wsgi_errors:
            original_wsgi_errors.write(environ['wsgi.errors'].getvalue())

        return [response]

    def free(self):
        self.pool.delete_all_runner()
        self.pool = None

    def get_domain(self):
        return self.config.get('router_domain')

    def get_app_name(self, environ):
        return self.router.get_route(environ)

    def handler404(self, environ, start_response):
        return self.app404(environ, start_response)
