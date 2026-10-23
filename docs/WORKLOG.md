# 작업 이력 / 할 일 (2026-10-23 기준)

새 세션은 이 문서와 루트의 `CLAUDE.md`를 먼저 읽고 시작하세요. 사용법은 `README.md`를 보세요.

## 한 줄 요약

arXiv 초록으로 만드는 LinkedIn 뉴스레터(LLM, Quantum Computing)를 "키워드 점수 기반 랜덤 5편"에서
**"한 주에 스토리 1개 + 근거 논문 2~3편 + AI가 쓴 Editor's Take"** 방식으로 바꾸고, 매주 월요일 클라우드 루틴이
초안을 만들어 **메일과 GitHub 브랜치**로 전달하도록 자동화했다. 기존 방식은 그대로 남아 있다.

## 정반합 정리 (왜 이렇게 바꿨나)

- 정(기존): 논문 5개를 같은 비중으로 나열, 초록 요약. 장점은 꾸준한 업로드와 자동화.
- 반(문제): 5개가 서로 무관해서 감흥과 인사이트가 없음. 반대 극단(1편 깊게)은 선정 실패 위험, 초록만으로는 깊이 한계.
- 합(채택): 군집 기반 스토리 1개 + 논문 2~3편 + 한 줄 언급 최대 3편. 독자는 실무자와 입문자("이게 왜 의미 있는지").
  Editor's Take는 사람이 쓸 시간이 없어 AI가 쓰되, 입장과 "무엇이 나오면 생각이 바뀌는지"를 반드시 넣는다.

## 구조

| 파일 | 역할 |
|---|---|
| `curated_newsletter.py` | 3단계 파이프라인: 초록 점수화(Haiku) → 스토리 선정(Opus) → 글 작성(Opus). 링크와 제목은 CSV에서 가져온다(LLM이 지어낼 수 없음) |
| `commands.py` | `--curated --planned-date`로 큐레이션 실행. Claude를 못 쓰면(종료 코드 3) 기존 키워드 선정으로 전환 |
| `newsletter_template.json` | `curated` 블록(제목, 캡션 인트로, 해시태그, `take_label`, 독자·관점)과 `curated_footers`(주차별로 도는 cert-bank 푸터 4개) |
| `utils/arxiv_web_crawler.py` | 크롤러. 이번에 고침(아래) |
| `99. Image/` | 표지 이미지. `llm/llm-curated-cover.png`, `quantum/quantum-curated-cover.png`, 생성 스크립트 `make_covers.py` |
| `drafts/` | (브랜치 `claude/newsletter-drafts`에만 있음) 루틴이 만든 초안과 `drafts/_history/` 스토리 기록 |

Claude 사용 순서: **구독(`claude` CLI) → `ANTHROPIC_API_KEY` → 기존 방식**. 구독 호출에서는 API 키 환경 변수를 제거한다
(있으면 API로 과금되므로). 한 방식이 실패하면 다음으로 넘어가고, 응답은 스키마로 검증해 한 번 재시도한다.
Windows `claude.cmd` 셸(인자 깨짐)은 프롬프트를 표준입력으로 넘겨 피했다(Linux에서만 흉내 내 검증).

## 루틴 (클라우드 예약 작업)

- 이름 `Weekly newsletter draft`, trigger `trig_01M4k2PvgH1nTzTGvkYYuwc9`, 환경 `env_01148h3mEhTsqkkrZwJcg1Xj`
- **매주 월요일 07:38 KST** (요청은 8시였지만 정각 지연을 피하려고 22분 앞당김). 다음 실행: 2026-10-26.
- 날짜 규칙: DATE_TO = 가장 최근 일요일, DATE_FROM = 그 6일 전(월요일), PLANNED = DATE_TO + 1일.
- 하는 일: 크롤링 → 큐레이션 → `claude/newsletter-drafts` 브랜치의 `drafts/<날짜>/`에 저장 → **본인에게 메일 1통씩**
  (맨 위 표지 이미지 링크, "1) POST TEXT"와 "2) NEWSLETTER ARTICLE" 구분) → 로컬 브랜치 정리 →
  머지된 `curated-newsletter`, `cover-images`만 원격에서 삭제(토큰이 없으면 건너뜀) → 짧은 보고서와 푸시 알림.
- 프롬프트 전문은 claude.ai/code/routines의 해당 루틴에 있다. 수신자 주소는 공개 저장소에 적지 않았으므로(프롬프트 6단계 참고)
  루틴에서 확인하세요.
- 루틴을 수정할 때: 저장소 연결(Repository)과 Gmail 커넥터는 **claude.ai 루틴 화면**에서만 설정된다(도구로는 못 함).
  네트워크는 환경 설정에서 `arxiv.org`를 허용(Custom + 패키지 매니저 포함)해 둔 상태다. 채팅의 "코드 실행 네트워크" 설정은
  클라우드 환경과 별개라서 효과가 없었다.

## 고친 문제 (기억해 둘 것)

