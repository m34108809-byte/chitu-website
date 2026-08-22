document.addEventListener('DOMContentLoaded', () => {
  const header = document.getElementById('header');
  const menuToggle = document.getElementById('menuToggle');
  const nav = document.getElementById('nav');

  // Header shadow on scroll
  window.addEventListener('scroll', () => {
    header.classList.toggle('scrolled', window.scrollY > 10);
  });

  // Mobile menu toggle
  menuToggle.addEventListener('click', () => nav.classList.toggle('open'));
  nav.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => nav.classList.remove('open'));
  });

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId === '#') return;
      const target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        window.scrollTo({ top: target.getBoundingClientRect().top + window.pageYOffset - 80, behavior: 'smooth' });
      }
    });
  });

  // Reveal observer (re-applied after render)
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });

  function observeReveals(root) {
    root.querySelectorAll('.feature-card, .location-card, .service-item, .faq-item, .subsidy-card').forEach(el => {
      el.classList.add('reveal');
      revealObserver.observe(el);
    });
  }

  /* ---------- helpers ---------- */
  const esc = (s) => String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');

  const ICONS = {
    'layers': '<path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/>',
    'box': '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/>',
    'users': '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
    'clock': '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    'shield': '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
    'map-pin': '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    'desk': '<rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/>',
    'office': '<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>',
    'meeting': '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M7 20h10M12 16v4"/>',
    'tea': '<path d="M18 8h1a4 4 0 0 1 0 8h-1M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"/><line x1="6" y1="1" x2="6" y2="4"/><line x1="10" y1="1" x2="10" y2="4"/><line x1="14" y1="1" x2="14" y2="4"/>',
    'doc': '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/>',
    'money': '<path d="M12 1v22M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
    'visa': '<rect x="4" y="3" width="16" height="18" rx="2"/><circle cx="12" cy="9" r="2.5"/><path d="M8 16c0-2 2-3 4-3s4 1 4 3"/><path d="M9 6h6"/>'
  };

  const svg = (key) => `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">${ICONS[key] || ICONS['box']}</svg>`;

  function imageHTML(path, label, cls) {
    if (path) {
      return `<img class="${cls}" data-cls="${cls}" src="${esc(path)}" alt="${esc(label)}">`;
    }
    return `<div class="img-placeholder ${cls}"><span>${esc(label)}<br><em>点击后台上传</em></span></div>`;
  }

  function attachImageFallback(root) {
    root.querySelectorAll('img[data-cls]').forEach(img => {
      img.addEventListener('error', () => {
        const ph = document.createElement('div');
        ph.className = 'img-placeholder ' + img.dataset.cls;
        ph.innerHTML = `<span>${esc(img.alt)}</span>`;
        img.replaceWith(ph);
      });
    });
  }

  function headerHTML(h) {
    return `<h2>${esc(h.title)}</h2><p>${esc(h.sub)}</p>`;
  }

  /* ---------- render ---------- */
  function render(content, images) {
    const data = content;
    const img = images || {};

    // Hero
    const heroText = document.getElementById('hero-text');
    const h = data.hero;
    heroText.innerHTML = `
      <h1>${esc(h.title)}</h1>
      <p class="subtitle">${esc(h.subtitle)}</p>
      <p class="lead">${esc(h.lead)}</p>
      <div class="hero-actions">
        <a href="${esc(h.cta1.href)}" class="btn btn-primary">${esc(h.cta1.text)}</a>
        <a href="${esc(h.cta2.href)}" class="btn btn-outline">${esc(h.cta2.text)}</a>
      </div>
      <div class="hero-meta">${h.meta.map(m => `<span>${esc(m.pre)}<strong>${esc(m.bold)}</strong>${esc(m.post)}</span>`).join('')}</div>`;
    document.getElementById('hero-visual').innerHTML = imageHTML(img.hero, '办公空间实景图', 'hero-img');

    // Hero background carousel
    const carousel = document.getElementById('hero-carousel');
    if (carousel) {
      const bgSlides = (h.bgImages || []).filter(bg => img[bg.imgKey]);
      if (bgSlides.length > 0) {
        carousel.innerHTML = bgSlides.map((bg, i) =>
          `<div class="hero-slide ${i === 0 ? 'active' : ''}" data-slide="${i}">
             <img src="${esc(img[bg.imgKey])}" alt="${esc(bg.label)}" data-cls="hero-slide-img">
           </div>`
        ).join('') +
        `<div class="hero-dots">${bgSlides.map((_, i) =>
          `<button class="hero-dot ${i === 0 ? 'active' : ''}" data-dot="${i}" aria-label="第${i+1}张"></button>`
        ).join('')}</div>`;
        initHeroCarousel(carousel, bgSlides.length);
      }
    }

    // Features
    document.getElementById('features-header').innerHTML = headerHTML(data.featuresHeader);
    document.getElementById('features-list').innerHTML = data.features.map(f => `
      <div class="feature-card">
        <div class="feature-icon">${svg(f.icon)}</div>
        <h3>${esc(f.title)}</h3>
        <p>${esc(f.desc)}</p>
      </div>`).join('');

    // Locations
    document.getElementById('locations-header').innerHTML = headerHTML(data.locationsHeader);
    document.getElementById('locations-list').innerHTML = data.locations.map(l => {
      const locSearch = encodeURIComponent(l.addr || l.name);
      const slug = l.slug ? `store-${esc(l.slug)}.html` : '#';
      return `
      <article class="location-card">
        <a class="location-img-link" href="${slug}">${imageHTML(img[l.imgKey], l.name + ' 门店实景图', 'location-img')}</a>
        <div class="location-tag">${esc(l.tag)}</div>
        <h3><a class="loc-name-link" href="${slug}">${esc(l.name)}</a></h3>
        <p class="location-addr">${esc(l.addr)}</p>
        <a class="location-position" href="https://map.baidu.com/search/${locSearch}" target="_blank" rel="noopener">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
          <span>${esc(l.position || l.metro)}</span>
        </a>
        <p class="location-metro"><span class="metro-icon">M</span> ${esc(l.metro)}</p>
        <div class="location-price">${esc(l.priceLabel)} <strong>${esc(l.price)}</strong>${esc(l.priceUnit)}</div>
        <ul class="location-highlights">${l.highlights.map(x => `<li>${esc(x)}</li>`).join('')}</ul>
        <div class="location-contact-row">
          <div class="location-contact"><span>联系人</span>${esc(l.contact || '专属顾问')}</div>
          <div class="location-btns">
            <a class="btn btn-white" href="tel:${esc(l.phone)}">预约看房</a>
            <a class="btn btn-outline" href="${slug}">门店详情 →</a>
          </div>
        </div>
      </article>`;
    }).join('');

    // Banner
    document.getElementById('banner-container').innerHTML = imageHTML(img.banner, '办公空间实景 · 多店环境', 'banner-img');

    // Gallery
    document.getElementById('gallery-header').innerHTML = headerHTML(data.galleryHeader);
    document.getElementById('gallery-list').innerHTML = data.gallery.map(g => {
      const cls = 'gallery-item' + (g.span ? ' span2' : '');
      if (img[g.imgKey]) {
        return `<img class="${cls}" data-cls="${cls}" src="${esc(img[g.imgKey])}" alt="${esc(g.label)}">`;
      }
      return `<div class="img-placeholder ${cls}"><span>${esc(g.label)}<br><em>点击后台上传</em></span></div>`;
    }).join('');

    // Services
    document.getElementById('services-header').innerHTML = headerHTML(data.servicesHeader);
    document.getElementById('services-list').innerHTML = data.services.map(s => `
      <div class="service-item">
        <div class="service-icon">${svg(s.icon)}</div>
        <div class="service-body"><h3>${esc(s.title)}</h3><p>${esc(s.desc)}</p></div>
      </div>`).join('');

    // Subsidy (企业补贴)
    document.getElementById('subsidy-header').innerHTML = headerHTML(data.subsidyHeader);
    document.getElementById('subsidy-list').innerHTML = data.subsidies.map(s => {
      const slug = s.slug ? `subsidy-${esc(s.slug)}.html` : '#';
      return `
      <article class="subsidy-card">
        <a class="subsidy-img-link" href="${slug}">${imageHTML(img[s.imgKey], s.name + ' 补贴配图', 'subsidy-img')}</a>
        <div class="location-tag">${esc(s.tag)}</div>
        <h3><a class="subsidy-name-link" href="${slug}">${esc(s.name)}</a></h3>
        <p class="subsidy-summary">${esc(s.summary)}</p>
        <div class="subsidy-facts">
          <span><b>对象</b>${esc(s.object)}</span>
          <span><b>标准</b>${esc(s.standard)}</span>
        </div>
        <a class="btn btn-outline" href="${slug}">补贴详情 →</a>
      </article>`;
    }).join('');

    // FAQ
    document.getElementById('faq-header').innerHTML = headerHTML(data.faqHeader);
    document.getElementById('faq-list').innerHTML = data.faqs.map(f => `
      <details class="faq-item">
        <summary>${esc(f.q)}</summary>
        <p>${esc(f.a)}</p>
      </details>`).join('');

    // Contact
    const c = data.contact;
    document.getElementById('contact-content').innerHTML = `
      <h2>${esc(c.title)}</h2>
      <p>${esc(c.sub)}</p>
      <a class="btn btn-primary btn-large" href="${esc(c.btnHref)}">${esc(c.btnText)}</a>
      <p class="cta-note">${esc(c.note)}</p>`;

    // Footer
    const f = data.footer;
    document.getElementById('footer-grid').innerHTML = `
      <div class="footer-brand">
        <img src="assets/logo.png" alt="赤兔文创" class="footer-logo">
        <p>${esc(f.brand)}</p>
      </div>
      <div class="footer-links">
        <h4>快速导航</h4>
        ${f.links.map(l => `<a href="${esc(l.href)}">${esc(l.text)}</a>`).join('')}
      </div>
      <div class="footer-contact">
        <h4>${esc(f.contactTitle)}</h4>
        ${f.contacts.map(x => `<p>${esc(x)}</p>`).join('')}
      </div>`;
    document.getElementById('footer-copy').innerHTML = `<p>${esc(f.copy)}</p>`;

    // Post-processing
    attachImageFallback(document.body);
    observeReveals(document.body);
  }

  /* ---------- language switch ---------- */
  const LANG_KEY = 'chitu_lang';
  let currentLang = localStorage.getItem(LANG_KEY) || 'zh';

  const NAV_TEXT = {
    zh: { about: '品牌', locations: '门店', gallery: '实景', services: '服务', subsidy: '企业补贴', faq: 'FAQ', contact: '联系我们' },
    en: { about: 'About', locations: 'Locations', gallery: 'Gallery', services: 'Spaces', subsidy: 'Subsidies', faq: 'FAQ', contact: 'Contact' },
    zhHant: { about: '品牌', locations: '門店', gallery: '實景', services: '服務', subsidy: '企業補貼', faq: 'FAQ', contact: '聯繫我們' }
  };

  function showLang(l) {
    currentLang = l;
    try { localStorage.setItem(LANG_KEY, l); } catch (e) {}
    const root = window.__SITE_DATA__ || {};
    const content = root[l] || root;
    const images = root.images || {};
    document.documentElement.lang = (l === 'en') ? 'en' : (l === 'zhHant' ? 'zh-Hant' : 'zh-CN');
    render(content, images);
    updateLangUI();
  }

  function updateLangUI() {
    const sw = document.getElementById('langSwitch');
    if (sw) {
      sw.querySelectorAll('button[data-lang]').forEach(b => {
        b.classList.toggle('active', b.dataset.lang === currentLang);
      });
    }
    const navText = NAV_TEXT[currentLang] || NAV_TEXT.zh;
    document.querySelectorAll('#nav a').forEach(a => {
      const key = (a.getAttribute('href') || '').replace('#', '');
      if (navText[key]) a.textContent = navText[key];
    });
  }

  /* ---------- hero carousel ---------- */
  function initHeroCarousel(root, count) {
    if (count <= 1) return;
    const slides = root.querySelectorAll('.hero-slide');
    const dots = root.querySelectorAll('.hero-dot');
    let current = 0;
    function show(idx) {
      current = idx;
      slides.forEach((s, i) => s.classList.toggle('active', i === current));
      dots.forEach((d, i) => d.classList.toggle('active', i === current));
    }
    dots.forEach((d, i) => d.addEventListener('click', () => show(i)));
    setInterval(() => show((current + 1) % count), 5000);
  }

  /* ---------- load ---------- */
  if (window.__SITE_DATA__) {
    // 静态托管模式（已内联数据，无需后端）
    showLang(currentLang);
  } else {
    // 本地后端模式
    fetch('/api/content')
      .then(r => { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
      .then(d => { window.__SITE_DATA__ = d; showLang(currentLang); })
      .catch(err => {
        document.getElementById('hero-text').innerHTML =
          '<h1>赤兔文创 · 创享办公社区</h1>' +
          '<p class="lead">请通过后台服务访问本站点（直接双击打开 html 无法加载内容）。' +
          '启动命令：<code>python server.py</code>，然后访问 http://localhost:8080/</p>';
        console.error('加载内容失败：', err);
      });
  }

  // 语言切换按钮
  const langSw = document.getElementById('langSwitch');
  if (langSw) {
    langSw.querySelectorAll('button[data-lang]').forEach(b => {
      b.addEventListener('click', () => showLang(b.dataset.lang));
    });
  }
});
