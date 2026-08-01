# nbpl

安装 nbpl 后，不需要在任何脚本中导入它。它会通过 Python 的 sitecustomize 启动钩子，在执行 Python 源文件时自动使用系统默认浏览器打开一个视频：

| 公网 IP 所在国家/地区代码 | 打开的链接 |
| --- | --- |
| CN（中国大陆） | https://www.bilibili.com/video/BV1GJ411x7h7 |
| 其他代码，或定位失败 | https://www.youtube.com/watch?v=dQw4w9WgXcQ |

地区查询使用 https://ipapi.co/json/。本包仅会读取进程命令行并发起一次 IP 地理位置查询；不会上传检测到的脚本路径。

## 安装

~~~bash
pip install nbpl
~~~

也可以直接从本仓库安装：

~~~bash
pip install git+https://github.com/hekuo5310/nbpl.git
~~~

## 自动使用

安装后，直接运行任意 Python 文件即可自动触发：

~~~bash
python app.py
~~~

如果只想作为独立监控器使用，仍可运行：

~~~bash
nbpl
~~~

独立监控器默认每秒检查一次；发现其他 Python 脚本后打开对应链接并退出。修改检查间隔：

~~~bash
nbpl --interval 2
~~~

本地测试时可跳过 IP 查询，直接指定地区：

~~~bash
nbpl --country-code CN
~~~

## 临时关闭自动触发

为避免自动打开浏览器，可在运行命令前设置环境变量：

~~~bash
NBPL_DISABLE_AUTO_OPEN=1 python app.py
~~~

Windows PowerShell：

~~~powershell
$env:NBPL_DISABLE_AUTO_OPEN = "1"; python app.py
~~~

## Python API

~~~python
from nbpl import run_once, watch

run_once()  # 仅当已有其他 Python 脚本在运行时才打开链接
watch(interval=1.0)  # 等待脚本出现，打开链接后返回
~~~
