// Compare rebuilt samasama-v2.html against the pre-refactor snapshot, route by route.
const { chromium } = require('playwright');
const fs = require('fs');

const DIR = '/tmp/sevbuild';
const NEW = 'file://' + DIR + '/samasama-v2.html';
const OLD = 'file://' + DIR + '/_site_before.html';

const GUIDE_IDS = JSON.parse(fs.readFileSync(DIR + '/data/guides.json', 'utf8')).map(g => g.id);
const DEST = JSON.parse(fs.readFileSync(DIR + '/data/all_destinations.json', 'utf8'));
const ALL_IDS = Object.keys(DEST);

const ROUTES = ['#/', '#/destinations', '#/guides', '#/where-to-buy', '#/about', '#/contact']
  .concat(ALL_IDS.map(id => '#/city/' + id));

const norm = s => s.replace(/\s+/g, ' ').trim();

async function capture(page, base, route) {
  const errs = [];
  const onErr = e => errs.push('pageerror: ' + String(e));
  const onCon = m => { if (m.type() === 'error' && !/commons|net::|Failed to load resource/.test(m.text())) errs.push('console: ' + m.text()); };
  page.on('pageerror', onErr); page.on('console', onCon);
  await page.goto(base + route, { waitUntil: 'load' });
  await page.waitForTimeout(150);
  const data = await page.evaluate(() => {
    const app = document.querySelector('#app') || document.body;
    return {
      text: app.innerText,
      links: [...document.querySelectorAll('a')].map(a => a.getAttribute('href')),
      deadAnchors: [...document.querySelectorAll('a[href="#"]')].length,
      nested: [...document.querySelectorAll('a a')].length,
      imgs: [...document.querySelectorAll('img')].map(i => ({
        src: i.getAttribute('src') || '', lazy: i.getAttribute('loading') || '',
        srcset: !!i.getAttribute('srcset'), sizes: !!i.getAttribute('sizes'),
        w: i.getAttribute('width'), h: i.getAttribute('height')
      })),
      pictures: [...document.querySelectorAll('picture')].length
    };
  });
  page.off('pageerror', onErr); page.off('console', onCon);
  data.errs = errs;
  return data;
}

(async () => {
  const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
  const pNew = await ctx.newPage(), pOld = await ctx.newPage();
  for (const p of [pNew, pOld]) await p.route('**commons.wikimedia.org**', r => r.abort());

  const problems = [];
  let jsErrors = 0, prevPics = 0, missingFiles = 0, noDim = 0;
  const seenPrevFiles = new Set();

  for (const r of ROUTES) {
    const a = await capture(pOld, OLD, r);
    const b = await capture(pNew, NEW, r);
    if (b.errs.length) { jsErrors += b.errs.length; problems.push(`[JS] ${r}: ${b.errs.slice(0, 2).join(' | ')}`); }
    if (norm(a.text) !== norm(b.text)) {
      const A = norm(a.text), B = norm(b.text);
      let i = 0; while (i < A.length && i < B.length && A[i] === B[i]) i++;
      problems.push(`[TEXT] ${r}\n    old: ...${A.slice(Math.max(0, i - 50), i + 80)}\n    new: ...${B.slice(Math.max(0, i - 50), i + 80)}`);
    }
    if (a.links.join('|') !== b.links.join('|')) {
      const miss = a.links.filter(x => !b.links.includes(x)), extra = b.links.filter(x => !a.links.includes(x));
      if (miss.length || extra.length) problems.push(`[LINKS] ${r} missing=${JSON.stringify(miss.slice(0, 4))} extra=${JSON.stringify(extra.slice(0, 4))}`);
      else problems.push(`[LINKORDER] ${r}`);
    }
    if (b.deadAnchors) problems.push(`[HREF#] ${r}: ${b.deadAnchors}`);
    if (b.nested) problems.push(`[NESTED] ${r}: ${b.nested}`);
    prevPics += b.pictures;
    for (const im of b.imgs) {
      if (im.src.startsWith('img/prev/')) {
        seenPrevFiles.add(im.src);
        if (!fs.existsSync(DIR + '/' + im.src)) { missingFiles++; problems.push(`[IMG404] ${r}: ${im.src}`); }
        if (!im.w || !im.h) { noDim++; problems.push(`[IMGDIM] ${r}: ${im.src}`); }
      }
    }
  }

  // srcset/sizes coverage + source file existence for <picture> sources
  await pNew.goto(NEW + '#/city/' + GUIDE_IDS[0], { waitUntil: 'load' });
  await pNew.waitForTimeout(250);
  const detail = await pNew.evaluate(() => {
    const pics = [...document.querySelectorAll('picture')];
    return {
      pictures: pics.length,
      srcTypes: pics.length ? [...pics[0].querySelectorAll('source')].map(s => s.type) : [],
      srcsets: pics.length ? [...pics[0].querySelectorAll('source')].map(s => s.getAttribute('srcset')) : [],
      totalImgs: document.querySelectorAll('img').length,
      lazy: document.querySelectorAll('img[loading="lazy"]').length,
      eager: [...document.querySelectorAll('img')].filter(i => i.getAttribute('loading') !== 'lazy').map(i => (i.getAttribute('src') || '').slice(0, 70)),
      withSrcset: document.querySelectorAll('img[srcset]').length,
      withSizes: document.querySelectorAll('img[sizes]').length,
      asyncDecode: document.querySelectorAll('img[decoding="async"]').length
    };
  });
  for (const ss of detail.srcsets) for (const part of (ss || '').split(',')) {
    const f = part.trim().split(' ')[0]; if (f && !fs.existsSync(DIR + '/' + f)) problems.push(`[SRC404] ${f}`);
  }

  // mobile overflow, new build
  const mob = await ctx.newPage();
  await mob.route('**commons.wikimedia.org**', r => r.abort());
  await mob.setViewportSize({ width: 390, height: 844 });
  const overflow = [];
  for (const r of ROUTES) {
    await mob.goto(NEW + r, { waitUntil: 'load' });
    await mob.waitForTimeout(110);
    const o = await mob.evaluate(() => ({ s: document.documentElement.scrollWidth, c: document.documentElement.clientWidth }));
    if (o.s > o.c + 1) overflow.push(`${r} (${o.s}>${o.c})`);
  }

  console.log('ROUTES CHECKED: ' + ROUTES.length + '  (6 static + ' + ALL_IDS.length + ' cities, ' + GUIDE_IDS.length + ' of them guides)');
  console.log('JS errors (new build): ' + jsErrors);
  console.log('<picture> previews rendered across all routes: ' + prevPics + '  | distinct prev files referenced: ' + seenPrevFiles.size);
  console.log('missing prev files: ' + missingFiles + ' | previews without width/height: ' + noDim);
  console.log('mobile 390x844 overflow: ' + (overflow.length ? overflow.join(', ') : 'none'));
  console.log('guide-city sample (' + GUIDE_IDS[0] + '): ' + JSON.stringify(detail, null, 1));
  console.log('--- PROBLEMS: ' + problems.length + ' ---');
  problems.slice(0, 50).forEach(p => console.log(p));
  if (problems.length > 50) console.log('... +' + (problems.length - 50) + ' more');
  await browser.close();
})();
