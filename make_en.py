#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成英文版 en 子树并合并进 data.json（中文保持顶层、images 共享）。"""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, 'data.json')

EN = {
    'brand': {
        'name': 'Chitu KEY TEAM · Creative Workspace Community',
        'wechat': '18903005927',
    },
    'hero': {
        'title': 'Chitu KEY TEAM · More Than an Office — A Business Growth Ecosystem',
        'subtitle': 'Move-in Ready · Furnished · 360° Growth Engine',
        'lead': 'We serve startups, small businesses, freelancers and corporate clients with end-to-end business services — workspace, company registration, tax & accounting, and foreign-visa assistance. Four locations across Haizhu District — pick the one nearest you.',
        'cta1': {'text': 'View Locations', 'href': '#locations'},
        'cta2': {'text': 'Call Us', 'href': 'tel:18903005927'},
        'meta': [
            {'pre': '', 'bold': 'Workstations / tea rooms / reception / lobby / common areas / meeting rooms / coffee bar', 'post': 'all included'},
            {'pre': '', 'bold': '24/7', 'post': 'private A/C & high-speed internet'},
            {'pre': 'Register your ', 'bold': 'company address', 'post': ''},
        ],
        'bgImages': [
            {'imgKey': 'bg1', 'label': 'Homepage background 1'},
            {'imgKey': 'bg2', 'label': 'Homepage background 2'},
            {'imgKey': 'bg3', 'label': 'Homepage background 3'},
        ],
    },
    'featuresHeader': {
        'title': 'Why Chitu KEY TEAM',
        'sub': 'Leave the hassle to us, keep your focus on the business',
    },
    'features': [
        {'icon': 'layers', 'title': 'Move-in Ready', 'desc': '24/7 A/C, property management, gigabit internet and cleaning — all included with no hidden fees, so your budget stays clear.'},
        {'icon': 'box', 'title': 'Furnished & Ready', 'desc': 'Fully furnished and finished — start working the day you sign, and register your company here.'},
        {'icon': 'users', 'title': 'Shared Spaces', 'desc': 'Meeting rooms, tea rooms, pantry, printing and front-desk mail handling — fully equipped to lower your operating costs.'},
        {'icon': 'clock', 'title': '24/7 Access', 'desc': 'Private A/C and high-speed internet available around the clock, flexibly matching your work rhythm.'},
        {'icon': 'shield', 'title': '360° Growth Engine', 'desc': 'Company registration, tax & accounting, policy subsidies and funding connections — supporting your business from 0 to 1.'},
        {'icon': 'map-pin', 'title': 'Multi-Location Network', 'desc': 'Four venues across Haizhu District (Xiaogang / Kecun / Lujiang / Baogang) — choose the nearest and switch freely.'},
    ],
    'locationsHeader': {
        'title': 'Four Locations in Haizhu',
        'sub': 'There is always one near you',
    },
    'locations': [
        {
            'imgKey': 'loc1', 'tag': 'Xiaogang', 'name': 'Chitu Ruyi Port',
            'addr': '5F-6F, No.271 Changgang East Rd, Haizhu District',
            'position': 'Exit A, Xiaogang Station (Line 8), 1-min walk',
            'metro': 'Exit A, Xiaogang Station (Line 8), 1-min walk',
            'priceLabel': 'Private Office', 'price': '¥980', 'priceUnit': '/mo',
            'highlights': [
                'New-Chinese-style soundproof tea room with kung-fu tea set and screen-sharing whiteboard',
                'Large meeting room (20-70 pax) with LED screen / audio / microphones',
                'Rent from 1 hour, self-check-in by QR code',
            ],
            'contact': 'Mr. Li', 'phone': '18102220465', 'slug': 'ruyi',
            'detail': 'Chitu Ruyi Port is located on 5F-6F, No.271 Changgang East Rd, Haizhu District, with convenient transport (Exit A, Xiaogang Station Line 8, 1-min walk). It is one of the co-working communities under Chitu KEY TEAM. The space is move-in ready and fully furnished — start working upon signing and register your company here. Equipped with meeting rooms, tea rooms, shared common areas and high-speed internet, with dedicated advisors providing one-stop company registration, tax & accounting, policy subsidies and business services.',
            'rooms': [
                {'name': 'Open Workspace', 'area': '~12㎡', 'capacity': '1 person', 'price': '¥500', 'unit': '/person/mo',
                 'config': 'Private desk + ergonomic chair; 2 free meeting-room hours monthly; access to lounge and free tea.'},
                {'name': 'Private Office', 'area': '~25㎡', 'capacity': '3-4 people', 'price': '¥980', 'unit': '/room/mo',
                 'config': 'Lockable door, company-registration ready, with desks and filing cabinet — ideal for startups to move in directly.'},
            ],
        },
        {
            'imgKey': 'loc2', 'tag': 'Kecun', 'name': 'Chitu Digital Port',
            'addr': "Above Agricultural Bank, No.302 Xin'gang Middle Rd, Haizhu District",
            'position': 'Exit D, Kecun Station (Line 3/8), 5-min walk',
            'metro': 'Exit D, Kecun Station (Line 3/8), 5-min walk',
            'priceLabel': '4-Person Office', 'price': '¥2800', 'priceUnit': '/mo',
            'highlights': [
                'Most layout options (4-10 pax and a 113㎡ large space)',
                'Large meeting rooms in modern / esports style, with whiteboard / mic / presenter remote',
                "'Pretend-to-work' day pass about ¥40/day",
            ],
            'contact': 'Mr. Guo', 'phone': '18102586047', 'slug': 'kecun',
            'detail': 'Chitu Digital Port is located above the Agricultural Bank, No.302 Xin\'gang Middle Rd, Haizhu District, with convenient transport (Exit D, Kecun Station Line 3/8, 5-min walk). It is one of the co-working communities under Chitu KEY TEAM. The space is move-in ready and fully furnished — start working upon signing and register your company here. Equipped with meeting rooms, tea rooms, shared common areas and high-speed internet, with dedicated advisors providing one-stop company registration, tax & accounting, policy subsidies and business services.',
            'rooms': [
                {'name': 'Open Workspace', 'area': '~12㎡', 'capacity': '1 person', 'price': '¥600', 'unit': '/person/mo',
                 'config': 'Window-side desk + ergonomic chair; access to lounge and free tea.'},
                {'name': '4-Person Office', 'area': '~30㎡', 'capacity': '4 people', 'price': '¥2800', 'unit': '/room/mo',
                 'config': 'Lockable door, company-registration ready, with 4 desks and filing cabinet — ideal for small teams.'},
            ],
        },
        {
            'imgKey': 'loc3', 'tag': 'Lujiang', 'name': 'Chitu Co-working (Lujiang)',
            'addr': '2F, No.64 Xiadu Rd',
            'position': 'Exit D, Lujiang Station (Line 8), ~200m',
            'metro': 'Exit D, Lujiang Station (Line 8), ~200m',
            'priceLabel': 'Private Office', 'price': '¥800', 'priceUnit': '/mo',
            'highlights': [
                'Convenient transport, 2-min walk',
                "'Pretend-to-work' desk long-term about ¥800/month",
                'Free tea / rest area / item storage / smart access',
            ],
            'contact': 'Ms. Zhang', 'phone': '13378682992', 'slug': 'lujiang',
            'detail': 'Chitu Co-working (Lujiang) is located on 2F, No.64 Xiadu Rd, with convenient transport (Exit D, Lujiang Station Line 8, ~200m). It is one of the co-working communities under Chitu KEY TEAM. The space is move-in ready and fully furnished — start working upon signing and register your company here. Equipped with meeting rooms, tea rooms, shared common areas and high-speed internet, with dedicated advisors providing one-stop company registration, tax & accounting, policy subsidies and business services.',
            'rooms': [
                {'name': 'Open Workspace', 'area': '~12㎡', 'capacity': '1 person', 'price': '¥500', 'unit': '/person/mo',
                 'config': 'Private desk + ergonomic chair; 2 free meeting-room hours monthly; access to lounge.'},
                {'name': 'Private Office', 'area': '~25㎡', 'capacity': '3-4 people', 'price': '¥980', 'unit': '/room/mo',
                 'config': 'Lockable door, company-registration ready, with desks and filing cabinet, near Lujiang Station.'},
            ],
        },
        {
            'imgKey': 'loc4', 'tag': 'Baogang', 'name': 'Qicheng Creative Space',
            'addr': '2F, Baogang Building, No.248 Baogang Rd',
            'position': 'Exit A, Fenghuang Xincun Station (Line 8), 10-min walk',
            'metro': 'Exit A, Fenghuang Xincun Station (Line 8), 10-min walk',
            'priceLabel': 'Single Room', 'price': '¥800', 'priceUnit': '/mo',
            'highlights': [
                'Lowest price among the four venues, best value',
                'Company & tax services: registration, clearing abnormal status, various licenses',
                'Near Jiangnanxi commercial area, private offices',
            ],
            'contact': 'Mr. Huang', 'phone': '19002093728', 'slug': 'baogang',
            'detail': 'Qicheng Creative Space is located on 2F, Baogang Building, No.248 Baogang Rd, with convenient transport (Exit A, Fenghuang Xincun Station Line 8, 10-min walk). It is one of the co-working communities under Chitu KEY TEAM. The space is move-in ready and fully furnished — start working upon signing and register your company here. Equipped with meeting rooms, tea rooms, shared common areas and high-speed internet, with dedicated advisors providing one-stop company registration, tax & accounting, policy subsidies and business services.',
            'rooms': [
                {'name': 'Open Workspace', 'area': '~12㎡', 'capacity': '1 person', 'price': '¥500', 'unit': '/person/mo',
                 'config': 'Private desk + ergonomic chair; 2 free meeting-room hours monthly; access to lounge and free tea.'},
            ],
        },
    ],
    'galleryHeader': {
        'title': 'Gallery',
        'sub': 'Comfortable spaces with bright, open working atmosphere',
    },
    'gallery': [
        {'imgKey': 'g1', 'label': 'Open Workspace', 'span': True},
        {'imgKey': 'g2', 'label': 'Private Office', 'span': False},
        {'imgKey': 'g3', 'label': 'Meeting Room', 'span': False},
        {'imgKey': 'g4', 'label': 'Tea Room', 'span': False},
        {'imgKey': 'g5', 'label': 'Lounge / Reception', 'span': True},
        {'imgKey': 'g6', 'label': 'Pitch / Event Area', 'span': False},
    ],
    'servicesHeader': {
        'title': 'Spaces & Services',
        'sub': 'More than a desk — your backbone for business growth',
    },
    'services': [
        {'icon': 'desk', 'title': 'Flexible Desk', 'desc': 'Day pass about ¥40/day; long-term desk about ¥800/person/mo — ideal for freelancers, exam prep and startups.'},
        {'icon': 'office', 'title': 'Private Office', 'desc': 'From 1-person to 113㎡ layouts, fully furnished and company-registration ready, move-in ready with no hidden fees.'},
        {'icon': 'meeting', 'title': 'Meeting Rooms', 'desc': 'Small (4-10 pax) ¥99/hr, medium (10-15 pax) ¥129/hr, large (20-70 pax) ¥159/hr — all with whiteboard, projector or LED screen.'},
        {'icon': 'tea', 'title': 'Tea Room', 'desc': '¥58/hr, quiet and elegant, with kung-fu tea set and free tea — ideal for business talks.'},
        {'icon': 'doc', 'title': 'Company & Tax Services', 'desc': 'Company registration, clearing abnormal status, and licenses for import/export, food, medical, labor dispatch, etc.'},
        {'icon': 'money', 'title': 'Policy & Funding', 'desc': 'Subsidy application support and funding connections to lower startup costs and accelerate growth.'},
        {'icon': 'visa', 'title': 'Foreign-Investment & Visa Services', 'desc': 'Foreign company registration, representative office setup, work/business visa assistance for foreigners, residence-permit extension and change — helping foreign talent and companies land in Guangzhou.'},
        {'icon': 'doc', 'title': 'Business Networking & Salons', 'desc': 'Regular and ad-hoc salons each month to foster resource integration, gathering members of the Greater Bay Area chambers of commerce — over a thousand enterprises meet at Chitu for business exchange, paving the way for your venture.'},
    ],
    'faqHeader': {
        'title': 'FAQ',
        'sub': 'What you may want to know before renting',
    },
    'faqs': [
        {'q': 'What is the move-in / signing process?', 'a': 'Viewing → signing (company registration available) → move in. Choose any of the four venues; actual availability is subject to real-time vacancies.'},
        {'q': 'What is included in the rent?', 'a': 'All-inclusive: water, A/C installation, property management, internet and cleaning are all free, with no hidden fees. Some value-added services (e.g. meeting rooms, tea rooms billed by time) are settled separately.'},
        {'q': 'Can you issue invoices?', 'a': 'Rent invoices available — general invoice ~6% / special invoice ~10% (subject to each venue\'s actual policy).'},
        {'q': 'Is a deposit required?', 'a': 'Deposit terms follow each venue\'s signing policy; the industry norm is two months\' deposit plus one month in advance. Confirm with the venue when viewing.'},
        {'q': 'Can I register a company here?', 'a': 'Yes. Chitu KEY TEAM provides a registered address and company/tax services. All are proper property certificates filed with the subdistrict office, enabling import/export, food, medical, labor dispatch, hazardous-chemical, publication and medical-device permits, etc.'},
        {'q': 'What amenities are included?', 'a': 'Tea rooms, meeting rooms, interview rooms, outdoor garden, smart locks, reception, negotiation rooms, pantry and coffee bar.'},
    ],
    'contact': {
        'title': 'Find the workspace that fits you — now',
        'sub': 'Add WeChat for real photos, vacancy shots and latest offers',
        'btnText': 'WeChat / Tel: 18903005927',
        'btnHref': 'tel:18903005927',
        'note': 'One WeChat ID for all; add it and a dedicated advisor will walk you through each venue\'s address and availability in detail.',
    },
    'footer': {
        'brand': 'Business Ecosystem Engine · Move-in Ready · Creative Workspace Community',
        'links': [
            {'text': 'About', 'href': '#about'},
            {'text': 'Locations', 'href': '#locations'},
            {'text': 'Spaces & Services', 'href': '#services'},
            {'text': 'FAQ', 'href': '#faq'},
            {'text': 'Subsidies', 'href': '#subsidy'},
        ],
        'contactTitle': 'Contact Us',
        'contacts': [
            'WeChat: 18903005927',
            'Service area: Haizhu District, Guangzhou (Xiaogang / Kecun / Lujiang / Baogang)',
        ],
        'copy': '© 2017 Chitu KEY TEAM · A brand of Guangzhou Redwood Cloud Technology Co., Ltd.',
    },
    'subsidyHeader': {
        'title': 'Business Subsidies',
        'sub': 'Government startup & employment subsidy application support — Chitu helps organize your documents for compliant claims and lower costs.',
    },
    'subsidies': [
        {
            'tag': 'Startup Grant', 'name': 'One-time Startup Grant', 'slug': 'startup-grant', 'imgKey': 'sub1',
            'summary': 'A one-time ¥10,000 startup grant for eligible legal representatives of newly registered startups, easing early-stage costs — no repayment required.',
            'policy': 'Policy basis: "Guangdong Employment and Entrepreneurship Subsidy Guidelines (2026 Revision)" (Yue Ren She Gui [2026] No.20), issued by the Guangdong Dept. of Human Resources & Social Security and the Dept. of Finance, effective June 17, 2026 for 5 years. Online filing via the Guangdong Public Employment Service Cloud Platform.',
            'object': '"Key supported entrepreneurship groups" who founded a startup in our province and serve as its legal representative / operator.',
            'objectDetail': 'Key supported entrepreneurship groups (below statutory retirement age, not yet receiving basic pension, meeting any one of the following):\n1. Students from regular universities, vocational and technical schools (enrolled or within 5 years of graduation) and overseas returnees within 5 years of graduation;\n2. Veterans;\n3. Registered unemployed persons in the province;\n4. Recognized employment-disadvantaged persons in the province;\n5. Returning entrepreneurs (three categories);\n6. Hong Kong, Macao and Taiwan residents under 45.',
            'standard': 'One-time ¥10,000.',
            'standardDetail': 'The same person and same startup entity may receive this subsidy only once; no repayment required.',
            'conditions': [
                'Startup entity: a micro/small enterprise, individual business, social organization, law firm, accounting firm or farmers\' cooperative registered in our province within 3 years, where you serve as legal representative / operator / responsible person.',
                'Registered for at least 12 months and not listed in the "Abnormal Operation List" by market regulators at application time.',
                'Normal operation for 6 consecutive months before applying, with at least 1 employee (other than the entrepreneur) paying social insurance per regulations.',
                'Note: entities that changed their legal representative cannot apply; applications are rejected if the applicant is covered by employer pension insurance at a unit not under their own name.',
            ],
            'materials': [
                'Basic identity proof of the eligible person.',
                'Supporting documents for the key supported group (e.g., graduation certificate for graduates, academic credential certification for returnees, veteran / demobilization certificate for veterans, household register or Employment & Entrepreneurship Certificate / social-insurance records for returnees).',
                'Proof of normal operation in the last 6 months: provide fund flow plus at least one of payroll, financial statements, tax records, operating license, contracts or order records.',
                'Micro/small enterprise proof: the "Basic Information of Surveyed Units" form (No. 101-1), or an "Enterprise Type Commitment Letter" if not within the reporting scope.',
            ],
            'process': [
                'Prepare business license, identity proof, key-group supporting docs and normal-operation proof.',
                'Apply online via the Guangdong Public Employment Service Cloud Platform (ggfw.hrss.gd.gov.cn) or submit to the local human-resources department / public employment service agency.',
                'District public employment agency and district HR bureau accept and review.',
                'Public notice of approved applicants.',
                'Subsidy funds transferred to the applicant\'s bank account.',
            ],
            'agency': 'Accepting agency: the district HR & social-security department / public employment service agency where the startup is registered.\nOnline filing: Guangdong Public Employment Service Cloud Platform https://ggfw.hrss.gd.gov.cn/employment/internet/portal/#/home\nDeadline: apply within 3 years from the startup\'s registration (for rent subsidy, the last application no later than 4 years from registration).',
            'company': [
                'Provide a compliant office address "ready for company registration" — lease contract matches the registration address, directly meeting the subsidy\'s hard venue requirement.',
                'One-stop company & tax services: business-license handling, bookkeeping and tax-record issuance, helping you prepare the "normal operation" proof.',
                'Dedicated park advisors help organize and pre-fill application documents and liaise with the subdistrict and HR departments to raise approval rates.',
                'Available upon move-in; get the address the same day at fastest, without delaying the "12 months from registration" clock.',
                'Note: subsidies are reviewed and paid by HR departments; final interpretation rests with the local HR department. Chitu provides the address and application assistance but does not guarantee approval.',
            ],
            'highlights': [
                'One-time payout, no repayment',
                'Can be combined with rent subsidy and job-creation subsidy',
                'Chitu helps organize application documents',
            ],
        },
        {
            'tag': 'Rent Subsidy', 'name': 'Startup Rent Subsidy', 'slug': 'rent-subsidy', 'imgKey': 'sub2',
            'summary': 'For eligible startups leasing a venue not under the founder\'s own name, a subsidy based on actual rent — up to ¥6,000/year in the Pearl River Delta, for up to 3 years.',
            'policy': 'Policy basis: "Guangdong Employment and Entrepreneurship Subsidy Guidelines (2026 Revision)" (Yue Ren She Gui [2026] No.20), issued by the Guangdong Dept. of Human Resources & Social Security and the Dept. of Finance, effective June 17, 2026 for 5 years. Online filing via the Guangdong Public Employment Service Cloud Platform.',
            'object': 'Legal representatives / operators of eligible startups who lease a venue not under their own name and belong to the "key supported entrepreneurship groups".',
            'objectDetail': 'Key supported entrepreneurship groups (below statutory retirement age, not yet receiving basic pension, meeting any one of the following):\n1. Students from regular universities, vocational and technical schools (enrolled or within 5 years of graduation) and overseas returnees within 5 years of graduation;\n2. Veterans;\n3. Registered unemployed persons in the province;\n4. Recognized employment-disadvantaged persons in the province;\n5. Returning entrepreneurs (three categories);\n6. Hong Kong, Macao and Taiwan residents under 45.',
            'standard': 'Up to ¥6,000/year in the Pearl River Delta, for up to 3 years (Guangzhou is in the PRD).',
            'standardDetail': 'If actual rent is below the cap, the actual rent is subsidized; if cumulative paid rent in a year exceeds the cap, the annual cap applies.',
            'conditions': [
                'Startup entity: micro/small enterprise, individual business, social organization, law firm, accounting firm or farmers\' cooperative registered in our province within 3 years, where you serve as legal representative / operator and belong to the key supported group.',
                'Registered for at least 12 months and not listed in the "Abnormal Operation List" at application.',
                'Normal operation for 6 consecutive months before applying, with at least 1 employee (other than you) paying social insurance.',
                'Leasing a venue not under your own name for business, with the lease address matching the registration address.',
                'The rent claimed occurred within 3 years from the startup\'s registration.',
                'Note: entities that changed their legal representative cannot apply; applications are rejected if the applicant is covered by employer pension insurance at a unit not under their own name.',
            ],
            'materials': [
                'Basic identity proof of the eligible person.',
                'Key-group supporting documents (same as the one-time startup grant).',
                'Proof of normal operation in the last 6 months (fund flow + at least one of payroll / financials / tax).',
                'Micro/small enterprise proof ("Basic Information of Surveyed Units" or "Enterprise Type Commitment Letter").',
                'Venue property proof, lease contract and rent invoice (full submission for first application; only operation proof + rent invoice + change docs for renewals).',
            ],
            'process': [
                'Sign a compliant lease (address matching registration) and obtain a rent invoice.',
                'Apply online via the Guangdong Public Employment Service Cloud Platform or submit to the local HR department.',
                'District public employment agency and district HR bureau accept, review and publicize.',
                'Subsidy paid annually (first application within 3 years of registration; last no later than 4 years).',
            ],
            'agency': 'Accepting agency: the district HR & social-security department / public employment service agency where the startup is registered.\nOnline filing: Guangdong Public Employment Service Cloud Platform https://ggfw.hrss.gd.gov.cn/employment/internet/portal/#/home\nDeadline: apply within 3 years from the startup\'s registration (for rent subsidy, the last application no later than 4 years from registration).',
            'company': [
                'Provide a compliant office address "ready for company registration" with lease matching the registration — exactly the core precondition for the rent subsidy.',
                'Move in and sign a proper lease with rent invoices available, directly meeting the "venue property proof, lease contract and rent invoice" requirement.',
                'One-stop company & tax services: business license, bookkeeping, tax records — preparing the "normal operation" proof.',
                'Dedicated advisors help organize documents and liaise with subdistrict / HR departments.',
                'All-inclusive pricing and flexible desks keep rent controllable, making the actual-rent subsidy more worthwhile.',
                'Note: subsidies are reviewed and paid by HR departments; final interpretation rests with the local HR department. Chitu provides address, contract, invoice and application assistance but does not guarantee approval.',
            ],
            'highlights': [
                'Subsidy proportional to actual rent',
                'Up to 3 years',
                'Requires a compliant venue with address matching registration',
            ],
        },
        {
            'tag': 'HMT Youth', 'name': 'HMT Youth Startup Support', 'slug': 'hmt-youth', 'imgKey': 'sub3',
            'summary': 'For Hong Kong, Macao and Taiwan residents under 45 with Chinese nationality, and eligible HMT youth, who start an early-stage business in Guangzhou (the nine GBA mainland cities) — a full-cycle package: one-time startup grant, rent subsidy, incubation & training subsidies, and guaranteed loans. Settling in Nansha adds a ¥20,000 startup grant and growth rewards up to ¥300,000.',
            'policy': 'Policy basis: "Implementation Rules for Supporting HMT Youth Employment and Entrepreneurship in the Guangdong-Hong Kong-Macao Greater Bay Area" (Yue Ren She Gui [2025] No.47, issued by Guangdong HR Dept., Taiwan Affairs Office, HMT Affairs Office, Finance Dept. and Tax Bureau; covers Guangzhou and the other eight GBA mainland cities); and "Nansha District, Guangzhou — Measures for Promoting HMT Youth Employment and Entrepreneurship" (Nansha HR Bureau, July 2026).',
            'object': 'HMT residents under 45 with Chinese nationality, and eligible HMT youth, who found an early-stage business in the nine GBA mainland cities and serve as its legal representative / operator.',
            'objectDetail': 'Key points:\n1. HMT youth: under 45 with Chinese nationality.\n2. Early-stage entity: micro/small enterprise, individual business, social organization, law firm, accounting firm or farmers\' cooperative registered in the nine GBA mainland cities within 3 years.\n3. Nansha offers additional tiered growth rewards for HMT startups first operating there (see "Standard").',
            'standard': 'Provincial rules: one-time startup grant ¥10,000; rent subsidy up to ¥6,000/year (up to 3 years); incubation subsidy ¥3,000/year (up to 2 years); training subsidy up to ¥2,800; guaranteed loans (personal up to ¥500k / partnership up to ¥3M / micro-enterprise up to ¥5M).\nNansha: startup grant ¥20,000 (6 months of actual operation); tiered growth rewards — year 1 ¥50k / year 2 ¥100k / year 3 ¥150k; outstanding-development award ¥300k; 1:1 matching of government grants up to ¥300k; competition support ¥50k; 50% interest discount up to ¥300k.',
            'standardDetail': 'Nansha rewards stack with provincial subsidies; for overlapping items, the higher amount applies (no duplication).',
            'conditions': [
                'Provincial one-time grant: the legal representative/operator is an HMT student enrolled or within 5 years of graduation (mainland or overseas university), or the entity is a post-house / B&B / farm-stay; registered for 6+ months, with employees (other than the founder) paying social insurance for 3 consecutive months before applying, and not on the Abnormal Operation List.',
                'Nansha startup grant: an HMT startup first operating in Nansha with 6 months of actual operation.',
                'Tiered growth rewards: 1 / 2 / 3 years of operation with clear / significant progress.',
            ],
            'materials': [
                'HMT resident ID (Residence Permit for HMT Residents / Mainland Travel Permit for HMT Residents).',
                'Education proof (graduation certificate for HMT students; degree authentication for overseas universities).',
                'Business license and normal-operation proof (fund flow + at least one of tax / social insurance / contracts & orders).',
                'Property proof / lease contract if premises are leased for business (for rent subsidy).',
                'Nansha additional rewards require actual-operation and progress evidence per district rules.',
            ],
            'process': [
                'Prepare HMT ID, education proof, business license and normal-operation evidence.',
                'Apply via the Guangdong Public Employment Service Cloud Platform (ggfw.hrss.gd.gov.cn) or the Nansha / registration-district HR department.',
                'Acceptance, review and public notice.',
                'Subsidy / reward paid to the company account.',
            ],
            'agency': 'Accepting agency: the HR & social-security department / public employment service agency of the registration district (Nansha).\nOnline filing: Guangdong Public Employment Service Cloud Platform https://ggfw.hrss.gd.gov.cn/employment/internet/portal/#/home\nNansha inquiries: Nansha District Bureau of Human Resources and Social Security, Guangzhou.',
            'company': [
                'Provide a compliant office address "ready for company registration" with lease matching the registration — meeting the hard venue requirement.',
                'Four Haizhu venues across Guangzhou for convenient landing and actual operation.',
                'One-stop company & tax services: business license, bookkeeping, tax records — preparing the normal-operation proof.',
                'Dedicated advisors organize and pre-fill documents and liaise with subdistrict / HR departments to raise approval rates.',
                'Note: subsidies are reviewed and paid by HR departments; final interpretation rests with the local HR department. Chitu provides the address and application assistance but does not guarantee approval.',
            ],
            'highlights': [
                'HMT-youth exclusive: grant + rent + incubation + training + loans',
                'Settling in Nansha adds ¥20k–¥300k growth rewards',
                'Chitu helps organize application documents',
            ],
        },
        {
            'tag': 'Foreign Talent', 'name': 'Foreign Talent Startup Support', 'slug': 'foreign-talent', 'imgKey': 'sub4',
            'summary': 'Ordinary foreign nationals are NOT covered by Guangdong\'s standard one-time startup / rent subsidies (those target Chinese citizens and HMT residents with Chinese nationality under 45). But foreign high-level talents, overseas-returnee foreign nationals and eligible foreign graduates can access talent / returnee channels, plus Nansha overseas-talent rewards and individual-income-tax subsidies in Guangzhou. Chitu offers a free eligibility assessment and handles work permits & residence.',
            'policy': 'Policy basis: Guangdong "Employment and Entrepreneurship Subsidy Guidelines (2026 Revision)" (Yue Ren She Gui [2026] No.20) explicitly excludes foreign nationals from "key supported entrepreneurship groups"; Guangzhou talent "Four Highs" policy and Nansha overseas-talent rewards.',
            'object': 'Foreign nationals holding a valid work / residence permit and meeting one of the following:\n1. Foreign high-level talent (Category A Foreigner Work Permit, or recognized high-level / scarce talent);\n2. Foreign students who graduated from Chinese universities with a bachelor\'s degree or above (may use the returnee / foreign-talent startup channel);\n3. Foreign entrepreneurial talents bringing scientific results or fitting Guangzhou\'s key industries.',
            'objectDetail': 'Important: Guangdong\'s one-time startup and rent subsidies go to "key supported entrepreneurship groups" — Chinese citizens and HMT residents (Chinese nationality), not ordinary foreigners. Foreign entrepreneurship support is delivered mainly through talent policies, which vary by city and talent profile and require eligibility / talent recognition first.',
            'standard': 'Supports accessible in Guangzhou / Nansha (subject to latest policy):\n· Up to ¥1,000,000 talent reward for internationally renowned PhDs or overseas-talent holders of international professional certificates newly working in Nansha;\n· Up to ¥5,000,000 annual fiscal subsidy for overseas talent whose Guangzhou individual income tax exceeds 15% of taxable income;\n· Foreign high-level talents can access guaranteed loans, project grants, venue and visa facilitation;\n· Foreign graduates in some cities (e.g. Xiamen, Shanghai) get ¥200k–¥500k startup funding via the returnee channel; Guangzhou mainly supports after talent recognition.',
            'standardDetail': 'These are talent-class supports, not a universal one-time startup subsidy; eligibility / talent recognition is required first, and amounts are subject to the registration district and talent departments.',
            'conditions': [
                'Obtain a lawful work / startup status in China (Foreigner Work Permit, residence permit, or set up a foreign-invested enterprise / representative office).',
                'Meet one of: high-level talent, overseas returnee (foreign), or key-industry direction.',
                'Register and actually operate a company in Guangzhou (especially Nansha).',
            ],
            'materials': [
                'Passport, visa / residence permit, Foreigner Work Permit.',
                'Degree authentication (overseas universities).',
                'High-level / scarce talent recognition materials (if applicable).',
                'Business license, actual-operation and investment evidence.',
            ],
            'process': [
                'Chitu / advisor runs a free eligibility assessment to identify the right talent / subsidy channel.',
                'Set up the foreign-invested enterprise or representative office, and obtain work permit & residence permit.',
                'Submit the corresponding grant / reward application to Nansha / Guangzhou talent or HR departments per recognition result.',
                'Paid after approval.',
            ],
            'agency': 'Accepting agencies: Guangzhou / Nansha HR & social-security departments, science & technology (talent) departments, and public security exit-entry authorities.\nOnline filing: Guangdong Government Service Net https://www.gdzwfw.gov.cn/ ; Guangdong Public Employment Service Cloud Platform https://ggfw.hrss.gd.gov.cn/\nNote: for foreigners, eligibility assessment comes first; final interpretation rests with each department.',
            'company': [
                'Foreign company registration, representative office setup, work / business visa assistance and residence-permit extension & change (see "Foreign-Investment & Visa Services").',
                'Free eligibility assessment first, to match applicable subsidy / talent-reward channels and avoid dead ends.',
                'Compliant office address ready for company registration plus one-stop company & tax services for landing and actual operation.',
                'Dedicated advisors liaise with subdistrict, HR and talent departments and help organize documents.',
                'Note: ordinary foreigners are not in Guangdong\'s standard startup-subsidy scope; whether you qualify depends on talent recognition and department interpretation. Chitu provides assessment, visa and application assistance but does not guarantee approval.',
            ],
            'highlights': [
                'Ordinary foreigners not in standard startup-subsidy scope (stated plainly)',
                'High-level / returnee channels + Nansha reward up to ¥1M',
                'Chitu free eligibility assessment + visa / residence handling',
            ],
        },
    ],
}


def main():
    with open(DATA, encoding='utf-8') as f:
        data = json.load(f)
    data['en'] = EN
    with open(DATA, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print('✅ en 子树已合并，顶层键:', list(data.keys()))


if __name__ == '__main__':
    main()
