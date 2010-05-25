#coding:utf-8
#アプリケーションのランナー
import sys

from apphosting.sandbox import _utils

class Runner(object):
    """
    ランナーはプロセスプールで保持される
    1プロセス1ランナー
    TODO:複数のプロセスで同じランナーが起動する可能性
    """
    def __init__(self, name, pool_conn, runner_conn):
        self._application = getattr(_utils.import_module(name), 'application')
        self._pool_conn = pool_conn
        self._runner_conn = runner_conn
        self.proc = None
        self.suspended = False

    def __call__(self):
        while not self.suspended:
            # environパラメータを待ちうけ
            environ = self._runner_conn.recv()
            # 停止信号
            if environ.get('RUNNER_SIGNAL') == 1:
                self.suspended = True
                continue
            # アプリケーションを実行
            status, headers, resp = self.main(environ)
            # start_resopnseの結果を返す
            self._runner_conn.send([status, headers])
            self._runner_conn.send(resp)
        # サスペンドされた場合パイプを閉じる
        self._runner_conn.close()
        sys.exit(0)

    def main(self, environ):
        """
        メインハンドラ
        アプリケーションの実行が完全に終わってから結果を返す
        """
        start_info = {
          'status': '',
          'headers': ()
        }
        def _start_response(status, headers, exc_info=None):
            start_info['status'] = status
            start_info['headers'] = headers
        response = self._application(environ, _start_response)
        return start_info['status'], start_info['headers'], ''.join(response)
