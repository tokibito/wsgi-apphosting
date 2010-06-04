#coding:utf-8
#サーバコンフィグ
import os
import yaml

class Config(object):
    def __init__(self, dic):
        self._dic = dic
        self._config = self.parse_config(dic)

    def parse_config(self, dic):
        results = {}
        def _parse(prefix, d):
            for k in d:
                if isinstance(d[k], dict):
                    _parse(prefix + k, d[k])
                else:
                    if prefix:
                        key = prefix + '_' + k
                    else:
                        key = k
                    results[key] = d[k]
        _parse('', dic)
        return results

    def update(self, conf):
        self._dic.update(conf._dic)
        self._config = self.parse_config(self._dic)

    def get(self, key, default=None):
        """
        キーによる値取得
        アンダースコアを利用した場合、一番上のディレクトリに階層構造の辞書に対して
        """
        return self._config.get(key, default)

class ConfigLoadError(Exception):
    pass

class FileConfig(Config):
    def __init__(self, path, parse_dic=None):
        if not os.path.exists(path):
            raise ConfigLoadError(path)
        self.path = path
        self.parse_dic = parse_dic or {}
        fin = open(path, 'r')
        self.body = fin.read()
        fin.close()
        dic = yaml.load(self.parse_text(self.body))
        super(FileConfig, self).__init__(dic)

    def parse_text(self, body):
        """
        ファイルから読み込んだテキストのキーワードを変換する
        """
        kwargs = {}
        kwargs.update(self.parse_dic)
        kwargs.update({
            'CONFIG_DIR': os.path.dirname(os.path.abspath(self.path)),
        })
        return body % kwargs
