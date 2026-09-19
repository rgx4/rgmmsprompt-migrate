#!/usr/bin/env python3
"""Summarise sampled or evented Speedscope profiles using only the stdlib."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable


def frame_label(frame: dict[str, Any]) -> str:
    name = str(frame.get("name", "<unnamed>"))
    file_name = frame.get("file")
    line = frame.get("line")
    if file_name:
        location = str(file_name)
        if line is not None:
            location += f":{line}"
        return f"{name} [{location}]"
    return name


def add_interval(
    stack: list[int],
    weight: float,
    self_time: dict[int, float],
    inclusive_time: dict[int, float],
) -> None:
    if weight <= 0 or not stack:
        return
    self_time[stack[-1]] += weight
    for frame_index in set(stack):
        inclusive_time[frame_index] += weight


def sampled_totals(profile: dict[str, Any]) -> tuple[dict[int, float], dict[int, float], float]:
    samples = profile.get("samples") or []
    weights = profile.get("weights")
    if weights is None:
        weights = [1.0] * len(samples)
    if len(weights) != len(samples):
        raise ValueError("Sample and weight counts differ")

    self_time: dict[int, float] = defaultdict(float)
    inclusive_time: dict[int, float] = defaultdict(float)
    total = 0.0
    for stack, raw_weight in zip(samples, weights):
        weight = float(raw_weight)
        add_interval([int(value) for value in stack], weight, self_time, inclusive_time)
        total += max(weight, 0.0)
    return self_time, inclusive_time, total


def evented_totals(profile: dict[str, Any]) -> tuple[dict[int, float], dict[int, float], float]:
    events = profile.get("events") or []
    self_time: dict[int, float] = defaultdict(float)
    inclusive_time: dict[int, float] = defaultdict(float)
    stack: list[int] = []
    start = float(profile.get("startValue", events[0].get("at", 0.0) if events else 0.0))
    previous = start

    for event in events:
        at = float(event.get("at", previous))
        if at < previous:
            raise ValueError("Event timestamps are not monotonic")
        add_interval(stack, at - previous, self_time, inclusive_time)
        kind = event.get("type")
        frame_index = int(event.get("frame", -1))
        if kind == "O":
            stack.append(frame_index)
        elif kind == "C":
            if not stack:
                raise ValueError("Close event encountered with an empty stack")
            opened = stack.pop()
            if opened != frame_index:
                raise ValueError(f"Mismatched close event: expected frame {opened}, got {frame_index}")
        else:
            raise ValueError(f"Unsupported event type: {kind!r}")
        previous = at

    end = float(profile.get("endValue", previous))
    if end < previous:
        raise ValueError("Profile endValue precedes the last event")
    add_interval(stack, end - previous, self_time, inclusive_time)
    return self_time, inclusive_time, max(end - start, 0.0)


def rows(
    values: dict[int, float],
    frames: list[dict[str, Any]],
    total: float,
    matcher: re.Pattern[str] | None,
    limit: int,
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for index, value in sorted(values.items(), key=lambda item: item[1], reverse=True):
        frame = frames[index] if 0 <= index < len(frames) else {"name": f"<invalid frame {index}>"}
        label = frame_label(frame)
        if matcher and not matcher.search(label):
            continue
        output.append(
            {
                "frame_index": index,
                "frame": label,
                "value": value,
                "percent": (value / total * 100.0) if total else 0.0,
            }
        )
        if len(output) >= limit:
            break
    return output


def summarise(document: dict[str, Any], selected: Iterable[int], top: int, match: str | None) -> dict[str, Any]:
    frames = document.get("shared", {}).get("frames") or []
    profiles = document.get("profiles") or []
    matcher = re.compile(match, re.IGNORECASE) if match else None
    summaries: list[dict[str, Any]] = []

    for index in selected:
        if index < 0 or index >= len(profiles):
            raise ValueError(f"Profile index {index} is out of range (0..{len(profiles) - 1})")
        profile = profiles[index]
        profile_type = profile.get("type")
        if profile_type == "sampled":
            self_time, inclusive_time, total = sampled_totals(profile)
        elif profile_type == "evented":
            self_time, inclusive_time, total = evented_totals(profile)
        else:
            raise ValueError(f"Unsupported profile type at index {index}: {profile_type!r}")

        summaries.append(
            {
                "profile_index": index,
                "name": profile.get("name", f"profile-{index}"),
                "type": profile_type,
                "unit": profile.get("unit", "none"),
                "total": total,
                "top_self": rows(self_time, frames, total, matcher, top),
                "top_inclusive": rows(inclusive_time, frames, total, matcher, top),
            }
        )
    return {"profiles": summaries}


def markdown_table(title: str, items: list[dict[str, Any]], unit: str) -> list[str]:
    lines = [f"### {title}", "", f"| Rank | Frame | Value ({unit}) | Percent |", "|---:|---|---:|---:|"]
    if not items:
        lines.append("| - | No matching frames | 0 | 0% |")
        return lines
    for rank, item in enumerate(items, start=1):
        safe_frame = str(item["frame"]).replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {rank} | `{safe_frame}` | {item['value']:.6g} | {item['percent']:.2f}% |")
    return lines


def to_markdown(summary: dict[str, Any]) -> str:
    lines = ["# Speedscope summary", ""]
    for profile in summary["profiles"]:
        lines.extend(
            [
                f"## Profile {profile['profile_index']}: {profile['name']}",
                "",
                f"- Type: `{profile['type']}`",
                f"- Unit: `{profile['unit']}`",
                f"- Total profile weight/duration: `{profile['total']:.6g}`",
                "",
            ]
        )
        lines.extend(markdown_table("Top self", profile["top_self"], profile["unit"]))
        lines.append("")
        lines.extend(markdown_table("Top inclusive", profile["top_inclusive"], profile["unit"]))
        lines.append("")
    lines.append("> Sampled weights show on-CPU profile weight; they do not by themselves explain wall-clock waits or downstream time.")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("trace", type=Path, help="Path to a .speedscope.json file")
    parser.add_argument("--top", type=int, default=20, help="Number of frames per table (default: 20)")
    parser.add_argument("--profile", type=int, action="append", help="Profile index; repeat to select multiple")
    parser.add_argument("--match", help="Case-insensitive regular expression applied to frame labels")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.top < 1:
        raise ValueError("--top must be at least 1")
    with args.trace.open("r", encoding="utf-8") as handle:
        document = json.load(handle)
    profile_count = len(document.get("profiles") or [])
    selected = args.profile if args.profile is not None else range(profile_count)
    summary = summarise(document, selected, args.top, args.match)
    if args.format == "json":
        json.dump(summary, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(to_markdown(summary))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, json.JSONDecodeError, re.error) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(2)

