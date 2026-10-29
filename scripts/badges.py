"""生成主页顶部的三个徽章（亮/暗两版）。WakaTime 时长从它的公开徽章里读，每天由 Actions 重跑。"""
import re, urllib.request, html, os
WAKA_USER = '649e7e90-2082-4317-97cd-f973f39aa2a1'
OUT = os.path.join(os.path.dirname(__file__), '..', 'assets', 'badges')
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Noto Sans SC', 'Microsoft YaHei', sans-serif"
THEMES = {
  'light': dict(bg='#ffffff', bd='#d1d9e0', label='#59636e', value='#1f2328'),
  'dark':  dict(bg='#0d1117', bd='#3d444d', label='#9198a1', value='#f0f6fc'),
}
# 14×14 线条图标，stroke 用各自的颜色
ICONS = {
  'pen':   '<path d="M3 11.5 2.5 13.5 4.5 13 12.5 5a1.4 1.4 0 0 0-2-2Z" /><path d="M9.5 4 11.5 6"/>',
  'grid':  '<rect x="2" y="2" width="4.5" height="4.5" rx="1"/><rect x="9.5" y="2" width="4.5" height="4.5" rx="1"/><rect x="2" y="9.5" width="4.5" height="4.5" rx="1"/><rect x="9.5" y="9.5" width="4.5" height="4.5" rx="1"/>',
  'clock': '<circle cx="8" cy="8" r="6"/><path d="M8 4.8V8l2.2 1.4"/>',
  'commit': '<circle cx="8" cy="8" r="2.6"/><path d="M1.5 8h3.9M10.6 8h3.9"/>',
}
def tw(s, size):
    return sum(size if ord(c) > 0x2e80 else size * (0.3 if c in '.,ilj ' else 0.42 if c in 'trf' else 0.58) for c in s)

def waka_time():
    svg = urllib.request.urlopen(f'https://wakatime.com/badge/user/{WAKA_USER}.svg', timeout=30).read().decode()
    h = re.search(r'([\d,]+) hrs?', svg)
    m = re.search(r'(\d+) mins?', svg)
    return f"{h.group(1) if h else 0} hrs {m.group(1) if m else 0} mins"

def contributions():
    # 公开主页上显示的数（含私有仓库的贡献），不需要 token
    page = urllib.request.urlopen('https://github.com/users/LZWcc/contributions', timeout=30).read().decode()
    return re.search(r'([\d,]+)\s+contributions?\s+in the last year', page).group(1)

def badge(name, icon, color, label, value):
    h, pad = 30, 12
    lw, vw = tw(label, 12), tw(value, 13)
    w = round(pad + 14 + 7 + lw + 8 + vw + pad + 2)  # 估算字宽，右边多留 2px 防止截字
    for mode, t in THEMES.items():
        x_label = pad + 14 + 7
        x_value = x_label + lw + 8
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<style>text{{font-family:{FONT}}}</style>
<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{(h-1)/2}" fill="{t['bg']}" stroke="{t['bd']}"/>
<g transform="translate({pad} 8)" fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{ICONS[icon]}</g>
<text x="{x_label}" y="19.5" font-size="12" fill="{t['label']}">{html.escape(label)}</text>
<text x="{x_value:.1f}" y="19.5" font-size="13" font-weight="600" fill="{t['value']}">{html.escape(value)}</text>
</svg>'''
        open(f"{OUT}/{name}{'-dark' if mode == 'dark' else ''}.svg", 'w').write(svg)
    print(name, w)

os.makedirs(OUT, exist_ok=True)
badge('blog', 'pen', '#e8590c', '博客', 'lzwcc.xyz')
badge('lab', 'grid', '#12b886', '作品站', 'lab.lzwcc.xyz')
badge('wakatime', 'clock', '#4c6ef5', 'WakaTime', waka_time())
badge('github', 'commit', '#2da44e', 'GitHub', f'{contributions()} contributions')
