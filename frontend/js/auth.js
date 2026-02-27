// frontend/js/auth.js
// ✅ Uses apiFetch (so it always hits /api/* via nginx)
// ✅ Provides session helpers + global login() for pages using onclick

(function () {
  "use strict";

  function getUser() {
    const u = localStorage.getItem("user");
    try {
      return u ? JSON.parse(u) : null;
    } catch {
      return null;
    }
  }

  function setSession({ access, refresh, user } = {}) {
    if (access) localStorage.setItem("access", access);
    if (refresh) localStorage.setItem("refresh", refresh);
    if (user) localStorage.setItem("user", JSON.stringify(user));
  }

  function requireAuthOrRedirect() {
    const access = localStorage.getItem("access");
    const user = getUser();
    if (!access || !user) {
      window.location.href = "login.html";
      return null;
    }
    return user;
  }

  function requireRole(role) {
    const user = requireAuthOrRedirect();
    if (!user) return null;

    if ((user.role || "").toUpperCase() !== String(role).toUpperCase()) {
      alert("Access denied: insufficient permissions.");
      window.location.href = "dashboard.html";
      return null;
    }
    return user;
  }

  function logout() {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    localStorage.removeItem("user");
    window.location.href = "login.html";
  }

  // expose helpers
  window.getUser = getUser;
  window.setSession = setSession;
  window.requireAuthOrRedirect = requireAuthOrRedirect;
  window.requireRole = requireRole;
  window.logout = logout;

  // ✅ global login() for pages using onclick="login()"
  window.login = async function () {
    const emailEl = document.getElementById("email");
    const passEl = document.getElementById("password");

    const email = (emailEl?.value || "").trim().toLowerCase();
    const password = passEl?.value || "";

    if (!email || !password) {
      alert("Email र password चाहिन्छ");
      return;
    }

    try {
      // ✅ correct JWT token endpoint (as per your login.html)
      const res = await window.apiFetch("/token/", {
        method: "POST",
        body: JSON.stringify({ email, password }),
      });

      const text = await res.text();
      let data = {};
      try { data = text ? JSON.parse(text) : {}; } catch {}

      if (!res.ok) {
        console.error("Login failed:", res.status, text);
        alert(data.detail || `Login failed (${res.status})`);
        return;
      }

      // Save tokens
      setSession({ access: data.access, refresh: data.refresh });

      // fetch profile
      const meRes = await window.apiFetch("/accounts/me/", { method: "GET" });
      const meText = await meRes.text();
      let me = {};
      try { me = meText ? JSON.parse(meText) : {}; } catch {}

      if (!meRes.ok) {
        alert(me.detail || "Logged in but failed to fetch profile");
        return;
      }

      setSession({ user: me });

      // redirect
      window.location.assign("dashboard.html");
    } catch (err) {
      console.error(err);
      alert("Network error");
    }
  };
})();