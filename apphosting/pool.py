#coding:utf-8
#sandboxのプロセス管理
from multiprocessing import Process, Pipe

from apphosting.sandbox import const
from apphosting.sandbox.main import Runner

class RunnerDoesNotExist(Exception):
    pass

class Pool(object):
    def __init__(self, provider, server_config=None, auto_create=True):
        """
        providerはアプリケーション提供モジュール
        """
        self._runners = {}
        self._server_config = server_config or {}
        self.auto_create = auto_create
        self.provider = provider

    def process(self, name, environ, start_response):
        conn = self.get_runner(name, self.auto_create)._pool_conn
        # environをランナーへ渡す
        conn.send(environ)
        # 結果を待ちうける
        start_response(*conn.recv())
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
        pool_conn, runner_conn = Pipe()
        self._runners[name] = Runner(name, self.provider, self._server_config, pool_conn, runner_conn)
        self._runners[name].proc = Process(target=self._runners[name])
        self._runners[name].proc.start()

    def delete_runner(self, name):
        """
        ランナーを解放
        """
        runner = self._runners[name]
        runner._pool_conn.send({'RUNNER_SIGNAL': const.RUNNER_SIGNAL_KILL})  # 停止信号送信
        del self._runners[name]

    def delete_all_runner(self):
        """
        ランナーをすべて解放
        """
        for name in self._runners.keys():
            self.delete_runner(name)
