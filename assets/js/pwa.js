/* Install prompt and a short splash. No network. */
(function () {
  var deferred = null;
  window.addEventListener("beforeinstallprompt", function (event) {
    event.preventDefault();
    deferred = event;
  });
  function splash() {
    var dlg = document.getElementById("pwa-splash");
    if (!dlg) {
      dlg = document.createElement("div");
      dlg.id = "pwa-splash";
      dlg.innerHTML = '<div data-pwa-close style="position:fixed;inset:0;background:rgba(4,47,46,.45);z-index:80"></div>' +
        '<section role="dialog" aria-modal="true" aria-labelledby="pwa-title" style="position:fixed;z-index:81;left:16px;right:16px;top:72px;max-width:420px;margin:0 auto;padding:16px;border-radius:16px;background:#f0fdfa;color:#042f2e;border:2px solid #0f766e">' +
        '<h2 id="pwa-title">CPaaS Lab</h2>' +
        '<p>Cypher Monkey, a lifelong student and AI builder, keeps this lab on your device. Add it from the browser menu if the install button stays quiet.</p>' +
        '<p><button type="button" data-pwa-go>Install</button> <button type="button" data-pwa-close>Close</button></p>' +
        '</section>';
      document.body.appendChild(dlg);
      dlg.addEventListener("click", function (event) {
        if (event.target.closest("[data-pwa-close]")) dlg.hidden = true;
        if (event.target.closest("[data-pwa-go]")) {
          if (deferred) {
            deferred.prompt();
            deferred = null;
          }
        }
      });
    }
    dlg.hidden = false;
    var go = dlg.querySelector("[data-pwa-go]");
    if (go) go.focus();
  }
  document.querySelectorAll("[data-pwa-install]").forEach(function (btn) {
    btn.addEventListener("click", splash);
  });
})();
