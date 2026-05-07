# Advanced Effects T51~T60 — 구현 레퍼런스

> SKILL.md §5에서 로드. Advanced Effects 10종의 PIL/FFmpeg/Remotion 구현.

---

## T51. chromatic-aberration (색수차 정적 분리) — T1부터 가능

```python
from PIL import Image, ImageChops
base = Image.open("bg.jpg").resize((W, H)).convert("RGB")
r, g, b = base.split()
# R 채널 좌측 8px · B 채널 우측 8px 시프트
out = Image.merge("RGB", (
    ImageChops.offset(r, -8, 0),
    g,
    ImageChops.offset(b, 8, 0),
))
out.save("01.png")
```

---

## T52. god-rays (빛줄기 발산)

```python
# T1 의사 god-rays: 중심에서 뻗어나가는 radial 스트라이프
img = Image.new("RGB", (W, H), (12, 10, 30))
over = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(over)
cx, cy = W // 2, 200
for angle in range(0, 360, 12):
    ex = cx + math.cos(math.radians(angle)) * 1800
    ey = cy + math.sin(math.radians(angle)) * 1800
    od.line((cx, cy, ex, ey), fill=(255, 230, 160, 60), width=60)
over = over.filter(ImageFilter.GaussianBlur(radius=22))
img = Image.alpha_composite(img.convert("RGBA"), over).convert("RGB")
# T3 FFmpeg 대안: -vf "gblur=sigma=20,geq='min(255, r(X,Y) + 80*sin(atan2(Y-H/2,X-W/2)*12))'"
```

---

## T53. light-sweep (대각선 빛 스윕) — T2 GIF 필수 프레임

```python
# 24프레임에 걸쳐 좌상→우하 대각선 빛 띠 이동
for i in range(24):
    base = Image.open("base.png").convert("RGBA")
    sweep = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sweep)
    x_off = int(-W + (i / 24) * (W * 2))
    sd.polygon([(x_off, 0), (x_off + 220, 0), (x_off - 200, H), (x_off - 420, H)],
               fill=(255, 255, 255, 90))
    sweep = sweep.filter(ImageFilter.GaussianBlur(radius=18))
    out = Image.alpha_composite(base, sweep).convert("RGB")
    out.save(f"sweep_{i:02}.png")
# imageio.mimsave("sweep.gif", imgs, duration=0.05, loop=0)
```

---

## T54. film-burn (필름 번인 플래시)

```python
# T2: 3프레임짜리 강렬한 화이트 플래시 + 주황 번인
import random
base = Image.open("base.png").convert("RGB")
for i, strength in enumerate([0.35, 0.65, 0.15]):
    img = base.copy()
    burn = Image.new("RGB", (W, H), (255, 180, 60))
    img = Image.blend(img, burn, strength)
    d = ImageDraw.Draw(img)
    for _ in range(8):
        x = random.randint(0, W)
        d.line((x, random.randint(0, H // 3), x + random.randint(-30, 30),
                random.randint(H * 2 // 3, H)),
               fill=(255, 255, 240), width=2)
    img.save(f"burn_{i}.png")
```

---

## T55. vhs-tracking (VHS 트래킹 왜곡) — T2 GIF

```python
base = Image.open("base.png").convert("RGB")
for f in range(12):
    img = base.copy()
    for _ in range(4):
        y = random.randint(0, H - 40)
        h = random.randint(8, 36)
        strip = img.crop((0, y, W, y + h))
        img.paste(strip, (random.randint(-25, 25), y))
    bottom = img.crop((0, int(H * 0.75), W, H))
    bottom = ImageChops.offset(bottom, random.randint(-6, 6), 0)
    img.paste(bottom, (0, int(H * 0.75)))
    img.save(f"vhs_{f:02}.png")
```

---

## T56. zoom-punch (타이밍 펀치 줌) — T3 Reels 필살기

```bash
# FFmpeg zoompan: 0.5초 구간에서 1.0 → 1.25 급증 → 1.0 복귀
ffmpeg -loop 1 -t 2.5 -i 01.png \
  -vf "zoompan=z='if(lt(in_time,1.0),1.0, if(lt(in_time,1.25),1+((in_time-1.0)*1.0), if(lt(in_time,1.5),1.25-((in_time-1.25)*1.0),1.0)))':d=1:s=1080x1920:fps=30" \
  -c:v libx264 -pix_fmt yuv420p punch.mp4
```

```tsx
// T4 Remotion
const z = spring({frame: frame - 30, fps, config: {damping: 10, stiffness: 200}});
const scale = 1 + z * 0.25;
```

---

