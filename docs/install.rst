============
インストール
============

wsgi-apphosting のインストール方法について解説します。

モジュールの入手
================

wsgi-apphosting のアーカイブの入手は bitbucket から行えます。

http://bitbucket.org/tokibito/wsgi-apphosting/

Mercurial を使用して clone するか、zip形式などでダウンロードできます。

セットアップ
============

依存モジュールのインストール
----------------------------

wsgi-apphosting は、 multiprocessing モジュールに依存しています。
Python2.5以前のバージョンでは、バックポートされた multiprocessing モジュールをインストールしておく必要があります。
Python2.6以上のバージョンでは、この操作は必要ありません。

::

  $ sudo easy_install multiprocessing

wsgi-apphosting のインストール
------------------------------

setup.py を実行してインストールします。

::

  $ cd wsgi-apphosting
  $ sudo python setup.py install
