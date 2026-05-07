"""
cardnews — PIL 공통 헬퍼 모듈 (Card News Builder Public Package)

모든 프리셋·모션 스니펫에서 재사용되는 PIL 헬퍼 함수 모음.
gen.py 최상단에서 `from scripts.pil_helpers import *` 로 임포트 권장.

- hex_to_rgb: MENU.md hex → RGB 튜플 변환
- fB/fb/fm: Pretendard Black/Bold/Medium 폰트 로더
- tag/credit/handle: 카드 하단 공통 요소
- gradient_bg/noise_overlay: 배경 이펙트
- hard_shadow/glass_card/clay_box: 프리셋별 박스 스타일
- iso_cube/faux_3d_text/chrome_text: 3D·타이포그래피 헬퍼
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops, ImageOps
import os
import math
import random

W, H = 1080, 1350          # 4:5 기본 (T1, T2)
REELS_W, REELS_H = 1080, 1920  # 9:16 (T3, T4)


def hex_to_rgb(hex_str):
    """MENU.md §1의 #RRGGBB → (R, G, B) 튜플"""
    h = hex_str.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def fB(size, font="Pretendard-Black.otf"):
    return ImageFont.truetype(font, size)


def fb(size, font="Pretendard-Bold.otf"):
    return ImageFont.truetype(font, size)


def fm(size, font="Pretendard-Medium.otf"):
    return ImageFont.truetype(font, size)


def tag(d, n, total=8, fill_color=(218, 119, 86), empty=(218, 208, 198), txt_c=(130, 125, 118)):
    """하단 페이지 카운터 N / 8 + dot 8개"""
    d.text((80, H - 105), f"{n} / {total}", font=fb(32), fill=txt_c)
    for i in range(total):
        col = fill_color if i < n else empty
        x = 760 + i * 26
        d.ellipse((x, H - 100, x + 16, H - 84), fill=col)


def credit(d, y=H - 95, color=(110, 110, 110)):
    """마지막 카드 크레딧 (필수)"""
    d.text((80, y), "© 2026 COMMME · Built with Claude Code", font=fb(22), fill=color)


def handle(d, y=H - 135, color=(180, 180, 180)):
    """CTA용 핸들 표기"""
    d.text((80, y), "@commme210  ·  Instagram & Threads", font=fb(32), fill=color)


def gradient_bg(size, c1, c2, direction='v'):
    """선형 그라디언트 (glass-morphism, y2k-chrome, vaporwave)"""
    w, h = size
    img = Image.new("RGB", size)
    d = ImageDraw.Draw(img)
    for i in range(h if direction == 'v' else w):
        t = i / (h if direction == 'v' else w)
        c = tuple(int(c1[j] + (c2[j] - c1[j]) * t) for j in range(3))
        if direction == 'v':
            d.line((0, i, w, i), fill=c)
        else:
            d.line((i, 0, i, h), fill=c)
    return img


def noise_overlay(img, strength=30):
    """리소그래프 · grain 노이즈"""
    noise = Image.new("RGB", img.size)
    nd = noise.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            v = random.randint(-strength, strength)
            nd[x, y] = (v + 128, v + 128, v + 128)
    return Image.blend(img, noise, 0.08)


def hard_shadow(d, box, offset=12, shadow_color=(0, 0, 0), fill=None, outline=None, width=6, radius=0):
    """Neo-brutalism 하드 섀도우 박스"""
    x1, y1, x2, y2 = box
    if radius > 0:
        d.rounded_rectangle((x1 + offset, y1 + offset, x2 + offset, y2 + offset),
                            radius=radius, fill=shadow_color)
        d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)
    else:
        d.rectangle((x1 + offset, y1 + offset, x2 + offset, y2 + offset), fill=shadow_color)
        d.rectangle(box, fill=fill, outline=outline, width=width)


def glass_card(img, box, alpha=90, border=(255, 255, 255, 180)):
    """Glass-morphism 반투명 카드"""
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rounded_rectangle(box, radius=40, fill=(255, 255, 255, alpha), outline=border, width=2)
    img = Image.alpha_composite(img.convert("RGBA"), overlay)
    return img.convert("RGB")


def clay_box(d, box, fill, radius=60, shadow1=(200, 180, 160), shadow2=(230, 215, 195)):
    """Claymorphism 말랑 박스 (그림자 2단 + 하이라이트)"""
    x1, y1, x2, y2 = box
    d.rounded_rectangle((x1 + 8, y1 + 12, x2 + 8, y2 + 12), radius=radius, fill=shadow1)
    d.rounded_rectangle((x1 + 4, y1 + 6, x2 + 4, y2 + 6), radius=radius, fill=shadow2)
    d.rounded_rectangle(box, radius=radius, fill=fill)


def iso_cube(d, x, y, size, color_top, color_left, color_right):
    """Isometric 30° cube (3면 색상 차등)"""
    dx = size * math.cos(math.radians(30))
    dy = size * math.sin(math.radians(30))
    d.polygon([(x, y), (x + dx, y - dy), (x + 2 * dx, y), (x + dx, y + dy)], fill=color_top)
    d.polygon([(x, y), (x + dx, y + dy), (x + dx, y + dy + size), (x, y + size)], fill=color_left)
    d.polygon([(x + dx, y + dy), (x + 2 * dx, y), (x + 2 * dx, y + size), (x + dx, y + dy + size)],
              fill=color_right)


def faux_3d_text(d, pos, text, size, color, depth=8, shadow_color=None):
    """5~8겹 오프셋 3D 타이포"""
    x, y = pos
    shadow_color = shadow_color or tuple(int(c * 0.3) for c in color)
    for i in range(depth, 0, -1):
        t = i / depth
        shade = tuple(int(color[j] * (1 - t) + shadow_color[j] * t) for j in range(3))
        d.text((x + i * 3, y + i * 3), text, font=fB(size), fill=shade)
    d.text((x, y), text, font=fB(size), fill=color)


def chrome_text(img, text, pos, size, grad_stops=None):
    """Y2K 크롬 텍스트 = 마스크 + 그라디언트"""
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).text(pos, text, font=fB(size), fill=255)
    stops = grad_stops or [(180, 220, 255), (255, 255, 255), (80, 120, 200), (30, 50, 120)]
    chrome = Image.new("RGB", (w, h))
    cd = ImageDraw.Draw(chrome)
    seg = h // (len(stops) - 1)
    for s in range(len(stops) - 1):
        c1, c2 = stops[s], stops[s + 1]
        for y in range(seg):
            t = y / seg
            c = tuple(int(c1[j] + (c2[j] - c1[j]) * t) for j in range(3))
            cd.line((0, s * seg + y, w, s * seg + y), fill=c)
    img.paste(chrome, (0, 0), mask)
    return img


# 자주 쓰는 상수 (핵심 3개 팔레트)
# i. claude — Warm Editorial
C_DARK = (20, 20, 20)
C_ORANGE = (218, 119, 86)
C_CREAM = (244, 229, 217)

# iii. neon — Cyber Neon
N_DARK = (8, 8, 12)
N_G = (0, 245, 160)
N_P = (255, 0, 128)
N_B = (0, 180, 255)

# xx. minimal — Pure B&W
M_BLACK = (0, 0, 0)
M_WHITE = (255, 255, 255)
M_GRAY = (136, 136, 136)
