/* Read this lab's room pages. The chat index and the lesson map both use this. */
import { readFileSync, readdirSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

export const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

export function decode(value) {
  return String(value || "")
    .replace(/<[^>]+>/g, " ")
    .replace(/&#x27;|&#39;/g, "'")
    .replace(/&quot;/g, '"')
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/\s+/g, " ")
    .trim();
}

function pick(html, re) {
  const match = html.match(re);
  return match ? decode(match[1]) : "";
}

export function sourceId(src, index) {
  const raw = src.url || src.title || `confirm-${index}`;
  const id = String(raw).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 96);
  return id || `src-${index}`;
}

export function loadLessons() {
  const dir = path.join(root, "rooms");
  const lessons = [];
  for (const name of readdirSync(dir).filter((file) => file.endsWith(".html")).sort()) {
    const slug = name.replace(/\.html$/, "");
    const html = readFileSync(path.join(dir, name), "utf8");
    const title = pick(html, /<h1>([\s\S]*?)<\/h1>/);
    const lede = pick(html, /<p class="lede">([\s\S]*?)<\/p>/);
    const kicker = pick(html, /<p class="kicker">([\s\S]*?)<\/p>/);
    const trackMatch = kicker.match(/T(\d+)/);
    const track = trackMatch ? Number(trackMatch[1]) : null;
    const five = html.match(/<section id="five"[\s\S]*?<ul>([\s\S]*?)<\/ul>/);
    const outcomes = five
      ? [...five[1].matchAll(/<li>([\s\S]*?)<\/li>/g)].map((item) => decode(item[1])).filter((line) => line.length >= 8)
      : [];
    const sourcesPath = path.join(root, "rooms", "sources", slug, "sources.json");
    let sources = [];
    try {
      const data = JSON.parse(readFileSync(sourcesPath, "utf8"));
      const seen = new Set();
      sources = (data.sources || []).map((src, index) => {
        let id = sourceId(src, index);
        while (seen.has(id)) id = `${id}-${index}`;
        seen.add(id);
        return { id, title: src.title || "", url: src.url || null, kind: src.kind || "" };
      });
    } catch (err) {
      sources = [];
    }
    const level = track == null ? null : Math.min(Math.max(track - 1, 0), 10);
    lessons.push({
      key: `rooms/${slug}`,
      slug,
      href: `rooms/${name}`,
      title,
      lede,
      kicker,
      track,
      level,
      outcomes,
      sources,
      confirm: /confirm/i.test(`${lede} ${outcomes.join(" ")}`),
    });
  }
  return lessons;
}

export function loadPages() {
  const names = [
    "index.html", "start.html", "diagrams.html", "flows.html", "play.html", "listen.html",
    "downloads.html", "quizzes.html", "flashcards.html", "ecosystem.html", "help.html",
    "legal.html", "charts.html",
  ];
  return names.map((name) => {
    const html = readFileSync(path.join(root, name), "utf8");
    return {
      href: name,
      title: pick(html, /<h1>([\s\S]*?)<\/h1>/) || name,
      lede: pick(html, /<p class="lede">([\s\S]*?)<\/p>/) || pick(html, /<meta name="description" content="([^"]+)"/),
    };
  });
}

export function loadTracks() {
  const dir = path.join(root, "tracks");
  return readdirSync(dir).filter((file) => /^T\d+\.html$/.test(file)).sort().map((name) => {
    const html = readFileSync(path.join(dir, name), "utf8");
    const n = Number(name.match(/T(\d+)/)[1]);
    return {
      href: `tracks/${name}`,
      title: pick(html, /<h1>([\s\S]*?)<\/h1>/),
      lede: pick(html, /<p class="lede">([\s\S]*?)<\/p>/),
      level: Math.min(Math.max(n - 1, 0), 10),
    };
  });
}
