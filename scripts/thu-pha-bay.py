#!/usr/bin/env python3
"""Thử phá từng bẫy trong scripts/kiem-tra.py: chép web ra thư mục tạm, cố ý gây
đúng lỗi của bẫy đó, chạy kiểm tra, bẫy PHẢI nổ. Thêm bẫy mới → thêm 1 dòng ở đây.

  python3 scripts/thu-pha-bay.py
"""
import os, re, shutil, subprocess, sys, tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
KT = os.path.join(ROOT, 'scripts', 'kiem-tra.py')

def sua(path, old, new, regex=False):
    s = open(path, encoding='utf-8').read()
    s2 = re.sub(old, new, s, count=1, flags=re.S) if regex else s.replace(old, new, 1)
    assert s2 != s, f'mẫu phá không khớp: {path}: {old[:50]!r}'
    open(path, 'w', encoding='utf-8').write(s2)

A = 'dat-mua-roi-de-do-tu-xa.html'     # bài mẫu
D = 'xu-ly-lan-chiem-dat-tu-xa.html'    # trang dịch vụ mẫu
PHA = [
 ('B01', A, r'("@type": "BreadcrumbList".*?)\}\]\}</script>', r'\1}]</script>', True),
 ('B02', A, 'Để không thì đất không tự mất, nhưng', 'Để không thì đất chẳng tự mất, nhưng', False),
 ('B03', 'llms.txt', 'GreenSpace', 'GreenSpace (xem nambanpanorama.com)', False),
 ('B04', A, '<p>Giao dịch khép lại', '<p>Script tự động lo hết. Giao dịch khép lại', False),
 ('B05', A, 'và cách theo dõi từ xa.">', 'và cách theo dõi từ xa, cách lập hồ sơ gốc, cách giữ mốc ranh, cách nhờ người trông khi ở xa">', False),
 ('B06', A, 'tính 2 triệu mỗi lô mỗi tháng. Không hợp đồng dài hạn, không phí ẩn, dừng bất kỳ lúc nào.</div>', 'tính 1,8 triệu mỗi lô mỗi tháng. Không hợp đồng dài hạn, không phí ẩn, dừng bất kỳ lúc nào.</div>', False),
 ('B06', A, 'đang theo <strong>50+ lô</strong>', 'đang theo <strong>60+ lô</strong>', False),
 ('B07', A, r'(class="float-btn float-call"[^>]*>)<svg.*?</svg>', r'\1<span style="font-size:22px;">&#9742;</span>', True),
 ('B07', A, '.float-btn{', '.float-bt{', False),
 ('B08', A, '<a class="cta-call" href="tel:0978758788">Gọi 0978 758 788</a>', '', False),
 ('B08', 'index.html', '<a class="mm-call" href="tel:0978758788"', '<a class="mm-call" href="#contact"', False),
 ('B08', 'index.html', '<a class="btn btn-primary" href="https://zalo.me/0978758788" target="_blank" rel="noopener" data-en="Message us on Zalo to pick the right plan">', '<a class="btn btn-primary" href="#contact" data-en="Message us on Zalo to pick the right plan">', False),
 ('B09', D, r'\n\s*<p class="quick-contact">.*?</p>\n', '\n', True),
 ('B10', A, '<script type="speculationrules">', '<script type="text/plain">', False),
 ('B11', 'sitemap.xml', r'(<loc>https://greenspacers\.vn/dat-mua-roi-de-do-tu-xa</loc>\s*<lastmod>)[^<]+', r'\g<1>2026-01-01', True),
 ('B12', A, '<a href="/cach-giu-dat-an-toan-tu-xa">', '<a href="/cach-giu-dat-an-toan-tu-xa.html">', False),
 ('B12', 'index.html', 'src="/images/hero-1.jpg"', 'src="images/hero-1.jpg"', False),
 ('B13', A, '<a class="skip-link" href="#main">Bỏ qua tới nội dung</a>\n', '', False),
 ('B13', A, "q.setAttribute('role','button');", '', False),
 ('B13', A, '<div class="tbl-wrap">', '<div>', False),
 ('B14', A, 'background:var(--gold);color:#1a1a1a;', 'background:var(--gold);color:white;', False),
 ('B14', A, ':focus-visible{outline:3px solid var(--gold);outline-offset:2px;box-shadow:0 0 0 2px #1a1a1a;}', ':focus-visible{outline:2px solid var(--gold);outline-offset:3px;}', False),
 ('B14', A, '.breadcrumb .sep{margin:0 6px;color:#6b6b6b;}', '.breadcrumb .sep{margin:0 6px;color:#ccc;}', False),
 ('B15', A, '<p>Giao dịch khép lại', '<p>Dịch vụ trông đất hàng đầu Nam Ban. Giao dịch khép lại', False),
 ('B16', 'index.html', r'<li class="update-item">.*?</li>', '', True),
 ('B17', A, '<title>Mua đất xong', '<title>25/9 — Mua đất xong', False),
 ('B19', 'dat-nen-phan-lo-nam-ban.html', r'srcset="/images/articles/dat-nen-phan-lo-nam-ban-640\.webp 640w, [^"]*"', 'srcset="/images/articles/dat-nen-phan-lo-nam-ban.webp"', True),
 ('B20', 'kiem-tra-dat-lam-ha.html', 'tình trạng đất tại Nam Ban, Lâm Hà, Lâm Đồng.', 'tình trạng đất tại Lâm Hà, Lâm Đồng.', False),
 ('B21', A, '<link rel="canonical" href="https://greenspacers.vn/dat-mua-roi-de-do-tu-xa">', '<link rel="canonical" href="https://greenspacers.vn/">', False),
]

def chay(root):
    return subprocess.run([sys.executable, KT, '--root', root, '--base-dir', ROOT], capture_output=True, text=True)

tmp = tempfile.mkdtemp()
try:
    r = chay(ROOT)
    if r.returncode != 0:
        print('Bản hiện tại chưa sạch — sửa trước khi thử phá:\n' + r.stdout); sys.exit(1)
    hong = 0
    for ma, f, old, new, rx in PHA:
        d = os.path.join(tmp, 'site'); shutil.rmtree(d, ignore_errors=True)
        shutil.copytree(ROOT, d, ignore=shutil.ignore_patterns('.git'))
        sua(os.path.join(d, f), old, new, rx)
        out = chay(d).stdout
        ok = f'[{ma}]' in out
        hong += not ok
        print(('✓ nổ ' if ok else '✗ KHÔNG NỔ ') + f'{ma}  ({f}: {old[:45]!r})')
    print('Tất cả bẫy đều nổ.' if not hong else f'{hong} bẫy không nổ — bẫy viết sai, phải sửa.')
    sys.exit(1 if hong else 0)
finally:
    shutil.rmtree(tmp, ignore_errors=True)
