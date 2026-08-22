#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
赤兔文创官网 · 后台服务（本地 & 云端通用）
- 托管官网静态文件（index.html / styles.css / script.js / assets/）
- 后台管理页面：/admin
- 内容接口：GET /api/content 读取，POST /api/content 保存（需密码）
- 图片上传：POST /api/upload（需密码，X-Filename 指定文件名，body 为图片二进制）

运行（本地）：
    python server.py
自定义端口/密码/数据目录：
    PORT=8080 CHITU_ADMIN_PASS=你的密码 CHITU_DATA_DIR=/data python server.py

云端部署（Railway 等）：
    PORT 由平台自动注入；CHITU_DATA_DIR 指向持久卷（如 /data）实现数据持久化，
    首次启动会自动从源码拷贝初始 data.json 与 assets 到持久目录。
"""
import json
import mimetypes
import os
import re
import shutil
import sys
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import build

# 数据持久化目录：云端用持久卷（如 /data），本地默认与代码同目录
DATA_DIR = os.environ.get('CHITU_DATA_DIR')
if DATA_DIR:
    os.makedirs(os.path.join(DATA_DIR, 'assets'), exist_ok=True)
    # 首次初始化：从源码拷贝初始 data.json 与 assets（仅在目标缺失时）
    _src_data = os.path.join(ROOT, 'data.json')
    _dst_data = os.path.join(DATA_DIR, 'data.json')
    if os.path.isfile(_src_data) and not os.path.isfile(_dst_data):
        with open(_src_data, 'rb') as f:
            _seed = f.read()
        with open(_dst_data, 'wb') as f:
            f.write(_seed)
    _src_assets = os.path.join(ROOT, 'assets')
    if os.path.isdir(_src_assets):
        for _fn in os.listdir(_src_assets):
            _sp = os.path.join(_src_assets, _fn)
            _dp = os.path.join(DATA_DIR, 'assets', _fn)
            if os.path.isfile(_sp) and not os.path.isfile(_dp):
                with open(_sp, 'rb') as f:
                    _b = f.read()
                with open(_dp, 'wb') as f:
                    f.write(_b)
else:
    DATA_DIR = ROOT

DATA = os.path.join(DATA_DIR, 'data.json')
ASSETS = os.path.join(DATA_DIR, 'assets')
ADMIN_PASS = os.environ.get('CHITU_ADMIN_PASS', 'chitu2026')


# 源码中由构建脚本生成的多语言子树（en=英文，zhHant=繁体中文），始终以源码为准同步到线上数据。
# 这样无论是否启用持久卷（CHITU_DATA_DIR），多语言内容都跟随最新部署，且后台只编辑中文不会丢失。
SYNC_LANGS = ['en', 'zhHant']


def _sync_langs():
    src = os.path.join(ROOT, 'data.json')
    if not os.path.isfile(src):
        return
    try:
        with open(src, 'r', encoding='utf-8') as f:
            src_data = json.load(f)
    except Exception:
        return
    if os.path.isfile(DATA):
        try:
            with open(DATA, 'r', encoding='utf-8') as f:
                d = json.load(f)
        except Exception:
            d = {}
    else:
        d = {}
    changed = False
    for lang in SYNC_LANGS:
        sub = src_data.get(lang)
        if not sub:
            continue
        if d.get(lang) == sub:
            continue
        d[lang] = sub
        changed = True
        print(' 已同步 %s 子树 -> %s' % (lang, DATA))
    if changed:
        try:
            tmp = DATA + '.tmp'
            with open(tmp, 'w', encoding='utf-8') as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
            os.replace(tmp, DATA)
        except Exception as e:
            print(' [warn] 无法同步语言子树到 %s: %s' % (DATA, e))


_sync_langs()


def _app_version():
    """基于静态资源修改时间生成版本号，用于 script.js / styles.css 的缓存击穿，
    确保每次部署后浏览器/CDN 拉取最新前端资源。"""
    try:
        return str(int(max(os.path.getmtime(os.path.join(ROOT, 'script.js')),
                            os.path.getmtime(os.path.join(ROOT, 'styles.css')))))
    except Exception:
        return '1'


APP_VERSION = _app_version()

# 站点正式域名（用于 sitemap.xml 的绝对地址），可用环境变量覆盖
SITE_BASE = os.environ.get('CHITU_SITE_BASE', 'https://keyteam.work').rstrip('/') + '/'


def build_sitemap():
    """动态生成 sitemap.xml（首页 / 门店 / 补贴页），始终与线上数据一致。"""
    urls = [SITE_BASE]
    try:
        with open(DATA, 'r', encoding='utf-8') as f:
            d = json.load(f)
        for loc in d.get('locations', []):
            slug = loc.get('slug')
            if slug:
                urls.append('%sstore-%s.html' % (SITE_BASE, slug))
        for sub in d.get('subsidies', []):
            slug = sub.get('slug')
            if slug:
                urls.append('%ssubsidy-%s.html' % (SITE_BASE, slug))
    except Exception:
        pass
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        lines.append('  <url><loc>%s</loc><changefreq>weekly</changefreq>'
                     '<priority>0.8</priority></url>' % u)
    lines.append('</urlset>')
    return '\n'.join(lines)


# 允许上传的图片扩展名
ALLOWED_EXT = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.svg', '.avif'}
SAFE_NAME = re.compile(r'^[A-Za-z0-9_.-]+$')

# 全局灯箱（lightbox）：点击前台任意内容图，全屏按原图分辨率查看。
# 通过事件委托生效，兼容首页 JS 动态渲染的图（带 data-cls）与门店详情页静态图。
_LIGHTBOX_HTML = (
    '<style>'
    '.lb-overlay{position:fixed;inset:0;background:rgba(8,20,15,.92);display:none;'
    'align-items:center;justify-content:center;z-index:99999;cursor:zoom-out;padding:20px}'
    '.lb-overlay.open{display:flex}'
    '.lb-overlay img{max-width:96vw;max-height:96vh;object-fit:contain;'
    'box-shadow:0 12px 60px rgba(0,0,0,.6);background:#fff}'
    '.lb-hint{position:fixed;left:0;right:0;bottom:16px;text-align:center;color:#fff;'
    'font-size:13px;opacity:.65;z-index:100000;pointer-events:none}'
    '</style>'
    '<div class="lb-overlay" id="lbOverlay"><img id="lbImg" alt=""><div class="lb-hint">点击任意处关闭 · 原图分辨率</div></div>'
    '<script>'
    '(function(){'
    "var SEL='[data-cls], .room-thumb img, .store-hero-img';"
    "document.addEventListener('click',function(e){"
    'var img=e.target.closest(SEL);'
    "if(!img||img.closest('.lb-overlay'))return;"
    'e.preventDefault();'
    "var ov=document.getElementById('lbOverlay');"
    "document.getElementById('lbImg').src=img.currentSrc||img.src;"
    "ov.classList.add('open');"
    '});'
    "document.getElementById('lbOverlay').addEventListener('click',function(){this.classList.remove('open');});"
    '})();'
    '</script>'
)


class Handler(SimpleHTTPRequestHandler):
    server_version = 'ChituSite/1.1'

    def _send(self, code, body, ctype='application/json; charset=utf-8'):
        if isinstance(body, str):
            body = body.encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def _auth(self):
        return self.headers.get('X-Admin-Password') == ADMIN_PASS

    def _inject(self, html):
        """在 HTML 末尾注入全局灯箱资源（仅作用于前台页面）。"""
        if isinstance(html, bytes):
            html = html.decode('utf-8')
        if '</body>' in html:
            return html.replace('</body>', _LIGHTBOX_HTML + '</body>', 1)
        return html + _LIGHTBOX_HTML

    def _serve_file(self, path, ctype):
        try:
            with open(path, 'rb') as f:
                body = f.read()
            self.send_response(200)
            self.send_header('Content-Type', ctype)
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except OSError:
            self._send(404, json.dumps({'error': 'not found'}))

    def do_GET(self):
        p = urlparse(self.path).path
        if p == '/sitemap.xml':
            return self._send(200, build_sitemap(), 'application/xml; charset=utf-8')
        if p in ('/admin', '/admin/'):
            return self._serve_file(os.path.join(ROOT, 'admin.html'), 'text/html; charset=utf-8')
        if p in ('/', '/index.html'):
            idx = os.path.join(ROOT, 'index.html')
            try:
                with open(idx, 'r', encoding='utf-8') as f:
                    html = f.read()
            except OSError:
                return self._send(404, json.dumps({'error': 'not found'}))
            html = html.replace('src="script.js"', 'src="script.js?v=%s"' % APP_VERSION)
            html = html.replace('href="styles.css"', 'href="styles.css?v=%s"' % APP_VERSION)
            return self._send(200, self._inject(html), 'text/html; charset=utf-8')
        if p == '/api/status':
            # 后台用此接口判断是否启用了持久化（CHITU_DATA_DIR 指向持久卷）
            persisted = bool(os.environ.get('CHITU_DATA_DIR'))
            return self._send(200, json.dumps({'persisted': persisted}), 'application/json; charset=utf-8')
        if p == '/api/content':
            try:
                with open(DATA, 'rb') as f:
                    body = f.read()
                return self._send(200, body, 'application/json; charset=utf-8')
            except OSError as e:
                return self._send(500, json.dumps({'error': str(e)}))

        # 门店 / 企业补贴 详情页：按需用最新数据动态生成
        m = re.match(r'^/(store|subsidy)-([A-Za-z0-9_-]+)\.html$', p)
        if m:
            kind, slug = m.group(1), m.group(2)
            try:
                with open(DATA, 'r', encoding='utf-8') as f:
                    d = json.load(f)
            except OSError:
                return self._send(404, json.dumps({'error': 'not found'}))
            item = None
            if kind == 'store':
                item = next((x for x in d.get('locations', []) if x.get('slug') == slug), None)
            else:
                item = next((x for x in d.get('subsidies', []) if x.get('slug') == slug), None)
            if not item:
                return self._send(404, json.dumps({'error': 'not found'}))
            html = build.render_store_page(item, d, APP_VERSION) if kind == 'store' else build.render_subsidy_page(item, d, APP_VERSION)
            return self._send(200, self._inject(html), 'text/html; charset=utf-8')
        # 持久化 assets（上传的图片在 DATA_DIR/assets）优先于源码 assets
        if p.startswith('/assets/') and DATA_DIR != ROOT:
            cand = os.path.join(DATA_DIR, p.lstrip('/'))
            if os.path.isfile(cand):
                return self._serve_file(cand, mimetypes.guess_type(cand)[0] or 'application/octet-stream')
        return super().do_GET()

    def do_POST(self):
        p = urlparse(self.path).path
        if p == '/api/check':
            if self._auth():
                return self._send(200, json.dumps({'ok': True}))
            return self._send(401, json.dumps({'error': '密码错误'}))
        if p == '/api/content':
            if not self._auth():
                return self._send(401, json.dumps({'error': '密码错误'}))
            length = int(self.headers.get('Content-Length', 0) or 0)
            raw = self.rfile.read(length)
            try:
                json.loads(raw)  # 校验是否为合法 JSON
                # 保存前自动备份当前版本（防止误操作/覆盖，保留最近 50 份）
                try:
                    if os.path.isfile(DATA):
                        bdir = os.path.join(DATA_DIR, 'backups')
                        os.makedirs(bdir, exist_ok=True)
                        bpath = os.path.join(bdir, 'data-%s.json' % time.strftime('%Y%m%d-%H%M%S'))
                        shutil.copy2(DATA, bpath)
                        olds = sorted(x for x in os.listdir(bdir)
                                      if x.startswith('data-') and x.endswith('.json'))
                        for x in olds[:-50]:
                            try:
                                os.remove(os.path.join(bdir, x))
                            except OSError:
                                pass
                except Exception as e:
                    print(' [warn] 保存前备份失败: %s' % e)
                tmp = DATA + '.tmp'
                with open(tmp, 'wb') as f:
                    f.write(raw)
                os.replace(tmp, DATA)
                return self._send(200, json.dumps({'ok': True}))
            except Exception as e:
                return self._send(400, json.dumps({'error': '保存失败：' + str(e)}))
        if p == '/api/upload':
            if not self._auth():
                return self._send(401, json.dumps({'error': '密码错误'}))
            fn = os.path.basename(self.headers.get('X-Filename', ''))
            if not SAFE_NAME.match(fn):
                return self._send(400, json.dumps({'error': '文件名不合法'}))
            ext = os.path.splitext(fn)[1].lower()
            if ext not in ALLOWED_EXT:
                return self._send(400, json.dumps({'error': '不支持的图片格式'}))
            length = int(self.headers.get('Content-Length', 0) or 0)
            data = self.rfile.read(length)
            os.makedirs(ASSETS, exist_ok=True)
            with open(os.path.join(ASSETS, fn), 'wb') as f:
                f.write(data)
            return self._send(200, json.dumps({'ok': True, 'path': 'assets/' + fn}))
        return self._send(404, json.dumps({'error': 'not found'}))

    def log_message(self, *args):
        pass


def main():
    # 端口：云端平台注入 PORT，本地可用 CHITU_PORT 覆盖，默认 8080
    port = int(os.environ.get('PORT') or os.environ.get('CHITU_PORT', '8080'))
    os.chdir(ROOT)
    srv = ThreadingHTTPServer(('0.0.0.0', port), Handler)
    print('=' * 48)
    print(' 赤兔文创官网 · 后台服务已启动')
    print(' 官网地址 : http://localhost:%d/' % port)
    print(' 后台管理 : http://localhost:%d/admin' % port)
    print(' 后台密码 : %s' % ADMIN_PASS)
    print(' 数据目录 : %s' % DATA_DIR)
    print('=' * 48)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print('\n服务已停止')


if __name__ == '__main__':
    main()
