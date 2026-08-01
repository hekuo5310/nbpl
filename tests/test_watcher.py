import unittest
from unittest.mock import patch

from nbpl.watcher import (
    BILIBILI_URL,
    YOUTUBE_URL,
    ScriptProcess,
    _script_from_cmdline,
    open_video_for_country,
    run_once,
    watch,
)


class WatcherTests(unittest.TestCase):
    def test_script_from_python_command_line(self):
        self.assertEqual(
            _script_from_cmdline(["python3", "-u", "server.py", "--port", "8000"]),
            "server.py",
        )

    def test_script_from_non_python_command_line_is_ignored(self):
        self.assertIsNone(_script_from_cmdline(["node", "script.py"]))

    @patch("nbpl.watcher.webbrowser.open")
    def test_china_opens_bilibili(self, browser_open):
        self.assertEqual(open_video_for_country("CN"), BILIBILI_URL)
        browser_open.assert_called_once_with(BILIBILI_URL)

    @patch("nbpl.watcher.webbrowser.open")
    def test_non_china_or_unknown_opens_youtube(self, browser_open):
        self.assertEqual(open_video_for_country(None), YOUTUBE_URL)
        browser_open.assert_called_once_with(YOUTUBE_URL)

    @patch("nbpl.watcher.open_video_for_country")
    @patch("nbpl.watcher.find_running_python_scripts")
    def test_run_once_does_nothing_without_script(self, find_scripts, open_video):
        find_scripts.return_value = []
        self.assertIsNone(run_once(country_code="CN"))
        open_video.assert_not_called()

    @patch("nbpl.watcher.open_video_for_country", return_value=BILIBILI_URL)
    @patch("nbpl.watcher.find_running_python_scripts")
    def test_run_once_opens_when_script_exists(self, find_scripts, open_video):
        find_scripts.return_value = [ScriptProcess(pid=1, script="app.py")]
        self.assertEqual(run_once(country_code="CN"), BILIBILI_URL)
        open_video.assert_called_once_with("CN")

    def test_watch_rejects_non_positive_interval(self):
        with self.assertRaises(ValueError):
            watch(interval=0, country_code="CN")
