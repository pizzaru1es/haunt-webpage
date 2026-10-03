import assert from 'node:assert/strict';
import test from 'node:test';
import { readFile } from 'node:fs/promises';
const source = await readFile(new URL('../src/worker.js', import.meta.url), 'utf8');
const { default: worker } = await import(`data:text/javascript;base64,${Buffer.from(source).toString('base64')}`);
const calls = [];
const env = { ASSETS: { fetch(request) { calls.push(request); return new Response('asset', {headers: {'Content-Type': 'text/html'}}); } } };
for (const path of ['/tours/kw-old-town-haunts', '/tours/kw-old-town-haunts/', '/tours/unknown-tour?source=messages']) {
  for (const method of ['GET', 'HEAD']) {
    test(`${method} ${path} falls back without caching`, async () => {
      const before = calls.length;
      const result = await worker.fetch(new Request(`https://gethauntapp.com${path}`, {method}), env);
      assert.equal(result.status, 302);
      assert.equal(result.headers.get('Location'), 'https://gethauntapp.com/');
      assert.equal(result.headers.get('Cache-Control'), 'no-store');
      assert.equal(await result.text(), '');
      assert.equal(calls.length, before);
    });
  }
}
test('canonical redirect preserves tour path and query', async () => {
  const result = await worker.fetch(new Request('https://www.gethauntapp.com/tours/kw-old-town-haunts?x=1'), env);
  assert.equal(result.status, 301);
  assert.equal(result.headers.get('Location'), 'https://gethauntapp.com/tours/kw-old-town-haunts?x=1');
});
test('legal redirect remains intact', async () => {
  const result = await worker.fetch(new Request('https://gethauntapp.com/legal/privacy'), env);
  assert.equal(result.status, 302);
  assert.match(result.headers.get('Location'), /^https:\/\/www.termsfeed.com\/live\//);
});
for (const [path, method] of [['/', 'GET'], ['/favicon.svg', 'GET'], ['/other', 'GET'], ['/tours', 'GET'], ['/tours/id/extra', 'GET'], ['/tours/id', 'POST']]) {
  test(`${method} ${path} retains asset handling`, async () => {
    const request = new Request(`https://gethauntapp.com${path}`, {method});
    assert.equal(await (await worker.fetch(request, env)).text(), 'asset');
    assert.equal(calls.at(-1), request);
  });
}
