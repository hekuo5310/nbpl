"""Python 启动钩子：无需在脚本中导入 nbpl。"""

try:
    from nbpl.watcher import maybe_open_for_current_python_script

    maybe_open_for_current_python_script()
except Exception:
    # 启动钩子不能阻止用户的 Python 程序正常运行。
    pass
