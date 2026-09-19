#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / ".copilot/skills/dotnet-runtime-analysis/scripts/summarize_speedscope.py"
FIXTURE = ROOT / "tests/fixtures/sample.speedscope.json"
sys.dont_write_bytecode = True


def load_module():
    spec = importlib.util.spec_from_file_location("summarize_speedscope", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    module = load_module()
    document = json.loads(FIXTURE.read_text(encoding="utf-8"))
    summary = module.summarise(document, [0, 1], 10, None)

    sampled = summary["profiles"][0]
    assert sampled["total"] == 10
    assert sampled["top_self"][0]["frame"].startswith("Controller")
    assert sampled["top_self"][0]["value"] == 6
    assert sampled["top_inclusive"][0]["frame"] == "Root"
    assert sampled["top_inclusive"][0]["value"] == 10

    evented = summary["profiles"][1]
    assert evented["total"] == 10
    assert evented["top_self"][0]["frame"].startswith("Controller")
    assert evented["top_self"][0]["value"] == 6
    assert evented["top_inclusive"][0]["frame"] == "Root"
    assert evented["top_inclusive"][0]["value"] == 10
    print("OK: Speedscope sampled and evented summaries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
