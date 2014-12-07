#!/usr/bin/env bash
# Builds the game with PyInstaller and zips it as dist/<NAME>-<platform>.zip
# Usage: build.sh <platform>   (env: PY, NAME, MAIN, DEPS)
set -euo pipefail
PLATFORM="$1"
PY="${PY:-python}"
"$PY" -m pip install $DEPS
"$PY" -m PyInstaller --noconfirm --onedir --name "$NAME" "$MAIN"
for f in *; do
  case "$f" in
    *.py|*.md|*.spec|build|dist|docs|experiments) ;;
    *) cp -R "$f" "dist/$NAME/" ;;
  esac
done
cd dist
"$PY" -c "import shutil, sys; shutil.make_archive(sys.argv[1], 'zip', '.', sys.argv[2])" "$NAME-$PLATFORM" "$NAME"
echo "Built dist/$NAME-$PLATFORM.zip"
