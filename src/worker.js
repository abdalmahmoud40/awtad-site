// أوتاد النخبة — Worker: الوظائف، طلبات التوظيف، لوحة الإدارة، الصور والألوان
// الملفات الثابتة في ./public تُخدم مباشرة، وهذا الملف يعمل فقط على المسارات المذكورة في run_worker_first.

const DOMAIN = 'https://awtad-trade.com';
const ORG_AR = 'شركة أوتاد النخبة للتجارة المحدودة';
const ORG_EN = 'Awtad Alnokhbah Trading Co. Ltd';
const MAX_CV = 5 * 1024 * 1024;
const MAX_IMG = 8 * 1024 * 1024;
const THEME_KEYS = ['--olive', '--olive-2', '--moss', '--green', '--green-2', '--sand', '--wheat'];
const JOB_TYPES = {
  FULL_TIME: ['دوام كامل', 'Full-time'], PART_TIME: ['دوام جزئي', 'Part-time'],
  CONTRACTOR: ['عقد مؤقت', 'Contract'], INTERN: ['تدريب', 'Internship'], TEMPORARY: ['عمل موسمي', 'Seasonal'],
};
const EXP = {
  '0-1': ['أقل من سنة', 'Less than 1 year'], '1-3': ['1 إلى 3 سنوات', '1 to 3 years'],
  '3-5': ['3 إلى 5 سنوات', '3 to 5 years'], '5-10': ['5 إلى 10 سنوات', '5 to 10 years'], '10+': ['أكثر من 10 سنوات', 'More than 10 years'],
};

// ذاكرة مؤقتة داخل الـ isolate لتقليل قراءات KV
const mem = { idx: null, idxAt: 0, theme: null, themeAt: 0, jobs: null, jobsAt: 0 };
const TTL = 30000;

const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const lines = (s) => String(s || '').split(/\r?\n/).map((x) => x.trim().replace(/^[-•*]\s*/, '')).filter(Boolean);
const today = () => new Date(Date.now() + 3 * 3600e3).toISOString().slice(0, 10); // توقيت السودان/الرياض تقريباً
const SEC = {
  'X-Content-Type-Options': 'nosniff', 'X-Frame-Options': 'DENY', 'Referrer-Policy': 'strict-origin-when-cross-origin',
  'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
};
const json = (data, status = 200, extra = {}) => new Response(JSON.stringify(data), { status, headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', ...SEC, ...extra } });
const html = (body, status = 200, extra = {}) => new Response(body, { status, headers: { 'Content-Type': 'text/html; charset=utf-8', ...SEC, ...extra } });

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    let p = url.pathname;
    try {
      if (p.length > 1 && p.endsWith('/') && (p.startsWith('/careers') || p.startsWith('/en/careers'))) {
        return Response.redirect(url.origin + p.slice(0, -1) + url.search, 301);
      }
      if (p === '/careers-shell' || p === '/en/careers-shell' || p.endsWith('careers-shell.html')) return notFound(env, url);
      if (p.startsWith('/assets/img/')) return serveImage(request, env, url);
      if (p === '/assets/style.css') return serveCss(request, env, url);
      if (p === '/sitemap.xml') return serveSitemap(env, url);
      if (p === '/api/apply' && request.method === 'POST') return apply(request, env, ctx, url);
      if (p === '/api/site' && request.method === 'GET') return json({ ok: true, social: await getSocial(env) }, 200, { 'Cache-Control': 'public, max-age=300' });
      if (p.startsWith('/api/admin/')) return admin(request, env, url);
      const m = p.match(/^\/(en\/)?careers(?:\/([a-z0-9-]{1,40}))?$/);
      if (m) return careers(env, url, m[1] ? 'en' : 'ar', m[2]);
      return env.ASSETS.fetch(request);
    } catch (e) {
      console.error(e);
      if (p.startsWith('/api/')) return json({ ok: false, error: 'server' }, 500);
      return env.ASSETS.fetch(request);
    }
  },
};

/* ---------------- مساعدات البيانات ---------------- */
async function getJobs(env, fresh = false) {
  if (!fresh && mem.jobs && Date.now() - mem.jobsAt < TTL) return mem.jobs;
  mem.jobs = (await env.KV.get('jobs', { type: 'json' })) || [];
  mem.jobsAt = Date.now();
  return mem.jobs;
}
async function saveJobs(env, jobs) { await env.KV.put('jobs', JSON.stringify(jobs)); mem.jobs = jobs; mem.jobsAt = Date.now(); }
const SOCIAL = { facebook: /(^|\.)facebook\.com$|(^|\.)fb\.com$/, instagram: /(^|\.)instagram\.com$/, x: /(^|\.)(x|twitter)\.com$/, tiktok: /(^|\.)tiktok\.com$/, linkedin: /(^|\.)linkedin\.com$/ };
async function getSocial(env) {
  if (mem.social && Date.now() - mem.socialAt < TTL) return mem.social;
  mem.social = (await env.KV.get('social', { type: 'json' })) || {}; mem.socialAt = Date.now();
  return mem.social;
}
async function getIdx(env) {
  if (mem.idx && Date.now() - mem.idxAt < TTL) return mem.idx;
  mem.idx = (await env.KV.get('imgidx', { type: 'json' })) || {}; mem.idxAt = Date.now();
  return mem.idx;
}
async function getTheme(env) {
  if (mem.theme && Date.now() - mem.themeAt < TTL) return mem.theme;
  mem.theme = (await env.KV.get('theme', { type: 'json' })) || {}; mem.themeAt = Date.now();
  return mem.theme;
}
const isOpen = (j) => j.status === 'open' && (!j.deadline || j.deadline >= today());
const pick = (j, f, lang) => (lang === 'en' ? (j[f + '_en'] || j[f + '_ar']) : (j[f + '_ar'] || j[f + '_en'])) || '';
const asset = (env, url, path) => env.ASSETS.fetch(new Request(new URL(path, url.origin)));

