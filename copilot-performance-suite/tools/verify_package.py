#!/usr/bin/env python3
"""Validate the performance suite package or an installed Copilot target."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


AGENTS = {
    "performance-orchestrator.agent.md",
    "frontend-performance-investigator.agent.md",
    "dotnet-performance-investigator.agent.md",
    "sql-performance-investigator.agent.md",
}

SKILLS = {
    "chrome-devtools",
    "sql-optimization",
    "analyzing-dotnet-performance",
    "dotnet-trace-collect",
    "dotnet-runtime-analysis",
    "dump-collect",
    "vercel-react-best-practices",
}


def frontmatter(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not match:
        raise ValueError(f"Missing YAML frontmatter: {path}")
    block = match.group(1)
    if not re.search(r"(?m)^name:\s*.+$", block):
        raise ValueError(f"Missing name in frontmatter: {path}")
    if not re.search(r"(?m)^description:\s*.+$", block):
        raise ValueError(f"Missing description in frontmatter: {path}")
    return block


def locate_payload(root: Path) -> Path:
    if (root / ".copilot" / "agents").is_dir():
        return root / ".copilot"
    if (root / "agents").is_dir() and (root / "skills").is_dir():
        return root
    if (root / ".github" / "agents").is_dir():
        return root / ".github"
    raise ValueError(f"Could not find agents/ and skills/ below {root}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    payload = locate_payload(root)

    errors: list[str] = []
    for name in sorted(AGENTS):
        path = payload / "agents" / name
        if not path.is_file():
            errors.append(f"Missing agent: {name}")
            continue
        try:
            block = frontmatter(path)
            if re.search(r"(?m)^tools:.*\bedit\b", block, re.IGNORECASE):
                errors.append(f"Read-only agent exposes edit tool: {name}")
            if "chrome-devtools" in block:
                for required in ("chrome-devtools-mcp@1.9.0", "--no-usage-statistics", "--no-performance-crux", "--redactNetworkHeaders"):
                    if required not in block:
                        errors.append(f"Chrome agent {name} is missing required MCP setting: {required}")
        except ValueError as error:
            errors.append(str(error))

    for name in sorted(SKILLS):
        path = payload / "skills" / name / "SKILL.md"
        if not path.is_file():
            errors.append(f"Missing skill: {name}")
            continue
        try:
            frontmatter(path)
        except ValueError as error:
            errors.append(str(error))

    runtime_script = payload / "skills" / "dotnet-runtime-analysis" / "scripts" / "summarize_speedscope.py"
    if runtime_script.is_file():
        try:
            compile(runtime_script.read_text(encoding="utf-8"), str(runtime_script), "exec")
        except SyntaxError as error:
            errors.append(f"Runtime analysis script does not compile: {error}")

    package_root = root if (root / "source-lock.json").is_file() else None
    if package_root:
        try:
            lock = json.loads((package_root / "source-lock.json").read_text(encoding="utf-8"))
            if lock.get("chrome_devtools_mcp", {}).get("npm_version") != "1.9.0":
                errors.append("Chrome DevTools MCP version does not match the agents' pinned version")
        except (OSError, json.JSONDecodeError) as error:
            errors.append(f"Invalid source-lock.json: {error}")
        try:
            plugin = json.loads((package_root / "plugin.json").read_text(encoding="utf-8"))
            if plugin.get("name") != "performance-investigation-suite":
                errors.append("plugin.json has the wrong plugin name")
            if plugin.get("agents") != ".copilot/agents/":
                errors.append("plugin.json does not point to the bundled agents")
            if plugin.get("skills") != [".copilot/skills/"]:
                errors.append("plugin.json does not point to the bundled skills")
        except (OSError, json.JSONDecodeError) as error:
            errors.append(f"Invalid plugin.json: {error}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"OK: {len(AGENTS)} agents and {len(SKILLS)} skills validated in {payload}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
