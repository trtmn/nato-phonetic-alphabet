// Shared footer links across the tools on apps.trtmn.io.
// To add an app, add an entry here and include this script on its page.
(function () {
  const APPS = [
    { name: "NATO Spelling", href: "/nato/" },
    { name: "Binary Converter", href: "/binary/" },
  ];

  const footer = document.getElementById("app-footer");
  if (!footer) return;

  const label = document.createElement("span");
  label.className = "footer-label";
  label.textContent = "// apps";
  footer.appendChild(label);

  const nav = document.createElement("nav");
  nav.className = "footer-links";
  nav.setAttribute("aria-label", "Apps");

  const here = window.location.pathname.replace(/\/+$/, "") || "/";
  for (const app of APPS) {
    const link = document.createElement("a");
    link.href = app.href;
    link.textContent = app.name;
    if (here === app.href.replace(/\/+$/, "")) {
      link.setAttribute("aria-current", "page");
    }
    nav.appendChild(link);
  }

  footer.appendChild(nav);
})();
