// Exercise the production controller with delayed CPU synthesis, no network/API.
const fs = require('fs');
const vm = require('vm');
const assert = require('assert/strict');
const source = fs.readFileSync('app.py', 'utf8').split('selfhost_script = r"""')[1].split('""".replace')[0].replace(/<\/?script>/g, '');
const flush = () => new Promise(r => setImmediate(r));
async function scenario(subject, fail = false) {
  let resolveSpeech, requests = 0, plays = 0;
  const buttons = ['female', 'thay_tri', 'nam_bo'].map(voice => ({
    dataset: {selfhostVoice: voice}, textContent: voice, style: {}, disabled: false,
    setAttribute() {}, addEventListener(_, fn) { this.click = fn; }
  }));
  const player = {src: 'female.mp3', paused: true, querySelector: () => ({src: 'female.mp3'}),
    addEventListener() {}, pause() { this.paused = true; },
    play() { plays++; this.paused = false; return Promise.resolve(); }};
  const status = {};
  const context = {GSAI_VOICE_CONFIG: {raw: 'Bài hiện tại', subject, endpoint: 'http://voice'},
    location: {hostname: 'localhost'}, document: {getElementById: () => status,
      querySelectorAll: () => buttons, querySelector: () => player},
    URL: {createObjectURL: () => 'blob:male', revokeObjectURL() {}},
    fetch: async url => {
      if (url.endsWith('/health')) return {ok: true, json: async () => ({available_voices: ['thay_tri', 'nam_bo']})};
      requests++; return new Promise(r => {resolveSpeech = r;});
    }, window: {parent: {location: {hostname: 'localhost'}}, addEventListener() {},
      GSAIScienceReader: {VERSION: 'test', prepareText: (raw, lang, actualSubject) => {
        assert.equal(actualSubject, subject); return raw;
      }}}};
  vm.runInNewContext(source, context);
  await flush();
  const first = buttons[1].click();
  const repeated = buttons[1].click();
  assert.equal(requests, 1, 'repeated selection reuses the pending request');
  assert.equal(buttons[0].disabled, false, 'ready female stays selectable');
  await buttons[0].click();
  assert.equal(player.src, 'female.mp3');
  const before = plays;
  resolveSpeech({ok: !fail, blob: async () => ({size: 100})});
  await Promise.all([first, repeated]);
  assert.equal(player.src, 'female.mp3', 'late synthesis cannot replace current voice');
  assert.equal(plays, before, 'late synthesis cannot start overlapping playback');
  assert.equal(buttons[0].disabled, false);
  if (!fail) { await buttons[1].click(); assert.equal(player.src, 'blob:male'); assert.equal(requests, 1); }
}
(async () => {
  for (const subject of ['Toán học', 'Ngữ văn', 'Vật lí', 'Hóa học', 'Sinh học', 'Lịch sử', 'Tin học']) await scenario(subject);
  await scenario('Ngữ văn', true);
  console.log('PASS: 7 subject contexts, delayed response, deduplication, ready-voice switch, stale failure and cache reuse');
})().catch(e => { console.error(e); process.exitCode = 1; });
