# -*- coding: utf-8 -*-
"""나무위키 직업 문서(extracted.txt) → jobs.json.
규칙(사용자 확정):
- 대제목 `N. 나라`(1~4: 투르/팬드래건/게이시르/한 제국), `5. 기타 계열`부터 버림.
- 부제목 `N.M. 세력`.
- 직업줄 `직업명 : 조건어빌...`(콜론). 습득줄 `ㄴ어빌...`.
- 어빌 토큰: 앞 숫자=최대레벨, 괄호 (n)=최단루트 최소레벨(사용자 확정). 숫자 없으면 레벨개념 없음.
- 그룹라벨(칼리프측 등, 콜론X)·각주[..]·루트설명 문단은 직업으로 취급 안 함.
- 가이드(시반 슈미터→시반블레이드, 왕국 기사단→성기사단)만 세력 단위로 보존.
"""
import re, json, os, sys
sys.stdout.reconfigure(encoding='utf-8')
PROJ = os.path.dirname(os.path.abspath(__file__))
SRC  = r"C:\Users\hyper\Projects\genesis3part1_editor\samples\job\extracted.txt"
OUT  = os.path.join(PROJ, 'jobs.json')

COUNTRIES_KEEP = ['투르', '팬드래건 왕국', '게이시르 제국', '한 제국']
GUIDE_FACTIONS = ['시반 슈미터', '왕국 기사단']   # 이 세력의 루트 설명만 가이드로 보존

def strip_notes(s):
    s = re.sub(r'\[[^\]]*\]', '', s)        # 각주 [1][A][스포일러]
    return re.sub(r'\s+', ' ', s).strip()

def parse_token(tok, is_cond):
    """어빌 토큰 → {name, max/lv, routeMin}. 실패 시 None."""
    tok = strip_notes(tok)
    if not tok: return None
    m = re.search(r'\((\d+)\)', tok)        # 괄호 숫자 = 루트 최소레벨
    route_min = int(m.group(1)) if m else None
    tok = re.sub(r'\([^)]*\)', '', tok).strip()   # 모든 괄호 내용 제거
    if not tok: return None
    mm = re.match(r'^(.*?)(\d+)$', tok)     # 끝자리 숫자 = 레벨
    if mm and mm.group(1).strip():
        name = mm.group(1).strip(); lv = int(mm.group(2))
    else:
        name = tok; lv = None
    name = re.sub(r'\s+', ' ', name).strip()
    if is_cond:
        return {'name': name, 'lv': lv}
    return {'name': name, 'max': lv, 'routeMin': route_min}

def split_tokens(s):
    return [t for t in (x.strip() for x in s.split(',')) if t]

# --- 파싱 ---
lines = [ln.rstrip() for ln in open(SRC, encoding='utf-8')]
country = None; faction = None; jobs = []; guides = {}
cur_job = None; faction_started_jobs = False
stop = False
for raw in lines:
    ln = raw.strip()
    if not ln: continue
    # 대제목
    mC = re.match(r'^(\d+)\.\s+(.+?)\s*\[편집\]$', ln)
    if mC:
        name = strip_notes(mC.group(2))
        if name == '기타 계열' or int(mC.group(1)) >= 5:
            stop = True; break
        country = name if name in COUNTRIES_KEEP else name
        faction = None; cur_job = None; faction_started_jobs = False
        continue
    # 부제목 (N.M.)
    mF = re.match(r'^\d+\.\d+\.\s+(.+?)\s*\[편집\]$', ln)
    if mF:
        faction = strip_notes(mF.group(1)); cur_job = None; faction_started_jobs = False
        continue
    if country is None: continue
    # 습득줄
    if ln.startswith('ㄴ'):
        if ln.startswith('ㄴㄴ'):   # 이중 = 서술 팁, 제외
            continue
        body = ln[1:].strip()
        if cur_job is not None:
            cur_job['learn'] = [t for t in (parse_token(x, False) for x in split_tokens(body)) if t]
        continue
    # 직업줄: '직업명 : 조건...' (콜론, → 없음)
    mJ = re.match(r'^([^:→]+?)\s*:\s*(.+)$', ln)
    if mJ and '→' not in ln:
        jname = strip_notes(mJ.group(1))
        cond  = mJ.group(2)
        # 직업명이 너무 길면(문장) 제외
        if jname and len(jname) <= 18:
            cur_job = {'name': jname, 'country': country, 'faction': faction,
                       'require': [t for t in (parse_token(x, True) for x in split_tokens(cond)) if t],
                       'learn': []}
            jobs.append(cur_job); faction_started_jobs = True
            continue
    # 가이드(루트 설명): 지정 세력에서 첫 직업줄 이전의 프로즈 문단만
    if faction in GUIDE_FACTIONS and not faction_started_jobs:
        if ('→' in ln) or ('루트' in ln) or ('전직경로' in ln) or ln.startswith('빨간'):
            guides.setdefault(faction, []).append(strip_notes(ln))
        continue
    # 그 외(그룹라벨/더미/잡문) 무시