async function notFound(env, url) {
  const r = await asset(env, url, '/404.html');
  return html(await r.text(), 404);
}

/* ---------------- الصور والألوان وخريطة الموقع ---------------- */
async function serveImage(request, env, url) {
  const name = decodeURIComponent(url.pathname.slice('/assets/img/'.length));
  const idx = await getIdx(env);
  if (idx[name]) {
    const { value, metadata } = await env.KV.getWithMetadata('img:' + name, { type: 'arrayBuffer', cacheTtl: 300 });
    if (value) {
      return new Response(value, { headers: { 'Content-Type': (metadata && metadata.type) || 'image/webp', 'Cache-Control': 'public, max-age=600', 'X-Content-Type-Options': 'nosniff' } });
    }
  }
  const r = await env.ASSETS.fetch(request);
  const h = new Headers(r.headers); h.set('Cache-Control', 'public, max-age=600');
  return new Response(r.body, { status: r.status, headers: h });
}

async function serveCss(request, env) {
  const r = await env.ASSETS.fetch(request);
  if (!r.ok) return r;
  const theme = await getTheme(env);
  let css = await r.text();
  const vars = THEME_KEYS.filter((k) => /^#[0-9a-fA-F]{6}$/.test(theme[k] || '')).map((k) => `${k}:${theme[k]}`);
  if (vars.length) css += `\n/* ألوان لوحة الإدارة */\n:root{${vars.join(';')}}\n`;
  return new Response(css, { headers: { 'Content-Type': 'text/css; charset=utf-8', 'Cache-Control': 'public, max-age=600' } });
}

async function serveSitemap(env, url) {
  const r = await asset(env, url, '/sitemap.xml');
  let xml = await r.text();
  const jobs = (await getJobs(env)).filter(isOpen);
  const d = today();
  let add = `<url><loc>${DOMAIN}/careers</loc><lastmod>${d}</lastmod><xhtml:link rel="alternate" hreflang="ar" href="${DOMAIN}/careers"/><xhtml:link rel="alternate" hreflang="en" href="${DOMAIN}/en/careers"/></url>`
    + `<url><loc>${DOMAIN}/en/careers</loc><lastmod>${d}</lastmod><xhtml:link rel="alternate" hreflang="ar" href="${DOMAIN}/careers"/><xhtml:link rel="alternate" hreflang="en" href="${DOMAIN}/en/careers"/></url>`;
  for (const j of jobs) {
    add += `<url><loc>${DOMAIN}/careers/${j.id}</loc><lastmod>${(j.updated || j.posted || d).slice(0, 10)}</lastmod></url>`;
    if (j.title_en) add += `<url><loc>${DOMAIN}/en/careers/${j.id}</loc><lastmod>${(j.updated || j.posted || d).slice(0, 10)}</lastmod></url>`;
  }
  xml = xml.replace('</urlset>', add + '</urlset>');
  return new Response(xml, { headers: { 'Content-Type': 'application/xml; charset=utf-8', 'Cache-Control': 'public, max-age=600' } });
}

/* ---------------- صفحات الوظائف ---------------- */
const L = (lang) => (lang === 'en' ? {
  careers: 'Careers', open: 'Open positions', openH: 'Current vacancies', none: 'There are no open vacancies right now.',
  noneP: 'You can still send us your CV through a general application and we will contact you when a suitable role opens.',
  general: 'General application', generalP: 'Didn’t find a suitable role? Send your CV and we will keep it on file.',
  details: 'View and apply', deadline: 'Apply by', dept: 'Department', loc: 'Location', type: 'Employment type', exp: 'Experience',
  posted: 'Posted', all: 'All', summary: 'About the role', resp: 'Responsibilities', req: 'Requirements', ben: 'What we offer',
  apply: 'Apply for this job', applyNow: 'Apply now', closed: 'Applications for this position are closed.', back: 'All vacancies',
  share: 'Share this job', copy: 'Copy link', copied: 'Link copied', listT: 'Careers | Awtad Alnokhbah Trading',
  listD: 'Current job vacancies at Awtad Alnokhbah Trading Co. Ltd in Sudan. Apply online and upload your CV.',
  sub: 'Join a Sudanese company working in livestock and agricultural production.',
  process: 'How we hire', processH: 'Our hiring steps',
  steps: [['Apply online', 'Fill in the form and upload your CV.'], ['Application review', 'Our HR team reviews every application.'], ['Interview', 'We invite shortlisted candidates to an interview.'], ['Job offer', 'The selected candidate receives a written offer.']],
  generalTitle: 'General application', generalSub: 'Send your CV for future opportunities at Awtad Alnokhbah.',
} : {
  careers: 'الوظائف', open: 'الوظائف الشاغرة', openH: 'فرص العمل المتاحة', none: 'لا توجد وظائف شاغرة حالياً.',
  noneP: 'يمكنك إرسال سيرتك الذاتية عبر طلب التوظيف العام، وسنتواصل معك عند توفر وظيفة مناسبة.',
  general: 'طلب توظيف عام', generalP: 'لم تجد وظيفة مناسبة؟ أرسل سيرتك الذاتية وسنحتفظ بها للفرص القادمة.',
  details: 'التفاصيل والتقديم', deadline: 'آخر موعد للتقديم', dept: 'القسم', loc: 'مكان العمل', type: 'نوع الدوام', exp: 'الخبرة المطلوبة',
  posted: 'تاريخ النشر', all: 'الكل', summary: 'عن الوظيفة', resp: 'المهام والمسؤوليات', req: 'المتطلبات والمؤهلات', ben: 'المزايا',
  apply: 'التقديم على الوظيفة', applyNow: 'قدّم الآن', closed: 'انتهى التقديم على هذه الوظيفة.', back: 'كل الوظائف',
  share: 'شارك الوظيفة', copy: 'نسخ الرابط', copied: 'تم نسخ الرابط', listT: 'الوظائف | أوتاد النخبة للتجارة',
  listD: 'الوظائف الشاغرة في شركة أوتاد النخبة للتجارة المحدودة في السودان. قدّم إلكترونياً وأرفق سيرتك الذاتية.',
  sub: 'انضم إلى شركة سودانية تعمل في الإنتاج الحيواني والزراعي.',
  process: 'كيف نوظّف', processH: 'مراحل التوظيف',
  steps: [['التقديم الإلكتروني', 'املأ النموذج وأرفق سيرتك الذاتية.'], ['مراجعة الطلب', 'يراجع فريق الموارد البشرية كل طلب.'], ['المقابلة', 'ندعو المرشحين المناسبين لمقابلة.'], ['العرض الوظيفي', 'يتلقى المرشح المختار عرضاً مكتوباً.']],
  generalTitle: 'طلب توظيف عام', generalSub: 'أرسل سيرتك الذاتية للفرص القادمة في أوتاد النخبة.',
});

const SLAB = '<span class="slab" aria-hidden="true"><i></i><i></i></span>';
const base = (lang) => (lang === 'en' ? '/en/careers' : '/careers');

async function shell(env, url, lang) {
  const r = await asset(env, url, lang === 'en' ? '/en/careers-shell.html' : '/careers-shell.html');
  return r.text();
}

function fill(sh, o) {
  let s = sh.split('__T__').join(esc(o.title)).split('__D__').join(esc(o.desc))
    .split('__H__').join(esc(o.h)).split('__S__').join(esc(o.sub)).split('__C__').join(o.crumb)
    .replace('<!--CAREERS-->', o.body);
  if (o.path) {
    s = s.split(`"${DOMAIN}/careers"`).join(`"${DOMAIN}/careers${o.path}"`).split(`"${DOMAIN}/en/careers"`).join(`"${DOMAIN}/en/careers${o.path}"`)
      .replace(/class="lang" href="\/(en\/)?careers"/, (m, en) => `class="lang" href="/${en || ''}careers${o.path}"`);
  }
  if (o.noindex) s = s.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex">');
  if (o.ld) s = s.replace('</head>', `<script type="application/ld+json">${JSON.stringify(o.ld).replace(/</g, '\\u003c')}</script>\n</head>`);
  return s;
}

function fmtDate(d, lang) {
  if (!d) return '';
  try { return new Date(d + 'T12:00:00Z').toLocaleDateString(lang === 'en' ? 'en-GB' : 'ar-EG-u-nu-latn', { day: 'numeric', month: 'long', year: 'numeric' }); } catch { return d; }
}

async function careers(env, url, lang, id) {
  const t = L(lang); const sh = await shell(env, url, lang);
  const jobs = await getJobs(env);
  const H = { 'Cache-Control': 'public, max-age=60' };
  if (!id) {
    const open = jobs.filter(isOpen).filter((j) => lang === 'ar' || j.title_en);
    const depts = [...new Set(open.map((j) => pick(j, 'dept', lang)).filter(Boolean))];
    const chips = depts.length > 1 ? `<div class="chips jchips" role="group" aria-label="${esc(t.dept)}"><button type="button" data-d="" aria-pressed="true">${t.all}</button>${depts.map((d) => `<button type="button" data-d="${esc(d)}" aria-pressed="false">${esc(d)}</button>`).join('')}</div>` : '';
    const cards = open.map((j) => `<article class="job" data-d="${esc(pick(j, 'dept', lang))}">
<div class="job-tags">${pick(j, 'dept', lang) ? `<span>${esc(pick(j, 'dept', lang))}</span>` : ''}<span>${esc((JOB_TYPES[j.type] || JOB_TYPES.FULL_TIME)[lang === 'en' ? 1 : 0])}</span></div>
<h3><a href="${base(lang)}/${j.id}">${esc(pick(j, 'title', lang))}</a></h3>
<p class="job-loc">${esc(pick(j, 'location', lang))}</p>
${pick(j, 'summary', lang) ? `<p class="job-sum">${esc(pick(j, 'summary', lang).slice(0, 180))}${pick(j, 'summary', lang).length > 180 ? '…' : ''}</p>` : ''}
<div class="job-foot">${j.deadline ? `<span>${t.deadline}: <b>${esc(fmtDate(j.deadline, lang))}</b></span>` : '<span></span>'}<a class="btn btn-green" href="${base(lang)}/${j.id}">${t.details}</a></div>
</article>`).join('');
    const sent = url.searchParams.get('sent') === '1'; const err = url.searchParams.get('error');
    const notice = sent ? `<div class="job-notice ok" role="status">${lang === 'en' ? 'Thank you. Your application has been received.' : 'شكراً لك، تم استلام طلبك بنجاح.'}</div>`
      : err ? `<div class="job-notice bad" role="alert">${lang === 'en' ? 'Your application could not be sent. Check the required fields and that the CV is a PDF or Word file under 5 MB, then try again.' : 'لم يُرسل طلبك. تأكد من تعبئة الحقول المطلوبة وأن السيرة الذاتية بصيغة PDF أو Word وحجمها أقل من 5 ميغابايت، ثم أعد المحاولة.'}</div>` : '';
    const body = `<section class="blk sand"><div class="wrap">${notice}
<div class="sec-head"><span class="eyebrow">${SLAB}${t.open}</span><h2>${t.openH}</h2></div>
${chips}
${open.length ? `<div class="jobs">${cards}</div>` : `<div class="job-empty"><h3>${t.none}</h3><p>${t.noneP}</p></div>`}
<div class="job-general"><div><h3>${t.general}</h3><p>${t.generalP}</p></div><a class="btn btn-olive" href="${base(lang)}/general">${t.applyNow}</a></div>
</div></section>
<section class="blk"><div class="wrap">
<div class="sec-head"><span class="eyebrow">${SLAB}${t.process}</span><h2>${t.processH}</h2></div>
<ol class="hire-steps">${t.steps.map(([h, d]) => `<li><h3>${h}</h3><p>${d}</p></li>`).join('')}</ol>
</div></section>`;
    return html(fill(sh, { title: t.listT, desc: t.listD, h: t.careers, sub: t.sub, crumb: esc(t.careers), body }), 200, H);
  }

  const crumbBase = `<a href="${base(lang)}">${t.careers}</a> / `;
  if (id === 'general') {
    const body = `<section class="blk sand"><div class="wrap job-narrow">${applyForm(lang, { id: 'general', title_ar: t.generalTitle, title_en: t.generalTitle }, t)}</div></section>`;
    return html(fill(sh, { title: `${t.generalTitle} | ${lang === 'en' ? 'Awtad Alnokhbah' : 'أوتاد النخبة'}`, desc: t.generalSub, h: t.generalTitle, sub: t.generalSub, crumb: crumbBase + esc(t.generalTitle), body, path: '/general' }), 200, H);
  }
  const j = jobs.find((x) => x.id === id && x.status !== 'draft');
  if (!j || (lang === 'en' && !j.title_en)) return notFound(env, url);
  const open = isOpen(j);
  const title = pick(j, 'title', lang);
  const typ = (JOB_TYPES[j.type] || JOB_TYPES.FULL_TIME)[lang === 'en' ? 1 : 0];
  const list = (arr) => `<ul class="checks one">${arr.map((x) => `<li>${esc(x)}</li>`).join('')}</ul>`;
  const resp = lines(pick(j, 'resp', lang)); const req = lines(pick(j, 'req', lang)); const ben = lines(pick(j, 'ben', lang));
  const summary = pick(j, 'summary', lang);
  const pageUrl = `${DOMAIN}${base(lang)}/${j.id}`;
  const shareTxt = encodeURIComponent(`${title} - ${lang === 'en' ? ORG_EN : ORG_AR}\n${pageUrl}`);
  const facts = [[t.dept, pick(j, 'dept', lang)], [t.loc, pick(j, 'location', lang)], [t.type, typ], [t.exp, EXP[j.exp] ? EXP[j.exp][lang === 'en' ? 1 : 0] : ''], [t.posted, fmtDate((j.posted || '').slice(0, 10), lang)], [t.deadline, fmtDate(j.deadline, lang)]].filter((x) => x[1]);
  const body = `<section class="blk"><div class="wrap job-grid">
<article class="job-body">
${summary ? `<h2>${t.summary}</h2>${summary.split(/\n{2,}/).map((p) => `<p>${esc(p).replace(/\n/g, '<br>')}</p>`).join('')}` : ''}
${resp.length ? `<h2>${t.resp}</h2>${list(resp)}` : ''}
${req.length ? `<h2>${t.req}</h2>${list(req)}` : ''}
${ben.length ? `<h2>${t.ben}</h2>${list(ben)}` : ''}
</article>
<aside class="job-side">
<dl>${facts.map(([k, v]) => `<dt>${k}</dt><dd>${esc(v)}</dd>`).join('')}</dl>
${open ? `<a class="btn btn-green" href="#apply">${t.applyNow}</a>` : `<p class="job-closed">${t.closed}</p>`}
<div class="job-share"><span>${t.share}</span>
<a href="https://wa.me/?text=${shareTxt}" target="_blank" rel="noopener">WhatsApp</a>
<a href="https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(pageUrl)}" target="_blank" rel="noopener">LinkedIn</a>
<button type="button" class="copy-link" data-url="${esc(pageUrl)}" data-done="${t.copied}">${t.copy}</button></div>
<a class="job-back" href="${base(lang)}">${t.back}</a>
</aside>
</div></section>
${open ? `<section class="blk sand" id="apply"><div class="wrap job-narrow">${applyForm(lang, j, t)}</div></section>` : ''}`;
  const descHtml = [summary && `<p>${esc(summary)}</p>`, resp.length && `<h3>${t.resp}</h3>${list(resp)}`, req.length && `<h3>${t.req}</h3>${list(req)}`, ben.length && `<h3>${t.ben}</h3>${list(ben)}`].filter(Boolean).join('');
  const ld = open ? {
    '@context': 'https://schema.org', '@type': 'JobPosting', title, description: descHtml || esc(title),
    identifier: { '@type': 'PropertyValue', name: lang === 'en' ? ORG_EN : ORG_AR, value: j.id },
    datePosted: (j.posted || today()).slice(0, 10), ...(j.deadline ? { validThrough: `${j.deadline}T23:59:59+03:00` } : {}),
    employmentType: j.type || 'FULL_TIME', directApply: true,
    hiringOrganization: { '@type': 'Organization', name: lang === 'en' ? ORG_EN : ORG_AR, sameAs: DOMAIN, logo: `${DOMAIN}/assets/img/logo.png` },
    jobLocation: { '@type': 'Place', address: { '@type': 'PostalAddress', addressLocality: pick(j, 'location', lang) || (lang === 'en' ? 'Wad Madani' : 'ود مدني'), addressCountry: 'SD' } },
  } : null;
  const metaDesc = (summary || `${title} - ${pick(j, 'location', lang)}`).replace(/\s+/g, ' ').slice(0, 155);
  return html(fill(sh, { title: `${title} | ${t.careers} | ${lang === 'en' ? 'Awtad Alnokhbah' : 'أوتاد النخبة'}`, desc: metaDesc, h: title, sub: [pick(j, 'dept', lang), pick(j, 'location', lang), typ].filter(Boolean).join(' · '), crumb: crumbBase + esc(title), body, path: '/' + j.id, ld, noindex: !open }), 200, H);
}

function applyForm(lang, j, t) {
  const a = lang !== 'en';
  const exp = Object.entries(EXP).map(([k, v]) => `<option value="${k}">${v[a ? 0 : 1]}</option>`).join('');
  return `<form class="wa formcard apply-form" id="applyForm" action="/api/apply" method="post" enctype="multipart/form-data">
<h2>${t.apply}: ${esc(pick(j, 'title', lang))}</h2>
<input type="hidden" name="job" value="${esc(j.id)}"><input type="hidden" name="lang" value="${lang}">
<div class="hp" aria-hidden="true"><label>Website<input name="website" tabindex="-1" autocomplete="off"></label></div>
<div class="row2">
<div class="f"><label for="an">${a ? 'الاسم الكامل' : 'Full name'} *</label><input id="an" name="name" required maxlength="120" autocomplete="name"></div>
<div class="f"><label for="ae">${a ? 'البريد الإلكتروني' : 'Email'} *</label><input id="ae" name="email" type="email" required maxlength="160" autocomplete="email" dir="ltr"></div>
</div>
<div class="row2">
<div class="f"><label for="ap">${a ? 'رقم الهاتف أو واتساب' : 'Phone or WhatsApp'} *</label><input id="ap" name="phone" type="tel" required maxlength="40" autocomplete="tel" dir="ltr"></div>
<div class="f"><label for="ac">${a ? 'المدينة / الولاية' : 'City / state'} *</label><input id="ac" name="city" required maxlength="80"></div>
</div>
<div class="row2">
<div class="f"><label for="ax">${a ? 'سنوات الخبرة' : 'Years of experience'} *</label><select id="ax" name="experience" required><option value="">${a ? 'اختر' : 'Select'}</option>${exp}</select></div>
<div class="f"><label for="aj">${a ? 'الوظيفة الحالية (اختياري)' : 'Current job title (optional)'}</label><input id="aj" name="current" maxlength="120"></div>
</div>
<div class="f"><label for="al">${a ? 'رابط LinkedIn (اختياري)' : 'LinkedIn profile (optional)'}</label><input id="al" name="linkedin" type="url" maxlength="200" dir="ltr" placeholder="https://www.linkedin.com/in/..."></div>
<div class="f"><label for="acv">${a ? 'السيرة الذاتية' : 'CV / résumé'} *</label>
<label class="drop" for="acv"><input id="acv" name="cv" type="file" required accept=".pdf,.doc,.docx,application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document">
<span class="drop-t">${a ? 'اضغط لاختيار الملف أو اسحبه هنا' : 'Click to choose a file or drag it here'}</span><span class="drop-h">PDF, DOC, DOCX · ${a ? 'الحد الأقصى 5 ميغابايت' : 'max 5 MB'}</span><span class="drop-f" id="acvName"></span></label></div>
<div class="f"><label for="am">${a ? 'رسالة تعريفية (اختياري)' : 'Cover letter (optional)'}</label><textarea id="am" name="cover" rows="5" maxlength="3000"></textarea></div>
<label class="consent"><input type="checkbox" name="consent" value="1" required> ${a ? 'أوافق على أن تحتفظ أوتاد النخبة ببياناتي وسيرتي الذاتية لأغراض التوظيف فقط.' : 'I agree that Awtad Alnokhbah may keep my details and CV for recruitment purposes only.'}</label>
<div class="err" id="applyErr" role="alert"></div>
<button class="btn btn-green" type="submit" id="applyBtn">${a ? 'إرسال الطلب' : 'Submit application'}</button>
<div class="apply-ok" id="applyOk" hidden><h3>${a ? 'تم استلام طلبك' : 'Application received'}</h3><p>${a ? 'شكراً لاهتمامك بالعمل في أوتاد النخبة. سيراجع فريق الموارد البشرية طلبك ويتواصل معك إذا كان ملفك مناسباً.' : 'Thank you for your interest in Awtad Alnokhbah. Our HR team will review your application and contact you if your profile is a match.'}</p></div>
</form>`;
}

/* ---------------- استقبال طلبات التوظيف ---------------- */
function sniff(buf) {
  const b = new Uint8Array(buf.slice(0, 8));
  if (b[0] === 0x25 && b[1] === 0x50 && b[2] === 0x44 && b[3] === 0x46) return ['application/pdf', 'pdf'];
  if (b[0] === 0x50 && b[1] === 0x4b) return ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'docx'];
  if (b[0] === 0xd0 && b[1] === 0xcf && b[2] === 0x11 && b[3] === 0xe0) return ['application/msword', 'doc'];
  return null;
}
function b64(buf) {
  const bytes = new Uint8Array(buf); let s = '';
  for (let i = 0; i < bytes.length; i += 0x8000) s += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
  return btoa(s);
}

