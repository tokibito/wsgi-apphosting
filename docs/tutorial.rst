==============
チュートリアル
==============

wsgi-apphosting には、デモ用のアプリケーションを同梱しています。動かしてみましょう。

ホスト名の設定
--------------

実行するアプリケーションを決定するために、HTTPでアクセスする際にはホスト名が必須になります。
アプリケーションにアクセスするコンピュータ側でホスト名を解決できなければなりません。
デモ用のアプリケーションは、 `アプリケーション名.example.com` というホスト名でアクセスされることを想定しています。

Windowsの場合
~~~~~~~~~~~~~

作者の手元には WindowsXP しか Windows の環境がないので、ここでは WindowsXP を前提にして記述します。
システムディレクトリ以下の `system32\\drivers\\etc\\hosts` ファイルにホスト名を記述します。

.. note::

  CドライブにWindowsXPをインストールしている場合は、 `C:\\WINDOWS\\system32\\drivers\\etc\\hosts` のようになります。

ホスト名は次のように記述します。

::

  # IPアドレスは、アクセス先のホストのアドレスに書き換えてください。
  192.168.1.2  simpleapp.example.com
  192.168.1.2  simpleapp2.example.com
  192.168.1.2  simpleapp3.example.com

wsgiref サーバの起動
--------------------

wsgi-apphosting のアーカイブの `sample/wsgiref/run.py` を実行します。

::

  $ python run.py

8080番ポートを使用してHTTPサーバが起動します。

動作確認
--------

ホスト名を設定したコンピュータから `http://simpleapp.example.com:8080/` へアクセスしてみましょう。
正常に動作している場合は、 plain/text で `It works!` と表示されます。

.. note::

  `simpleapp` はフレームワークを使用していないWSGIアプリケーション、 `simpleapp2` は Flask を使用したアプリケーション、
  `simpleapp3` は Django を使用したアプリケーションです。
