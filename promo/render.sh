#!/usr/bin/env bash
# Card News Builder — Promo Video Re-render
# Usage: bash render.sh
# Prereq: bgm.mp3, subtitles.ass, frames/cut-{1..8}.png, fonts/Pretendard-Black.otf, fonts/Inter-SemiBold.ttf
#
# Output: output/cardnews-promo-v1.mp4 (30s, 1080×1080, h264+aac, ~600KB)

set -e
cd "$(dirname "$0")"

# Step 1: Re-capture frames (optional, only if you want to update screenshots)
if [ "$1" = "--recapture" ]; then
  echo "[0/3] Re-capturing 8 frames via Playwright..."
  py capture.py
fi

echo "[1/3] Generating raw.mp4 (concat 8 frames → 30s 1:1)..."
ffmpeg -y -f concat -safe 0 -i output/concat.txt \
  -t 30 \
  -vf "scale=1080:576,pad=1080:1080:0:252:black,fps=30" \
  -c:v libx264 -pix_fmt yuv420p -crf 23 -preset medium \
  output/raw.mp4

echo "[2/3] Adding subtitles (KO + EN dual)..."
ffmpeg -y -i output/raw.mp4 \
  -vf "ass=subtitles.ass:fontsdir=fonts" \
  -c:v libx264 -pix_fmt yuv420p -crf 23 -preset medium \
  output/subbed.mp4

if [ -f bgm.mp3 ]; then
  echo "[3/3] Adding BGM (lo-fi) + final mp4..."
  ffmpeg -y -i output/subbed.mp4 -i bgm.mp3 \
    -filter_complex "[1:a]atrim=0:30,afade=t=in:st=0:d=1,afade=t=out:st=28:d=2,volume=0.6[a]" \
    -map 0:v -map "[a]" \
    -c:v copy -c:a aac -b:a 128k -shortest \
    output/cardnews-promo-v1.mp4
  echo "Done: output/cardnews-promo-v1.mp4"
  ls -la output/cardnews-promo-v1.mp4
else
  echo "[3/3] bgm.mp3 not found — skipping BGM step."
  echo "Use output/subbed.mp4 as preview, or download BGM and re-run."
  cp output/subbed.mp4 output/cardnews-promo-v1-noaudio.mp4
  echo "Output: output/cardnews-promo-v1-noaudio.mp4 (no audio)"
  ls -la output/cardnews-promo-v1-noaudio.mp4
fi