## T57. liquid-morph (액체 변형) — T4 Remotion 추천

```tsx
// flubber SVG path morph + damped spring
import { interpolate } from "remotion";
import { toPathString, interpolate as flubber } from "flubber";
const t = spring({frame, fps});
const interpolator = flubber("M10,10 L200,10 L200,200 L10,200Z",
                             "M100,10 C180,40 220,160 100,200 C20,160 -20,40 100,10Z");
const d = interpolator(t);
return <svg><path d={d} fill={NEON_P}/></svg>;
```

```python
# T2 대안: PIL에서 rounded_rectangle radius 가변 (사각 → 원형)
for i in range(10):
    r = int(i * 150 / 9)
    img = Image.new("RGB", (W, H), (8, 8, 12))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((340, 500, 740, 900), radius=r, fill=(255, 0, 128))
    img.save(f"liqm_{i:02}.png")
```

---

## T58. motion-blur (피사체 궤적 블러)

```python
positions = [(80 + i * 80, 500) for i in range(10)]
for i, (x, y) in enumerate(positions):
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    ghost = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(ghost)
    for k in range(max(0, i - 4), i):
        a = int(60 + (k - max(0, i - 4)) * 40)
        gd.ellipse((positions[k][0] - 40, y - 40, positions[k][0] + 40, y + 40),
                   fill=(0, 180, 255, a))
    ghost = ghost.filter(ImageFilter.GaussianBlur(radius=8))
    img = Image.alpha_composite(img.convert("RGBA"), ghost).convert("RGB")
    d = ImageDraw.Draw(img)
    d.ellipse((x - 40, y - 40, x + 40, y + 40), fill=(0, 120, 220))
    img.save(f"mblur_{i:02}.png")
```

---

## T59. rgb-trail (RGB 채널 잔상) — T2 GIF 최고

```python
frames = [...]  # 이미 렌더된 PIL 프레임 리스트
for i, base in enumerate(frames):
    r, g, b = base.split()
    out = Image.merge("RGB", (
        ImageChops.offset(r, -6 * ((i % 3) - 1), 0),
        g,
        ImageChops.offset(b,  6 * ((i % 3) - 1), 0),
    ))
    out.save(f"trail_{i:02}.png")
```

---

## T60. hologram-flicker (홀로그램 깜빡임)

```python
base = Image.open("base.png").convert("RGB")
for f in range(12):
    img = base.copy()
    over = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(over)
    for y in range(0, H, 3 if f % 2 == 0 else 4):
        od.line((0, y, W, y), fill=(120, 200, 255, 28))
    alpha = [1.0, 0.35, 0.9, 1.0, 0.55, 1.0, 0.8, 1.0, 0.25, 0.95, 1.0, 0.7][f]
    tint = Image.new("RGB", img.size, (80, 160, 220))
    img = Image.blend(img, tint, 0.15)
    img = img.convert("RGBA")
    bg = Image.new("RGB", img.size, (6, 6, 12))
    img = Image.blend(bg.convert("RGBA"), img, alpha).convert("RGBA")
    img = Image.alpha_composite(img, over).convert("RGB")
    img.save(f"holo_{f:02}.png")
```

---

## Tier 매트릭스

| 효과 | T1 PNG | T2 GIF | T3 Reels | T4 Remotion | 비고 |
|------|:---:|:---:|:---:|:---:|------|
| T51 chromatic-aberration | ✅ | ✅ | ✅✅ | ✅✅ | 정적 PNG도 즉시 적용 |
| T52 god-rays | ✅ | ✅ | ✅✅ | ✅✅ | radial blur 블러량이 관건 |
| T53 light-sweep | ⭕ | ✅ | ✅✅ | ✅✅ | 24프레임 GIF 가장 효과적 |
| T54 film-burn | ❌ | ✅ | ✅✅ | ✅✅ | 3프레임 펀치 플래시 |
| T55 vhs-tracking | ⭕(의사) | ✅✅ | ✅ | ✅ | T2 GIF가 감성 최고 |
| T56 zoom-punch | ❌ | ⭕ | ✅✅ | ✅✅ | spring 감쇠 필수 |
| T57 liquid-morph | ❌ | ⭕ | ✅ | ✅✅ | flubber + Remotion |
| T58 motion-blur | ⭕ | ✅ | ✅✅ | ✅✅ | 잔상 alpha 선형증가 |
| T59 rgb-trail | ⭕ | ✅✅ | ✅ | ✅ | T2 GIF에서 가장 감각적 |
| T60 hologram-flicker | ❌ | ✅✅ | ✅ | ✅✅ | 투명도 + 스캔라인 조합 |
