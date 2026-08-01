"""nbpl 的进程监控与地区检测逻辑。"""

from __future__ import annotations

import os
import sys
import time
import webbrowser
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

BILIBILI_URL = "https://www.bilibili.com/video/BV1GJ411x7h7"
YOUTUBE_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
IP_API_URL = "https://ipapi.co/json/"


@dataclass(frozen=True)
class ScriptProcess:
    """一个关联到 Python 源文件的运行中 Python 解释器。"""

    pid: int
    script: str


def _is_python_interpreter(executable: str) -> bool:
    name = Path(executable).name.lower()
    return name.startswith("python") or name in {"py", "py.exe"}


def _script_from_cmdline(cmdline: list[str]) -> Optional[str]:
    """从 Python 解释器的命令行中返回第一个直接传入的源文件。"""
    if not cmdline or not _is_python_interpreter(cmdline[0]):
        return None

    for argument in cmdline[1:]:
        if argument.lower().endswith((".py", ".pyw")):
            return argument
    return None


def find_running_python_scripts() -> list[ScriptProcess]:
    """列出正在执行 Python 源文件的其他进程。"""
    try:
        import psutil
    except ImportError as exc:
        raise RuntimeError("nbpl 依赖 psutil，请重新安装本包") from exc

    found: list[ScriptProcess] = []
    this_pid = os.getpid()
    for process in psutil.process_iter(["pid", "cmdline"]):
        try:
            info = process.info
            pid = info["pid"]
            if pid == this_pid:
                continue
            script = _script_from_cmdline(info.get("cmdline") or [])
            if script:
                found.append(ScriptProcess(pid=pid, script=script))
        except (psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess):
            continue
    return found


def detect_country_code(timeout: float = 5.0) -> Optional[str]:
    """返回公网 IP 的国家/地区代码；无法判断时返回 None。"""
    try:
        import requests
    except ImportError as exc:
        raise RuntimeError("nbpl 依赖 requests，请重新安装本包") from exc

    try:
        response = requests.get(IP_API_URL, timeout=timeout)
        response.raise_for_status()
        country_code = response.json().get("country_code")
        return country_code.upper() if isinstance(country_code, str) else None
    except (requests.RequestException, ValueError):
        return None


def open_video_for_country(country_code: Optional[str]) -> str:
    """按国家/地区代码打开并返回相应的视频 URL。"""
    url = BILIBILI_URL if country_code == "CN" else YOUTUBE_URL
    webbrowser.open(url)
    return url


def maybe_open_for_current_python_script() -> Optional[str]:
    """当前解释器执行 Python 源文件时自动打开视频。

    设置环境变量 NBPL_DISABLE_AUTO_OPEN=1 可关闭自动行为。
    """
    if os.environ.get("NBPL_DISABLE_AUTO_OPEN") == "1":
        return None
    script = sys.argv[0] if sys.argv else ""
    if not script.lower().endswith((".py", ".pyw")):
        return None
    return open_video_for_country(detect_country_code())


def run_once(country_code: Optional[str] = None) -> Optional[str]:
    """发现其他 Python 脚本正在运行时，仅打开一次视频。

    可传入 country_code 以方便测试；未传入时会通过公网 IP 检测。
    """
    if not find_running_python_scripts():
        return None
    return open_video_for_country(
        detect_country_code() if country_code is None else country_code
    )


def watch(
    interval: float = 1.0,
    country_code: Optional[str] = None,
    on_open: Optional[Callable[[str], None]] = None,
) -> None:
    """等待 Python 脚本出现，打开视频后返回。"""
    if interval <= 0:
        raise ValueError("interval 必须大于零")

    while True:
        url = run_once(country_code=country_code)
        if url:
            if on_open:
                on_open(url)
            return
        time.sleep(interval)
