// Validates data/lesson-map.json against the room pages on disk.
// Every lesson needs a level 0-10, at least one outcome, source ids that exist, and a matching title.
// Run: node scripts/validate_lessons.mjs
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { loadLessons } from "../pipeline/lessons.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const map = JSON.parse(readFileSync(path.join(root, "data/lesson-map.json"), "utf8"));
const schema = JSON.parse(readFileSync(path.join(root, "data/lesson-schema.json"), "utf8"));
const lessons = loadLessons();
const problems = [];
const mapped = new Map(map.lessons.map((lesson) => [lesson.key, lesson]));
const seen = new Set();
const required = schema.required;

for (const lesson of lessons) {
  seen.add(lesson.key);
  const row = mapped.get(lesson.key);
  if (!row) {
    problems.push(`${lesson.key}: not in lesson-map.json`);
    continue;
  }
  for (const field of required) if (!(field in row)) problems.push(`${lesson.key}: missing field ${field}`);
  if (!Number.isInteger(row.level) || row.level < 0 || row.level > 10) problems.push(`${lesson.key}: level must be 0-10`);
  if (!Array.isArray(row.outcomes) || row.outcomes.length < 1 || row.outcomes.some((item) => typeof item !== "string" || item.length < 8)) {
    problems.push(`${lesson.key}: needs at least one outcome`);
  }
  if (!Array.isArray(row.sources) || row.sources.length < 1) problems.push(`${lesson.key}: needs at least one source`);
  const ids = new Set(lesson.sources.map((src) => src.id));
  for (const id of row.sources || []) if (!ids.has(id)) problems.push(`${lesson.key}: unknown source id ${id}`);
  if (JSON.stringify(row.sources) !== JSON.stringify(lesson.sources.map((src) => src.id))) {
    problems.push(`${lesson.key}: sources differ from the room sources file`);
  }
  if (row.title !== lesson.title) problems.push(`${lesson.key}: title differs from the room page`);
  if (row.level !== lesson.level) problems.push(`${lesson.key}: level differs from the track kicker`);
  if (row.last_verified !== null && !/^\d{4}-\d{2}-\d{2}$/.test(row.last_verified)) {
    problems.push(`${lesson.key}: last_verified must be null or YYYY-MM-DD`);
  }
}
for (const key of mapped.keys()) if (!seen.has(key)) problems.push(`${key}: in lesson-map.json but no such room`);

const perLevel = {};
for (const row of map.lessons) perLevel[row.level] = (perLevel[row.level] || 0) + 1;
for (const problem of problems) console.log("FAIL", problem);
console.log("lessons:", seen.size, "mapped:", mapped.size, "per level:", JSON.stringify(perLevel));
console.log("validate_lessons:", problems.length, "problems");
process.exit(problems.length ? 1 : 0);
