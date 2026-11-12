// Serves the static tools in ./web under apps.trtmn.io/<app>/.
//
// The asset tree mirrors the URL paths (web/nato/, web/binary/, plus the
// shared style.css and theme.js at the root), so no rewriting is needed:
// an app's bare path just redirects to its trailing-slash form.

const APPS = new Set(["nato", "binary"]);
const SHARED = new Set(["/style.css", "/theme.js"]);

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const firstSegment = url.pathname.split("/")[1];

    // /nato -> /nato/, so relative asset URLs resolve inside the app.
    if (APPS.has(firstSegment) && url.pathname === `/${firstSegment}`) {
      url.pathname = `/${firstSegment}/`;
      return Response.redirect(url.toString(), 308);
    }

    if (APPS.has(firstSegment) || SHARED.has(url.pathname)) {
      return env.ASSETS.fetch(request);
    }

    return new Response("Not found", { status: 404 });
  },
};
