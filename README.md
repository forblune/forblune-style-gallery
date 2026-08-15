# Forblune Style Gallery

Forblune 웹 디자인 언어 시스템 v2의 8개 카테고리(Editorial · Kinetic · Cinematic · Corporate · Product · Commerce · Experimental · Utility)마다 예시 사이트 3개씩, 총 24개를 만들어 한 곳에서 비교해 보는 갤러리입니다. 카테고리별 문법이 실제 사이트에서 어떻게 다르게 읽히는지 확인하고, 새 프로젝트의 스타일을 정할 때 레퍼런스로 쓰기 위한 것입니다.

- 허브: `index.html` — 카테고리 필터, 라이브 미리보기(iframe 축소), 명명·Core Message·검토 요약 카드 24장
- 각 사이트: `sites/<slug>/index.html` — 외부 라이브러리 없는 단일 HTML 파일(인라인 CSS/JS), Pretendard CDN + 시스템 폴백
- 확인일 2026-08-16: 24개 중 정상 24개, 총 34,789줄

## 폴더 구조

```
forblune-style-gallery/
├── index.html                 # 갤러리 허브 (필터·미리보기·검토 요약)
├── README.md
├── deploy.sh                  # dist/ 구성 후 Cloudflare Workers Static Assets 배포
├── wrangler.toml
├── _reference/
│   ├── design-language.md     # Notion 원문 + Micro Element Library 요약 (8개 카테고리 문법, DNA 지표)
│   ├── anti-ai-slop.md        # AI 티 제거 기준 (금지 패턴, 리뷰 체크리스트 16항목)
│   ├── audit/deai-reviews.json
│   └── research/anti-ai-look-deep-dive.md
└── sites/
    └── <slug>/
        ├── index.html         # 예시 사이트 본문 (단일 파일)
        └── meta.json          # 명명·팔레트·섹션·인터랙션 기록 (허브는 읽지 않음, 배포본에서 제외)
```

## 카테고리

| 카테고리 | 한글 · 유형 | 중심 가치 | 핵심 감정 | 설득 수단 | 리듬 |
|---|---|---|---|---|---|
| Editorial | 에디토리얼 · 감성형 | 취향과 이미지 | Desire · 갖고 싶다 | 이미지·큐레이션 | Slow |
| Kinetic | 키네틱 · 임팩트형 | 에너지와 임팩트 | Excitement · 강하다 | 임팩트·모션 | Fast |
| Cinematic | 시네마틱 · 서사형 | 서사와 전문성 | Trust · 믿을 수 있다 | 사람·과정·철학 | Slow |
| Corporate | 코퍼레이트 · 신뢰형 | 신뢰와 정보 | Trust / Clarity · 이해된다 | 근거·구조·실적 | Balanced |
| Product | 프로덕트 · 기능형 | 기능과 사용성 | Clarity · 쓰고 싶다 | 기능 시연·사용 흐름 | Balanced |
| Commerce | 커머스 · 구매형 | 탐색과 구매 | Desire + Clarity | 상품·가격·혜택·리뷰 | Balanced~Fast |
| Experimental | 익스페리멘털 · 경험형 | 독창성과 경험 | Surprise / Curiosity | 경험 자체·인터랙션 | 가변 |
| Utility | 유틸리티 · 업무형 | 효율과 업무 | Control · 통제된다 | 데이터·상태·속도 | Fast (반응) |

Editorial · Kinetic · Cinematic은 Notion 원문의 기준 사례(f0ring, FlyOne V1, FlyOne V2)를 따르고, 나머지 다섯은 Notion에 한 줄 정의만 있어 `_reference/design-language.md`에서 파생 기준을 세웠습니다.

## 예시 사이트 24개

명명은 `Primary Style / Product Type / Tone` 순서입니다. 줄 수는 `sites/<slug>/index.html`의 `wc -l` 기준(2026-08-16 확인, 빈 줄 포함).

