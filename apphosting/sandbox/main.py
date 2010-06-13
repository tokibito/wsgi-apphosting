#coding:utf-8
#アプリケーションのランナー
import sys
from datetime import datetime

from apphosting import const
from apphosting.sandbox import utils

class Runner(object):
    """
    ランナーはプロセスプールで保持される
    1プロセス1ランナー
    TODO:複数のプロセスで同じランナーが起動する可能性
    providerはアプリケーション提供モジュール
    """

    def __init__(self, name, provider, server_config, pool_conn, runner_conn):
        self.provider = utils.import_module(provider)
        self._server_config = server_config
        self._application = self.provider.get_application(name, self._server_config)
        self._pool_conn = pool_conn
        self._runner_conn = runner_conn
        self.proc = None
        self.suspended = False
        self.ctime = datetime.now()
        self.utime = datetime.now()
        self.processed = 0

    def __call__(self):
        while not self.suspended:
            # environパラメータを待ちうけ
            environ = self._runner_conn.recv()
            signal = environ.get('RUNNER_SIGNAL')
            # 停止
            if signal == const.RUNNER_SIGNAL_KILL:
                self.suspended = True
                continue
            # 情報取得
            elif signal == const.RUNNER_SIGNAL_INFO:
                self._runner_conn.send({
                    'ctime': self.ctime,
                    'utime': self.utime,
                    'processed': self.processed
                })
                continue
            # アプリケーションを実行
            status, headers, resp = self.main(environ)
            # start_resopnseの結果を返す
            self._runner_conn.send([status, headers])
            self._runner_conn.send(resp)
            # 実行回数カウント
            self.processed += 1
            # 最後に実行した時間
            self.utime = datetime.now()
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
