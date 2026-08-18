// dist/ 를 훑어 sitemap.xml 과 robots.txt 를 만든다.
// 손으로 적으면 예시 사이트나 영문판이 늘 때 그대로 낡는다.
import { readdirSync, statSync, writeFileSync, existsSync } from "node:fs";
import { join } from "node:path";

const SITE = "https://gallery.forblune.com";
const DIST = new URL("../dist/", import.meta.url).pathname;
const date = process.env.SITEMAP_DATE || new Date().toISOString().slice(0, 10);

function walk(dir, base = "") {
  const out = [];
  for (const name of readdirSync(dir)) {
    const full = join(dir, name);
    if (statSync(full).isDirectory()) out.push(...walk(full, `${base}${name}/`));
    else if (name === "index.html") out.push(`/${base}`);
  }
  return out;
}

const paths = walk(DIST).sort();
// 영문판이 있는 한국어 페이지끼리 hreflang 으로 묶는다.
const hasEn = new Set(paths.filter((p) => p.endsWith("/en/")).map((p) => p.slice(0, -3)));

const entry = (p) => {
  const alt = p.endsWith("/en/") ? p.slice(0, -3) : hasEn.has(p) ? `${p}en/` : null;
  const self = p.endsWith("/en/") ? "en" : "ko";
  const lines = [`    <loc>${SITE}${p}</loc>`, `    <lastmod>${date}</lastmod>`];
  if (alt) {
    const other = self === "ko" ? "en" : "ko";
    lines.push(`    <xhtml:link rel="alternate" hreflang="${self}" href="${SITE}${p}"/>`);
    lines.push(`    <xhtml:link rel="alternate" hreflang="${other}" href="${SITE}${alt}"/>`);
  }
  lines.push(`    <priority>${p === "/" ? "1.0" : self === "en" ? "0.6" : "0.7"}</priority>`);
  return `  <url>\n${lines.join("\n")}\n  </url>`;
};

writeFileSync(join(DIST, "sitemap.xml"),
`<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
${paths.map(entry).join("\n")}
</urlset>
`, "utf8");

writeFileSync(join(DIST, "robots.txt"),
`User-agent: *
Allow: /

Sitemap: ${SITE}/sitemap.xml
`, "utf8");

console.log(`sitemap.xml — ${paths.length}개 URL (영문 ${paths.filter(p=>p.endsWith('/en/')).length}, hreflang 쌍 ${hasEn.size})`);
if (existsSync(join(DIST, "sites/commerce-booking/__wb.html")))
  console.log("경고: __wb.html 이 dist 에 남아 있다");
