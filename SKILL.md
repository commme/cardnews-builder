---
name: cardnews
description: 인스타그램 카드뉴스 8컷 자동 생성 스킬 (Claude Code용). 빌더(menu.html)에서 팔레트·프리셋·모션을 클릭하면 일관된 디자인의 8컷이 PNG/GIF/Reels MP4/Remotion 영상으로 출력됨. 트리거 키워드는 "카드뉴스 만들어", "8컷 요약", "인스타용 카드뉴스", "instagram carousel", "card news"입니다.
---

# 🎨 Card News Builder Skill

> Claude Code용 인스타그램 카드뉴스 8컷 자동 생성 스킬.
> 빌더에서 클릭만 하면 일관된 디자인의 8컷이 PNG/GIF/MP4로 나옵니다.

## 0. 빠른 사용

1. `menu.html`을 브라우저에서 엽니다 (또는 `python -m http.server 9230`로 서빙).
2. 빌더에서 출력 → 팔레트 → 슬롯(커버/내용/CTA) 토글 → 프리셋·모션 선택.
3. **[복사]** 버튼 클릭.
4. Claude Code 채팅에 붙여넣기 → 8컷 PNG 자동 생성.

## 1. 자료 카탈로그 (요약)

| 분류 | 개수 | ID 범위 | 자세히 |
|------|------|---------|---------|
| 팔레트 | 20 | P-1 ~ P-20 | `MENU.md` §1 |
| 프리셋 | 50 | F-1 ~ F-50 (Classic 10 + Trendy 15 + Typography 8 + Data 9 + Novelty 8) | `MENU.md` §2 |
| 모션 | 60 | M-1 ~ M-60 (출력 4 + 효과 56) | `MENU.md` §3 |
| 조합 수 | 60,000 | 20 × 50 × 60 | — |

## 2. 빌더 입력 처리 (menu.html 출력 양식)

사용자가 menu.html 빌더에서 복사한 프롬프트가 들어오면 다음 규칙으로 처리한다.

### 2.1 입력 양식

```
cardnews 스킬로 만들어줘.

[출력] M-{n} (이름)        ← 결과물 형식
[비율] {ratio} ({W}×{H})    ← 결과물 픽셀 사이즈
[팔레트] P-{n} (이름)       ← 8컷 전체 적용
[프리셋]
- 커버: F-{n} (이름)
- 내용: F-{n} (이름)
- CTA: F-{n} (이름)
[모션]
- 커버: M-{n} (이름)
- 내용: M-{n} (이름)
- CTA: M-{n} (이름)

주제: {텍스트}
```

### 2.1.1 비율 → 픽셀 매핑

| 비율 | 픽셀 (W×H) | 용도 |
|------|-----------|------|
| 1:1 | 1080×1080 | 인스타 정사각, 트위터 카드 |
| 4:5 | 1080×1350 | 인스타 캐러셀 기본 (세로 길게) |
| 9:16 | 1080×1920 | 인스타 Reels, 유튜브 Shorts, TikTok |
| 16:9 | 1920×1080 | 유튜브, 블로그 가로, 데스크톱 와이드 |

### 2.2 8컷 슬롯 매핑

| 컷 # | 슬롯 | 적용 프리셋·모션 |
|------|------|-------------------|
| 1 | 커버 | cover.preset · cover.motion |
| 2~7 (6장) | 내용 | content.preset · content.motion |
| 8 | CTA · 크레딧 | cta.preset · cta.motion |

### 2.3 출력 포맷별 분기 (M-1 ~ M-4)

- **M-1 (static-png)**: PIL → 1080×1350 PNG 8장 (인스타 캐러셀 기본)
- **M-2 (animated-gif)**: PIL → PNG 8장 + FFmpeg → GIF 순환
- **M-3 (reels-mp4)**: PIL → PNG 8장 + FFmpeg → 1080×1920 9:16 MP4
- **M-4 (remotion)**: React Remotion `.tsx` 컴포넌트 코드 생성 (사용자가 별도 렌더)

### 2.4 팔레트 색상 매핑

`MENU.md` §1에서 P-{n} 항목 조회 후 다음 변수에 매핑:

```python
bg     = colors[0]
accent = colors[1]
fg     = colors[-1]
muted  = colors[-2] if len(colors) >= 4 else shade(fg, -30)
line   = shade(bg, 15)
```

`shade(hex, percent)` = 각 RGB 채널에 `round(255 * percent / 100)` 더하기, [0,255] 클램프.

### 2.5 프리셋·모션 의미

각 F-{n} / M-{n}의 정확한 디자인·애니메이션 명세는 `MENU.md` §2/§3 + `references/preset-motion-pairings.md` (1·2·3순위 페어링) + `references/motion-advanced.md` (고급 효과) 참조.

## 3. 처리 절차

### Step 1. 빌더 입력 파싱
- 정규식으로 `[출력]`, `[팔레트]`, `[프리셋] - 커버/내용/CTA`, `[모션] - 커버/내용/CTA`, `주제:` 7개 필드 추출

### Step 2. 카탈로그 조회
- `MENU.md`에서 P-{n}, F-{n}, M-{n}의 상세 설명/색상/명세 조회

### Step 3. 8컷 카피 초안 작성
- 주제를 받아 커버 (1) / 본문 6장 (2~7) / CTA · 크레딧 (8) 구조로 분배
- 각 컷에 어떤 프리셋·모션 적용할지 슬롯 매핑(§2.2) 따라 결정

### Step 4. 출력 생성
- M-1: `scripts/pil_helpers.py`의 헬퍼 호출 → 1080×1350 PNG 8장 → `output/` 디렉토리에 저장
- M-2/M-3: 위 PNG 8장 + FFmpeg 호출
- M-4: Remotion `.tsx` 코드 생성

## 4. 의존성

- Python 3.9+
- Pillow (`pip install Pillow`)
- FFmpeg (선택, M-2/M-3 출력 시)
- 폰트: Pretendard Variable (`scripts/pil_helpers.py`가 시스템에서 자동 탐색)

## 5. 트리거 키워드

자연어 활성화: "카드뉴스 만들어", "8컷 요약", "인스타용 카드뉴스", "card news", "instagram carousel"

명시 호출: "cardnews 스킬로 만들어줘"

## 6. 라이선스

MIT © 2026 COMMME — 자유롭게 사용·수정·재배포 가능. 자세한 내용은 `LICENSE` 참조.

## 7. 변경 이력

| 날짜 | 버전 | 변경 |
|------|------|------|
| 2026-05-04 | v1.0 | Public 첫 릴리즈. 인터랙티브 빌더 v3 + 50 프리셋 + 60 모션 + 3-슬롯 프롬프트 + PIL 헬퍼 + MIT 라이선스. |