1. **크롤러 500**: arXiv가 첫 페이지의 `arxiv-search-parameters` 쿠키를 보낸 2페이지 이후 요청에 500을 준다. 쿠키를 매번 비우고,
   5xx는 재시도, 페이지 간격 5초, 범위 구간(밀집 페이지)이 끝나면 연속 2페이지가 성기면 종료. LLM 주간 후보 3편 → 약 960편.
   트레이드오프: 성긴 꼬리의 약 190편(16%)은 포기.
2. **`pandas`가 arXiv ID를 숫자로 읽음** → `dtype={'arxiv_id': str}`.
3. **같은 주 재생성 시 그 주의 논문이 "사용됨"으로 빠짐** → 다른 주의 기록만 제외.
4. 메일/붙여넣기 때 보이지 않는 BOM → 초안을 BOM 없이 저장.
5. `commands.py`가 `python` 대신 `sys.executable`을 쓴다. 한글 Windows 콘솔 출력 오류 방지(`errors='replace'`).
6. `requirements.txt`에 `anthropic`, `pandas`, `beautifulsoup4` 추가(크롤러가 쓰는데 빠져 있었음).

## 검증 이력

- 구독 경로 실제 실행 OK(일반 방식과 `claude.cmd` 방식 모두), API 경로는 가짜 클라이언트로만 확인, 폴백 체인(구독 실패 → API → 종료 코드 3 → 기존 방식) OK.
- 새 클론 + 빈 가상환경에서 `--help`, `--dry-run`, 파일 없음 오류 메시지, 폴백 확인(Python 3.13만).
- 루틴 시험 실행 4회: 1회차는 저장소 미연결로 실패 → 연결 후 2~4회차 성공. 4회차(최종) 결과: 두 주제 모두 크롤링 → 초안 → 브랜치 → 메일 정상,
  표지 링크 200. 4회차 초안의 숫자는 원본 초록과 대조해 일치 확인.
- 시험 메일 제목은 `[TEST]`로 시작. 시험 실행은 스토리 기록을 남기지 않는다.

## PR 이력

- #2 큐레이션 + 크롤러 수정 + README + 푸터 (머지 `846007c`)
- #3 표지 이미지 (머지 `77a8808`)
- 이 문서와 `CLAUDE.md`, `99. Image/make_covers.py`는 `worklog` 브랜치의 PR로 머지

## 할 일 (우선순위 순)

1. **첫 정식 실행(2026-10-26 월 07:38 KST) 확인**: 메일 2통(제목에 `[TEST]` 없음), `claude/newsletter-drafts`의
   `drafts/2026-10-26/`와 `drafts/_history/`, 보고서의 "스토리 기록 복원 여부"(첫 주는 기록 없음이 정상).
2. **발행 전 사람의 검토**: Editor's Take는 초록만 읽고 쓴 AI 의견이다. 숫자·링크를 훑고 Take에 동의하는지 확인.
3. 원격 브랜치 `curated-newsletter`, `cover-images`(둘 다 머지됨)가 남아 있으면 GitHub에서 Delete branch.
   기존 `weekly-newsletter-automation` 브랜치는 이 작업과 무관하므로 건드리지 않았다.
4. 시험 메일 4통(`[TEST]`)이 실제로 도착했는지 사용자가 확인(도착 여부는 보고서의 "발송 성공"만 확인했고 메일함은 열어 보지 않았다).
5. Windows 로컬 실행은 직접 해 보지 못했다. 첫 실행은 `--dry-run`으로. 구독이 안 되면 API/기존 방식으로 자동 전환된다.
6. (선택) 후원 링크: 지금 푸터는 cert-bank 사이트만 건다. `support.html`은 사이트 안에서 이어진다.
7. (선택) 기존 방식의 `rank_parser.py`는 후보가 선택 편수보다 적으면 오류가 난다(이번 변경과 무관한 기존 제약).
8. (선택) Editor's Take 공개 방식: 지금 라벨은 "💭 Editor's Take". AI 보조 표기를 넣으려면 `newsletter_template.json`의 `take_label`을 바꾼다.
9. 표지 이미지를 바꾸려면 `99. Image/make_covers.py`의 `COVERS`를 고쳐 실행(Chromium, Pillow, Inter 폰트 필요).

## 결정 사항 / 사용자 지침

- 응답은 한국어. 사용자는 영어가 모국어가 아니며, 메시지의 어색한 표현을 짧게 교정해 달라는 설정이 있다(반복 패턴: "-ㄹ지/-려나" 붙여 쓰기, 보조 동사 "주다" 띄어 쓰기, "되/돼").
- Take는 자동화한다(직접 쓸 시간 없음). 독자는 실무자와 입문자 중심.
- 푸터는 cert-bank 한 줄(고정 문구 4개 돌려쓰기, API 불필요).
- 결과는 **메일과 브랜치 둘 다**. 메일은 본인에게만. 이미지는 첨부가 아니라 저장소 링크(약 1MB 첨부를 모델이 인자로 옮기는 건 신뢰하기 어려움).
- 2026-10-23 사용자 지침: "특별한 제약이 없으면 앞으로는 PR을 자율적으로 머지해서 진행". 머지가 아닌 되돌리기 어려운 작업(브랜치 삭제 등)은 별도 확인.
