# technical-newletter

arXiv 논문 초록으로 LinkedIn 뉴스레터(LLM, Quantum Computing)를 만듭니다.

## 두 가지 방식

| | 큐레이션 방식 (`--curated`, 권장) | 기존 방식 |
|---|---|---|
| 선정 | 이번 주 **스토리 1개** + 논문 2~3편 + 한 줄 언급 최대 3편 | 키워드 점수 기반 랜덤 5편 |
| 글 | 훅, 무슨 일이 있었나, 왜 중요한가, 쉬운 설명, 현실 점검, Editor's Take | 초록 요약 나열 |
| 요약 | Claude가 자동 작성 | `llm` 열을 직접 채움 (GPT 웹) |

큐레이션 흐름: 초록 점수화(Haiku) → 스토리 선정(Opus) → 글 작성(Opus). 링크와 제목은 CSV에서 가져오므로 LLM이 지어낼 수 없습니다. 지난 호에서 쓴 논문과 스토리는 `<Query>/newsletter/history.json`으로 기록해 다음 주에 제외합니다.

## 사용법

```bash
pip install -r requirements.txt

# 크롤링 + 큐레이션 (Query: LLM | "Quantum Computing")
python commands.py --query LLM --date-from 2026-09-28 --date-to 2026-10-04 --curated --planned-date 2026-10-12
```

결과: `<Query>/newsletter/curated_<날짜>.txt`와 같은 내용의 `.md` (위쪽 게시글 캡션 + 아래 본문). **LinkedIn에 올릴 때는 `.md`를 쓰세요.** 메일에서 복사하면 이모지가 이미지로, 링크가 리다이렉트 주소로 바뀝니다. `.md`를 로컬 미리보기(VS Code 등)에서 열어, 게시글 글은 코드 블록에서, 본문은 렌더링된 미리보기에서 복사합니다. **발행 전에 직접 읽고 Editor's Take를 확인하세요.** 초록만 보고 쓴 AI 초안입니다.

### Claude 사용 순서

1. **구독**: `claude` CLI에 로그인되어 있으면 사용 (`claude auth status`). 이때 `ANTHROPIC_API_KEY`는 자동으로 무시합니다.
2. **API**: 구독이 없거나 실패하면 `ANTHROPIC_API_KEY` 사용.
3. **기존 방식**: 둘 다 없으면 키워드 선정으로 전환 (`weekly_newsletter.py`는 `llm` 열을 직접 채운 뒤 실행).

실행 도중 한 방식이 실패하면 다음 방식으로 이어서 진행합니다. `claude`가 PATH에 없으면 `CLAUDE_BIN=<claude 실행 파일 경로>`로 지정하세요. Windows에서는 네이티브 설치(`claude.exe`)를 권장하며, npm 설치(`claude.cmd`)도 동작하도록 인자를 단순화해 두었습니다.

### 자주 쓰는 옵션 (`curated_newsletter.py`)

| 옵션 | 설명 |
|---|---|
| `--dry-run` | API 호출 없이 후보 논문과 사용할 방식만 확인 |
| `--rerun` | 캐시(`<Query>/curation/*.json`)를 무시하고 처음부터 다시 생성 |
| `--lang Korean` | 작성 언어 변경 (기본 English) |
| `--backend subscription\|api` | 방식 강제 지정 |
| `--writing-model`, `--analysis-model` | 모델 변경 |

스토리가 마음에 들지 않으면 `<Query>/curation/*_plan.json`을 고친 뒤 `--rerun` 없이 다시 실행하면 글 작성 단계부터 다시 합니다.

### 템플릿

문구(제목, 해시태그, 캡션 인트로, `take_label`, 독자·관점 설명)는 `newsletter_template.json`의 `curated` 블록에서 수정합니다. 본문 끝(꼬리말 바로 위)에는 `curated_footers`의 문구가 주차마다 돌아가며 한 줄 들어갑니다(API 불필요, 비우면 푸터 없음).

`.md` 본문의 구분선과 부제목은 `newsletter_template.json`의 `curated_layout`에서 정합니다. **지금은 `dividers`가 비어 있어 구분선을 넣지 않습니다**(LinkedIn의 구분선 버튼으로 직접 넣는 방식). 자동으로 넣고 싶으면 `dividers`에 `between_sections`(섹션 사이), `before_papers`, `between_papers`, `before_footer` 중 원하는 위치를 넣습니다. `divider_length`는 글자 줄의 길이(기본 30, 데스크톱에서 한 줄의 약 70%)입니다. 글자 줄은 화면 너비에 맞춰 늘거나 줄지 않으므로 너무 길면 폭이 좁은 화면(모바일)에서 두 줄로 꺾일 수 있습니다. `divider_style`은 기본 `line`(`──────` 글자 줄, 어떤 방식으로 붙여도 유지됨)이고, `hr`은 마크다운 가로선(`---`)인데 LinkedIn에 붙이면 글자 `---`로 들어오는 경우가 있었습니다. `subtitle_level`은 날짜 줄의 크기로, 기본 0은 굵은 글씨(붙인 뒤 편집기에서 부제목 스타일을 한 번 지정), 2는 `##` 헤딩입니다.

## 기존 방식

`100. Guide/뉴스레터 가이드.txt` 참고. (`commands.py` → `llm` 열 추가 → `daily_newsletter.py` / `weekly_newsletter.py`)
