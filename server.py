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
import sys
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


def _sync_en():
    """en 是多语言翻译资产（由 make_en.py 基于中文源生成），始终以源码为准。
    这样无论是否启用持久卷（CHITU_DATA_DIR），线上英文内容都跟随最新部署，
    且后台只编辑中文、保存时不会丢失英文子树。"""
    src = os.path.join(ROOT, 'data.json')
    if not os.path.isfile(src):
        return
    try:
        with open(src, 'r', encoding='utf-8') as f:
            src_data = json.load(f)
    except Exception:
        return
    en = src_data.get('en')
    if not en:
        return
    if os.path.isfile(DATA):
        try:
            with open(DATA, 'r', encoding='utf-8') as f:
                d = json.load(f)
        except Exception:
            d = {}
    else:
        d = {}
    if d.get('en') == en:
        return
    d['en'] = en
    try:
        tmp = DATA + '.tmp'
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
        os.replace(tmp, DATA)
        print(' 已同步 en 子树 -> %s' % DATA)
    except Exception as e:
        print(' [warn] 无法同步 en 子树到 %s: %s' % (DATA, e))


_sync_en()

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
        if p in ('/admin', '/admin/'):
            return self._serve_file(os.path.join(ROOT, 'admin.html'), 'text/html; charset=utf-8')
        if p in ('/', '/index.html'):
            idx = os.path.join(ROOT, 'index.html')
            try:
                with open(idx, 'r', encoding='utf-8') as f:
                    html = f.read()
            except OSError:
                return self._send(404, json.dumps({'error': 'not found'}))
            return self._send(200, self._inject(html), 'text/html; charset=utf-8')
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
            html = build.render_store_page(item, d) if kind == 'store' else build.render_subsidy_page(item, d)
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
