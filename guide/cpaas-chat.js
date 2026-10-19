/* Offline study-guide chat. Quotes the lab index. No network model. */
import { createRetriever } from "../shared/pybot-chat/engine.js";
import { chatMarkup, paintChat } from "../shared/pybot-chat/ui.js";

const mount = document.querySelector("[data-cpaas-chat]");
if (mount) {
  const scriptUrl = import.meta.url;
  const base = scriptUrl.slice(0, scriptUrl.indexOf("guide/cpaas-chat.js"));
  const examples = [
    "What is SIP?",
    "What is a webhook?",
    "E.164 numbers",
    "STIR and SHAKEN",
    "What can you help with?",
  ];
  mount.innerHTML = chatMarkup(examples);
  const root = mount.querySelector("[data-py-chat]");
  const messages = [];
  let retriever = null;
  let busy = false;

  function absHref(href) {
    if (!href || /^(https?:|data:|#)/.test(href)) return href || "";
    return base + href.replace(/^\//, "");
  }

  function show() {
    const view = messages.map((msg) => ({
      ...msg,
      href: absHref(msg.href),
      closest: (msg.closest || []).map((hit) => ({ ...hit, href: absHref(hit.href) })),
    }));
    paintChat(root, view, busy);
  }

  function pushBot(answer) {
    messages.push({
      role: "bot",
      text: answer.text,
      href: answer.href || "",
      link: answer.link || "",
      example: answer.example || "",
      follow: answer.follow || "",
      followQ: answer.followQ || "",
      closest: answer.closest || [],
    });
    show();
  }

  async function ask(text) {
    const q = String(text || "").trim();
    if (!q || busy) return;
    messages.push({ role: "user", text: q });
    const field = root.querySelector("#py-chat-input");
    if (field) field.value = "";
    if (!retriever) {
      pushBot({ text: "I don't have that yet. The offline index has not loaded.", href: "" });
      return;
    }
    busy = true;
    show();
    const answer = retriever.ask(q, {});
    busy = false;
    pushBot(answer);
  }

  root.addEventListener("submit", (event) => {
    event.preventDefault();
    const field = root.querySelector("#py-chat-input");
    ask(field && field.value);
  });
  root.addEventListener("click", (event) => {
    const chip = event.target.closest("[data-py-ask]");
    if (chip) {
      ask(chip.getAttribute("data-py-ask"));
      return;
    }
    if (event.target.closest("[data-py-clear]")) {
      messages.length = 0;
      show();
      return;
    }
    const read = event.target.closest("[data-py-read]");
    if (read && window.speechSynthesis) {
      const index = Number(read.getAttribute("data-py-read"));
      const msg = messages[index];
      if (msg && msg.text) {
        window.speechSynthesis.cancel();
        window.speechSynthesis.speak(new SpeechSynthesisUtterance(msg.text));
      }
    }
  });
  const mic = root.querySelector("[data-py-mic]");
  const Rec = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (mic) {
    mic.addEventListener("click", () => {
      if (!Rec) {
        pushBot({ text: "This browser has no speech recognition. Type the question instead.", href: "" });
        const field = root.querySelector("#py-chat-input");
        if (field) field.focus();
        return;
      }
      const rec = new Rec();
      rec.lang = "en-US";
      rec.onresult = (event) => ask(event.results[0][0].transcript);
      rec.onerror = () => pushBot({ text: "I could not hear that. Type the question instead.", href: "" });
      try { rec.start(); } catch (err) {
        pushBot({ text: "The mic did not start. Type the question instead.", href: "" });
      }
    });
  }

  show();
  fetch(new URL("assets/data/cpaasbot-index.json", base))
    .then((res) => (res.ok ? res.json() : null))
    .then((index) => {
      if (!index) return;
      retriever = createRetriever(index);
    })
    .catch(() => { retriever = null; });
}
