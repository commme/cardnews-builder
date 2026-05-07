"""
Card News Builder Promo — Capture v6
F-8 split-screen 텍스트(VS/GO)를 240px 거대 폰트 + 풀스크린 1300x1300으로 표시
→ 모션 6종이 큰 텍스트 위에서 명확하게 보임

viewport 1500x1500, 자막/BGM 없음, video record 모드, 약 25초

10컷 흐름:
  cut-1: 빌더 첫 화면 (P-3 neon + F-8 split-screen, 작게)
  cut-2: 팔레트 P-11 sakura (라이브 recolor)
  ===== 풀스크린 모션 데모 (텍스트 거대 + 모션) =====
  cut-3: M-45 split-reveal (F-8 1순위)
  cut-4: M-15 scale-pop
  cut-5: M-21 glitch-rgb
  cut-6: M-11 typewriter-cursor
  cut-7: M-25 sparkle
  cut-8: M-13 letter-drop
  ===== 빌더 복귀 =====
  cut-9: 비율 9:16 + 출력 M-2
  cut-10: 60,000 + MIT 아웃트로
"""
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent.resolve()
REC_DIR = HERE / 'output' / 'recording'
URL = 'http://localhost:9240/menu.html'


def fullscreen_preview(page):
    """프리뷰만 풀스크린 1300x1300 + mm-* 폰트를 거대화 + 빌더 어둡게"""
    page.evaluate("""
        // 1. 프리뷰 박스 풀스크린 확대
        const pv = document.querySelector('#preview-canvas');
        if (pv) {
            pv.style.position = 'fixed';
            pv.style.top = '50%';
            pv.style.left = '50%';
            pv.style.width = '1300px';
            pv.style.height = '1300px';
            pv.style.transform = 'translate(-50%, -50%)';
            pv.style.zIndex = '9000';
            pv.style.outline = '4px solid #00F5A0';
            pv.style.boxShadow = '0 0 80px 16px rgba(0,245,160,0.5)';
        }
        // 2. 미니맵 폰트 거대화 (F-8 split-screen 등)
        let s = document.getElementById('fs-style');
        if (!s) {
            s = document.createElement('style');
            s.id = 'fs-style';
            s.innerHTML = `
                .mm-split-screen > div { font-size: 240px !important; letter-spacing:-0.05em !important; }
                .mm-grid-poster > div { font-size: 200px !important; }
                .mm-headline-news .h { font-size: 100px !important; line-height: 1.05 !important; }
                .mm-headline-news .sub { font-size: 36px !important; }
                .mm-headline-news .tag { font-size: 28px !important; padding: 6px 16px !important; }
                .mm-checklist .ck { font-size: 64px !important; padding: 12px 24px !important; }
            `;
            document.head.appendChild(s);
        }
        // 3. 빌더 어둡게 백드롭
        let bk = document.getElementById('fs-backdrop');
        if (!bk) {
            bk = document.createElement('div');
            bk.id = 'fs-backdrop';
            bk.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.88);z-index:8500;';
            document.body.appendChild(bk);
        }
    """)


def restore(page):
    """풀스크린 모드 해제"""
    page.evaluate("""
        const pv = document.querySelector('#preview-canvas');
        if (pv) {
            pv.style.position=''; pv.style.top=''; pv.style.left='';
            pv.style.width=''; pv.style.height=''; pv.style.transform='';
            pv.style.zIndex=''; pv.style.outline=''; pv.style.boxShadow='';
        }
        const s = document.getElementById('fs-style'); if (s) s.remove();
        const b = document.getElementById('fs-backdrop'); if (b) b.remove();
    """)


def motion_cut(page, motion_id):
    """모션 적용 → 풀스크린 → 2회 재생"""
    page.evaluate(f"state.cover.motion='{motion_id}'; render(); applyPreview();")
    time.sleep(0.2)
    fullscreen_preview(page)
    time.sleep(0.2)
    page.evaluate("applyPreview();")  # 풀스크린 후 다시 재생
    time.sleep(1.4)
    page.evaluate("applyPreview();")  # 한 번 더
    time.sleep(1.2)
    restore(page)