| # | slug | 카테고리 | 브랜드 | 업종 | 명명 (Primary / Product Type / Tone) | Secondary / Accent | 줄 수 |
|---|---|---|---|---|---|---|---|
| 1 | `editorial-perfume` | Editorial | 무향 MUHYANG | 니치 향수 브랜드 | Editorial / Commerce / Soft · Quiet · Curated | Commerce / Product | 1,250 |
| 2 | `editorial-stay` | Editorial | 숲결 스테이 | 제주 독채 스테이(숙소) | Editorial / Brand Landing (예약 유도) / Soft · Warm · Slow | Commerce / Cinematic | 1,626 |
| 3 | `editorial-select` | Editorial | 고요 GOYO | 문구·리빙 편집숍 | Editorial / Commerce / Curated · Neutral · Calm | Commerce / Product | 1,533 |
| 4 | `kinetic-sneaker` | Kinetic | VOLT LAB | 스트리트 스니커 드롭 스토어 | Kinetic / Commerce (Drop) / Bold · Loud · Fast | Commerce / Experimental | 1,543 |
| 5 | `kinetic-festival` | Kinetic | PULSE FEST 2026 | 일렉트로닉 뮤직 페스티벌 | Kinetic / Event Landing / Bold · Energetic · Colorful | Experimental / Corporate | 1,348 |
| 6 | `kinetic-esports` | Kinetic | APEX NINE | e스포츠 프로 팀 | Kinetic / Brand Landing / Bold · Technical · Sharp | Corporate / Commerce | 1,575 |
| 7 | `cinematic-architecture` | Cinematic | 온결 건축 ONGYEOL | 건축 설계 스튜디오 | Cinematic / Portfolio / Serious · Crafted · Quiet | Editorial / Corporate | 1,203 |
| 8 | `cinematic-chef` | Cinematic | 화로 火爐 | 셰프 오마카세 레스토랑 | Cinematic / Brand Site (예약 문의) / Serious · Warm · Human | Editorial / Commerce | 1,346 |
| 9 | `cinematic-photographer` | Cinematic | 정하늘 JEONG HANEUL | 다큐멘터리 사진가 | Cinematic / Portfolio / Serious · Human · Documentary | Editorial / Corporate | 1,664 |
| 10 | `corporate-hospital` | Corporate | 바른마디 정형외과 | 정형외과 의원 | Corporate / Information Site / Trustworthy · Calm · Clear | Cinematic / Product | 1,601 |
| 11 | `corporate-lawfirm` | Corporate | 법무법인 서로 | 법무법인 | Corporate / Information Site / Serious · Precise · Composed | Editorial / Cinematic | 1,898 |
| 12 | `corporate-b2b` | Corporate | 한결정밀 | 정밀 가공 부품 제조(B2B) | Corporate / B2B Company Site / Technical · Trustworthy · Solid | Product / Utility | 1,839 |
| 13 | `product-saas` | Product | 인보이스플로우 InvoiceFlow | 소상공인 청구·세금계산서 SaaS | Product / SaaS Landing / Clear · Friendly · Confident | Corporate / Utility | 1,418 |
| 14 | `product-app` | Product | 잠결 | 수면 트래킹 모바일 앱 | Product / App Landing / Soft · Clear · Reassuring | Editorial / Utility | 1,524 |
| 15 | `product-devtool` | Product | Relay API | 알림·메시지 발송 API 플랫폼 | Product / Developer Platform Landing / Technical · Precise · Minimal | Utility / Kinetic | 1,407 |
| 16 | `commerce-grocery` | Commerce | 새벽밭 | 산지직송 식료품 온라인 마켓 | Commerce / Storefront / Fresh · Clear · Trustworthy | Editorial / Product | 1,535 |
| 17 | `commerce-booking` | Commerce | 무브룸 MOVEROOM | 요가·필라테스 클래스 예약 | Commerce / Booking / Clear · Calm · Efficient | Product / Editorial | 1,607 |
| 18 | `commerce-furniture` | Commerce | 결 가구 GYEOL | 온라인 가구 쇼핑몰 | Commerce / Storefront (Category Page) / Neutral · Warm · Practical | Editorial / Product | 1,569 |
| 19 | `experimental-campaign` | Experimental | 물의 기억 — 담수(淡水) 캠페인 | 생수 브랜드 캠페인 마이크로사이트 | Experimental / Campaign Microsite / Poetic · Bold · Immersive | Editorial / Cinematic | 1,412 |
| 20 | `experimental-art` | Experimental | 빛의 잔향 AFTERGLOW | 미디어아트 전시 | Experimental / Exhibition Site / Dark · Immersive · Curious | Cinematic / Kinetic | 1,384 |
| 21 | `experimental-launch` | Experimental | ORBIT ONE | 스마트 링 신제품 티저 | Experimental / Product Teaser / Bold · Futuristic · Minimal | Kinetic / Product | 1,342 |
| 22 | `utility-dashboard` | Utility | 브루잉 OS — 매장 운영 대시보드 | 카페 체인 매장 운영 대시보드 | Utility / Dashboard / Neutral · Dense · Calm | Product / Corporate | 885 |
| 23 | `utility-erp` | Utility | 스톡플로우 — 재고·발주 관리 | 소매 재고·발주 내부 도구(ERP) | Utility / Internal Tool / Neutral · Dense · Functional | Product / Corporate | 994 |
| 24 | `utility-admin` | Utility | 헬프데스크 콘솔 | 고객지원 티켓 관리 콘솔 | Utility / Admin Console / Neutral · Dark · Focused | Product / Corporate | 1,286 |

