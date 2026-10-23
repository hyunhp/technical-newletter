# technical-newletter

arXiv 초록으로 LinkedIn 뉴스레터(LLM, Quantum Computing)를 만드는 저장소. 응답은 한국어로 한다.

## 시작하기 전에

1. `docs/WORKLOG.md`를 읽는다(작업 이력, 현재 상태, 할 일, 결정 사항).
2. 사용법은 `README.md`, 설정 문구는 `newsletter_template.json`의 `curated` 블록.

## 규칙

- 기본 흐름은 `python commands.py --query LLM|"Quantum Computing" --date-from YYYY-MM-DD --date-to YYYY-MM-DD --curated --planned-date YYYY-MM-DD`.
  기존 방식(`--curated` 없이)은 그대로 둔다.
- `LLM/`, `Quantum_Computing/` 폴더(크롤링 결과, 초안, 캐시)는 git에서 제외되어 있다. 루틴이 만든 초안은 브랜치 `claude/newsletter-drafts`의 `drafts/`에 있다.
- Editor's Take는 초록만 읽고 쓴 AI 초안이다. 숫자와 링크는 원본 초록과 대조해 확인한 뒤 발행한다. 논문, 숫자, 링크를 지어내지 않는다.
- 메일은 소유자 본인에게만 보낸다. 주소는 루틴 프롬프트에 있고 이 저장소는 공개이므로 파일에 적지 않는다.
- 사용자 지침: 특별한 제약이 없으면 이 작업의 PR은 자율적으로 머지한다. 브랜치 삭제처럼 되돌리기 어려운 작업은 먼저 확인한다.
- `gh pr create`는 GraphQL이라 클라우드 세션에서 막힌다. `gh api repos/hyunhp/technical-newletter/pulls`(REST)를 쓴다.
