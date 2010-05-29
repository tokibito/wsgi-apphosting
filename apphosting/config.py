#coding:utf-8
#サーバコンフィグ
import os
import yaml

class ConfigLoadError(Exception):
    pass

class Config(object):
    def __init__(self, path):
        if not os.path.exists(path):
            raise ConfigLoadError(path)
        self.path = path
        fin = open(path, 'r')
        self.body = fin.read()
        fin.close()
        self._config = self.parse_config(yaml.load(self.parse_text(self.body)))

    def parse_text(self, body):
        """
        ファイルから読み込んだテキストのキーワードを変換する
        """
        kwargs = {
            'CONFIG_DIR': os.path.dirname(os.path.abspath(self.path)),
        }
        return body % kwargs

    def parse_config(self, dic):
        results = {}
        def _parse(prefix, d):
            for k in d:
                if isinstance(d[k], dict):
                    _parse(prefix + k, d[k])
                else:
                    results[prefix + '_' + k] = d[k]
        _parse('', dic)
        return results

    def get(self, key, default=None):
        """
        キーによる値取得
        アンダースコアを利用した場合、一番上のディレクトリに階層構造の辞書に対して
        """
        return self._config.get(key, default)
