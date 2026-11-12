// Serves the static page from ./web under apps.trtmn.io/nato/.
//
// Worker routes on a path (apps.trtmn.io/nato*) still hand the Worker the
// full pathname, so strip the mount prefix before asking the ASSETS binding
// for a file. Relative URLs in index.html then resolve under /nato/.

const PREFIX = "/nato";

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // /nato -> /nato/, so relative assets resolve correctly.
    if (url.pathname === PREFIX) {
      url.pathname = `${PREFIX}/`;
      return Response.redirect(url.toString(), 308);
    }

    if (!url.pathname.startsWith(`${PREFIX}/`)) {
      return new Response("Not found", { status: 404 });
    }

    // A request built from the original URL plus the rewritten path, and
    // from the original request so method, headers, and body carry over.
    url.pathname = url.pathname.slice(PREFIX.length);
    return env.ASSETS.fetch(new Request(url, request));
  },
};