data = {'countries': COUNTRIES_KEEP, 'jobs': jobs,
        'guides': {k: ' '.join(v) for k, v in guides.items()}}

# --- tables.json 와 매핑 ---
tables = json.load(open(os.path.join(PROJ, 'tables.json'), encoding='utf-8'))
abil = tables.get('Abil', {}); job = tables.get('Job', {})
def norm(s): return re.sub(r'\s+', '', s).upper()
abil_rev = {};
for k, v in abil.items():
    abil_rev.setdefault(norm(v), int(k))
job_rev = {}
for k, v in job.items():
    job_rev.setdefault(norm(v), int(k))
# 문서표기 → Abil.txt 정식명 별칭 (띄어쓰기는 norm()이 무시하므로 철자 차이만)
ABIL_ALIAS = {
    '대쉬':'댓쉬', '라이트닝볼트':'라이트닝 볼츠', '쉐도우쉴드':'쉐도우 실드',
    '아이스쉴드':'아이스 실드', '썬더스탐':'썬더 스톰', '혈랑마혼':'혈랑마흔',
    '화이어애로우':'화이어 에로우',
    '소환수제어':'소환능력',          # 문서 표기 → 게임 내 '소환능력'(#119)
    # '필살6연사'는 Abil #151(쌍권총 연사→필살 6연사로 수정됨)와 norm 일치하여 자동 매핑
}
ABIL_ALIAS_N = {norm(k): norm(v) for k, v in ABIL_ALIAS.items()}

def map_abil(name):
    n = norm(name)
    v = abil_rev.get(n)
    if v is not None: return v
    if n in ABIL_ALIAS_N:                       # 철자 별칭
        v = abil_rev.get(ABIL_ALIAS_N[n])
        if v is not None: return v
    v = abil_rev.get(norm(name + ' 장비'))       # 장비 어빌(갑옷/장검/권총 …)
    if v is not None: return v
    return None

# 문서표기 → Job.txt 정식명 별칭
JOB_ALIAS = {
    '드라군':'드래군', '로얄 가드':'로열가드', '로얄 나이트':'로열나이트',
    '사막 레인저':'사막레인져', '에스코트':'에스코드', '정글 레인저':'정글레인져',
    '제너럴':'제네럴', '파이어 마스터':'화이어마스터',
}
JOB_ALIAS_N = {norm(k): norm(v) for k, v in JOB_ALIAS.items()}
# 중복 직업명(나이트/디펜더/스카우트)을 나라로 구분 — 게이시르 제국은 별도 Job ID
JOB_CONTEXT = {('게이시르 제국','나이트'):53, ('게이시르 제국','디펜더'):54, ('게이시르 제국','스카우트'):55}

def map_job(name, country):
    if (country, name) in JOB_CONTEXT: return JOB_CONTEXT[(country, name)]
    n = norm(name)
    v = job_rev.get(n)
    if v is not None: return v
    if n in JOB_ALIAS_N: return job_rev.get(JOB_ALIAS_N[n])
    return None

unmapped_abil = {}; unmapped_job = {}
for jb in jobs:
    jid = map_job(jb['name'], jb['country'])
    jb['jobId'] = jid
    if jid is None: unmapped_job[jb['name']] = unmapped_job.get(jb['name'], 0) + 1
    for t in jb['require']:
        t['abilId'] = map_abil(t['name'])
        if t['abilId'] is None: unmapped_abil[t['name']] = unmapped_abil.get(t['name'], 0) + 1
    for t in jb['learn']:
        t['abilId'] = map_abil(t['name'])
        if t['abilId'] is None: unmapped_abil[t['name']] = unmapped_abil.get(t['name'], 0) + 1

json.dump(data, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# --- 리포트 ---
from collections import Counter
cc = Counter(j['country'] for j in jobs)
print("=== jobs.json 생성 ===", OUT)
print("총 직업:", len(jobs))
for c in COUNTRIES_KEEP: print(f"  {c}: {cc.get(c,0)}")
print("가이드:", list(data['guides'].keys()))
print("\n미매핑 직업명(", len(unmapped_job), "):")
for n in sorted(unmapped_job): print("   ", n)
print("\n미매핑 어빌명(", len(unmapped_abil), "):")
for n in sorted(unmapped_abil): print(f"    {n} (x{unmapped_abil[n]})")
