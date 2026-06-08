# -*- coding: utf-8 -*-
"""주요캐릭터 전직공략.txt → jobguide.json.
구조: `<에피소드>` 구분 / 각 에피소드 안 `N. 캐릭터명` 헤더로 캐릭터 구역 / 맨 끝 `[출처]` 한 줄.
- 에피소드: 시반 슈미터(0)/크림슨 크루세이드(1)/아포칼립스(2)
- 캐릭터 헤더는 에피소드 내에서 1,2,3… 순번이 연속될 때만 헤더로 인정(본문 오탐 방지)
- 출처 라인은 반드시 별도 보존(jobguide.json.source)
"""
import re, json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
PROJ = os.path.dirname(os.path.abspath(__file__))
SRC  = r"C:\Users\hyper\Projects\genesis3part1_editor\samples\job\주요캐릭터 전직공략.txt"
OUT  = os.path.join(PROJ, 'jobguide.json')

EP_INDEX = {'시반 슈미터': 0, '크림슨 크루세이드': 1, '아포칼립스': 2}

raw_lines = open(SRC, encoding='utf-8').read().split('\n')
source = ''
lines = []
for l in raw_lines:
    if l.strip().startswith('[출처]'):
        source = l.strip()
        continue
    lines.append(l)

def trim_block(ls):
    while ls and not ls[0].strip(): ls.pop(0)
    while ls and not ls[-1].strip(): ls.pop()
    return '\n'.join(ls)

episodes = []
cur_ep = None; cur_char = None; expected = 0
for l in lines:
    s = l.strip()
    mE = re.match(r'^<(.+)>$', s)
    if mE:
        cur_ep = {'title': mE.group(1), 'epIndex': EP_INDEX.get(mE.group(1)), 'intro': [], 'chars': []}
        episodes.append(cur_ep); cur_char = None; expected = 0
        continue
    if cur_ep is None:
        continue
    mC = re.match(r'^(\d+)\.\s+(.+)$', s)
    if mC and int(mC.group(1)) == expected + 1:
        expected = int(mC.group(1))
        cur_char = {'num': expected, 'name': mC.group(2).strip(), 'lines': []}
        cur_ep['chars'].append(cur_char)
        continue
    (cur_char['lines'] if cur_char else cur_ep['intro']).append(l)

# 본문 문자열화
for ep in episodes:
    ep['intro'] = trim_block(ep['intro'])
    for c in ep['chars']:
        c['body'] = trim_block(c.pop('lines'))

data = {'source': source, 'episodes': episodes}
json.dump(data, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

print('=== jobguide.json ===', OUT)
print('source 보존:', bool(source))
for ep in episodes:
    print(f"  [{ep['epIndex']}] {ep['title']}: {len(ep['chars'])}명 -> " + ', '.join(c['name'] for c in ep['chars']))
