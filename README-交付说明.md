# 赤兔官网（keyteam.work）— 源码交付说明

> 交付日期：2026-09-23 ｜ 线上地址：https://keyteam.work ｜ 后台：https://keyteam.work/admin
> 当前部署平台：Railway（git push 自动部署）｜ 代码仓库：github.com/m34108809-byte/chitu-website（main 分支）

## 一、项目概述

赤兔文创 / 赤兔 KEY TEAM 官网，单站点支持**简体中文 / 繁体中文 / English** 三语切换（前端无刷新切换，localStorage 记忆）。

- 首页：门店卡片、服务、企业补贴（4 张补贴页）、实景图库、FAQ、联系区块
- 门店详情页 ×4：如意坊 / 客村 / 鹭江 / 宝岗（store-ruyi / kecun / lujiang / baogang），含房型卡片、临租空间（会议室/茶室/课室 时租·半日·全日 + 美团入口）、补贴、表单
- 补贴详情页 ×4（subsidy-*.html）
- 管理后台 /admin：可视化编辑全部文案、房型、临租、价格、图片上传裁剪，无需改代码

## 二、文件结构

```
website/
├── server.py               # 后端服务（Python 标准库，无框架）：静态托管 + 动态渲染详情页 + REST API + 后台
├── build.py                # 静态构建：data.json → dist/（首页/详情页/补贴页/sitemap）
├── index.html              # 首页模板（构建输入）
├── admin.html              # 管理后台（单文件，内联 JS，登录密码见下）
├── script.js / styles.css  # 前端交互与样式（源文件，构建时复制进 dist 并加 ?v= 缓存戳）
├── data.json               # 全站数据（顶层=简体中文；en / zhHant = 英文/繁体平行子树）
├── room-translations.json  # 内置译文字典：房型 en（按 slug+中文房名）、临租 en（"_hourly" 键）
├── make_en.py / make_tw.py / make_hourly.py  # data.json 内容生成/更新脚本（历史工具）
├── requirements.txt        # 依赖：opencc-python-reimplemented（简转繁）
├── Procfile / railway.json / runtime.txt / vercel.json  # 部署配置
├── assets/                 # 图片源（logo、门店封面、图库、banner）
├── dist/                   # 构建产物（线上同款，可直接静态预览；实际线上由 server.py 动态渲染详情页）
└── backups-local/          # 历史数据备份快照（版本1-3，供参考数据结构）
```

## 三、本地运行

```bash
pip install -r requirements.txt
python server.py
# 默认 http://localhost:8080（端口：环境变量 PORT / CHITU_PORT）
# 后台登录密码：环境变量 CHITU_ADMIN_PASS，未设置时默认 chitu2026（上线务必修改）
# 数据目录：环境变量 CHITU_DATA_DIR，未设置时用代码同目录（本地开发即用项目根的 data.json）
```

构建静态版（可选，仅用于纯静态托管）：`python build.py` → 输出 dist/

## 四、部署（Railway）

1. 连接 GitHub 仓库，push main 自动部署（NIXPACKS 构建，startCommand: `python server.py`，健康检查 `/`）
2. **必须挂持久卷**：项目画布右键 Add Volume（或 Ctrl+K → Create Volume），服务选 web，挂载路径 `/data`
3. 代码自动识别卷：`CHITU_DATA_DIR` 环境变量**或** Railway 注入的 `RAILWAY_VOLUME_MOUNT_PATH`，二者任一存在即启用持久化（`/api/status` 可查 `persisted` 字段）
4. 建议设置 `CHITU_ADMIN_PASS` 环境变量改掉默认后台密码

## 五、关键机制（改代码前必读）

### 1. 三语数据模型
- `data.json` 顶层 = 简中；`en` / `zhHant` = 平行子树（结构同顶层）
- **后台只编辑中文层**；繁英由代码生成，不提供后台编辑
- 保存 / 启动时 `_sync_langs()`（server.py）：
  - en/zhHant 整树先以源码 data.json 为基准同步
  - `_sync_rooms_to_langs()` 再把**线上中文层**的 rooms / hourly / meituan 镜像过去：
    - zhHant：OpenCC s2t 逐字段转换
    - en：优先用 `room-translations.json` 译文字典（按中文房名/临租名匹配）→ 其次 imgKey 匹配 → 兜底显示中文（价格等中性字段始终实时跟随中文层）
  - **给技术人员：用户新起名字的房型/临租，英文页会暂显示中文，需把译文补进 room-translations.json**（keyed by slug + 中文名；临租放 "_hourly"）
- `SYNC_STORE_FIELDS`（hourly/meituan）：部署只补缺失、不覆盖线上已有内容 → **内容与部署分离，重新部署不会覆盖后台编辑**（曾因无持久卷丢失过数据，现已修）

### 2. 数据与备份
- 线上数据存持久卷 `/data/data.json` + `/data/assets/`（后台上传的图片）
- 每次后台保存前自动备份到数据卷 `backups/`（保留最近 50 份）
- admin 后台有「导出备份 / 导入恢复」按钮；`/api/status` 返回持久化与备份计数

### 3. 缓存
- script.js / styles.css 以 `?v=<文件mtime>` 注入版本号，改文件即自动破缓存

### 4. API 一览（server.py）
- `GET  /api/content` 全量数据 ｜ `POST /api/content` 保存（附 X-Admin-Token）
- `POST /api/upload` 图片上传（multipart，存数据卷 assets/）
- `GET  /api/status` 持久化/备份状态
- 门店详情页、补贴页由 server 按线上数据动态渲染（与 build.py 的静态渲染共享模板逻辑，**两处渲染有重复代码，优化可先合并**）

## 六、已知技术债 / 优化建议（按优先级）

1. **web 框架**：server.py 基于 http.server 手写路由，建议迁移 Flask/FastAPI；路由、鉴权、错误处理都会更稳
2. **鉴权**：后台为单密码（明文比对 X-Admin-Token），无用户/角色/CSRF 防护；建议加会话与 bcrypt
3. **渲染逻辑去重**：build.py 与 server.py 各有一套门店页渲染，改一处易漏另一处，建议抽公共模板模块或统一由动态渲染输出
4. **admin.html 单文件**：内联 JS 约 600 行，建议拆分模块 + 构建压缩
5. **图片**：上传图片无压缩/CDN，assets 与数据卷双轨（源码 assets + 上传 assets），建议统一对象存储 + CDN
6. **英文译文自动化**：room-translations.json 人工维护，可接翻译 API 兜底新词条
7. **测试**：无自动化测试，关键逻辑（_sync_langs 合并语义）建议补 pytest 用例——特别是「只补缺失不覆盖」与译文字典优先级
8. **SEO**：已有 sitemap.xml/robots.txt 动态输出；可再补 og meta、结构化数据

## 七、联系与上下文

- 内容运营方：赤兔文创（广州红杉投资）招商团队；网站主要给港澳台及外国创业者看
- 数据当前真实有效：四店房型（11/9/7/10）、临租报价、补贴政策（人社部门公开政策）
- backups-local/版本3-2026-08-23.json 为最近一次全量快照，可用「导入恢复」直接还原
