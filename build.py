#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把"数据驱动"版的赤兔官网构建为纯静态站点（dist/），用于 CloudStudio 公网部署。
- 读取 data.json -> 生成 dist/content.js（内联 window.__SITE_DATA__，含 zh + en 子树 + images）
- 复制 styles.css / script.js / assets/ 到 dist/
- index.html 注入 content.js 引用，前端优先用内联数据，无需后端
- 为每个带 slug 的门店/补贴生成双语详情页（store-<slug>.html / subsidy-<slug>.html），
  页面内同时含中文层(#store-zh)与英文层(#store-en)，由底部脚本按 localStorage 切换。
后台（server.py / admin.html）不参与静态部署，保留本地编辑用。
"""
import json
import os
import shutil
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
# 站点正式域名（用于 sitemap.xml / robots.txt 的绝对地址）。
# 部署到最终域名后，如需更换可改这里，或用环境变量覆盖：
#   SITE_BASE=https://你的域名/ python3 build.py
SITE_BASE = os.environ.get("SITE_BASE", "https://keyteam.work/")


def e(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            .replace('"', '&quot;').replace("'", '&#39;'))


def ml(s):
    """多行文本：转义后把换行转成 <br>。"""
    return e(s).replace('\n', '<br>')


# 详情页底部语言切换脚本（普通字符串，{ } 为 JS 语法，无需转义）
SWITCH_JS = """
(function(){
  var NAV={
    zh:{about:'品牌',locations:'门店',gallery:'实景',services:'服务',subsidy:'企业补贴',faq:'FAQ',contact:'联系我们'},
    en:{about:'About',locations:'Locations',gallery:'Gallery',services:'Spaces',subsidy:'Subsidies',faq:'FAQ',contact:'Contact'},
    zhHant:{about:'品牌',locations:'門店',gallery:'實景',services:'服務',subsidy:'企業補貼',faq:'FAQ',contact:'聯繫我們'}
  };
  var LAYERS={zh:'store-zh',en:'store-en',zhHant:'store-tw'};
  var KEY='chitu_lang';
  function apply(l){
    if(!NAV[l]) l='zh';
    try{localStorage.setItem(KEY,l);}catch(e){}
    for(var k in LAYERS){var el=document.getElementById(LAYERS[k]); if(el) el.style.display=(k===l)?'':'none';}
    document.documentElement.lang=(l==='en')?'en':((l==='zhHant')?'zh-Hant':'zh-CN');
    var btns=document.querySelectorAll('#langSwitch button');
    for(var i=0;i<btns.length;i++){btns[i].classList.toggle('active',btns[i].dataset.lang===l);}
    var t=NAV[l]; var as=document.querySelectorAll('#nav a[data-nav]');
    for(var j=0;j<as.length;j++){var kk=as[j].dataset.nav; if(t[kk])as[j].textContent=t[kk];}
  }
  var saved=localStorage.getItem(KEY)||'zh';
  apply(saved);
  var sb=document.querySelectorAll('#langSwitch button');
  for(var m=0;m<sb.length;m++){sb[m].addEventListener('click',function(){apply(this.dataset.lang);});}
})();
"""

NAV_ITEMS = [('about', '品牌', 'About'), ('locations', '门店', 'Locations'),
             ('gallery', '实景', 'Gallery'), ('services', '服务', 'Spaces'),
             ('subsidy', '企业补贴', 'Subsidies'), ('faq', 'FAQ', 'FAQ'),
             ('contact', '联系我们', 'Contact')]


def _store_inner(loc, data, images):
    """生成门店详情页主体 HTML（不含外壳），返回 (inner_html, meta)。"""
    img = images
    ipath = img.get(loc.get('imgKey', ''))
    addr = loc.get('addr', '') or loc.get('name', '')
    q = quote(addr)
    map_url = f'https://map.baidu.com/search/{q}'
    brand = data.get('brand', {})
    footer = data.get('footer', {})
    contact = data.get('contact', {})
    if ipath:
        hero = f'<img class="store-hero-img" src="{e(ipath)}" alt="{e(loc.get("name"))}">'
    else:
        hero = '<div class="img-placeholder"><span>门店实景图<br><em>点击后台上传</em></span></div>'
    detail = loc.get('detail', '')
    detail_html = f'<div class="store-detail-text">{ml(detail)}</div>' if detail else ''
    highlights = ''.join(f'<li>{e(h)}</li>' for h in loc.get('highlights', []))
    rooms = loc.get('rooms', [])
    room_cards = ''
    for r in rooms:
        rimg = img.get(r.get('imgKey', ''))
        if rimg:
            thumb = f'<img src="{e(rimg)}" alt="{e(r.get("name", ""))}">'
        else:
            thumb = '<div class="room-thumb-ph">房型图</div>'
        rmeta = ' · '.join(x for x in [r.get('area', ''), r.get('capacity', '')] if x)
        room_cards += (
            '<div class="room-card">'
            '<div class="room-thumb">' + thumb + '</div>'
            '<div class="room-body">'
            f'<h3>{e(r.get("name", ""))}</h3>'
            + (f'<div class="room-meta">{e(rmeta)}</div>' if rmeta else '')
            + (f'<p class="room-config">{e(r.get("config", ""))}</p>' if r.get('config') else '')
            + f'<div class="room-price">{e(r.get("price", ""))}<span>{e(r.get("unit", ""))}</span></div>'
            '</div></div>'
        )
    rooms_block = (
        '<section class="store-rooms">'
        '<div class="rooms-head"><h2>户型与价格</h2>'
        '<p>灵活选择，拎包入驻。实时空置与具体房型欢迎来电预约看房。</p></div>'
        f'<div class="room-grid">{room_cards}</div>'
        '</section>'
    ) if rooms else ''
    footer_links = ''.join(
        f'<a href="{e(l.get("href", "#"))}">{e(l.get("text", ""))}</a>' for l in footer.get('links', []))
    footer_contacts = ''.join(f'<p>{e(c)}</p>' for c in footer.get('contacts', []))
    phone = loc.get('phone', '')
    name = loc.get('name', '')
    og_image = ipath if ipath else 'assets/logo.png'
    jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": name,
        "image": og_image,
        "telephone": f"+86-{phone}" if phone else "",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": addr,
            "addressLocality": "广州市",
            "addressRegion": "广东省",
            "addressCountry": "CN"
        },
        "description": f"赤兔文创 {name}，位于{addr}，提供灵活工位、可注册地址与工商财税企业服务。",
        "areaServed": "广州海珠区"
    }, ensure_ascii=False)
    inner = f'''  <section class="store-hero">
    {hero}
    <div class="store-hero-overlay">
      <div class="container">
        <span class="location-tag">{e(loc.get('tag', ''))}</span>
        <h1>{e(name)}</h1>
        <p>{e(addr)}</p>
      </div>
    </div>
  </section>
  <section class="section section-light">
    <div class="container">
      {detail_html}
      <div class="store-detail">
        <div class="store-info">
          <h2>门店信息</h2>
          <ul class="store-facts">
            <li><b>地址</b><span>{e(addr)}</span></li>
            <li><b>定位</b><a href="{map_url}" target="_blank" rel="noopener">{e(loc.get('position') or loc.get('metro', ''))} · 点此导航</a></li>
            <li><b>地铁</b><span>{e(loc.get('metro', ''))}</span></li>
            <li><b>联系人</b><span>{e(loc.get('contact') or '专属顾问')}</span></li>
            <li><b>电话</b><a href="tel:{e(phone)}">{e(phone)}</a></li>
          </ul>
          <div class="location-price">{e(loc.get('priceLabel', ''))} <strong>{e(loc.get('price', ''))}</strong>{e(loc.get('priceUnit', ''))}</div>
          <div class="store-actions">
            <a class="btn btn-primary" href="tel:{e(phone)}">电话预约看房</a>
            <a class="btn btn-outline" href="{map_url}" target="_blank" rel="noopener">地图导航</a>
            <a class="btn btn-outline" href="index.html#locations">返回门店列表</a>
          </div>
        </div>
        <div class="store-highlights">
          <h2>门店亮点</h2>
          <ul>{highlights}</ul>
          <p class="store-note">{e(contact.get('note', ''))}</p>
        </div>
      </div>
      {rooms_block}
    </div>
  </section>'''
    meta = {'title': name, 'jsonld': jsonld, 'og_image': og_image, 'phone': phone}
    return inner, meta


def _subsidy_inner(sub, data, images):
    """生成补贴详情页主体 HTML（不含外壳），返回 (inner_html, meta)。"""
    img = images
    ipath = img.get(sub.get('imgKey', ''))
    brand = data.get('brand', {})
    footer = data.get('footer', {})
    contact = data.get('contact', {})
    if ipath:
        hero = f'<img class="store-hero-img" src="{e(ipath)}" alt="{e(sub.get("name"))}">'
    else:
        hero = '<div class="img-placeholder"><span>补贴配图<br><em>点击后台上传</em></span></div>'
    policy = (f'<div class="subsidy-policy"><span class="sp-label">政策依据</span>{ml(sub.get("policy", ""))}</div>'
              if sub.get('policy') else '')
    object_html = f'<p class="subsidy-obj">{e(sub.get("object", ""))}</p>'
    if sub.get('objectDetail'):
        object_html += f'<div class="subsidy-obj-detail">{ml(sub.get("objectDetail", ""))}</div>'
    standard_html = f'<p class="subsidy-std">{e(sub.get("standard", ""))}</p>'
    if sub.get('standardDetail'):
        standard_html += f'<p class="subsidy-std-note">{ml(sub.get("standardDetail", ""))}</p>'
    conditions = ''.join(f'<li>{e(c)}</li>' for c in sub.get('conditions', []))
    materials = ''.join(f'<li>{e(m)}</li>' for m in sub.get('materials', []))
    process = ''.join(
        f'<li><span class="step-n">{i + 1}</span><span>{e(p)}</span></li>'
        for i, p in enumerate(sub.get('process', [])))
    agency = (f'<div class="subsidy-agency"><span class="sp-label">受理与申办</span>{ml(sub.get("agency", ""))}</div>'
              if sub.get('agency') else '')
    company = ''.join(f'<li>{e(c)}</li>' for c in sub.get('company', []))
    company_html = (f'<div class="subsidy-company"><h2>赤兔能为你做什么</h2><ul>{company}</ul></div>'
                    if company else '')
    disclaimer = ('本页政策内容整理自《广东省就业创业补贴补助申请办理指导清单（2026年修订版）》'
                  '（粤人社规〔2026〕20号），仅供参考；具体申领条件、材料与流程以登记注册地'
                  '人力资源社会保障部门最新公布为准。')
    summary = sub.get('summary', '')
    footer_links = ''.join(
        f'<a href="{e(l.get("href", "#"))}">{e(l.get("text", ""))}</a>' for l in footer.get('links', []))
    footer_contacts = ''.join(f'<p>{e(c)}</p>' for c in footer.get('contacts', []))
    phone = (brand.get('wechat') or contact.get('btnHref', '').replace('tel:', '') or '18903005927')
    name = sub.get('name', '')
    og_image = ipath if ipath else 'assets/logo.png'
    jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "Service",
        "name": name,
        "image": og_image,
        "provider": {
            "@type": "Organization",
            "name": brand.get('name', '赤兔文创'),
            "telephone": "+86-18903005927"
        },
        "areaServed": "广州海珠区",
        "description": (sub.get('summary') or name)
    }, ensure_ascii=False)
    inner = f'''  <section class="store-hero">
    {hero}
    <div class="store-hero-overlay">
      <div class="container">
        <span class="location-tag">{e(sub.get('tag', ''))}</span>
        <h1>{e(name)}</h1>
        <p>{e(sub.get('standard', ''))}</p>
      </div>
    </div>
  </section>

  {policy}

  <section class="section section-light">
    <div class="container sub-detail">
      {f'<p class="subsidy-summary">{e(summary)}</p>' if summary else ''}
      <div class="sub-block"><h2>补贴对象</h2>{object_html}</div>
      <div class="sub-block"><h2>补贴标准</h2>{standard_html}</div>
      <div class="sub-block"><h2>申请条件</h2><ul class="subsidy-cond">{conditions}</ul></div>
      <div class="sub-block"><h2>所需材料</h2><ul class="subsidy-mat">{materials}</ul></div>
      <div class="sub-block"><h2>办理流程</h2><ol class="subsidy-flow">{process}</ol></div>
      {agency}
      {company_html}
      <div class="store-actions sub-actions">
        <a class="btn btn-primary" href="tel:{e(phone)}">咨询补贴详情</a>
        <a class="btn btn-outline" href="index.html#subsidy">返回企业补贴</a>
      </div>
      <p class="subsidy-disclaimer">{e(disclaimer)}</p>
    </div>
  </section>'''
    meta = {'title': name, 'jsonld': jsonld, 'og_image': og_image, 'phone': phone}
    return inner, meta


def _shell(zh_inner, en_inner, tw_inner, title, jsonld, og_image, phone, version=''):
    """组装完整详情页：中/英双层 + 切换按钮 + 切换脚本。"""
    nav_html = ''.join(f'<a href="index.html#{k}" data-nav="{k}">{zh}</a>' for k, zh, en in NAV_ITEMS)
    footer_nav = ''.join(f'<a href="index.html#{k}">{zh}</a>' for k, zh, en in NAV_ITEMS)
    css = f'styles.css?v={version}' if version else 'styles.css'
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(title)} · 赤兔文创 | 广州海珠联合办公</title>
<meta name="robots" content="index,follow">
<meta property="og:title" content="{e(title)}">
<meta property="og:image" content="{e(og_image)}">
<script type="application/ld+json">{jsonld}</script>
<link rel="stylesheet" href="{css}">
</head>
<body>
<header class="header"><div class="container nav-container">
<a href="index.html" class="logo"><img src="assets/logo.png" alt="赤兔文创"></a>
<nav class="nav" id="nav">{nav_html}</nav>
<div class="lang-switch" id="langSwitch"><button type="button" data-lang="zh" class="active">中</button><button type="button" data-lang="zhHant">繁</button><button type="button" data-lang="en">EN</button></div>
<button class="menu-toggle" id="menuToggle"><span></span><span></span><span></span></button>
</div></header>
<main>
<div id="store-zh">{zh_inner}</div>
<div id="store-en" style="display:none">{en_inner}</div>
<div id="store-tw" style="display:none">{tw_inner}</div>
</main>
<footer class="footer"><div class="container footer-grid"><div class="footer-brand"><img src="assets/logo.png" alt="赤兔文创" class="footer-logo"><p>企业生态引擎 · 拎包入驻 · 创享办公社区</p></div><div class="footer-links"><h4>快速导航</h4>{footer_nav}</div><div class="footer-contact"><h4>联系我们</h4><p>微信：18903005927</p></div></div><div class="container footer-copy"><p>© 2017 赤兔文创 · 广州红杉云科技有限公司旗下品牌</p></div></footer>
<a href="tel:{e(phone)}" class="float-cta" aria-label="电话咨询"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg></a>
<script>{SWITCH_JS}</script>
</body>
</html>'''


def render_store_page(loc, data, version=''):
    images = data.get('images', {})
    en = data.get('en') or {}
    tw = data.get('zhHant') or {}
    en_loc = next((x for x in en.get('locations', []) if x.get('slug') == loc.get('slug')), None)
    tw_loc = next((x for x in tw.get('locations', []) if x.get('slug') == loc.get('slug')), None)
    zh_inner, zh_meta = _store_inner(loc, data, images)
    en_inner = _store_inner(en_loc, en, images)[0] if en_loc else zh_inner
    tw_inner = _store_inner(tw_loc, tw, images)[0] if tw_loc else zh_inner
    return _shell(zh_inner, en_inner, tw_inner, zh_meta['title'], zh_meta['jsonld'], zh_meta['og_image'], zh_meta['phone'], version)


def render_subsidy_page(sub, data, version=''):
    images = data.get('images', {})
    en = data.get('en') or {}
    tw = data.get('zhHant') or {}
    en_sub = next((x for x in en.get('subsidies', []) if x.get('slug') == sub.get('slug')), None)
    tw_sub = next((x for x in tw.get('subsidies', []) if x.get('slug') == sub.get('slug')), None)
    zh_inner, zh_meta = _subsidy_inner(sub, data, images)
    en_inner = _subsidy_inner(en_sub, en, images)[0] if en_sub else zh_inner
    tw_inner = _subsidy_inner(tw_sub, tw, images)[0] if tw_sub else zh_inner
    return _shell(zh_inner, en_inner, tw_inner, zh_meta['title'], zh_meta['jsonld'], zh_meta['og_image'], zh_meta['phone'], version)


def main():
    with open(os.path.join(ROOT, "data.json"), encoding="utf-8") as f:
        data = json.load(f)

    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)

    # 复制静态资源
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(DIST, "assets"))
    shutil.copy(os.path.join(ROOT, "styles.css"), os.path.join(DIST, "styles.css"))
    shutil.copy(os.path.join(ROOT, "script.js"), os.path.join(DIST, "script.js"))

    # 生成内联数据文件（含 zh + en 子树 + images）
    with open(os.path.join(DIST, "content.js"), "w", encoding="utf-8") as f:
        f.write("window.__SITE_DATA__ = ")
        json.dump(data, f, ensure_ascii=False)
        f.write(";")

    # 注入 content.js（在 script.js 之前）
    with open(os.path.join(ROOT, "index.html"), encoding="utf-8") as f:
        html = f.read()
    html = html.replace(
        '<script src="script.js"></script>',
        '<script src="content.js"></script>\n  <script src="script.js"></script>',
    )
    with open(os.path.join(DIST, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)

    # 生成各门店独立详情页（双语）
    store_count = 0
    for loc in data.get('locations', []):
        slug = loc.get('slug')
        if not slug:
            continue
        page = render_store_page(loc, data)
        with open(os.path.join(DIST, f'store-{slug}.html'), 'w', encoding='utf-8') as f:
            f.write(page)
        store_count += 1

    # 生成各企业补贴独立详情页（双语）
    subsidy_count = 0
    for sub in data.get('subsidies', []):
        slug = sub.get('slug')
        if not slug:
            continue
        page = render_subsidy_page(sub, data)
        with open(os.path.join(DIST, f'subsidy-{slug}.html'), 'w', encoding='utf-8') as f:
            f.write(page)
        subsidy_count += 1

    # 生成 sitemap.xml 与 robots.txt（绝对地址基于 SITE_BASE）
    all_pages = ["index.html"]
    for loc in data.get('locations', []):
        if loc.get('slug'):
            all_pages.append(f"store-{loc['slug']}.html")
    for sub in data.get('subsidies', []):
        if sub.get('slug'):
            all_pages.append(f"subsidy-{sub['slug']}.html")
    sm = ['<?xml version="1.0" encoding="UTF-8"?>',
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in all_pages:
        sm.append(f'  <url><loc>{SITE_BASE}{u}</loc>'
                  f'<changefreq>weekly</changefreq><priority>0.8</priority></url>')
    sm.append('</urlset>')
    with open(os.path.join(DIST, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(sm))
    with open(os.path.join(DIST, 'robots.txt'), 'w', encoding='utf-8') as f:
        f.write(f"User-agent: *\nAllow: /\nSitemap: {SITE_BASE}sitemap.xml\n")

    print("✅ 构建完成 ->", DIST)
    print("   内联数据大小:", os.path.getsize(os.path.join(DIST, "content.js")), "bytes")
    print("   assets 文件数:", len(os.listdir(os.path.join(DIST, "assets"))))
    print("   门店详情页(双语):", store_count, " | 企业补贴页(双语):", subsidy_count)
    print("   sitemap.xml / robots.txt 已生成 (SITE_BASE =", SITE_BASE, ")")


if __name__ == "__main__":
    main()
