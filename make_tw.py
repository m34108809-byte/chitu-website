# -*- coding: utf-8 -*-
"""生成繁体中文子树（zhHant）。

将 data.json 顶层「简体中文」内容（除 images / en / zhHant 外）用 OpenCC 转为繁体，
写入 data['zhHant'] 平行子树，结构与 en 一致。后台编辑中文后，重跑本脚本即可同步繁体。

仅本地构建期使用（不依赖运行时），用带 opencc 的 Python 运行：
    python make_tw.py
"""
import json
import os

try:
    import opencc
except ImportError:
    raise SystemExit("需要 opencc：pip install opencc-python-reimplemented")

cc = opencc.OpenCC('s2t')
ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'data.json')

# 这些顶层键不参与转换（图片路径 / 英文 / 已有的繁体）
EXCLUDE = {'images', 'en', 'zhHant'}


def conv(v):
    if isinstance(v, str):
        return cc.convert(v)
    if isinstance(v, list):
        return [conv(x) for x in v]
    if isinstance(v, dict):
        return {k: conv(x) for k, x in v.items()}
    return v


def main():
    with open(SRC, encoding='utf-8') as f:
        d = json.load(f)
    zhHant = {}
    for k, v in d.items():
        if k in EXCLUDE:
            continue
        zhHant[k] = conv(v)
    d['zhHant'] = zhHant
    with open(SRC, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print("✅ zhHant 已生成，顶层键：", list(zhHant.keys()))
    print("   门店数:", len(zhHant.get('locations', [])),
          " | 补贴数:", len(zhHant.get('subsidies', [])),
          " | FAQ数:", len(zhHant.get('faqs', [])))


if __name__ == '__main__':
    main()
