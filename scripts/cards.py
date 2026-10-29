"""生成作品卡片（亮/暗两版）。缩略图在 assets/thumbs，来自作品站的封面；改文字后重新运行。"""
import os
ROOT = os.path.join(os.path.dirname(__file__), '..')
import base64, html
W, H = 460, 150
TH_W, TH_H = 176, 110  # 16:10 缩略图
THEMES = {
  'light': dict(bg='#ffffff', bd='#d1d9e0', title='#1f2328', desc='#59636e', meta='#59636e', pill_bg='#ddf4ff', pill_fg='#0969da', th_bd='#e6e9ed'),
  'dark':  dict(bg='#0d1117', bd='#3d444d', title='#f0f6fc', desc='#9198a1', meta='#9198a1', pill_bg='#121d2f', pill_fg='#4493f8', th_bd='#262c36'),
}
CARDS = [
  dict(slug='niwa', title='Niwa · 庭', pill='Edge 扩展商店',
       lines=['Edge / Chrome 新标签页扩展', '节气山水，快捷方式和小组件自由摆放'],
       tech=[('WXT','#67d55e'),('React','#61dafb'),('TypeScript','#3178c6')]),
  dict(slug='maintpilot', title='MaintPilot', pill='在线演示',
       lines=['设备检修的 AI 诊断系统', '答案能追溯到手册页码'],
       tech=[('Vue 3','#41b883'),('Go','#00add8'),('pgvector','#336791')]),
  dict(slug='token-stats', title='token-stats', pill='开源',
       lines=['汇总几台机器的 AI 编程用量', '上面那张卡片就是它每天生成的'],
       tech=[('Python','#3572a5'),('SQLite','#0f80cc'),('Actions','#2088ff')]),
  dict(slug='lab', title='UI Motion Lab', pill='作品站',
       lines=['我的作品站', '收录的组件和动效都能上手试'],
       tech=[('Nuxt 4','#00dc82'),('Vue','#41b883'),('TypeScript','#3178c6')]),
]
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Noto Sans SC', 'Microsoft YaHei', sans-serif"
def tw(s, size):  # 粗估文字宽度：中文按 1 个字号，其他按 0.58
    return sum(size if ord(c) > 0x2e80 else size*0.58 for c in s)
for c in CARDS:
    for mode, t in THEMES.items():
        th = f"{ROOT}/assets/thumbs/{c['slug']}{'-dark' if mode=='dark' else ''}.jpg"
        b64 = base64.b64encode(open(th,'rb').read()).decode()
        x0 = 16 + TH_W + 18
        pw = tw(c['pill'], 11) + 16
        tech, x = [], x0
        for name, col in c['tech']:
            tech.append(f'<circle cx="{x+5:.0f}" cy="122" r="5" fill="{col}"/><text x="{x+14:.0f}" y="126" class="m">{html.escape(name)}</text>')
            x += 14 + tw(name, 12) + 12
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<style>text{{font-family:{FONT}}} .t{{font-size:17px;font-weight:600;fill:{t['title']}}} .d{{font-size:13px;fill:{t['desc']}}} .m{{font-size:12px;fill:{t['meta']}}} .p{{font-size:11px;fill:{t['pill_fg']}}}</style>
<defs><clipPath id="c"><rect x="16" y="20" width="{TH_W}" height="{TH_H}" rx="6"/></clipPath></defs>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="10" fill="{t['bg']}" stroke="{t['bd']}"/>
<image x="16" y="20" width="{TH_W}" height="{TH_H}" preserveAspectRatio="xMidYMid slice" clip-path="url(#c)" href="data:image/jpeg;base64,{b64}"/>
<rect x="16.5" y="20.5" width="{TH_W-1}" height="{TH_H-1}" rx="6" fill="none" stroke="{t['th_bd']}"/>
<text x="{x0}" y="42" class="t">{html.escape(c['title'])}</text>
<rect x="{W-16-pw:.0f}" y="28" width="{pw:.0f}" height="19" rx="9.5" fill="{t['pill_bg']}"/>
<text x="{W-16-pw/2:.0f}" y="41.5" class="p" text-anchor="middle">{html.escape(c['pill'])}</text>
<text x="{x0}" y="70" class="d">{html.escape(c['lines'][0])}</text>
<text x="{x0}" y="90" class="d">{html.escape(c['lines'][1])}</text>
{''.join(tech)}
</svg>'''
        out = f"{ROOT}/assets/cards/{c['slug']}{'-dark' if mode=='dark' else ''}.svg"
        open(out,'w').write(svg)
        print(out, len(svg)//1024, 'KB', 'tech end x', round(x))
