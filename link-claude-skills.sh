#!/usr/bin/env bash
set -euo pipefail

mkdir -p .claude/skills

for skill in \
  clinica-mobile-producto \
  clinica-mobile-flet \
  clinica-mobile-integracion
do
  rm -rf ".claude/skills/$skill"
  ln -s "../../.agents/skills/$skill" ".claude/skills/$skill"
done

echo "Claude project skills linked to .agents/skills."
