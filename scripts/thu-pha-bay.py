#!/usr/bin/env python3
"""Thử phá từng bẫy trong scripts/kiem-tra.py: chép web ra thư mục tạm, cố ý gây
đúng lỗi của bẫy đó, chạy kiểm tra, bẫy PHẢI nổ. Thêm bẫy mới → thêm 1 dòng ở đây.

  python3 scripts/thu-pha-bay.py
"""
import os, re, shutil, subprocess, sys, tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
KT = os.path.join(ROOT, 'scripts', 'kiem-tra.py')

def sua(path, old, new, regex=False):
    if regex in ('strip', 'gps'):   # phá ảnh: xoá dấu bản quyền / gắn GPS
        from PIL import Image
        im = Image.open(path); ex = Image.Exif()
        if regex == 'gps':
            ex = im.getexif(); ex[0x8825] = {1: 'N', 2: (11.0, 50.0, 0.0), 3: 'E', 4: (108.0, 20.0, 0.0)}
        im.save(path, exif=ex.tobytes(), **({'xmp': im.info['xmp']} if regex == 'gps' and 'xmp' in im.info else {})); return
    s = open(path, encoding='utf-8').read()
    s2 = re.sub(old, new, s, count=1, flags=re.S) if regex else s.replace(old, new, 1)
    assert s2 != s, f'mẫu phá không khớp: {path}: {old[:50]!r}'
    open(path, 'w', encoding='utf-8').write(s2)

