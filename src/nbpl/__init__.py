"""Detect running Python scripts and open the appropriate video."""

from .watcher import (
    BILIBILI_URL,
    YOUTUBE_URL,
    ScriptProcess,
    detect_country_code,
    find_running_python_scripts,
    open_video_for_country,
    run_once,
    watch,
)

__all__ = [
    "BILIBILI_URL",
    "YOUTUBE_URL",
    "ScriptProcess",
    "detect_country_code",
    "find_running_python_scripts",
    "open_video_for_country",
    "run_once",
    "watch",
]
