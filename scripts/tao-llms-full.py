#!/usr/bin/env python3
"""Sinh llms-full.txt — bản mô tả đầy đủ GreenSpace cho các trợ lý tìm kiếm trích dẫn đúng.

Mọi chữ lấy từ trang thật (title, mô tả, đoạn trả lời đầu, hỏi đáp đang hiện) và giá từ
data/so-lieu.json — không gõ tay, nên không lệch với web. Bẫy B35 trong kiem-tra.py so file
với bản sinh lại: sửa trang xong mà quên chạy lệnh này thì bị chặn.

  python3 scripts/tao-llms-full.py          # ghi llms-full.txt
  python3 scripts/tao-llms-full.py --check  # chỉ so, lệch thì thoát mã 1
"""
import glob, html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = 'https://greenspacers.vn/'


def chu(x):
    x = re.sub(r'<[^>]+>', '', x)
    return re.sub(r'\s+', ' ', html.unescape(x)).strip()


def sinh(root=ROOT):
    so = json.load(open(os.path.join(root, 'data', 'so-lieu.json'), encoding='utf-8'))
    sm = open(os.path.join(root, 'sitemap.xml'), encoding='utf-8').read()
    lm = dict(re.findall(r'<loc>https://greenspacers\.vn/([^<]*)</loc>\s*<lastmod>([^<]*)</lastmod>', sm))
    trang = []
    for p in sorted(glob.glob(os.path.join(root, '*.html'))):
        s = open(p, encoding='utf-8').read(); f = os.path.basename(p)
        rb = re.search(r'<meta name="robots" content="([^"]*)"', s)
        if rb and 'noindex' in rb.group(1): continue
        slug = '' if f == 'index.html' else f[:-5]
        faq = []
        for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
            try: d = json.loads(x)
            except ValueError: continue   # JSON hỏng: bẫy B01 báo, ở đây bỏ qua để không sập
            if d.get('@type') == 'FAQPage':
                faq = [(chu(q['name']), chu(q['acceptedAnswer']['text'])) for q in d['mainEntity']]
        lead = re.search(r'<p class="answer-lead">(.*?)</p>', s, re.S)
        trang.append(dict(slug=slug, title=chu(re.search(r'<title>(.*?)</title>', s, re.S).group(1)),
                          desc=chu(re.search(r'<meta name="description" content="([^"]*)"', s).group(1)),
                          lead=chu(lead.group(1)) if lead else '', faq=faq, lm=lm.get(slug, '')))
    trang.sort(key=lambda t: (t['slug'] != '', t['slug']))
    g = so['gia_dong_thang']
    out = ['# GreenSpace — bản đầy đủ', '',
           '> Trông coi, quản lý đất, nhà và vườn tại Nam Ban, Lâm Hà, Lâm Đồng cho người sống ở xa. '
           'Đội ngũ người địa phương Nam Ban. Người sáng lập & CEO: Đoàn Quốc Duyệt.', '',
           '## Thông tin chính', '',
           f'- Web: {URL}',
           '- Liên hệ: Zalo / điện thoại 0978 758 788',
           '- Khu vực: Nam Ban, Lâm Hà, Lâm Đồng và vùng lân cận',
           f'- Đã làm: hơn {so["so_nam_lam"]} năm; đang theo {so["so_lo_dang_theo"]} lô',
           f'- Giá tham khảo đất: gói cơ bản {g[0]}/tháng; gói chuyên nghiệp {g[2]}/tháng; từ 3 lô {g[1]}/lô/tháng',
           f'- Giá tham khảo nhà vườn (đất + nhà + vườn): từ {g[3]}/tháng',
           '- Không hợp đồng dài hạn, không phí ẩn.', '',
           '## Các trang', '']
    for t in trang:
        out += [f'### {t["title"]}', '', f'- URL: {URL}{t["slug"]}']
        if t['lm']: out.append(f'- Cập nhật: {t["lm"]}')
        out.append(f'- Tóm tắt: {t["desc"]}')
        if t['lead'] and t['lead'] != t['desc']: out.append(f'- Trả lời nhanh: {t["lead"]}')
        if t['faq']:
            out += ['', 'Hỏi đáp:']
            out += [f'- **{q}** {a}' for q, a in t['faq']]
        out.append('')
    return '\n'.join(out).rstrip() + '\n'


if __name__ == '__main__':
    moi = sinh(); p = os.path.join(ROOT, 'llms-full.txt')
    if '--check' in sys.argv:
        cu = open(p, encoding='utf-8').read() if os.path.exists(p) else ''
        sys.exit(0 if cu == moi else 1)
    open(p, 'w', encoding='utf-8').write(moi)
    print(f'Đã ghi llms-full.txt ({len(moi):,} ký tự, {moi.count(chr(10)+"### ")} trang).')
