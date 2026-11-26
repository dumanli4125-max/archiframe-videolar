#!/usr/bin/env bash
# Hazır bir MP4'ün sesini -14 LUFS'a çeker (görüntüye dokunmaz). Kullanım: bash renorm.sh videolar/02-x.mp4
set -euo pipefail
T=$(mktemp -d); bash "$(dirname "$0")/loudnorm.sh" "$1" "$T/a.m4a"
ffmpeg -y -loglevel error -i "$1" -i "$T/a.m4a" -map 0:v -map 1:a -c copy "$T/o.mp4" && mv "$T/o.mp4" "$1"; rm -rf "$T"
ffmpeg -i "$1" -af loudnorm=print_format=summary -f null - 2>&1 | grep "Input Integrated"
