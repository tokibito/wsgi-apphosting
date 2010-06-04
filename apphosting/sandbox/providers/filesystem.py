#coding:utf-8
#APPDIRのディレクトリをPYTHONPATHに追加してインポート
import os
import sys

from apphosting.config import FileConfig
from apphosting.sandbox import utils

def get_application(app_name, server_config):
    path = server_config.get('app_dir')
    app_config = FileConfig(
        os.path.join(os.path.join(path, app_name.replace('.', os.sep), 'app.yaml')),
        parse_dic={'app_name': app_name},
    )
    if path and not path in sys.path:
        sys.path.append(path)
    entry_point = app_config.get('application_entry_point', '')
    return getattr(utils.import_module(entry_point), 'application')
