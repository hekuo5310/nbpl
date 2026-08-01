"""Command-line interface for nbpl."""

from __future__ import annotations

import argparse

from .watcher import watch


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Open a region-specific video when a Python script is running."
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=1.0,
        help="seconds between process checks (default: 1)",
    )
    parser.add_argument(
        "--country-code",
        help="override public-IP detection, useful for testing (for example CN)",
    )
    args = parser.parse_args()
    watch(interval=args.interval, country_code=args.country_code)
