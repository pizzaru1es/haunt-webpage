// Canonical-host enforcer.
// Any request hitting the workers.dev origin is 301'd to the canonical
// gethauntapp.com host, preserving path + querystring. All other hosts
// (gethauntapp.com itself, custom-domain previews) pass through to the
// static-assets binding unchanged.

const CANONICAL_HOST = 'gethauntapp.com';

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.hostname.endsWith('.workers.dev')) {
      url.hostname = CANONICAL_HOST;
      url.port = '';
      return Response.redirect(url.toString(), 301);
    }
    return env.ASSETS.fetch(request);
  },
};
