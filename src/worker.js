// Canonical-host enforcer.
// Any request hitting HTTP, www, or the workers.dev origin is 301'd to the
// canonical HTTPS gethauntapp.com host, preserving path + querystring. All
// other hosts (gethauntapp.com itself, custom-domain previews) pass through to
// the static-assets binding unchanged.

const CANONICAL_HOST = 'gethauntapp.com';

const LEGAL_REDIRECTS = {
  '/legal/privacy': 'https://www.termsfeed.com/live/8583a3c4-b482-42ff-8fbc-4fc74843dece',
  '/legal/terms':   'https://www.termsfeed.com/live/3565d48d-9378-4633-a34c-45940a664cc4',
  '/legal':         '/legal/privacy',
};

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (
      url.protocol !== 'https:' ||
      url.hostname === `www.${CANONICAL_HOST}` ||
      url.hostname.endsWith('.workers.dev')
    ) {
      url.protocol = 'https:';
      url.hostname = CANONICAL_HOST;
      url.port = '';
      return Response.redirect(url.toString(), 301);
    }

    const path = url.pathname.replace(/\/$/, '') || '/';
    if (path in LEGAL_REDIRECTS) {
      const target = LEGAL_REDIRECTS[path];
      const dest = target.startsWith('/') ? new URL(target, url).toString() : target;
      return Response.redirect(dest, 302);
    }

    return env.ASSETS.fetch(request);
  },
};
