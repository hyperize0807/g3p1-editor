# 창세기전3 파트1 세이브 에디터

[창세기전3: 파트1](https://en.wikipedia.org/wiki/The_War_of_Genesis_III) 의 세이브 파일(`g3xxxx.sav`)을 편집하는 **브라우저 기반** 에디터입니다.
설치가 필요 없는 단일 HTML 파일이며, 세이브 파일은 전부 브라우저 안에서만 처리됩니다(업로드 없음).

> 게임 실행 파일을 역분석하여 세이브 포맷·변조방지 체크섬을 직접 구현했습니다. 저장 시 체크섬이 자동 재계산되어 게임이 정상 로드합니다.

## 빠른 시작

1. [`dist/index.html`](dist/index.html) 을 내려받아 브라우저로 엽니다.
2. `.sav` 파일을 열고 → 편집 → **저장(다운로드)**.
3. 자세한 사용법은 **[사용자 가이드](dist/USER_GUIDE.md)** 참고.

> ⚠️ 편집 전 **세이브 파일을 반드시 백업**하세요.

## 기능

- 🔢 **버전 1.03+ / 1.04 지원**: 로드 시 자동 감지·표시, 저장 시 버전 선택(기본=로드 버전). 두 버전 외 패턴은 안전을 위해 로드 거부
- 💰 소지금 (에피소드별, 현재 진행 에피소드 자동 표시)
- 🧑 캐릭터: 식별정보 / 능력치(HP·EXP·STR~WTP) / 장비 / **어빌리티(최대 레벨 자동 적용)**
- 🎒 보관함: 현재 에피소드는 안전 편집, 그 외는 "위험 영역"으로 분리
- 📖 아이템 사전: 이름(한/영)·설명 검색 + 분류 필터(무기/써크렛/방어구/장신구/소비) + 무기 TS/SS 공격스탯
- 아이템 드롭다운(장비·보관함): 커스텀 드롭다운으로 이름 강조(굵게/색) + 설명 + 무기 TS/SS + 검색, 펼쳐서 비교·선택
- 중복 없는 캐릭터 목록 + 모든 에피소드 블록 일괄 적용
- 저장 시 변조방지 체크섬 자동 재계산

## 폴더 구조

```
dist/        배포물 (최종 사용자용)
  index.html     에디터 (단일 파일, 데이터 내장)
  USER_GUIDE.md  사용자 가이드
docs/
  SAVE_FORMAT.md 세이브 파일 포맷 명세 (역분석 결과)
tools/        유지보수/빌드용
  build_editor.py   index.html 빌드 (tables.json + abil_max.json + item_info.json 내장)
  gen_tables.py     G3Data/*.txt → tables.json
  abimax2.py        Abi.dat → abil_max.json (어빌리티 최대 레벨)
  gen_itemdat.py    Item.dat → item_info.json (아이템 이름/설명)
  tables.json       이름 테이블(아이템/캐릭터/직업 등)
  abil_max.json     어빌리티별 최대 레벨
  item_info.json    아이템 이름(한/영)·설명
  G3Data/           게임에서 추출한 이름 테이블 원본(CP949)
samples/      (git 제외) 테스트용 세이브, 원본 SaveEdit.exe
```

## 빌드 (개발자용)

`dist/index.html` 은 다음으로 재생성합니다:

```sh
python tools/build_editor.py        # tools/*.json 을 index.html(dist/)에 내장
```

데이터 테이블을 다시 추출하려면(게임 설치 필요, `tools/*.py` 내 경로 수정):

```sh
python tools/gen_tables.py          # G3Data/*.txt -> tools/tables.json
python tools/abimax2.py             # <게임>/dats/Abi.dat -> tools/abil_max.json
python tools/gen_itemdat.py         # <게임>/dats/Item.dat -> tools/item_info.json
```

## 포맷 명세

세이브 파일 구조(난독화/체크섬/레코드 레이아웃/소지금/보관함/어빌리티 등)는
**[docs/SAVE_FORMAT.md](docs/SAVE_FORMAT.md)** 에 정리되어 있습니다.

## 면책 / 라이선스

- 팬메이드 비공식 도구입니다. 게임 및 그 데이터의 권리는 원저작권자에게 있습니다.
- 이름 테이블 등 일부 게임 파생 데이터를 포함합니다. 개인적·비상업적 용도로 사용하세요.
- 세이브 편집은 본인 책임하에, 반드시 백업 후 사용하세요.
