# coding:utf-8
# ルーティング提供

SEP_HOSTNAME = ':'
SEP_DOMAIN = '.'
HTTP_PORT = 80

class HostnameError(Exception):
    pass

class RoutingError(Exception):
    pass

def split_hostname(hostname):
    """
    WSGI environのHTTP_HOSTからホスト名とポートを返す
    """
    if hostname.count(SEP_HOSTNAME) > 1:
        raise HostnameError
    if SEP_HOSTNAME in hostname:
        return hostname.split(SEP_HOSTNAME)
    return hostname, HTTP_PORT

def split_domain(domain):
    """
    ドメイン名を分割する
    """
    if SEP_HOSTNAME in domain:
        raise HostnameError
    return domain.split(SEP_DOMAIN)

def split_subdomain(domain, hostname):
    """
    サブドメイン部分を抽出する
    """
    name = hostname[:-len(domain)]
    if name.endswith(SEP_DOMAIN):
        return name[:-1]
    return name

class Router(object):
    def get_route(self, environ):
        pass

class DomainRouter(Router):
    """
    ドメイン名から実行するアプリケーション名を取得するルータ
    app.example.com形式
    """
    def __init__(self, domain):
        self.domain = domain

    def is_valid(self, domain, port):
        """
        バリデーションは継承したクラスで実装
        """
        return True

    def get_route(self, environ):
        hostname, port = split_hostname(environ.get('HTTP_HOST', ''))
        if not self.is_valid(hostname, port):
            raise RoutingError
        app_host = split_subdomain(self.domain, hostname)
        return app_host

class UserDomainRouter(DomainRouter):
    """
    ドメイン名から実行するユーザ名とアプリケーション名を取得するルータ
    app.user.example.com形式
    """
    def get_route(self, environ):
        app_host = super(UserDomainRouter, self).get_route(environ)
        if not app_host:
            user = '_admin'
            app_name = 'hosting'
        elif app_host.count(SEP_DOMAIN) == 1:
            app_name, user = split_domain(app_host)
        else:
            raise RoutingError
        return '%(user)s.%(app_name)s' % {'user': user, 'app_name': app_name}
