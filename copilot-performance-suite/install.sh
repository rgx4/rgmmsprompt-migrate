#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
payload="$script_dir/.copilot"
scope="user"
project_path=""
force="false"

usage() {
  echo "Usage: ./install.sh [--user | --project PATH] [--force]"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --user)
      scope="user"
      shift
      ;;
    --project)
      [[ $# -ge 2 ]] || { usage; exit 2; }
      scope="project"
      project_path="$2"
      shift 2
      ;;
    --force)
      force="true"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      exit 2
      ;;
  esac
done

if [[ "$scope" == "user" ]]; then
  target="${COPILOT_HOME:-${HOME}/.copilot}"
else
  target="$(cd "$project_path" && pwd)/.github"
fi

conflicts=()
for source_file in "$payload"/agents/*.agent.md; do
  destination="$target/agents/$(basename "$source_file")"
  [[ -e "$destination" ]] && conflicts+=("$destination")
done
for source_dir in "$payload"/skills/*; do
  destination="$target/skills/$(basename "$source_dir")"
  [[ -e "$destination" ]] && conflicts+=("$destination")
done

if [[ ${#conflicts[@]} -gt 0 && "$force" != "true" ]]; then
  echo "Installation stopped because these targets already exist:" >&2
  printf '  %s\n' "${conflicts[@]}" >&2
  echo "Re-run with --force to merge/overwrite matching files." >&2
  exit 3
fi

mkdir -p "$target/agents" "$target/skills"
cp -R "$payload/agents/." "$target/agents/"
cp -R "$payload/skills/." "$target/skills/"
python3 "$script_dir/tools/verify_package.py" "$target"
echo "Installed performance suite in $target"
echo "Restart GitHub Copilot CLI before selecting performance-orchestrator."

