# -*- coding: utf-8 -*-
# dats/Item.dat -> tools/item_info.json  (아이템 영문명/설명/공격스탯/분류 추출)
# Item.dat: 텍스트는 XOR 0xFF, 숫자는 평문(raw). 204바이트 고정 레코드, record(id)=(id-1)*204 (id 1=단검..).
#   [text/decoded] +0x02 한글명(참고), +0x20 영문명, +0x6A 설명(null종료 CP949)
#   [raw/평문]      +0x50 TS(단일 공격력), +0x69 SS(연속 공격 스킬 공격력)  ※무기만 >0
# 분류(cat)는 Item.txt id 구간 기반(게임상 고정): 무기/써크렛/방어구/장신구/소비/기타.
# (한글 이름은 tools/G3Data/Item.txt(tables.json)에서 가져오므로 여기선 제외 → 오타수정 단일소스 유지)
import json, os

GAME = r"D:\DGGL\Games\G3P1103p_Win_260518"      # 게임 설치 경로
PROJ = os.path.dirname(os.path.abspath(__file__))  # tools/
REC = 204
ENG_OFF, DESC_OFF, TS_OFF, SS_OFF = 0x20, 0x6A, 0x50, 0x69

def cstr(d, o, mx=96):
    e = o
    while e < o + mx and e < len(d) and d[e] != 0:
        e += 1
    try:
        return d[o:e].decode("cp949").strip()
    except Exception:
        return ""

def category(i):
    if 70 <= i <= 75:   return "써크렛"
    if 76 <= i <= 96:   return "방어구"
    if 97 <= i <= 125:  return "장신구"
    if 126 <= i <= 143: return "소비"
    if (1 <= i <= 69) or (144 <= i <= 181): return "무기"
    return "기타"

def main():
    raw = open(os.path.join(GAME, "dats", "Item.dat"), "rb").read()  # 평문 숫자용
    d = bytes(b ^ 0xFF for b in raw)                                  # 텍스트 디코드용
    n = len(d) // REC
    info = {}
    for r in range(n):
        b = r * REC
        item_id = r + 1                      # record index 0 = item id 1
        eng = cstr(d, b + ENG_OFF)
        name = cstr(d, b + 0x02)             # 잡음 설명 필터용(참고)
        desc = cstr(d, b + DESC_OFF)
        ts, ss = raw[b + TS_OFF], raw[b + SS_OFF]
        entry = {"eng": eng, "cat": category(item_id)}
        if desc and desc != name:
            entry["desc"] = desc
        if ts: entry["ts"] = ts              # 무기만 >0
        if ss: entry["ss"] = ss
        info[item_id] = entry
    info[0] = {"eng": "", "cat": "기타"}     # 없음
    out = os.path.join(PROJ, "item_info.json")
    json.dump(info, open(out, "w", encoding="utf-8"), ensure_ascii=False)
    have = sum(1 for v in info.values() if v.get("desc"))
    wep = sum(1 for v in info.values() if v.get("ts") or v.get("ss"))
    print("records=%d entries=%d desc=%d weapon(ts/ss)=%d -> %s" % (n, len(info), have, wep, out))
    for sid in (7, 16, 22, 53, 25, 126):     # 검증 샘플 (TS/SS 예시 포함)
        v = info.get(sid, {})
        print("  id%-3d [%s] TS:%s SS:%s | %s" % (sid, v.get("cat"), v.get("ts"), v.get("ss"), v.get("desc", "")))

if __name__ == "__main__":
    main()
