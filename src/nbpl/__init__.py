"""检测运行中的 Python 脚本，并打开对应的视频。"""

from .watcher import (
    BILIBILI_URL,
    YOUTUBE_URL,
    ScriptProcess,
    detect_country_code,
    find_running_python_scripts,
    maybe_open_for_current_python_script,
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
    "maybe_open_for_current_python_script",
    "open_video_for_country",
    "run_once",
    "watch",
]
