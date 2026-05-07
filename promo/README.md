# Card News Builder — 홍보영상 v1.0

스레드(Threads) 게시용 30초 1:1 홍보영상.
**메인 앵글**: "60,000 조합으로 카드뉴스를 1분에"

## 산출물

- `output/cardnews-promo-v1.mp4` — 최종 영상 (자막 + BGM 포함, 스레드 업로드용)
- `output/cardnews-promo-v1-noaudio.mp4` — BGM 없는 미리보기 (BGM 다운로드 전 임시)
- `output/subbed.mp4` — 자막만 합성된 중간 산출물
- `output/raw.mp4` — 자막·BGM 없는 raw 30초 영상

## 폴더 구조

```
promo/
├── README.md                # 이 파일
├── script.md                # 스토리보드 + 자막 SSOT
├── subtitles.ass            # FFmpeg libass용 자막 (한+영 듀얼)
├── capture.py               # Playwright 자동 캡처 스크립트
├── render.sh                # FFmpeg 합성 명령 묶음
├── bgm.mp3                  # lo-fi BGM (Pixabay 다운로드, .gitignore)
├── fonts/
│   ├── Pretendard-Black.otf # 한국어 자막
│   └── Inter-SemiBold.ttf   # 영어 자막
├── frames/                  # 캡처 시퀀스 (.gitignore)
│   └── cut-1.png ~ cut-8.png
└── output/                  # 합성 산출물 (.gitignore 일부)
    ├── concat.txt
    ├── raw.mp4
    ├── subbed.mp4
    ├── cardnews-promo-v1-noaudio.mp4
    └── cardnews-promo-v1.mp4   # ← 최종, .gitignore에서 negation으로 포함
```

## 재생성 방법

### 사전 준비

1. **FFmpeg 설치** (8.0+ 권장):
   - macOS: `brew install ffmpeg`
   - Windows: `choco install ffmpeg` 또는 `winget install ffmpeg`
   - Linux: `sudo apt install ffmpeg`

2. **Python + Playwright** (캡처용):
   ```bash
   pip install playwright
   playwright install chromium  # 또는 시스템 Chrome 사용 (capture.py가 자동 fallback)
   ```

3. **BGM 다운로드** (Pixabay):
   - https://pixabay.com/music/search/genre/lo-fi/
   - 30초 이상 lo-fi 트랙 1곡 선택 → mp3 다운로드
   - `promo/bgm.mp3` 경로에 저장
   - License: Pixabay Content License (상업 사용 OK, 출처 표기 불필요)

4. **빌더 서버** 실행:
   ```bash
   cd projects/cardnews-public
   python -m http.server 9240
   ```

### 실행

전체 파이프라인:
```bash
cd projects/cardnews-public/promo
bash render.sh
```

프레임 재캡처까지 포함:
```bash
bash render.sh --recapture
```

### 단계별 수동 실행

1. **캡처** (8개 PNG): `py capture.py`
2. **raw.mp4** (30s 1:1):
   ```bash
   ffmpeg -y -f concat -safe 0 -i output/concat.txt -t 30 \
     -vf "scale=1080:576,pad=1080:1080:0:252:black,fps=30" \
     -c:v libx264 -pix_fmt yuv420p -crf 23 -preset medium \
     output/raw.mp4
   ```
3. **자막 합성**:
   ```bash
   ffmpeg -y -i output/raw.mp4 \
     -vf "ass=subtitles.ass:fontsdir=fonts" \
     -c:v libx264 -pix_fmt yuv420p -crf 23 \
     output/subbed.mp4
   ```
4. **BGM 합성** (final):
   ```bash
   ffmpeg -y -i output/subbed.mp4 -i bgm.mp3 \
     -filter_complex "[1:a]atrim=0:30,afade=t=in:st=0:d=1,afade=t=out:st=28:d=2,volume=0.6[a]" \
     -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 128k -shortest \
     output/cardnews-promo-v1.mp4
   ```

## 자막 수정

`script.md`(SSOT) → `subtitles.ass` 동기화 → Task 6, 7 재실행:
```bash
bash render.sh
```

## BGM 변경

`bgm.mp3`만 교체하고 Task 7만 재실행:
```bash
ffmpeg -y -i output/subbed.mp4 -i bgm.mp3 \
  -filter_complex "[1:a]atrim=0:30,afade=t=in:st=0:d=1,afade=t=out:st=28:d=2,volume=0.6[a]" \
  -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 128k -shortest \
  output/cardnews-promo-v1.mp4
```

## 라이선스

- 영상 저작권: MIT © 2026 COMMME (cardnews-public 패키지에 포함)
- 폰트: Pretendard (SIL OFL 1.1) · Inter (SIL OFL 1.1)
- BGM: Pixabay Content License (다운로드 트랙명 채워주세요)

## 크레딧

Built with Claude Code · Playwright · FFmpeg · Pretendard · Inter
