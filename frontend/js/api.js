(function () {
  "use strict";

  const API_BASE = "/api";

  function apiUrl(path) {
    if (!path.startsWith("/")) path = "/" + path;
    return API_BASE + path;
  }

  function getAccess() {
    return (localStorage.getItem("access") || "").replace(/^Bearer\s+/i, "").trim();
  }

  async function apiFetch(path, options = {}) {
    const headers = new Headers(options.headers || {});
    if (!headers.has("Accept")) headers.set("Accept", "application/json");

    if (options.body && !headers.has("Content-Type")) {
      headers.set("Content-Type", "application/json");
    }

    const token = getAccess();
    if (token && !headers.has("Authorization")) {
      headers.set("Authorization", "Bearer " + token);
    }

    return fetch(apiUrl(path), {
      ...options,
      headers,
      credentials: "include",
    });
  }

  window.apiFetch = apiFetch;
})();