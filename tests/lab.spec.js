import { test, expect } from "@playwright/test";
import fs from "node:fs";
import path from "node:path";

const shotDir = path.join("docs", "screenshots");
fs.mkdirSync(shotDir, { recursive: true });

async function quiet(page) {
  await page.addInitScript(() => {
    localStorage.setItem("cpaas-guide-v1", JSON.stringify({ tour: 1, greeted: 1 }));
  });
}

async function shot(page, name) {
  await page.screenshot({ path: path.join(shotDir, name), fullPage: false });
}

test.describe("desktop", () => {
  test.use({ viewport: { width: 1440, height: 900 } });
  test("home, bot, lesson", async ({ page }) => {
    await quiet(page);
    await page.goto("/index.html");
    await expect(page.locator("main h1")).toBeVisible();
    await shot(page, "home-1440.png");
    await page.locator(".monkey-btn").click();
    await expect(page.locator("#py-chat-input")).toBeVisible();
    await page.locator("#py-chat-input").fill("what is SIP");
    await page.locator(".py-chat-form button[type=submit]").click();
    await expect(page.locator(".py-msg-bot").last()).toContainText(/SIP/);
    await shot(page, "bot-1440.png");
    await page.goto("/rooms/sip-jobs.html");
    await expect(page.locator("main h1")).toContainText(/SIP/);
    await shot(page, "lesson-1440.png");
  });
});

test.describe("phone", () => {
  test.use({ viewport: { width: 390, height: 844 } });
  test("home, bot, lesson", async ({ page }) => {
    await quiet(page);
    await page.goto("/index.html");
    await expect(page.locator("main h1")).toBeVisible();
    await shot(page, "home-390.png");
    await page.locator("[data-open-guide]").click();
    const input = page.locator("#py-chat-input");
    const send = page.locator(".py-chat-form button[type=submit]");
    await expect(input).toBeVisible();
    await expect(send).toBeVisible();
    expect((await input.boundingBox()).width).toBeGreaterThanOrEqual(180);
    await shot(page, "bot-390.png");
    await page.goto("/rooms/sip-jobs.html");
    await expect(page.locator("main h1")).toContainText(/SIP/);
    await shot(page, "lesson-390.png");
  });
});

test("offline lesson and chat", async ({ page, context }) => {
  await quiet(page);
  await page.goto("/index.html");
  await page.waitForFunction(() => navigator.serviceWorker.ready);
  await page.waitForTimeout(800);
  await context.setOffline(true);
  await page.reload();
  await expect(page.locator("main h1")).toBeVisible();
  await page.goto("/rooms/sip-jobs.html");
  await expect(page.locator("main h1")).toContainText(/SIP/);
  await page.locator(".monkey-btn").click();
  await page.locator("#py-chat-input").fill("what is SIP");
  await page.locator(".py-chat-form button[type=submit]").click();
  await expect(page.locator(".py-msg-bot").last()).toContainText(/SIP/);
});

test.describe("short phone", () => {
  test.use({ viewport: { width: 390, height: 430 } });
  test("chat input stays above the dock", async ({ page }) => {
    await quiet(page);
    await page.goto("/index.html");
    await page.locator("[data-open-guide]").click();
    const input = page.locator("#py-chat-input");
    const send = page.locator(".py-chat-form button[type=submit]");
    await expect(input).toBeVisible();
    await expect(send).toBeVisible();
    await expect(page.locator(".phone-bar")).toBeHidden();
    const covered = await page.evaluate(() => {
      function hit(el) {
        const box = el.getBoundingClientRect();
        const x = Math.min(window.innerWidth - 2, Math.max(2, box.left + box.width / 2));
        const y = Math.min(window.innerHeight - 2, Math.max(2, box.top + box.height / 2));
        const top = document.elementFromPoint(x, y);
        const inView = box.top >= 0 && box.bottom <= window.innerHeight && box.left >= 0 && box.right <= window.innerWidth;
        return { inView, covered: !(top === el || el.contains(top)), tag: top ? top.tagName : "" };
      }
      return {
        input: hit(document.querySelector("#py-chat-input")),
        send: hit(document.querySelector(".py-chat-form button[type=submit]")),
      };
    });
    expect(covered.input.inView).toBe(true);
    expect(covered.send.inView).toBe(true);
    expect(covered.input.covered).toBe(false);
    expect(covered.send.covered).toBe(false);
    expect((await input.boundingBox()).width).toBeGreaterThanOrEqual(180);
    await input.fill("what is SIP");
    await send.click();
    await expect(page.locator(".py-msg-bot").last()).toContainText(/SIP/);
    await expect(input).toBeVisible();
    await shot(page, "bot-390x430.png");
  });
});

test("simulator labels itself", async ({ page }) => {
  await quiet(page);
  await page.goto("/play.html");
  await expect(page.locator(".sim-flag")).toContainText(/Simulation/);
  await page.locator("#sim-form button[type=submit]").click();
  await expect(page.locator("#sim-out")).toContainText(/Not run on a network|Simulated/);
  await page.locator(".choice[data-choice=rtp]").click();
  await expect(page.locator(".quiz-note")).toBeVisible();
});
