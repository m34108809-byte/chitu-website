#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给四个门店注入「临租」数据（会议室/茶室/课室），并同步英文版。

临租价均为「美团团购参考价」，请以后台/美团商家后台实际价格为准。
meituan 字段默认指向美团搜索（占位），请替换为各店真实的美团商家页URL：
  美团App → 我的店铺 → 分享 → 复制链接。
"""
import json
import os
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, 'data.json')

# 各店临租（中文）。hourly=时租 halfDay=半日 fullDay=全日
HOURLY = {
    'ruyi': [
        {'cat': '会议室', 'name': '小型会议室', 'capacity': '4-6人', 'area': '约20㎡',
         'hourly': '¥80', 'halfDay': '¥300', 'fullDay': '¥500',
         'config': '高清投屏、白板、高速WiFi，适合商务洽谈与小团队会议。'},
        {'cat': '会议室', 'name': '中型会议室', 'capacity': '10-15人', 'area': '约35㎡',
         'hourly': '¥120', 'halfDay': '¥450', 'fullDay': '¥800',
         'config': 'LED屏、音响、麦克风，适合项目评审与路演。'},
        {'cat': '会议室', 'name': '大型会议室', 'capacity': '20-50人', 'area': '约70㎡',
         'hourly': '¥160', 'halfDay': '¥600', 'fullDay': '¥1100',
         'config': '全套影音设备，适合发布会、培训与大型会议。'},
        {'cat': '茶室', 'name': '新中式茶室包厢', 'capacity': '2-4人', 'area': '约15㎡',
         'hourly': '¥58', 'halfDay': '¥220', 'fullDay': '¥400',
         'config': '独立隔音、功夫茶具、免费茶叶，适合私密商务洽谈。'},
        {'cat': '课室', 'name': '培训课室', 'capacity': '20-40人', 'area': '约50㎡',
         'hourly': '¥100', 'halfDay': '¥380', 'fullDay': '¥700',
         'config': '课桌椅、投屏、白板，适合培训、沙龙与分享会。'},
    ],
    'kecun': [
        {'cat': '会议室', 'name': '小型会议室', 'capacity': '4-6人', 'area': '约20㎡',
         'hourly': '¥80', 'halfDay': '¥300', 'fullDay': '¥500',
         'config': '白板、投屏、高速WiFi，适合团队碰头与面试。'},
        {'cat': '会议室', 'name': '中型会议室', 'capacity': '10-15人', 'area': '约40㎡',
         'hourly': '¥120', 'halfDay': '¥450', 'fullDay': '¥800',
         'config': '音响、麦克风、LED屏，适合项目评审。'},
        {'cat': '会议室', 'name': '大型会议室（113㎡）', 'capacity': '30-80人', 'area': '约113㎡',
         'hourly': '¥180', 'halfDay': '¥700', 'fullDay': '¥1300',
         'config': '电竞/现代双风格，全套影音，适合发布会与大型活动。'},
        {'cat': '茶室', 'name': '新中式茶室包厢', 'capacity': '2-4人', 'area': '约15㎡',
         'hourly': '¥58', 'halfDay': '¥220', 'fullDay': '¥400',
         'config': '独立隔音、功夫茶具、免费茶叶，适合私密洽谈。'},
        {'cat': '课室', 'name': '培训课室', 'capacity': '20-40人', 'area': '约55㎡',
         'hourly': '¥100', 'halfDay': '¥380', 'fullDay': '¥700',
         'config': '课桌椅、投屏、白板，适合培训与分享会。'},
    ],
    'lujiang': [
        {'cat': '会议室', 'name': '小型会议室', 'capacity': '4-6人', 'area': '约18㎡',
         'hourly': '¥80', 'halfDay': '¥300', 'fullDay': '¥500',
         'config': '白板、投屏、高速WiFi，适合商务洽谈。'},
        {'cat': '会议室', 'name': '中型会议室', 'capacity': '10-15人', 'area': '约35㎡',
         'hourly': '¥120', 'halfDay': '¥450', 'fullDay': '¥800',
         'config': '音响、麦克风、投屏，适合评审与路演。'},
        {'cat': '茶室', 'name': '新中式茶室包厢', 'capacity': '2-4人', 'area': '约15㎡',
         'hourly': '¥58', 'halfDay': '¥220', 'fullDay': '¥400',
         'config': '独立隔音、功夫茶具、免费茶叶，适合私密会客。'},
        {'cat': '课室', 'name': '培训课室', 'capacity': '20-40人', 'area': '约50㎡',
         'hourly': '¥100', 'halfDay': '¥380', 'fullDay': '¥700',
         'config': '课桌椅、投屏、白板，适合培训、沙龙。'},
    ],
    'baogang': [
        {'cat': '会议室', 'name': '小型会议室', 'capacity': '4-6人', 'area': '约18㎡',
         'hourly': '¥70', 'halfDay': '¥260', 'fullDay': '¥450',
         'config': '白板、投屏、高速WiFi，适合商务洽谈（本店价格最优）。'},
        {'cat': '会议室', 'name': '中型会议室', 'capacity': '10-15人', 'area': '约35㎡',
         'hourly': '¥110', 'halfDay': '¥400', 'fullDay': '¥720',
         'config': '音响、麦克风、投屏，适合项目评审。'},
        {'cat': '茶室', 'name': '新中式茶室包厢', 'capacity': '2-4人', 'area': '约15㎡',
         'hourly': '¥50', 'halfDay': '¥190', 'fullDay': '¥360',
         'config': '独立隔音、功夫茶具、免费茶叶，适合私密会客。'},
        {'cat': '课室', 'name': '培训课室', 'capacity': '20-40人', 'area': '约50㎡',
         'hourly': '¥90', 'halfDay': '¥340', 'fullDay': '¥620',
         'config': '课桌椅、投屏、白板，适合培训、沙龙。'},
    ],
}

# 英文版（与中文平行）
HOURLY_EN = {
    'ruyi': [
        {'cat': 'Meeting Room', 'name': 'Small Meeting Room', 'capacity': '4-6 pax', 'area': '~20㎡',
         'hourly': '¥80', 'halfDay': '¥300', 'fullDay': '¥500',
         'config': 'HD screen, whiteboard and high-speed WiFi — ideal for talks and small-team meetings.'},
        {'cat': 'Meeting Room', 'name': 'Medium Meeting Room', 'capacity': '10-15 pax', 'area': '~35㎡',
         'hourly': '¥120', 'halfDay': '¥450', 'fullDay': '¥800',
         'config': 'LED screen, audio and mics — good for reviews and pitches.'},
        {'cat': 'Meeting Room', 'name': 'Large Meeting Room', 'capacity': '20-50 pax', 'area': '~70㎡',
         'hourly': '¥160', 'halfDay': '¥600', 'fullDay': '¥1100',
         'config': 'Full AV setup — for launches, training and large meetings.'},
        {'cat': 'Tea Room', 'name': 'New-Chinese Tea Room', 'capacity': '2-4 pax', 'area': '~15㎡',
         'hourly': '¥58', 'halfDay': '¥220', 'fullDay': '¥400',
         'config': 'Soundproof, kung-fu tea set and free tea — for private business talks.'},
        {'cat': 'Training Room', 'name': 'Training Room', 'capacity': '20-40 pax', 'area': '~50㎡',
         'hourly': '¥100', 'halfDay': '¥380', 'fullDay': '¥700',
         'config': 'Desks, screen and whiteboard — for training, salons and meetups.'},
    ],
    'kecun': [
        {'cat': 'Meeting Room', 'name': 'Small Meeting Room', 'capacity': '4-6 pax', 'area': '~20㎡',
         'hourly': '¥80', 'halfDay': '¥300', 'fullDay': '¥500',
         'config': 'Whiteboard, screen and WiFi — for standups and interviews.'},
        {'cat': 'Meeting Room', 'name': 'Medium Meeting Room', 'capacity': '10-15 pax', 'area': '~40㎡',
         'hourly': '¥120', 'halfDay': '¥450', 'fullDay': '¥800',
         'config': 'Audio, mics and LED screen — for reviews.'},
        {'cat': 'Meeting Room', 'name': 'Large Meeting Room (113㎡)', 'capacity': '30-80 pax', 'area': '~113㎡',
         'hourly': '¥180', 'halfDay': '¥700', 'fullDay': '¥1300',
         'config': 'Modern / esports dual style, full AV — for launches and big events.'},
        {'cat': 'Tea Room', 'name': 'New-Chinese Tea Room', 'capacity': '2-4 pax', 'area': '~15㎡',
         'hourly': '¥58', 'halfDay': '¥220', 'fullDay': '¥400',
         'config': 'Soundproof, kung-fu tea set and free tea — for private talks.'},
        {'cat': 'Training Room', 'name': 'Training Room', 'capacity': '20-40 pax', 'area': '~55㎡',
         'hourly': '¥100', 'halfDay': '¥380', 'fullDay': '¥700',
         'config': 'Desks, screen and whiteboard — for training and meetups.'},
    ],
    'lujiang': [
        {'cat': 'Meeting Room', 'name': 'Small Meeting Room', 'capacity': '4-6 pax', 'area': '~18㎡',
         'hourly': '¥80', 'halfDay': '¥300', 'fullDay': '¥500',
         'config': 'Whiteboard, screen and WiFi — for business talks.'},
        {'cat': 'Meeting Room', 'name': 'Medium Meeting Room', 'capacity': '10-15 pax', 'area': '~35㎡',
         'hourly': '¥120', 'halfDay': '¥450', 'fullDay': '¥800',
         'config': 'Audio, mics and screen — for reviews and pitches.'},
        {'cat': 'Tea Room', 'name': 'New-Chinese Tea Room', 'capacity': '2-4 pax', 'area': '~15㎡',
         'hourly': '¥58', 'halfDay': '¥220', 'fullDay': '¥400',
         'config': 'Soundproof, kung-fu tea set and free tea — for private meetings.'},
        {'cat': 'Training Room', 'name': 'Training Room', 'capacity': '20-40 pax', 'area': '~50㎡',
         'hourly': '¥100', 'halfDay': '¥380', 'fullDay': '¥700',
         'config': 'Desks, screen and whiteboard — for training and salons.'},
    ],
    'baogang': [
        {'cat': 'Meeting Room', 'name': 'Small Meeting Room', 'capacity': '4-6 pax', 'area': '~18㎡',
         'hourly': '¥70', 'halfDay': '¥260', 'fullDay': '¥450',
         'config': 'Whiteboard, screen and WiFi — for talks (best value here).'},
        {'cat': 'Meeting Room', 'name': 'Medium Meeting Room', 'capacity': '10-15 pax', 'area': '~35㎡',
         'hourly': '¥110', 'halfDay': '¥400', 'fullDay': '¥720',
         'config': 'Audio, mics and screen — for reviews.'},
        {'cat': 'Tea Room', 'name': 'New-Chinese Tea Room', 'capacity': '2-4 pax', 'area': '~15㎡',
         'hourly': '¥50', 'halfDay': '¥190', 'fullDay': '¥360',
         'config': 'Soundproof, kung-fu tea set and free tea — for private meetings.'},
        {'cat': 'Training Room', 'name': 'Training Room', 'capacity': '20-40 pax', 'area': '~50㎡',
         'hourly': '¥90', 'halfDay': '¥340', 'fullDay': '¥620',
         'config': 'Desks, screen and whiteboard — for training and salons.'},
    ],
}

# 美团团购入口（占位：美团搜索）。请替换为各店真实商家页URL。
MEITUAN = {
    'ruyi': 'https://www.meituan.com/search/?query=' + quote('赤兔如意港 会议室'),
    'kecun': 'https://www.meituan.com/search/?query=' + quote('赤兔数字港 会议室'),
    'lujiang': 'https://www.meituan.com/search/?query=' + quote('赤兔联合办公鹭江 会议室'),
    'baogang': 'https://www.meituan.com/search/?query=' + quote('企程创意空间 会议室'),
}


def main():
    with open(DATA, encoding='utf-8') as f:
        data = json.load(f)
    for loc in data.get('locations', []):
        slug = loc.get('slug')
        if slug in HOURLY:
            loc['hourly'] = HOURLY[slug]
            loc['meituan'] = MEITUAN[slug]
    # 英文同步
    en = data.get('en')
    if en:
        for loc in en.get('locations', []):
            slug = loc.get('slug')
            if slug in HOURLY_EN:
                loc['hourly'] = HOURLY_EN[slug]
                loc['meituan'] = MEITUAN[slug]
    with open(DATA, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print('✅ 临租数据已注入，四店 hourly 条数:',
          {s: len(HOURLY[s]) for s in HOURLY})
    print('   en 同步:', all(s in [l.get('slug') for l in data['en']['locations']] for s in HOURLY_EN))


if __name__ == '__main__':
    main()
