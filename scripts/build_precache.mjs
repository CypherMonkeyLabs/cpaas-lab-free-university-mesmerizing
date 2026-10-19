/* Fill SHELL_ASSETS in sw.js from a required list, under a 3.5 MB budget. */
import fs from "node:fs";
import path from "node:path";

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const budget = 3_500_000;
const required = [
  "index.html",
  "offline.html",
  "start.html",
  "play.html",
  "rooms/sip-jobs.html",
  "manifest.webmanifest",
  "favicon.svg",
  "assets/data/cpaasbot-index.json",
  "assets/data/catalog.json",
  "shared/pybot-chat/engine.js",
  "shared/pybot-chat/ui.js",
  "shared/pybot-chat/chat.css",
  "guide/guide.js",
  "guide/guide.css",
  "guide/dragbot.js",
  "guide/cpaas-chat.js",
  "assets/js/frame.js",
  "assets/js/university.js",
  "assets/js/pwa.js",
  "assets/js/theme-boot.js",
  "assets/js/play.js",
  "assets/css/studio.css",
  "assets/icon-192.png",
  "assets/icon-512.png",
  "assets/icon-maskable-512.png",
];
for (const name of fs.readdirSync(path.join(root, "assets/css"))) {
  if (name.endsWith(".css")) required.push(`assets/css/${name}`);
}
for (const name of fs.readdirSync(path.join(root, "assets/fonts"))) {
  if (name.endsWith(".woff2")) required.push(`assets/fonts/${name}`);
}

const chosen = [];
let total = 0;
for (const rel of required) {
  const abs = path.join(root, rel);
  if (!fs.existsSync(abs) || chosen.includes(rel)) continue;
  const size = fs.statSync(abs).size;
  if (total + size > budget) {
    console.log("skip over budget", rel, size);
    continue;
  }
  chosen.push(rel);
  total += size;
}
const body = chosen.map((rel) => `  "./${rel}",`).join("\n");
const swPath = path.join(root, "sw.js");
let sw = fs.readFileSync(swPath, "utf8");
sw = sw.replace(/const SHELL_ASSETS = \[[\s\S]*?\];/, `const SHELL_ASSETS = [\n  "./",\n${body}\n];`);
sw = sw.replace(/cpaas-lab-v\d+/, "cpaas-lab-v4");
fs.writeFileSync(swPath, sw);
console.log(`precache ${chosen.length + 1} files, ${total} bytes, budget ${budget}`);
