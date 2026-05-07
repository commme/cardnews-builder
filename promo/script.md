# 카드뉴스 빌더 홍보영상 v2.0 — Script & Subtitles

**길이**: 30초 / **비율**: 1:1 (1080×1080) / **자막**: 한국어 + 영어 듀얼

> v2.0 변경점: 비율 토글(1:1/4:5/9:16/16:9) + 출력 포맷(M-1~M-4) + 다양한 모션(M-15/M-21/M-25) + 팔레트 P-1/P-11/P-19 데모를 명시적으로 보여주도록 storyboard 재설계.

## 컷 구조

| # | 시간 | 화면 | 한국어 (위) | English (below) |
|---|------|------|------------|-----------------|
| 1 | 0~3s | 빌더 첫 화면 (P-1, 1:1, M-1) | 카드뉴스 만들기, 막막하셨죠? | Tired of making card news? |
| 2 | 3~7s | P-1 + 모션 M-15 scale-pop 프리뷰 | 팔레트 1번 + Scale-pop 모션 | P-1 + scale-pop motion |
| 3 | 7~11s | 비율 토글 9:16 (1080×1920) | 4가지 비율, 즉시 전환 | 4 aspects, instant switch |
| 4 | 11~15s | 1:1 복귀 + 출력포맷 M-2 GIF 강조 | 출력 4종 · PNG GIF Reels Remotion | 4 outputs · PNG GIF Reels Remotion |
| 5 | 15~19s | P-11 + 모션 M-21 glitch-rgb 프리뷰 | 팔레트 11번 · Glitch 모션 | P-11 · Glitch motion |
| 6 | 19~23s | P-19 + 모션 M-25 sparkle 프리뷰 | 팔레트 19번 · Sparkle 모션 | P-19 · Sparkle motion |
| 7 | 23~27s | 헤더 칩 60,000 줌인 + 복사 토스트 | 20 × 50 × 60 = 60,000 조합 | 20 × 50 × 60 = 60,000 |
| 8 | 27~30s | 로고 + GitHub + MIT | MIT · 오픈소스 · 무료 | MIT · Open Source · Free |

총: 3+4+4+4+4+4+4+3 = 30초

## 자막 디자인

- 한국어: Pretendard Black, 56pt, white #FFFFFF, black background 80% opacity
- 영어: Inter SemiBold, 36pt, white #FFFFFF, black background 80% opacity
- 위치: 한국어 상단 60px 마진, 영어 하단 60px 마진
- 등장 효과: 컷 시작 0.3초 fade-in, 컷 끝 0.3초 fade-out

## 자막 SSOT 동기화

`subtitles.ass`와 본 파일은 동기화되어야 함. 자막 수정 시 둘 다 갱신.

## 데모 핵심 (v2.0 강조 포인트)

1. **비율 4종**: 1:1 정사각 → 9:16 Reels (cut-3에서 토글 시각화)
2. **출력 4종**: M-1 PNG / M-2 GIF / M-3 Reels MP4 / M-4 Remotion (cut-4에서 M-2 강조)
3. **팔레트 다양성**: P-1 (cut-1,2) → P-11 (cut-5) → P-19 (cut-6) — 라이브 recolor 효과
4. **모션 다양성**: M-15 scale-pop (Kinetic) → M-21 glitch-rgb (Effect) → M-25 sparkle (Effect)
5. **조합 강조**: 20 × 50 × 60 = 60,000 (cut-7 헤더 줌인)
