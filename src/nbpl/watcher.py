"""Process watching and country detection for nbpl."""

from __future__ import annotations

import os
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
    """A running Python interpreter associated with a ``.py`` file."""

    pid: int
    script: str


def _is_python_interpreter(executable: str) -> bool:
    name = Path(executable).name.lower()
    return name.startswith("python") or name in {"py", "py.exe"}


def _script_from_cmdline(cmdline: list[str]) -> Optional[str]:
    """Return the first direct .py argument after a Python interpreter."""
    if not cmdline or not _is_python_interpreter(cmdline[0]):
        return None

    for argument in cmdline[1:]:
        if argument.lower().endswith((".py", ".pyw")):
            return argument
    return None


def find_running_python_scripts() -> list[ScriptProcess]:
    """List other running processes that execute a Python source file."""
    try:
        import psutil
    except ImportError as exc:  # pragma: no cover - dependency is installed normally
        raise RuntimeError("nbpl requires psutil; reinstall the package") from exc

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
    """Return the public IP country code, or ``None`` if it cannot be determined."""
    try:
        import requests
    except ImportError as exc:  # pragma: no cover - dependency is installed normally
        raise RuntimeError("nbpl requires requests; reinstall the package") from exc

    try:
        response = requests.get(IP_API_URL, timeout=timeout)
        response.raise_for_status()
        country_code = response.json().get("country_code")
        return country_code.upper() if isinstance(country_code, str) else None
    except (requests.RequestException, ValueError):
        return None


def open_video_for_country(country_code: Optional[str]) -> str:
    """Open and return the configured video URL for a country code."""
    url = BILIBILI_URL if country_code == "CN" else YOUTUBE_URL
    webbrowser.open(url)
    return url


def run_once(country_code: Optional[str] = None) -> Optional[str]:
    """Open a video once if at least one other Python script is running.

    ``country_code`` is injectable for deterministic use and tests. If omitted,
    nbpl discovers the country from the public IP address.
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
    """Wait for a Python script to appear, then open the video and return."""
    if interval <= 0:
        raise ValueError("interval must be greater than zero")

    while True:
        url = run_once(country_code=country_code)
        if url:
            if on_open:
                on_open(url)
            return
        time.sleep(interval)
