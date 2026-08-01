"""nbpl 的命令行入口。"""

from __future__ import annotations

import argparse

from .watcher import watch


def main() -> None:
    parser = argparse.ArgumentParser(
        description="检测到 Python 脚本运行时，按所在地区打开对应的视频。"
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=1.0,
        help="进程检查间隔（秒），默认：1",
    )
    parser.add_argument(
        "--country-code",
        help="覆盖公网 IP 地区检测，适合测试，例如 CN",
    )
    args = parser.parse_args()
    watch(interval=args.interval, country_code=args.country_code)