async function apply(request, env, ctx, url) {
  const wantsJson = (request.headers.get('Accept') || '').includes('application/json');
  const fail = (code, status = 400) => wantsJson ? json({ ok: false, error: code }, status) : Response.redirect(url.origin + '/careers?error=' + code, 303);
  const len = +request.headers.get('Content-Length') || 0;
  if (len > MAX_CV + 200000) return fail('size', 413);
  const ip = request.headers.get('CF-Connecting-IP') || 'x';
  const rlKey = 'rl:apply:' + ip; const n = +(await env.KV.get(rlKey)) || 0;
  if (n >= 6) return fail('rate', 429);

  const fd = await request.formData();
  const g = (k, max = 200) => String(fd.get(k) || '').trim().slice(0, max);
  if (g('website')) return wantsJson ? json({ ok: true }) : Response.redirect(url.origin + '/careers', 303); // فخ للبرامج الآلية
  const lang = g('lang') === 'en' ? 'en' : 'ar';
  const d = { name: g('name', 120), email: g('email', 160), phone: g('phone', 40), city: g('city', 80), experience: g('experience', 10), current: g('current', 120), linkedin: g('linkedin', 200), cover: g('cover', 3000), jobId: g('job', 40) };
  if (!d.name || !d.phone || !d.city || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(d.email) || !fd.get('consent')) return fail('fields');
  if (d.linkedin && !/^https?:\/\//i.test(d.linkedin)) d.linkedin = '';
  const file = fd.get('cv');
  if (!file || typeof file === 'string' || !file.size) return fail('cv');
  if (file.size > MAX_CV) return fail('size', 413);
  const buf = await file.arrayBuffer();
  const kind = sniff(buf);
  if (!kind) return fail('type');

  const jobs = await getJobs(env);
  const job = jobs.find((x) => x.id === d.jobId);
  if (d.jobId !== 'general' && (!job || !isOpen(job))) return fail('closed');
  d.jobTitle = job ? (job.title_ar || job.title_en) : 'طلب توظيف عام';
  d.created = new Date().toISOString(); d.status = 'new'; d.lang = lang;
  const id = String(9999999999999 - Date.now()).padStart(13, '0') + '-' + Math.random().toString(36).slice(2, 7);
  const safeName = d.name.replace(/[^\p{L}\p{N} _-]/gu, '').replace(/\s+/g, '_').slice(0, 50) || 'cv';
  d.cvName = `CV_${safeName}.${kind[1]}`; d.cvType = kind[0]; d.cvSize = file.size; d.id = id;

  await env.KV.put('cv:' + id, buf, { metadata: { type: kind[0], name: d.cvName } });
  await env.KV.put('app:' + id, JSON.stringify(d), { metadata: meta(d) });
  ctx.waitUntil(env.KV.put(rlKey, String(n + 1), { expirationTtl: 3600 }));
  ctx.waitUntil(notify(env, d, buf));
  return wantsJson ? json({ ok: true }) : Response.redirect(url.origin + (lang === 'en' ? '/en/careers' : '/careers') + '?sent=1', 303);
}

const meta = (d) => ({ n: d.name.slice(0, 60), e: d.email.slice(0, 80), p: d.phone.slice(0, 30), c: d.city.slice(0, 40), j: d.jobTitle.slice(0, 80), jid: d.jobId, x: d.experience, s: d.status, t: d.created });

async function sendMail(env, payload) {
  if (!env.RESEND_API_KEY) return;
  const r = await fetch('https://api.resend.com/emails', { method: 'POST', headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
  if (!r.ok) console.error('resend', r.status, await r.text());
}

async function notify(env, d, buf) {
  const from = env.MAIL_FROM || 'Awtad Careers <careers@awtad-trade.com>';
  const hr = env.HR_EMAIL || 'hr@awtad-trade.com';
  const row = (k, v) => v ? `<tr><td style="padding:6px 10px;color:#5B6152;white-space:nowrap">${k}</td><td style="padding:6px 10px;color:#1D2116">${esc(v)}</td></tr>` : '';
  const body = `<div dir="rtl" style="font-family:Arial,Tahoma,sans-serif;font-size:14px">
<h2 style="color:#363D1C;margin:0 0 10px">طلب توظيف جديد: ${esc(d.jobTitle)}</h2>
<table style="border-collapse:collapse;background:#F5F1E6;border-radius:6px">${row('الاسم', d.name)}${row('البريد', d.email)}${row('الهاتف', d.phone)}${row('المدينة', d.city)}${row('الخبرة', EXP[d.experience] ? EXP[d.experience][0] : d.experience)}${row('الوظيفة الحالية', d.current)}${row('LinkedIn', d.linkedin)}</table>
${d.cover ? `<h3 style="color:#363D1C">الرسالة التعريفية</h3><p style="white-space:pre-wrap">${esc(d.cover)}</p>` : ''}
<p style="color:#5B6152">السيرة الذاتية مرفقة، والطلب محفوظ في لوحة الإدارة: <a href="${DOMAIN}/admin">${DOMAIN}/admin</a></p></div>`;
  const tasks = [sendMail(env, { from, to: [hr], reply_to: d.email, subject: `طلب توظيف: ${d.jobTitle} - ${d.name}`, html: body, attachments: [{ filename: d.cvName, content: b64(buf) }] })];
  const en = d.lang === 'en';
  tasks.push(sendMail(env, { from, to: [d.email], reply_to: hr,
    subject: en ? `We received your application - ${ORG_EN}` : `تم استلام طلبك - ${ORG_AR}`,
    html: en
      ? `<div style="font-family:Arial,sans-serif;font-size:14px;color:#1D2116"><p>Dear ${esc(d.name)},</p><p>Thank you for applying for <b>${esc(d.jobTitle)}</b> at ${ORG_EN}. Our HR team will review your application and contact you if your profile matches the role.</p><p>Kind regards,<br>HR team<br>${ORG_EN}<br><a href="${DOMAIN}">awtad-trade.com</a></p></div>`
      : `<div dir="rtl" style="font-family:Arial,Tahoma,sans-serif;font-size:14px;color:#1D2116"><p>عزيزي/عزيزتي ${esc(d.name)}،</p><p>شكراً لتقديمك على وظيفة <b>${esc(d.jobTitle)}</b> في ${ORG_AR}. سيراجع فريق الموارد البشرية طلبك ويتواصل معك إذا كان ملفك مناسباً للوظيفة.</p><p>مع التحية،<br>فريق الموارد البشرية<br>${ORG_AR}<br><a href="${DOMAIN}">awtad-trade.com</a></p></div>`,
  }));
  await Promise.all(tasks);
}

/* ---------------- لوحة الإدارة ---------------- */
async function hmac(key, msg) {
  const k = await crypto.subtle.importKey('raw', new TextEncoder().encode(key), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const sig = await crypto.subtle.sign('HMAC', k, new TextEncoder().encode(msg));
  return [...new Uint8Array(sig)].map((b) => b.toString(16).padStart(2, '0')).join('');
}
function safeEq(a, b) { if (a.length !== b.length) return false; let r = 0; for (let i = 0; i < a.length; i++) r |= a.charCodeAt(i) ^ b.charCodeAt(i); return r === 0; }
async function authed(request, env) {
  if (!env.ADMIN_PASSWORD) return false;
  const c = (request.headers.get('Cookie') || '').match(/(?:^|;\s*)aw_admin=([0-9]+)\.([0-9a-f]{64})/);
  if (!c || +c[1] < Date.now()) return false;
  return safeEq(c[2], await hmac(env.ADMIN_PASSWORD, 'admin|' + c[1]));
}

async function admin(request, env, url) {
  const p = url.pathname.slice('/api/admin/'.length); const m = request.method;
  if (m !== 'GET' && request.headers.get('X-Admin') !== '1') return json({ ok: false, error: 'csrf' }, 403);

  if (p === 'login' && m === 'POST') {
    if (!env.ADMIN_PASSWORD) return json({ ok: false, error: 'nopass' }, 500);
    const ip = request.headers.get('CF-Connecting-IP') || 'x'; const rk = 'rl:login:' + ip;
    const n = +(await env.KV.get(rk)) || 0;
    if (n >= 8) return json({ ok: false, error: 'rate' }, 429);
    const { password } = await request.json().catch(() => ({}));
    if (typeof password !== 'string' || !safeEq(await hmac('x', password), await hmac('x', env.ADMIN_PASSWORD))) {
      await env.KV.put(rk, String(n + 1), { expirationTtl: 900 });
      return json({ ok: false, error: 'wrong' }, 401);
    }
    const exp = Date.now() + 7 * 864e5;
    return json({ ok: true }, 200, { 'Set-Cookie': `aw_admin=${exp}.${await hmac(env.ADMIN_PASSWORD, 'admin|' + exp)}; Path=/; HttpOnly; Secure; SameSite=Strict; Max-Age=${7 * 86400}` });
  }
  if (p === 'logout') return json({ ok: true }, 200, { 'Set-Cookie': 'aw_admin=; Path=/; HttpOnly; Secure; SameSite=Strict; Max-Age=0' });
  if (!(await authed(request, env))) return json({ ok: false, error: 'auth' }, 401);
  if (p === 'me') return json({ ok: true, mail: !!env.RESEND_API_KEY });

  // الوظائف
  if (p === 'jobs' && m === 'GET') return json({ ok: true, jobs: await getJobs(env, true), today: today() });
  if (p === 'jobs' && m === 'POST') {
    const b = await request.json(); const jobs = await getJobs(env, true);
    const F = ['title_ar', 'title_en', 'dept_ar', 'dept_en', 'location_ar', 'location_en', 'summary_ar', 'summary_en', 'resp_ar', 'resp_en', 'req_ar', 'req_en', 'ben_ar', 'ben_en'];
    const clean = {}; for (const f of F) clean[f] = String(b[f] || '').trim().slice(0, f.startsWith('title') || f.startsWith('dept') || f.startsWith('location') ? 140 : 5000);
    if (!clean.title_ar) return json({ ok: false, error: 'title' }, 400);
    clean.type = JOB_TYPES[b.type] ? b.type : 'FULL_TIME';
    clean.exp = EXP[b.exp] ? b.exp : '';
    clean.deadline = /^\d{4}-\d{2}-\d{2}$/.test(b.deadline || '') ? b.deadline : '';
    clean.status = ['open', 'closed', 'draft'].includes(b.status) ? b.status : 'draft';
    const now = new Date().toISOString();
    let job = jobs.find((x) => x.id === b.id);
    if (job) { Object.assign(job, clean, { updated: now }); if (clean.status === 'open' && !job.posted) job.posted = now; }
    else { job = { id: 'j' + Date.now().toString(36), posted: clean.status === 'open' ? now : '', updated: now, ...clean }; jobs.unshift(job); }
    await saveJobs(env, jobs);
    return json({ ok: true, job });
  }
  const jm = p.match(/^jobs\/([a-z0-9-]+)$/);
  if (jm && m === 'DELETE') { const jobs = (await getJobs(env, true)).filter((x) => x.id !== jm[1]); await saveJobs(env, jobs); return json({ ok: true }); }

  // الطلبات
  if (p === 'apps' && m === 'GET') {
    const r = await env.KV.list({ prefix: 'app:', limit: 200, cursor: url.searchParams.get('cursor') || undefined });
    return json({ ok: true, apps: r.keys.map((k) => ({ id: k.name.slice(4), ...k.metadata })), cursor: r.list_complete ? null : r.cursor });
  }
  const am = p.match(/^apps\/([0-9a-z-]+)$/);
  if (am) {
    const key = 'app:' + am[1];
    if (m === 'GET') { const d = await env.KV.get(key, { type: 'json' }); return d ? json({ ok: true, app: d }) : json({ ok: false }, 404); }
    if (m === 'PATCH') {
      const d = await env.KV.get(key, { type: 'json' }); if (!d) return json({ ok: false }, 404);
      const b = await request.json();
      if (['new', 'reviewed', 'shortlisted', 'interview', 'rejected', 'hired'].includes(b.status)) d.status = b.status;
      if (typeof b.note === 'string') d.note = b.note.slice(0, 2000);
      await env.KV.put(key, JSON.stringify(d), { metadata: meta(d) });
      return json({ ok: true });
    }
    if (m === 'DELETE') { await env.KV.delete(key); await env.KV.delete('cv:' + am[1]); return json({ ok: true }); }
  }
  const cm = p.match(/^cv\/([0-9a-z-]+)$/);
  if (cm) {
    const { value, metadata } = await env.KV.getWithMetadata('cv:' + cm[1], { type: 'arrayBuffer' });
    if (!value) return json({ ok: false }, 404);
    const fn = (metadata && metadata.name) || 'cv';
    return new Response(value, { headers: { 'Content-Type': (metadata && metadata.type) || 'application/octet-stream', 'Content-Disposition': `attachment; filename="cv.${fn.split('.').pop()}"; filename*=UTF-8''${encodeURIComponent(fn)}`, 'Cache-Control': 'no-store', ...SEC } });
  }

  // الصور
  if (p === 'images' && m === 'GET') {
    const man = await (await asset(env, url, '/assets/img/manifest.json')).json();
    return json({ ok: true, images: man, overrides: await env.KV.get('imgidx', { type: 'json' }) || {} });
  }
  const im = p.match(/^images\/([a-z0-9._-]+)$/);
  if (im) {
    const name = im[1];
    const man = await (await asset(env, url, '/assets/img/manifest.json')).json();
    if (!man.some((x) => x.file === name)) return json({ ok: false, error: 'name' }, 400);
    const idx = (await env.KV.get('imgidx', { type: 'json' })) || {};
    if (m === 'PUT') {
      const type = (request.headers.get('Content-Type') || '').split(';')[0];
      if (!/^image\/(webp|png|jpeg)$/.test(type)) return json({ ok: false, error: 'type' }, 400);
      const buf = await request.arrayBuffer();
      if (!buf.byteLength || buf.byteLength > MAX_IMG) return json({ ok: false, error: 'size' }, 413);
      const v = Date.now();
      await env.KV.put('img:' + name, buf, { metadata: { type, v } });
      idx[name] = v; await env.KV.put('imgidx', JSON.stringify(idx)); mem.idx = idx; mem.idxAt = Date.now();
      return json({ ok: true, v });
    }
    if (m === 'DELETE') {
      await env.KV.delete('img:' + name); delete idx[name];
      await env.KV.put('imgidx', JSON.stringify(idx)); mem.idx = idx; mem.idxAt = Date.now();
      return json({ ok: true });
    }
  }

  // روابط التواصل الاجتماعي
  if (p === 'social' && m === 'GET') return json({ ok: true, social: await env.KV.get('social', { type: 'json' }) || {} });
  if (p === 'social' && m === 'POST') {
    const b = await request.json(); const out = {}; const bad = [];
    for (const k of Object.keys(SOCIAL)) {
      let v = String(b[k] || '').trim(); if (!v) continue;
      if (!/^https?:\/\//i.test(v)) v = 'https://' + v;
      try { const u = new URL(v); if (u.protocol === 'https:' && SOCIAL[k].test(u.hostname.toLowerCase())) out[k] = u.href; else bad.push(k); } catch { bad.push(k); }
    }
    if (bad.length) return json({ ok: false, error: 'url', bad }, 400);
    await env.KV.put('social', JSON.stringify(out)); mem.social = out; mem.socialAt = Date.now();
    return json({ ok: true, social: out });
  }

  // الألوان
  if (p === 'theme' && m === 'GET') return json({ ok: true, theme: (await env.KV.get('theme', { type: 'json' })) || {} });
  if (p === 'theme' && m === 'POST') {
    const b = await request.json(); const th = {};
    for (const k of THEME_KEYS) if (/^#[0-9a-fA-F]{6}$/.test(b[k] || '')) th[k] = b[k];
    await env.KV.put('theme', JSON.stringify(th)); mem.theme = th; mem.themeAt = Date.now();
    return json({ ok: true, theme: th });
  }
  return json({ ok: false, error: 'notfound' }, 404);
}
