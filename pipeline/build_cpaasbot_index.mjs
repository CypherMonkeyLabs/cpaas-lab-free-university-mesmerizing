/* Build the offline chat index from this lab's own pages.
   Usage: node pipeline/build_cpaasbot_index.mjs
   Writes assets/data/cpaasbot-index.json and data/lesson-map.json. */
import { writeFileSync, mkdirSync } from "node:fs";
import path from "node:path";
import { tokens } from "../shared/pybot-chat/engine.js";
import { loadLessons, loadPages, loadTracks, root } from "./lessons.mjs";

const SYN = {
  websockets: "websocket",
  trunking: "trunk",
  trunks: "trunk",
  attestations: "attest",
  attestation: "attest",
  proxies: "proxy",
  gateways: "gateway",
  carriers: "carrier",
  webhooks: "webhook",
  messages: "message",
  messaging: "message",
  numbers: "number",
  recordings: "recording",
  conferences: "conference",
};

function dated(text, confirm) {
  let ex = String(text || "").replace(/\s+/g, " ").trim();
  if (!ex) ex = "This page is part of the CPaaS study lab.";
  ex += " Source date: 2026-10.";
  if (confirm) ex += " Unconfirmed where the page says confirm.";
  return ex;
}

function docFrom(id, kind, title, href, section, excerpt, example, extra) {
  const body = `${title}. ${excerpt}. ${example || ""}. ${extra || ""}`;
  return {
    i: id,
    k: kind,
    ti: title,
    h: href,
    s: section,
    ex: excerpt,
    eg: example || "",
    w: tokens(body, SYN),
    tw: tokens(title, SYN),
  };
}

const lessons = loadLessons();
const docs = [];
for (const lesson of lessons) {
  const ex = dated(lesson.lede, lesson.confirm);
  const eg = lesson.outcomes[0] || "";
  docs.push(docFrom(
    `lesson:${lesson.slug}`,
    "lesson",
    lesson.title,
    lesson.href,
    lesson.kicker,
    ex,
    eg,
    lesson.outcomes.slice(0, 5).join(" "),
  ));
}
for (const page of loadPages()) {
  docs.push(docFrom(`page:${page.href}`, "page", page.title, page.href, "lab", dated(page.lede, /confirm/i.test(page.lede)), "", page.title));
}
for (const track of loadTracks()) {
  docs.push(docFrom(`level:${track.href}`, "level", track.title, track.href, "track", dated(track.lede, /confirm/i.test(track.lede)), "", track.title));
}

const seeds = [];
for (const doc of docs) {
  if (doc.k !== "lesson") continue;
  const all = (doc.tw || []).filter((term) => term.length >= 3).slice(0, 4);
  if (!all.length) continue;
  const allow = [...new Set([...(doc.tw || []), ...(doc.w || [])])].slice(0, 28);
  seeds.push({
    i: doc.i,
    h: doc.h,
    ti: doc.ti,
    k: "lesson",
    ex: doc.ex,
    eg: doc.eg,
    topic: all[0],
    all,
    allow,
    how: false,
    rank: 4,
  });
}

const index = { v: 2, syn: SYN, seeds, docs };
const outDir = path.join(root, "assets", "data");
mkdirSync(outDir, { recursive: true });
mkdirSync(path.join(root, "data"), { recursive: true });
writeFileSync(path.join(outDir, "cpaasbot-index.json"), `${JSON.stringify(index)}\n`);

const map = {
  lab: "cpaas",
  note: "Levels follow the track number: T1 is 0 through T11 is 10. T12 shares level 10. last_verified is null because the pages record 2026-10, not a day.",
  lessons: lessons.map((lesson) => ({
    key: lesson.key,
    title: lesson.title,
    level: lesson.level,
    outcomes: lesson.outcomes.length ? lesson.outcomes : [lesson.lede].filter((line) => line.length >= 8),
    sources: lesson.sources.map((src) => src.id),
    last_verified: null,
  })),
};
writeFileSync(path.join(root, "data", "lesson-map.json"), `${JSON.stringify(map, null, 2)}\n`);
console.log(`index docs ${docs.length}, seeds ${seeds.length}, lessons ${lessons.length}`);