A = 'dat-mua-roi-de-do-tu-xa.html'     # bài mẫu
D = 'xu-ly-lan-chiem-dat-tu-xa.html'    # trang dịch vụ mẫu
PHA = [
 ('B01', A, r'("@type": "BreadcrumbList".*?)\}\]\}</script>', r'\1}]</script>', True),
 ('B02', A, 'Để không thì đất không tự mất, nhưng', 'Để không thì đất chẳng tự mất, nhưng', False),
 ('B03', 'llms.txt', 'GreenSpace', 'GreenSpace (xem namban' + 'amaronap'[::-1] + '.com)', False),
 ('B32', 'images/founder.jpg', b'', b'', 'strip'),
 ('B32', 'images/hero-1.jpg', b'', b'', 'gps'),
 ('B33', '.vercelignore', 'CLAUDE.md\n', '', False),
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
 ('B22', A, '<p class="subtitle">', '<p class="subtitle-moi">', False),
 ('B23', 'index.html', 'onclick="toggleFaq(this)"', 'onclick="moFaq(this)"', False),
 ('B23', 'index.html', 'id="mobileMenu"', 'id="mobileMenu2"', False),
 ('B24', A, '<h2>"Mua xong là xong?"', '<h3>"Mua xong là xong?"', False),
 ('B25', A, 'class="faq-item open" onclick', 'class="faq-item" onclick', False),
 ('B25', 'index.html', '<button class="faq-q open"', '<button class="faq-q"', False),
 ('B26', 'index.html', 'data-lang="en" type="button" aria-pressed="false"', 'data-lang="en" type="button"', False),
 ('B27', A, '<p>Giao dịch khép lại', '<p>Đất ở huyện Lâm Hà. Giao dịch khép lại', False),
 ('B27', 'quan-ly-dat-nam-ban.html', 'kèm cấp huyện cũ.', 'kèm cấp huyện.', False),   # bỏ chữ "cũ" thì phải nổ lại
 ('B06', 'thue-nguoi-trong-coi-dat-nam-ban.html', 'khoảng 6–12 triệu đồng/tháng', 'khoảng 6–15 triệu đồng/tháng', False),   # giá ngoài chưa ghi nguồn
 ('B28', 'index.html', "'Phần lớn các lần kiểm tra, mọi thứ vẫn ổn.", "'80% trường hợp mọi thứ ổn.", False),
 ('B28', A, '<p>Giao dịch khép lại', '<p>Theo thống kê, ai cũng vậy. Giao dịch khép lại', False),
 ('B04', 'index.html', "'Mảnh đất không biết nói", "'Hệ thống tự động báo cáo. Mảnh đất không biết nói", False),
 ('B29', A, 'Việc cần làm là', 'Việc cần làm là là', False),
 ('B30', 'dat-nam-ban-view-dep.html', '<a href="/dat-nen-phan-lo-nam-ban">Đất nền, phân lô Nam Ban — "rõ ranh" tới khi nào? →</a>', '', False),
 ('B34', A, '<link rel="alternate" type="application/rss+xml" title="GreenSpace — Bài mới" href="https://greenspacers.vn/feed.xml">\n', '', False),
 ('B34', 'kiem-tra-dat-lam-ha.html', r'"author": \{[^}]*\}, ', '', True),
 ('B35', 'cau-hoi-thuong-gap.html', 'Giải đáp thắc mắc về trông coi', 'Giải đáp mọi thắc mắc về trông coi', False),
 ('B37', 'index.html', '"priceRange":', '"aggregateRating": {"@type": "AggregateRating", "ratingValue": "5", "reviewCount": "3"}, "priceRange":', False),
 ('B11', 'quan-ly-dat-nam-ban.html', r'("@type": "WebPage".*?"dateModified": ")[0-9-]+', r'\g<1>2026-01-01', True),
 ('B38', D, 'đội ở Nam Ban ra kiểm tra', 'chúng tôi ra kiểm tra', False),
 ('B40', D, 'Lô ở Nam Ban, Lâm Hà, Lâm Đồng có người', 'Lô ở Nam Ban có người', False),
 ('B40', 'cach-giu-dat-an-toan-tu-xa.html', 'faq-q">Trông coi đất ở xa cần làm gì?', 'faq-q">Cần làm gì?', False),
 ('B40', A, '<title>Mua đất xong', '<title>Trông coi đất ở xa: mua đất xong', False),
 ('B41', 'kiem-tra-dat-lam-ha.html', '<title>Kiểm tra đất Lâm Hà', '<title>Kiểm tra đất Nam Ban Lâm Hà', False),
 ('B42', 'quan-ly-tai-san-nha-vuon-nam-ban.html', 'chúng tôi kết nối, hẹn lịch', 'chúng tôi chăm vườn, hẹn lịch', False),
 ('B39', 've-greenspace.html', '<h2>Tóm tắt</h2>', '<h2>Tóm tắt</h2><p>' + 'Nam Ban Nam Ban Nam Ban Nam Ban Nam Ban Nam Ban Nam Ban Nam Ban Nam Ban Nam Ban. ' * 2 + '</p>', False),
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
        # chỉ chép file git quản lý (kể cả file mới chưa commit), bỏ tài liệu nội bộ bị .gitignore
        for rel in subprocess.run(['git', '-C', ROOT, 'ls-files', '--cached', '--others', '--exclude-standard'], capture_output=True, text=True).stdout.split('\n'):
            if rel and os.path.isfile(os.path.join(ROOT, rel)):
                os.makedirs(os.path.dirname(os.path.join(d, rel)) or d, exist_ok=True)
                shutil.copy2(os.path.join(ROOT, rel), os.path.join(d, rel))
        sua(os.path.join(d, f), old, new, rx)
        out = chay(d).stdout
        ok = f'[{ma}]' in out and (rx != 'gps' or 'GPS' in out)   # phá GPS phải nổ đúng lý do GPS
        hong += not ok
        print(('✓ nổ ' if ok else '✗ KHÔNG NỔ ') + f'{ma}  ({f}: {old[:45]!r})')
    print('Tất cả bẫy đều nổ.' if not hong else f'{hong} bẫy không nổ — bẫy viết sai, phải sửa.')
    sys.exit(1 if hong else 0)
finally:
    shutil.rmtree(tmp, ignore_errors=True)
