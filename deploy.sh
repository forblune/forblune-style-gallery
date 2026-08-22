#!/usr/bin/env bash
# Forblune Style Gallery — 배포 스크립트
# 1) dist/ 를 공개용 파일만으로 재구성 (index.html, sites/**, 404.html)
# 2) Cloudflare Workers Static Assets 로 배포 (wrangler.toml 의 custom_domain 라우트가 gallery.forblune.com 을 연결)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

rm -rf dist
mkdir -p dist
cp index.html dist/
[ -f 404.html ] && cp 404.html dist/ || true
[ -f og.png ] && cp og.png dist/ || true   # 링크 공유 미리보기 이미지
cp -r sites dist/sites
cp -r shots dist/shots   # 허브 카드 썸네일
# meta.json 은 허브가 쓰지 않으므로 공개본에서 제외
find dist/sites -name meta.json -delete
# __wb.html 은 작업용 파일이다. 운영에 나가면 안 된다
find dist/sites -name '__wb.html' -delete

# sitemap.xml · robots.txt 생성 (dist 를 훑어 만들므로 페이지가 늘어도 안 낡는다)
node tools/gen-sitemap.mjs

echo "dist/ 구성 완료:"; find dist -maxdepth 2 | head -40

CLOUDFLARE_ACCOUNT_ID=8e7db1ee168c06561f422235363c977c npx --yes wrangler@4.123.0 deploy
