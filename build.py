#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把"数据驱动"版的赤兔官网构建为纯静态站点（dist/），用于 CloudStudio 公网部署。
- 读取 data.json -> 生成 dist/content.js（内联 window.__SITE_DATA__）
- 复制 styles.css / script.js / assets/ 到 dist/
- index.html 注入 content.js 引用，前端优先用内联数据，无需后端
- 为每个带 slug 的门店生成 store-<slug>.html 独立详情页
后台（server.py / admin.html）不参与静态部署，保留本地编辑用。
"""
import json
import os
import shutil
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")


def e(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            .replace('"', '&quot;').replace("'", '&#39;'))


def ml(s):
    """多行文本：转义后把换行转成 <br>。"""
    return e(s).replace('\n', '<br>')


def render_store_page(loc, data):
    img = data.get('images', {})
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
    # 房型区块（后续可填真实房型）
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
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(loc.get('name', ''))} · 赤兔文创</title>
<meta name="description" content="{e(addr)}">
<link rel="stylesheet" href="styles.css">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&family=Noto+Serif+SC:wght@500;600;700&display=swap" rel="stylesheet">
</head>
<body>
<header class="header">
  <div class="container nav-container">
    <a href="index.html" class="logo"><img src="assets/logo.png" alt="赤兔文创"></a>
    <nav class="nav">
      <a href="index.html#about">品牌</a>
      <a href="index.html#locations">门店</a>
      <a href="index.html#gallery">实景</a>
      <a href="index.html#services">服务</a>
      <a href="index.html#faq">FAQ</a>
      <a href="index.html#contact" class="nav-cta">联系我们</a>
    </nav>
  </div>
</header>
<main>
  <section class="store-hero">
    {hero}
    <div class="store-hero-overlay">
      <div class="container">
        <span class="location-tag">{e(loc.get('tag', ''))}</span>
        <h1>{e(loc.get('name', ''))}</h1>
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
  </section>
</main>
<footer class="footer">
  <div class="container footer-grid">
    <div class="footer-brand">
      <img src="assets/logo.png" alt="赤兔文创" class="footer-logo">
      <p>{e(footer.get('brand', ''))}</p>
    </div>
    <div class="footer-links"><h4>快速导航</h4>{footer_links}</div>
    <div class="footer-contact"><h4>{e(footer.get('contactTitle', '联系我们'))}</h4>{footer_contacts}</div>
  </div>
  <div class="container footer-copy"><p>{e(footer.get('copy', ''))}</p></div>
</footer>
    <a href="tel:{e(phone)}" class="float-cta" aria-label="电话咨询">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
</a>
</body>
</html>'''


def render_subsidy_page(sub, data):
    img = data.get('images', {})
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
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(sub.get('name', ''))} · 企业补贴 · 赤兔文创</title>
<meta name="description" content="{e(sub.get('summary', ''))}">
<link rel="stylesheet" href="styles.css">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&family=Noto+Serif+SC:wght@500;600;700&display=swap" rel="stylesheet">
</head>
<body>
<header class="header">
  <div class="container nav-container">
    <a href="index.html" class="logo"><img src="assets/logo.png" alt="赤兔文创"></a>
    <nav class="nav">
      <a href="index.html#about">品牌</a>
      <a href="index.html#locations">门店</a>
      <a href="index.html#gallery">实景</a>
      <a href="index.html#services">服务</a>
      <a href="index.html#subsidy">企业补贴</a>
      <a href="index.html#faq">FAQ</a>
      <a href="index.html#contact" class="nav-cta">联系我们</a>
    </nav>
  </div>
</header>
<main>
  <section class="store-hero">
    {hero}
    <div class="store-hero-overlay">
      <div class="container">
        <span class="location-tag">{e(sub.get('tag', ''))}</span>
        <h1>{e(sub.get('name', ''))}</h1>
        <p>{e(sub.get('standard', ''))}</p>
      </div>
    </div>
  </section>

  {policy}

  <section class="section section-light">
    <div class="container sub-detail">
      {f'<p class="subsidy-summary">{e(summary)}</p>' if summary else ''}
      <div class="sub-block">
        <h2>补贴对象</h2>
        {object_html}
      </div>
      <div class="sub-block">
        <h2>补贴标准</h2>
        {standard_html}
      </div>
      <div class="sub-block">
        <h2>申请条件</h2>
        <ul class="subsidy-cond">{conditions}</ul>
      </div>
      <div class="sub-block">
        <h2>所需材料</h2>
        <ul class="subsidy-mat">{materials}</ul>
      </div>
      <div class="sub-block">
        <h2>办理流程</h2>
        <ol class="subsidy-flow">{process}</ol>
      </div>
      {agency}
      {company_html}
      <div class="store-actions sub-actions">
        <a class="btn btn-primary" href="tel:{e(phone)}">咨询补贴详情</a>
        <a class="btn btn-outline" href="index.html#subsidy">返回企业补贴</a>
      </div>
      <p class="subsidy-disclaimer">{e(disclaimer)}</p>
    </div>
  </section>
</main>
<footer class="footer">
  <div class="container footer-grid">
    <div class="footer-brand">
      <img src="assets/logo.png" alt="赤兔文创" class="footer-logo">
      <p>{e(footer.get('brand', ''))}</p>
    </div>
    <div class="footer-links"><h4>快速导航</h4>{footer_links}</div>
    <div class="footer-contact"><h4>{e(footer.get('contactTitle', '联系我们'))}</h4>{footer_contacts}</div>
  </div>
  <div class="container footer-copy"><p>{e(footer.get('copy', ''))}</p></div>
</footer>
<a href="tel:{e(phone)}" class="float-cta" aria-label="电话咨询">
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
</a>
</body>
</html>'''


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

    # 生成内联数据文件
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

    # 生成各门店独立详情页
    store_count = 0
    for loc in data.get('locations', []):
        slug = loc.get('slug')
        if not slug:
            continue
        page = render_store_page(loc, data)
        with open(os.path.join(DIST, f'store-{slug}.html'), 'w', encoding='utf-8') as f:
            f.write(page)
        store_count += 1

    # 生成各企业补贴独立详情页
    subsidy_count = 0
    for sub in data.get('subsidies', []):
        slug = sub.get('slug')
        if not slug:
            continue
        page = render_subsidy_page(sub, data)
        with open(os.path.join(DIST, f'subsidy-{slug}.html'), 'w', encoding='utf-8') as f:
            f.write(page)
        subsidy_count += 1

    print("✅ 构建完成 ->", DIST)
    print("   内联数据大小:", os.path.getsize(os.path.join(DIST, "content.js")), "bytes")
    print("   assets 文件数:", len(os.listdir(os.path.join(DIST, "assets"))))
    print("   门店详情页:", store_count, " | 企业补贴页:", subsidy_count)


if __name__ == "__main__":
    main()
