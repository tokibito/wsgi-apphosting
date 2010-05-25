#coding:utf-8
#sandboxのプロセス管理
from multiprocessing import Process, Pipe

from apphosting.sandbox._main import Runner

RUNNER_SIGNAL_KILL = 1

class Pool(object):
    def __init__(self):
        self._runners = {}

    def process(self, name, environ, start_response):
        if not name in self._runners:
            self.create_runner(name)
        conn = self._runners[name]._pool_conn
        # environをランナーへ渡す
        conn.send(environ)
        # 結果を待ちうける
        start_response(*conn.recv())
        resp = conn.recv()
        return resp

    def create_runner(self, name):
        """
        新規ランナーを作成
        """
        pool_conn, runner_conn = Pipe()
        self._runners[name] = Runner(name, pool_conn, runner_conn)
        self._runners[name].proc = Process(target=self._runners[name])
        self._runners[name].proc.start()

    def delete_runner(self, name):
        """
        ランナーを解放
        """
        runner = self._runners[name]
        runner._pool_conn.send({'RUNNER_SIGNAL': RUNNER_SIGNAL_KILL})  # 停止信号送信
        del self._runners[name]

    def delete_all_runner(self):
        """
        ランナーをすべて解放
        """
        for name in self._runners.keys():
            self.delete_runner(name)
