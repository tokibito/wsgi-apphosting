#coding:utf-8
#sandboxのプロセス管理
import logging
from multiprocessing import Process, Pipe

from apphosting import const
from apphosting.config import Config
from apphosting.sandbox import utils
from apphosting.sandbox.main import Runner

class RunnerDoesNotExist(Exception):
    pass

class Pool(object):
    runner_class = Runner
    default_max_runners = 5

    def __init__(self, provider, server_config=None, auto_create=True, *args, **kwargs):
        """
        providerはアプリケーション提供モジュール
        """
        self._runners = {}
        self.server_config = Config(const.DEFAULT_CONFIG)
        if not server_config is None:
            self.server_config.update(server_config)
        self.auto_create = auto_create
        self.provider = provider
        self.provider_module = utils.import_module(self.provider)
        self.max_runners = kwargs.get('max_runners') \
            or self.server_config.get('app_max_runners') \
            or self.default_max_runners

    def process(self, name, environ, start_response):
        conn = self.get_runner(name, self.auto_create)._pool_conn
        # environをランナーへ渡す
        conn.send(environ)
        # 結果を待ちうける
        args = conn.recv()
        start_response(*args)
        return conn.recv()

    def process_info(self, name):
        """
        ランナーの情報を返す
        """
        conn = self.get_runner(name, self.auto_create)._pool_conn
        # environをランナーへ渡す
        conn.send({'RUNNER_SIGNAL': const.RUNNER_SIGNAL_INFO})
        # 結果を待ちうける
        return conn.recv()

    def has_application(self, name):
        """
        アプリケーションが存在するか
        """
        return self.provider_module.has_application(name, self.server_config)

    def get_runner(self, name, auto_create=None):
        """
        ランナーを返す
        """
        if auto_create is None:
            auto_create = self.auto_create
        if not name in self._runners:
            if auto_create:
                self.create_runner(name)
            else:
                raise RunnerDoesNotExist
        return self._runners[name]

    def create_runner(self, name):
        """
        新規ランナーを作成
        """
        # 最大数を超えている場合は一番古いものを終了する
        while len(self._runners) >= self.max_runners:
            old_runner_name = sorted(self._runners.items(), key=lambda v: v[1].ctime)[0][0]
            self.delete_runner(old_runner_name)
        pool_conn, runner_conn = Pipe()
        self._runners[name] = self.runner_class(
            name,
            self.provider,
            self.server_config,
            pool_conn,
            runner_conn
        )
        self._runners[name].proc = Process(target=self._runners[name])
        self._runners[name].proc.start()

    def delete_runner(self, name):
        """
        ランナーを解放
        """
        runner = self._runners[name]
        runner._pool_conn.send({'RUNNER_SIGNAL': const.RUNNER_SIGNAL_KILL})  # 停止信号送信
        del self._runners[name]
        logging.info('deleted runner => "%s"' % name)

    def delete_all_runner(self):
        """
        ランナーをすべて解放
        """
        for name in self._runners.keys():
            self.delete_runner(name)