## 로컬 실행

```bash
cd forblune-style-gallery
python -m http.server 8080
# http://localhost:8080          — 허브
# http://localhost:8080/sites/editorial-perfume/index.html — 개별 사이트
```

`index.html`을 파일로 바로 열어도(`file://`) 카드와 필터는 동작하지만, 미리보기 iframe과 상대 경로 링크는 로컬 서버에서 여는 편이 안정적입니다.

## 기준 문서

- Notion 원문 — [Forblune 웹 디자인 언어 시스템 · v2](https://app.notion.com/p/3bb5baabfd1b81e3b0d8fcfeaf33916d)
- `_reference/design-language.md` — 에이전트용 요약(8개 카테고리 문법·DNA 지표·카피 공식)
- `_reference/anti-ai-slop.md` — AI 티 제거 기준(§2~§7 금지·대체 규칙, §8 리뷰 체크리스트)

기존 레퍼런스: [f0ring](https://f0ring.co.kr) (Editorial / Commerce / Soft · Curated) · [FlyOne V1](https://forblune.github.io/flyone-landing/) (Kinetic / Brand Landing / Bold · Energetic) · [FlyOne V2](https://forblune.github.io/flyone-landing/v2/) (Cinematic / Portfolio / Serious · Human)

## 배포

- 정본 URL: **https://gallery.forblune.com** (Cloudflare Workers Static Assets, 계정 Rjsgml13486@gmail.com, `wrangler.toml`의 `custom_domain` 라우트로 DNS·인증서 자동 생성 — 2026-08-16 배포)
- 백업 URL: https://forblune-style-gallery.rjsgml13486.workers.dev
- 소스: https://github.com/forblune/forblune-style-gallery
- 개별 사이트: `https://gallery.forblune.com/sites/<slug>/` (예: https://gallery.forblune.com/sites/kinetic-sneaker/)
- 재배포: `bash deploy.sh` — `dist/`에 `index.html` + `sites/**`(meta.json 제외)를 복사한 뒤 `wrangler deploy` (사전에 `npx wrangler login` 필요)

## 허브 갱신

`index.html`과 이 README의 사이트 표는 같은 데이터에서 만들어집니다. 사이트를 추가하거나 검토 점수가 바뀌면 허브의 카드와 README 표를 함께 갱신하세요.