def main():
    REC_DIR.mkdir(parents=True, exist_ok=True)
    for old in REC_DIR.glob('*.webm'):
        try: old.unlink()
        except: pass

    with sync_playwright() as p:
        try:
            browser = p.chromium.launch(channel='chrome', headless=True)
        except Exception:
            browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1500, 'height': 1500},
            record_video_dir=str(REC_DIR),
            record_video_size={'width': 1500, 'height': 1500},
        )
        page = context.new_page()
        print('[v6] navigating + recording start')
        page.goto(URL, wait_until='networkidle')
        time.sleep(0.6)

        # cut 1: P-3 neon + F-8 split-screen (빌더 화면, 작게)
        print('[cut-1] P-3 + F-8 split-screen (builder view)')
        page.evaluate("""
            setState({palette:'P-3', aspect:'1:1', output:'M-1', activeSlot:'cover'});
            state.cover.preset = 'F-8';
            state.cover.motion = 'M-1';
            render(); applyPreview();
        """)
        time.sleep(2.0)

        # cut 2: P-11 sakura
        print('[cut-2] palette P-11 sakura')
        page.evaluate("setState({palette:'P-11'}); applyPreview();")
        time.sleep(2.0)

        # cut 3~8: 풀스크린 모션 6종 (텍스트 거대 + 모션)
        for label, mid in [
            ('cut-3 M-45 split-reveal [STAR F-8 #1]', 'M-45'),
            ('cut-4 M-15 scale-pop [STAR]',           'M-15'),
            ('cut-5 M-21 glitch-rgb [STAR]',          'M-21'),
            ('cut-6 M-11 typewriter-cursor',          'M-11'),
            ('cut-7 M-25 sparkle',                    'M-25'),
            ('cut-8 M-13 letter-drop',                'M-13'),
        ]:
            print(f'[{label}]')
            motion_cut(page, mid)

        # cut 9: 비율 9:16 + 출력 M-2
        print('[cut-9] aspect 9:16 + output M-2')
        page.evaluate("""
            setState({aspect:'9:16', output:'M-2'});
            setTimeout(() => {
                document.querySelectorAll('.of-card').forEach(c => {
                    if (c.dataset.id === 'M-2') {
                        c.style.outline='3px solid #00F5A0';
                        c.style.boxShadow='0 0 24px rgba(0,245,160,0.7)';
                        c.style.transform='scale(1.08)';
                        c.style.transition='all 0.3s ease';
                    }
                });
                document.querySelectorAll('.aspect-btn').forEach(b => {
                    if (b.dataset.aspect === '9:16') {
                        b.style.boxShadow='0 0 16px rgba(0,245,160,0.7)';
                        b.style.transform='scale(1.1)';
                    }
                });
            }, 30);
        """)
        time.sleep(2.5)

        # cut 10: 아웃트로
        print('[cut-10] outro')
        page.evaluate("""
            const o = document.createElement('div');
            o.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.96);z-index:9999;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:Pretendard Variable,sans-serif;color:#fff;text-align:center;';
            o.innerHTML = '<div style="font-size:120px;font-weight:900;background:linear-gradient(90deg,#DA7756,#00F5A0,#FF0080);-webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:-0.04em;line-height:1.05;">Card News<br>Builder</div>'
                + '<div style="font-size:48px;color:#00F5A0;margin-top:36px;font-weight:800;">20 × 50 × 60 = 60,000</div>'
                + '<div style="font-size:32px;color:#aaa;margin-top:20px;font-weight:600;">MIT · Open Source · Free</div>'
                + '<div style="font-size:18px;color:#666;margin-top:72px;font-family:Space Mono,monospace;">© 2026 COMMME · Built with Claude Code</div>';
            document.body.appendChild(o);
        """)
        time.sleep(3.0)

        video_path = page.video.path()
        page.close()
        context.close()
        browser.close()

    print(f'\n[OK] webm: {video_path}')
    webms = sorted(REC_DIR.glob('*.webm'))
    if not webms:
        print('[ERR] no webm'); sys.exit(1)
    for f in webms:
        print(f'  {f.name}: {f.stat().st_size/1024:.0f} KB')


if __name__ == '__main__':
    main()
