# 🎨 Card News Builder

> Claude Code용 인스타그램 카드뉴스 8컷 자동 생성 스킬.
> 빌더에서 클릭만 하면 일관된 디자인의 8컷이 PNG/GIF/MP4로 나옵니다.

---

## 무엇을 만들 수 있나

![빌더 미리보기](docs/screenshots/01-builder-overview.png)
*20 팔레트 × 50 프리셋 × 60 모션 = 60,000 조합. 슬롯별(커버/내용/CTA) 다른 디자인 가능.*

![팔레트 라이브 recolor](docs/screenshots/02-palette-recolor.png)
*팔레트 클릭 → 50개 프리셋 카드가 즉시 새 색으로 recolor.*

![3-슬롯 토글](docs/screenshots/03-slot-toggle.png)
*커버·내용·CTA 슬롯을 토글하며 각각 다른 프리셋·모션 지정.*

![최종 8컷 출력](docs/screenshots/04-final-output.png)
*프롬프트 복사 → Claude Code 붙여넣기 → 1080×1350 PNG 8장 자동 생성.*

> 위 스크린샷은 실제 캡처 후속 작업. 현재는 슬롯만 표시.

---

## 빠른 시작 (5분)

### 1. 설치

```bash
git clone https://github.com/<your-username>/cardnews-builder.git
cp -r cardnews-builder ~/.claude/skills/cardnews
```

> Windows PowerShell:
> ```powershell
> git clone https://github.com/<your-username>/cardnews-builder.git
> Copy-Item -Recurse cardnews-builder $env:USERPROFILE\.claude\skills\cardnews
> ```

### 2. 의존성

```bash
pip install Pillow
```

GIF 또는 9:16 MP4 출력을 원하면 FFmpeg 추가:

- macOS: `brew install ffmpeg`
- Linux: `sudo apt install ffmpeg`
- Windows: `choco install ffmpeg` 또는 [공식 사이트](https://ffmpeg.org/download.html)

### 3. 사용

1. 빌더 열기:
   ```bash
   cd ~/.claude/skills/cardnews
   python -m http.server 9230
   ```
   브라우저: `http://localhost:9230/menu.html`

2. 빌더에서 클릭:
   - **출력 포맷** 선택 (M-1 PNG / M-2 GIF / M-3 Reels / M-4 Remotion)
   - **팔레트** 선택 (P-1 ~ P-20)
   - **슬롯 토글** (커버 / 내용 / CTA) → 각 슬롯에 프리셋·모션 지정
   - **주제** 입력 → **[복사]** 버튼 클릭

3. Claude Code 채팅에 붙여넣기 → 8컷 PNG 자동 생성

---

## 자료 카탈로그

| 분류 | 개수 | ID 범위 |
|------|------|---------|
| 팔레트 | 20 | P-1 ~ P-20 |
| 프리셋 | 50 (Classic 10 + Trendy 15 + Typography 8 + Data 9 + Novelty 8) | F-1 ~ F-50 |
| 모션 | 60 (출력 포맷 4 + 효과 56) | M-1 ~ M-60 |
| **총 조합** | **60,000** | 20 × 50 × 60 |

자세한 카탈로그는 [`MENU.md`](MENU.md) 참조.
프리셋 × 모션 페어링 추천은 [`references/preset-motion-pairings.md`](references/preset-motion-pairings.md) 참조.

---

## 폴더 구조

```
cardnews/
├── README.md                       ← 이 파일
├── LICENSE                         ← MIT
├── SKILL.md                        ← Claude Code 스킬 정의
├── MENU.md                         ← 재료 카탈로그
├── menu.html                       ← 인터랙티브 빌더 v3
├── references/
│   ├── motion-advanced.md
│   └── preset-motion-pairings.md
├── scripts/
│   └── pil_helpers.py              ← PIL 헬퍼 (PNG 생성)
└── .gitignore
```

---

## FAQ

**Q. 빌더에서 본 미리보기와 실제 PNG 출력이 다를 수 있나?**
A. 빌더의 미니 카드 미리보기는 데모용 단순화 버전이고, 실제 PNG는 1080×1350으로 풀 디자인이 적용됨. 색·구성·타이포는 일관되게 유지됨.

**Q. 모션 효과(M-5 ~ M-60)가 PNG에선 안 보이는데?**
A. 모션 효과는 M-2(GIF) / M-3(Reels MP4) / M-4(Remotion) 출력에만 적용됨. M-1(PNG)은 정적 8장이라 효과는 카피 문구의 등장 순서·강조에만 반영.

**Q. 폰트가 안 나와요.**
A. Pretendard Variable이 시스템에 없어서 그래요. macOS/Linux: 시스템에 폰트 설치, Windows: 폰트 폴더에 ttf 추가. 또는 `scripts/pil_helpers.py`의 `FONT_PATH`를 직접 지정.

---

## 라이선스

MIT © 2026 COMMME

자유롭게 사용·수정·재배포 가능. 상업 사용 OK. 자세한 내용은 [`LICENSE`](LICENSE) 참조.

---

## 크레딧

- Built with [Claude Code](https://claude.com/claude-code)
- 폰트: [Pretendard](https://github.com/orioncactus/pretendard) · Space Mono
- 영감: 인스타 카드뉴스 + 노션 템플릿 + 카피라이팅 패턴
