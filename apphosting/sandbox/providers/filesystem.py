#coding:utf-8
#APPDIRのディレクトリをPYTHONPATHに追加してインポート
import sys

from apphosting.sandbox import utils

def get_application(name, server_config):
    path = server_config.get('APPDIR')
    if path and not path in sys.path:
        sys.path.append(path)
    return getattr(utils.import_module(name), 'application')
