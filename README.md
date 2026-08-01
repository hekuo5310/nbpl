# nbpl

`nbpl` waits until it detects another running Python process whose command line includes a `.py` or `.pyw` file. It then opens one video in the system default browser:

| Public IP country code | URL |
| --- | --- |
| `CN` (China mainland) | https://www.bilibili.com/video/BV1GJ411x7h7 |
| Any other value, including an unavailable lookup | https://www.youtube.com/watch?v=dQw4w9WgXcQ |

The country lookup uses `https://ipapi.co/json/`. The package only reads process command lines and makes that one IP-location request; it does not upload the detected script paths.

## Install

```bash
pip install nbpl
```

## Use

Start the watcher:

```bash
nbpl
```

Or:

```bash
python -m nbpl
```

The command checks once per second by default, opens the appropriate link after it finds a Python script, then exits. To use a different polling interval:

```bash
nbpl --interval 2
```

For deterministic local testing, bypass the IP lookup:

```bash
nbpl --country-code CN
```

## Python API

```python
from nbpl import run_once, watch

run_once()  # only opens a link when another Python script is already running
watch(interval=1.0)  # waits for one, opens the link, and returns
```
