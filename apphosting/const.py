# coding:utf-8

# Runnerへの命令信号
RUNNER_SIGNAL_KILL = 1
RUNNER_SIGNAL_INFO = 2

# 各設定のデフォルト値
DEFAULT_MAX_RUNNERS = 5

DEFAULT_CONFIG = {
    'app': {
        'max_runners': DEFAULT_MAX_RUNNERS,
    }
}
