#!/usr/bin/env python3
"""Bẫy kiểm tra GreenSpace — chạy trên CI mỗi lần push, và chạy tay trước khi đẩy.

Mỗi bẫy = một lỗi đã từng gặp thật (ở GreenSpace hoặc Nam Ban Villas), xem
docs/LOI-DA-GAP-VA-CACH-KIEM.md. Thêm bẫy mới thì phải thử phá bằng
scripts/thu-pha-bay.py (cố ý gây lỗi, thấy bẫy nổ, trả lại).

Cách chạy:
  python3 scripts/kiem-tra.py                       # kiểm thư mục hiện tại
  python3 scripts/kiem-tra.py --base-ref origin/main # thêm bẫy so với bản gốc (lastmod lùi, mất khối có ngày)
  python3 scripts/kiem-tra.py --root DIR --base-dir DIR2
"""
import argparse, glob, html, json, os, re, subprocess, sys

ap = argparse.ArgumentParser()
ap.add_argument('--root', default='.')
ap.add_argument('--base-ref', default=os.environ.get('BASE_REF', ''))
ap.add_argument('--base-dir', default='')
A = ap.parse_args()
ROOT = A.root
LOI = []
def L(ma, msg): LOI.append(f'[{ma}] {msg}')
def rd(p):
    with open(os.path.join(ROOT, p), encoding='utf-8') as fh: return fh.read()
def base(p):
    """Nội dung file ở bản gốc (để so) — None nếu không có."""
    if A.base_dir:
        q = os.path.join(A.base_dir, p)
        return open(q, encoding='utf-8').read() if os.path.exists(q) else None
    if A.base_ref:
        r = subprocess.run(['git', '-C', ROOT, 'show', f'{A.base_ref}:{p}'], capture_output=True, text=True)
        return r.stdout if r.returncode == 0 else None
    return None

SO = json.load(open(os.path.join(ROOT, 'data', 'so-lieu.json'), encoding='utf-8'))
PAGES = sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, '*.html')))
SRC = {f: rd(f) for f in PAGES}
def robots(s):
    m = re.search(r'<meta name="robots" content="([^"]*)"', s); return m.group(1) if m else ''
IDX = [f for f in PAGES if 'noindex' not in robots(SRC[f])]
def slug(f): return '' if f == 'index.html' else f[:-5]
def ld(s):
    out = []
    for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            d = json.loads(x)
        except Exception:
            continue
        out += d if isinstance(d, list) else [d]
    return out
def chu(s):
    """Chữ khách đọc được trong <body>."""
    b = s[s.find('<body'):] if '<body' in s else s
    b = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', b, flags=re.S)
    b = re.sub(r'<!--.*?-->', ' ', b, flags=re.S)
    b = re.sub(r'</?(?:a|strong|em|b|i|span|abbr|time|small)\b[^>]*>', '', b)  # thẻ trong dòng: bỏ, không chèn dấu cách
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', b)))
def norm(t): return re.sub(r'\s+', ' ', html.unescape(t)).strip()
def meta(s, key):
    m = re.search(r'<meta (?:name|property)="%s" content="([^"]*)"' % re.escape(key), s)
    return html.unescape(m.group(1)) if m else None
def khung(s):
    """Chữ ở phần khung: title, meta, alt, JSON-LD."""
    parts = re.findall(r'<title>(.*?)</title>', s, re.S)
    parts += re.findall(r'<meta (?:name|property)="(?:description|og:title|og:description|twitter:title|twitter:description|keywords)" content="([^"]*)"', s)
    parts += re.findall(r'\balt="([^"]*)"', s)
    parts += re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S)
    return html.unescape(' '.join(parts))

# ---------- B01 JSON-LD phải đọc được ----------
for f in PAGES:
    for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>', SRC[f], re.S):
        try: json.loads(x)
        except Exception as e: L('B01', f'{f}: JSON-LD hỏng ({e})')

# ---------- B02 FAQ trong schema phải hiện nguyên văn trên trang ----------
for f in PAGES:
    t = norm(chu(SRC[f]))
    for d in ld(SRC[f]):
        if d.get('@type') != 'FAQPage': continue
        for q in d.get('mainEntity', []):
            qn = norm(q['name']); an = norm(q['acceptedAnswer']['text'])
            if qn not in t: L('B02', f'{f}: câu hỏi schema không hiện trên trang: {qn[:60]}')
            elif an not in t: L('B02', f'{f}: câu trả lời schema lệch chữ hiển thị: {qn[:60]}')

# ---------- B03 Luật link: không nhắc/link web thứ ba của chủ ở bất kỳ đâu ----------
# Tên bị cấm KHÔNG viết thẳng ra trong repo công khai — ghép ngược để bẫy vẫn dò được.
CAM = 'amaronap'[::-1]
def file_trong_repo():
    r = subprocess.run(['git', '-C', ROOT, 'ls-files', '--cached', '--others', '--exclude-standard'], capture_output=True, text=True)
    if r.returncode == 0 and r.stdout.strip(): return r.stdout.split('\n')
    return [os.path.relpath(os.path.join(d, x), ROOT) for d, _, fs in os.walk(ROOT) if '/.git' not in d + '/' for x in fs]
for p in file_trong_repo():
    q = os.path.join(ROOT, p)
    if not p or not os.path.isfile(q): continue
    b = open(q, 'rb').read()
    if CAM.encode() in b.lower():
        L('B03', f'{p}: có tên web thứ ba bị cấm (kể cả metadata ảnh) — luật link')

# ---------- B32 Ảnh mang dấu bản quyền GreenSpace, không GPS ----------
# Đóng dấu: python3 scripts/dong-dau-anh.py (chèn thẳng vào file, không nén lại).
def exif_tiff(b, p):
    """Lấy khối TIFF của EXIF trong JPEG (APP1) hoặc WebP (chunk EXIF)."""
    if p.lower().endswith(('.jpg', '.jpeg')):
        k = b.find(b'Exif\x00\x00'); return b[k + 6:] if k >= 0 else None
    k = b.find(b'EXIF', 12)
    if k < 0: return None
    t = b[k + 8:k + 8 + int.from_bytes(b[k + 4:k + 8], 'little')]
    return t[6:] if t.startswith(b'Exif\x00\x00') else t
def co_gps(t):
    if not t or t[:2] not in (b'MM', b'II'): return False
    e = '>' if t[:2] == b'MM' else '<'
    try:
        o = int.from_bytes(t[4:8], 'big' if e == '>' else 'little'); n = int.from_bytes(t[o:o + 2], 'big' if e == '>' else 'little')
        return any(int.from_bytes(t[o + 2 + 12 * i:o + 4 + 12 * i], 'big' if e == '>' else 'little') == 0x8825 for i in range(n))
    except Exception: return False
for p in file_trong_repo():
    if not p.startswith('images/') or not p.lower().endswith(('.jpg', '.jpeg', '.webp')): continue
    b = open(os.path.join(ROOT, p), 'rb').read(); t = exif_tiff(b, p)
    xmp = b[b.find(b'<x:xmpmeta'):] if b'<x:xmpmeta' in b else b''
    if not t or b'greenspacers.vn' not in t or b'greenspacers.vn' not in xmp:
        L('B32', f'{p}: ảnh thiếu dấu bản quyền GreenSpace (EXIF + XMP) — chạy python3 scripts/dong-dau-anh.py')
    if co_gps(t) or b'GPSLatitude' in b:
        L('B32', f'{p}: ảnh có toạ độ GPS — lộ vị trí, phải xoá')

# ---------- B33 Tài liệu/code nội bộ không lên web ----------
vi = open(os.path.join(ROOT, '.vercelignore'), encoding='utf-8').read().split() if os.path.exists(os.path.join(ROOT, '.vercelignore')) else []
for m in ('CLAUDE.md', 'docs/', 'scripts/', 'data/', 'fb-queue/', '.github/'):
    if m not in vi: L('B33', f'.vercelignore thiếu "{m}" — file nội bộ sẽ công khai trên greenspacers.vn')

# ---------- B04 Không chữ máy móc trong chữ khách đọc ----------
MAY = re.compile(r'\b(script|scripts|tự động|auto|bot|chatbot|nhập tay|thuật toán|automation)\b', re.I)
for f in IDX:
    for nguon, t in (('thân trang', chu(SRC[f])), ('khung', khung(SRC[f]))):
        for m in list(MAY.finditer(t)) + list(re.finditer(r'\bAI\b', t)):
            L('B04', f'{f} ({nguon}): chữ máy móc "{m.group(0)}" — …{t[max(0, m.start()-40):m.end()+20]}…')
for _l in ('llms.txt', 'llms-full.txt'):
    if os.path.exists(os.path.join(ROOT, _l)):
        for m in MAY.finditer(rd(_l)): L('B04', f'{_l}: chữ máy móc "{m.group(0)}"')

# ---------- B05 Mô tả: ≤160 ký tự, hết câu, có "Nam Ban"; og không cụt ----------
for f in IDX:
    s = SRC[f]; d = meta(s, 'description')
    if not d: L('B05', f'{f}: thiếu meta description'); continue
    if len(d) > 160: L('B05', f'{f}: meta description {len(d)} ký tự (>160) — rút ở ranh câu, đọc lại')
    if d.rstrip()[-1] not in '.?!…': L('B05', f'{f}: meta description không kết thúc bằng dấu câu (cụt?): …{d[-30:]}')
    for k in ('description', 'og:description', 'twitter:description'):
        v = meta(s, k) or ''
        if v.count('(') != v.count(')'): L('B05', f'{f}: {k} ngoặc mở chưa đóng — mô tả bị cắt dở')
        if v and 'Nam Ban' not in v: L('B05', f'{f}: {k} thiếu "Nam Ban"')
        if 'Lâm Hà' in v and 'Nam Ban' not in v: L('B20', f'{f}: {k} có "Lâm Hà" mà không neo "Nam Ban"')
    for dd in ld(s):
        if dd.get('@type') in ('BlogPosting', 'Service') and 'Nam Ban' not in dd.get('description', 'Nam Ban'):
            L('B05', f'{f}: JSON-LD {dd["@type"]} description thiếu "Nam Ban"')

# ---------- B06 Giá và số liệu phải khớp một nguồn (data/so-lieu.json) ----------
GIA_OK = set(SO['gia_trieu_thang']) | set(SO['gia_dong_thang']) | set(SO.get('gia_tham_chieu_ngoai', {}).get('gia_trieu_thang', []))   # giá ngoài có nguồn ghi trong so-lieu
for f in PAGES:
    t = chu(SRC[f]) + ' ' + khung(SRC[f])
    for m in re.finditer(r'(\d{1,3}(?:[.,]\d{1,3})*)\s*(triệu|tr|đ)(?!\w)(?=[^.;:]{0,30}?tháng)', t):
        v = m.group(1) + ('đ' if m.group(2) == 'đ' else '')
        if v not in GIA_OK:
            L('B06', f'{f}: giá "{m.group(0)}…/tháng" không có trong data/so-lieu.json — …{t[max(0, m.start()-40):m.end()+30]}…')
    for m in re.finditer(r'(\d+)\+\s*lô', t):
        if m.group(1) + '+' != SO['so_lo_dang_theo']: L('B06', f'{f}: "{m.group(0)}" lệch số lô chuẩn {SO["so_lo_dang_theo"]}')
    for m in re.finditer(r'hơn\s+(\d+)\s+năm', t):
        if m.group(1) != SO['so_nam_lam']: L('B06', f'{f}: "{m.group(0)}" lệch số năm chuẩn {SO["so_nam_lam"]}')

# ---------- B07 Nút Gọi nổi: icon SVG + nhãn, và CSS có thật cho đúng markup ----------
for f in PAGES:
    s = SRC[f]
    if 'class="float-buttons"' not in s: continue
    fb = re.search(r'<div class="float-buttons">(.*?)</div>', s, re.S).group(1)
    call = re.search(r'<a [^>]*class="float-btn float-call"[^>]*>(.*?)</a>', fb, re.S)
    zalo = re.search(r'<a [^>]*class="float-btn float-zalo"[^>]*>', fb)
    if not call or '<svg' not in call.group(1) or '<path' not in call.group(1):
        L('B07', f'{f}: nút Gọi nổi không có icon SVG (ký tự như ☎ phụ thuộc font máy → có máy hiện nút rỗng)')
    if '&#9742;' in fb or '☎' in fb: L('B07', f'{f}: nút nổi còn dùng ký tự ☎')
    for nm, tag in (('Gọi', call.group(0) if call else ''), ('Zalo', zalo.group(0) if zalo else '')):
        if 'aria-label=' not in tag: L('B07', f'{f}: nút {nm} nổi thiếu aria-label')
    css = ' '.join(re.findall(r'<style[^>]*>(.*?)</style>', s, re.S))
    if not re.search(r'\.float-btn\s*\{[^}]*width', css): L('B07', f'{f}: thiếu CSS .float-btn (có markup mà không có kiểu → nút rỗng)')
    if not re.search(r'\.float-call\s*\{[^}]*background', css): L('B07', f'{f}: thiếu CSS nền .float-call')

# ---------- B08 Liên hệ ngay trong trang (không chỉ nút nổi) ----------
for f in IDX + ['404.html']:
    if f not in SRC: continue
    s = re.sub(r'<div class="float-buttons">.*?</div>', '', SRC[f], flags=re.S)
    if 'zalo.me/0978758788' not in s: L('B08', f'{f}: không có link Zalo trong trang')
    if 'tel:0978758788' not in s: L('B08', f'{f}: không có link Gọi trong trang')
    for m in re.finditer(r'<div class="cta-box">(.*?)</div>', s, re.S):
        if 'tel:' not in m.group(1) or 'zalo.me' not in m.group(1): L('B08', f'{f}: khối cta-box thiếu cặp Zalo + Gọi')
if 'index.html' in SRC:
    mm = re.search(r'<div class="mobile-menu" id="mobileMenu">(.*?)</div>', SRC['index.html'], re.S)
    if not mm or 'tel:' not in mm.group(1) or 'zalo.me' not in mm.group(1):
        L('B08', 'index.html: menu điện thoại thiếu Zalo/Gọi')
    for lab in ('Nhắn Zalo để chọn gói phù hợp', 'Kiểm tra đất của tôi', 'Tư vấn ngay'):
        m = re.search(r'<(a|button)\b[^>]*>' + re.escape(lab), SRC['index.html'])
        if not m or m.group(1) != 'a' or 'zalo.me' not in m.group(0):
            L('B08', f'index.html: nút "{lab}" không đi thẳng Zalo')

# ---------- B09 Trang dịch vụ: cặp Zalo/Gọi ngay dưới đoạn mở ----------
for f in SO['trang_dich_vu']:
    s = SRC.get(f, '')
    mn = s[s.find('<main'):] if '<main' in s else s
    qc, h2 = mn.find('class="quick-contact"'), mn.find('<h2')
    if qc < 0: L('B09', f'{f}: trang dịch vụ thiếu cặp nút Zalo/Gọi đầu trang (quick-contact)')
    elif h2 >= 0 and qc > h2: L('B09', f'{f}: quick-contact nằm sau H2 đầu tiên — phải ở ngay dưới đoạn mở')

# ---------- B10 speculationrules trên mọi trang lập chỉ mục ----------
for f in IDX:
    if '<script type="speculationrules">' not in SRC[f]: L('B10', f'{f}: thiếu speculationrules')

# ---------- B11 Sitemap: đủ trang, lastmod = dateModified, lastmod chỉ tiến ----------
sm = rd('sitemap.xml')
LM = dict(re.findall(r'<loc>https://greenspacers\.vn/([^<]*)</loc>\s*<lastmod>([^<]*)</lastmod>', sm))
for f in IDX:
    if slug(f) not in LM: L('B11', f'{f}: trang lập chỉ mục nhưng không có trong sitemap')
for sl in LM:
    if (sl + '.html' if sl else 'index.html') not in IDX: L('B11', f'sitemap có /{sl} nhưng không phải trang lập chỉ mục')
for f in IDX:
    for d in ld(SRC[f]):
        if d.get('@type') in ('WebPage', 'AboutPage') and 'dateModified' in d and slug(f) in LM and LM[slug(f)] != d['dateModified']:
            L('B11', f'{f}: {d["@type"]} dateModified {d["dateModified"]} ≠ sitemap lastmod {LM[slug(f)]}')
        if d.get('@type') == 'BlogPosting':
            dp, dm = d.get('datePublished', ''), d.get('dateModified', '')
            if dm < dp: L('B11', f'{f}: dateModified {dm} < datePublished {dp}')
            if slug(f) in LM and LM[slug(f)] != dm: L('B11', f'{f}: sitemap lastmod {LM[slug(f)]} ≠ dateModified {dm}')
b = base('sitemap.xml')
if b:
    OLD = dict(re.findall(r'<loc>https://greenspacers\.vn/([^<]*)</loc>\s*<lastmod>([^<]*)</lastmod>', b))
    vj = rd('vercel.json')
    for sl, d in OLD.items():
        if sl not in LM:
            if f'"/{sl}"' not in vj: L('B16', f'sitemap mất /{sl} mà không có redirect 301 trong vercel.json')
        elif LM[sl] < d: L('B11', f'/{sl}: lastmod lùi từ {d} về {LM[sl]} (chỉ được tiến)')

# ---------- B12 Đường dẫn: ảnh tuyệt đối + tồn tại, link nội bộ sạch ----------
for f in PAGES:
    s = re.sub(r'<!--.*?-->', '', SRC[f], flags=re.S)
    for u in re.findall(r'<(?:img|source)[^>]*?\ssrc="([^"]+)"', s) + [x.split()[0] for ss in re.findall(r'srcset="([^"]+)"', s) for x in ss.split(',')]:
        if u.startswith(('data:', 'https://')): continue
        if not u.startswith('/'): L('B12', f'{f}: ảnh đường dẫn tương đối "{u}"'); continue
        if not os.path.exists(os.path.join(ROOT, u.lstrip('/'))): L('B12', f'{f}: ảnh không tồn tại "{u}"')
    for h in re.findall(r'href="(/[^"#?]*)', s):
        if h == '/' or h.startswith('/images/') or h.endswith(('.xml', '.txt')): continue
        if h.endswith('.html'): L('B12', f'{f}: link "{h}" có đuôi .html (gây chuyển hướng)')
        elif h.endswith('/'): L('B12', f'{f}: link "{h}" có dấu / cuối (gây chuyển hướng)')
        elif not os.path.exists(os.path.join(ROOT, h.lstrip('/') + '.html')): L('B12', f'{f}: link chết "{h}"')

# ---------- B13 Tiếp cận: skip link, <main>, FAQ bằng bàn phím, không chặn zoom, bảng cuộn ----------
for f in IDX + ['404.html']:
    s = SRC.get(f, '')
    if 'class="skip-link"' not in s: L('B13', f'{f}: thiếu skip link')
    if not re.search(r'<main[^>]*\bid="main"', s): L('B13', f'{f}: thiếu <main id="main">')
    if re.search(r'class="faq-item[^"]*" onclick', s) and "setAttribute('role','button')" not in s:
        L('B13', f'{f}: FAQ chỉ mở bằng chuột (thiếu script bàn phím)')
    if re.search(r'user-scalable=no|maximum-scale=1', s): L('B13', f'{f}: viewport chặn phóng to')
    for m in re.finditer(r'<table', s):
        if not re.search(r'<div class="(tbl-wrap|ptbl-wrap)">\s*$', s[max(0, m.start()-120):m.start()]):
            L('B13', f'{f}: bảng không bọc vùng cuộn ngang')
    for m in re.finditer(r'<img\b[^>]*>', s):
        if 'alt=' not in m.group(0): L('B13', f'{f}: ảnh thiếu alt')

# ---------- B14 Tương phản chữ (công thức WCAG) ----------
def lum(h):
    h = h.lstrip('#'); h = ''.join(c * 2 for c in h) if len(h) == 3 else h
    c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    c = [x / 12.92 if x <= .03928 else ((x + .055) / 1.055) ** 2.4 for x in c]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]
def ratio(a, b):
    la, lb = lum(a), lum(b); return (max(la, lb) + .05) / (min(la, lb) + .05)
NAMED = {'white': '#ffffff', 'black': '#000000'}
for f in PAGES:
    s = SRC[f]; css = ' '.join(re.findall(r'<style[^>]*>(.*?)</style>', s, re.S))
    VARS = dict(re.findall(r'(--[\w-]+)\s*:\s*(#[0-9a-fA-F]{3,6})\b', css))
    def col(v):
        v = v.strip().split('!')[0].strip()
        m = re.fullmatch(r'var\((--[\w-]+)\)', v)
        if m: v = VARS.get(m.group(1), '')
        v = NAMED.get(v, v)
        return v if re.fullmatch(r'#[0-9a-fA-F]{3}|#[0-9a-fA-F]{6}', v) else None
    for sel, body in re.findall(r'([^{}]+)\{([^{}]*)\}', css):
        c = re.search(r'(?:^|;)\s*color\s*:\s*([^;]+)', body); bgm = re.search(r'background(?:-color)?\s*:\s*([^;]+)', body)
        if c and bgm:
            fc, bc = col(c.group(1)), col(bgm.group(1))
            if fc and bc and ratio(fc, bc) < 4.5:
                L('B14', f'{f}: "{sel.strip()[:50]}" chữ {fc} trên nền {bc} chỉ {ratio(fc, bc):.2f}:1 (cần 4.5)')
    bg = col('var(--bg)') or '#f9f8f6'
    if f != 'index.html':
        for sel in ('.breadcrumb', '.footer', '.xref', '.subtitle', '.breadcrumb .sep'):
            m = re.search(re.escape(sel) + r'\{([^}]*)\}', css)
            c = m and re.search(r'(?:^|;)color:([^;]+)', m.group(1))
            if c and col(c.group(1)) and ratio(col(c.group(1)), bg) < 4.5:
                L('B14', f'{f}: {sel} màu {col(c.group(1))} trên nền {bg} chỉ {ratio(col(c.group(1)), bg):.2f}:1')
    if re.search(r':focus-visible\{outline:2px solid var\(--gold\);outline-offset:3px;\}', css):
        L('B14', f'{f}: viền focus chỉ màu vàng — trên nền sáng chỉ 2.1:1, gần như tàng hình')

# ---------- B15 Không nói quá ----------
QUA = re.compile(r'(100% sổ|hàng đầu|số 1\b|tốt nhất|uy tín nhất|duy nhất|cam kết 100%|không bao giờ mất)', re.I)
for f in IDX:
    t = chu(SRC[f]) + ' ' + khung(SRC[f])
    for m in QUA.finditer(t): L('B15', f'{f}: nói quá "{m.group(0)}" — …{t[max(0, m.start()-40):m.end()+30]}…')

# ---------- B16 Không tự xoá nội dung có ngày ----------
b = base('index.html')
if b and 'index.html' in SRC:
    n0, n1 = b.count('<li class="update-item"'), SRC['index.html'].count('<li class="update-item"')
    if n1 < n0: L('B16', f'index.html: ô Cập nhật còn {n1} mục, bản gốc có {n0} — không được xoá tin cũ có ngày')

# ---------- B17 Title/H1 không chứa ngày/tuần (đổi liên tục → Google đánh giá lại) ----------
for f in IDX:
    for tag in re.findall(r'<title>(.*?)</title>', SRC[f]) + re.findall(r'<h1[^>]*>(.*?)</h1>', SRC[f], re.S):
        if re.search(r'\b\d{1,2}/\d{1,2}\b|\btuần\s*\d', tag): L('B17', f'{f}: title/H1 chứa ngày/tuần: {norm(tag)[:60]}')

# ---------- B19 Ảnh đầu bài có bản nhỏ cho điện thoại ----------
for f in PAGES:
    for m in re.finditer(r'<picture>(.*?)</picture>', SRC[f], re.S):
        if 'article-hero' in m.group(1) and not re.search(r'srcset="[^"]*\s\d+w', m.group(1)):
            L('B19', f'{f}: ảnh đầu bài không có srcset nhiều cỡ (điện thoại tải ảnh 1200px)')

# ---------- B22 Lớp CSS dùng mà trang không định nghĩa (bài học gốc: chép tay nhiều trang thì có trang sai) ----------
LOP_KHONG_CAN_CSS = {'services-head-left', 'footer-cta-text', 'in', 'open', 'is-active', 'is-open', 'yes', 'no'}  # vỏ bọc/trạng thái JS — đã soát tay
for f in PAGES:
    s = SRC[f]; css = ' '.join(re.findall(r'<style[^>]*>(.*?)</style>', s, re.S))
    js = ' '.join(re.findall(r'<script(?![^>]*ld\+json)[^>]*>(.*?)</script>', s, re.S))
    than = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', s, flags=re.S)
    thieu = set()
    for cl in re.findall(r'class="([^"]+)"', than):
        for c in cl.split():
            if c in LOP_KHONG_CAN_CSS or c in js: continue
            if not re.search(r'\.' + re.escape(c) + r'(?![\w-])', css): thieu.add(c)
    for c in sorted(thieu): L('B22', f'{f}: dùng class "{c}" nhưng trang không có CSS cho nó')

# ---------- B23 Nút gọi hàm JS / id phải có thật trên trang ----------
for f in PAGES:
    s = SRC[f]; js = ' '.join(re.findall(r'<script(?![^>]*(?:ld\+json|speculationrules))[^>]*>(.*?)</script>', s, re.S))
    for fn in set(re.findall(r'\son\w+="\s*([A-Za-z_]\w*)\(', s)):
        if not re.search(r'function\s+' + fn + r'\b|\b' + fn + r'\s*=\s*function', js): L('B23', f'{f}: onclick gọi {fn}() nhưng trang không có hàm đó (nút bấm không ăn)')
    for i in set(re.findall(r"getElementById\('([^']+)'\)", js)):
        if f'id="{i}"' not in s: L('B23', f'{f}: JS tìm id "{i}" không có trên trang')

# ---------- B24 Bậc tiêu đề không nhảy cóc ----------
for f in PAGES:
    s = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', SRC[f], flags=re.S); t = 0
    for m in re.finditer(r'<h([1-6])\b', s):
        h = int(m.group(1))
        if t and h > t + 1: L('B24', f'{f}: tiêu đề nhảy h{t}→h{h}'); break
        t = h

# ---------- B25 Câu hỏi FAQ mở sẵn (đáp án hiện thẳng cho khách, Google, AI) ----------
for f in PAGES:
    s = SRC[f]
    dong = len(re.findall(r'class="faq-item" onclick', s)) + len(re.findall(r'<button class="faq-q"(?! open)', s)) + len(re.findall(r'<details(?![^>]*\bopen)', s))
    if dong: L('B25', f'{f}: {dong} câu hỏi đang đóng — phải mở sẵn')

# ---------- B26 Nút bật/tắt có aria-pressed ----------
for f in PAGES:
    for m in re.finditer(r'<button[^>]*class="[^"]*lang-opt[^"]*"[^>]*>', SRC[f]):
        if 'aria-pressed=' not in m.group(0): L('B26', f'{f}: nút đổi ngôn ngữ thiếu aria-pressed')

def chu_js(s):
    """Chữ khách đọc nằm trong chuỗi JS (câu xoay vòng, bản dịch…): chuỗi có dấu tiếng Việt hoặc ≥4 từ."""
    out = []
    for js in re.findall(r'<script(?![^>]*(?:ld\+json|speculationrules))[^>]*>(.*?)</script>', s, re.S):
        for q in re.findall(r"'((?:[^'\\\n]|\\.){12,})'|\"((?:[^\"\\\n]|\\.){12,})\"", js):
            t = q[0] or q[1]
            if re.search(r'[à-ỹđ]', t) or len(t.split()) >= 4: out.append(t)
    return ' '.join(out)

# ---------- B27 Tên hành chính đã bỏ từ 1/7/2025 ----------
for f in IDX:
    t = chu(SRC[f]) + ' ' + khung(SRC[f]) + ' ' + chu_js(SRC[f])
    # được nhắc tên cũ khi nói rõ là cũ ngay sau đó ("thị trấn Nam Ban cũ", "cấp huyện cũ")
    for m in re.finditer(r'\b(huyện|thị trấn)\b(?![^.;:!?]{0,25}\bcũ\b)', t, re.I):
        L('B27', f'{f}: "{m.group(0)}" — cấp huyện/thị trấn đã bỏ từ 1/7/2025 — …{t[max(0, m.start()-40):m.end()+30]}…')

# ---------- B28 Số thống kê không nguồn (cả trong chuỗi JS) ----------
for f in IDX:
    t = chu(SRC[f]) + ' ' + khung(SRC[f]) + ' ' + chu_js(SRC[f])
    for m in re.finditer(r'(Khảo sát của|Theo số liệu|Theo thống kê|chuyên gia cho rằng|nhiều người cho rằng|\d{1,3}\s*%\s*(?:trường hợp|khách|chủ đất|người|nhà đầu tư|of the time|of cases))', t, re.I):
        L('B28', f'{f}: số thống kê không nguồn "{m.group(0)}" — gỡ, đừng làm mềm câu')
    for m in MAY.finditer(chu_js(SRC[f])): L('B04', f'{f} (chuỗi JS): chữ máy móc "{m.group(0)}"')

# ---------- B29 Lặp từ gõ nhầm (sau mỗi lần thay hàng loạt) ----------
LAP = re.compile(r'\b(nên|của|là|và|thì|đã|được|cho|với|trong|trung tâm|các|những|một) \1\b', re.I)
for f in PAGES:
    t = chu(SRC[f]) + ' ' + khung(SRC[f])
    for m in LAP.finditer(t): L('B29', f'{f}: lặp từ "{m.group(0)}" — …{t[max(0, m.start()-30):m.end()+30]}…')

# ---------- B30 Bài không lẻ loi: mỗi bài có ≥ 3 link vào từ trang khác ----------
VAO = {f: set() for f in IDX}
for g in IDX:   # chỉ đếm link từ trang lập chỉ mục (trang noindex như anh-da-dung không tính)
    for h in set(re.findall(r'href="/([a-z0-9-]+)"', SRC[g])):
        if h + '.html' in VAO and h + '.html' != g: VAO[h + '.html'].add(g)
for f, v in VAO.items():
    if f != 'index.html' and len(v) < 3: L('B30', f'{f}: chỉ {len(v)} trang trỏ vào — nối vào khối "Bài liên quan" của bài cùng cụm (chữ neo là câu hỏi)')

# ---------- B34 Mỗi trang: khai RSS, có người viết, có ngày cập nhật ----------
for f in IDX:
    s = SRC[f]; ds = ld(s)
    if 'type="application/rss+xml"' not in s: L('B34', f'{f}: thiếu <link rel="alternate" type="application/rss+xml"> trong <head>')
    if not any('author' in d for d in ds): L('B34', f'{f}: JSON-LD chưa có người viết (author)')
    if not any('dateModified' in d for d in ds): L('B34', f'{f}: JSON-LD chưa có ngày cập nhật (dateModified)')

# ---------- B35 llms-full.txt khớp bản sinh từ trang thật ----------
import importlib.util as _iu
try:   # một bẫy lỗi không được làm sập cả bộ kiểm tra
    _sp = _iu.spec_from_file_location('tlf', os.path.join(ROOT, 'scripts', 'tao-llms-full.py')); _tlf = _iu.module_from_spec(_sp); _sp.loader.exec_module(_tlf)
    if not os.path.exists(os.path.join(ROOT, 'llms-full.txt')) or rd('llms-full.txt') != _tlf.sinh(ROOT):
        L('B35', 'llms-full.txt cũ/lệch so với trang — chạy python3 scripts/tao-llms-full.py')
except Exception as e:
    L('B35', f'không sinh được llms-full.txt để so ({type(e).__name__}: {e})')

# ---------- B37 Không tự chấm sao cho mình (Google cấm đánh giá tự khai; khách không chấm sao) ----------
for f in PAGES:
    for d in ld(SRC[f]):
        if 'aggregateRating' in d or 'review' in d or d.get('@type') in ('Review', 'AggregateRating'):
            L('B37', f'{f}: JSON-LD có đánh giá/sao tự khai ({d.get("@type")}) — gỡ, giữ lời khách ở phần hiển thị')

# ---------- B38 Nói dịch vụ phải nói ở đâu (chủ web chốt 26/9): lời mời cuối trang có Nam Ban / Lâm Hà ----------
for f in IDX + ['404.html']:
    s = SRC.get(f, '')
    if '<div class="cta-box">' not in s: continue
    i = s.index('<div class="cta-box">'); blk = s[i:s.index('</div>', i)]
    if not re.search('Nam Ban|Lâm Hà', re.sub(r'<a [^>]*>.*?</a>', '', blk, flags=re.S)):
        L('B38', f'{f}: khối lời mời cuối trang (cta-box) nói dịch vụ chung chung — thêm "Nam Ban" / "Lâm Hà" tự nhiên vào câu')

# ---------- B39 Không nhồi địa danh: "Nam Ban" ≤ 4% số chữ trên trang ----------
for f in IDX:
    t = chu(SRC[f]); w = len(t.split()); n = len(re.findall(r'Nam Ban', t))
    if w and n * 2 / w > 0.04:
        L('B39', f'{f}: "Nam Ban" chiếm {100 * n * 2 / w:.1f}% số chữ ({n} lần / {w} chữ) — quá dày, Google coi là nhồi từ khoá')

# ---------- B21 canonical / og:url đúng địa chỉ ----------
for f in IDX:
    want = 'https://greenspacers.vn/' + slug(f)
    c = re.search(r'<link rel="canonical" href="([^"]*)"', SRC[f])
    if not c or c.group(1) != want: L('B21', f'{f}: canonical {c.group(1) if c else "thiếu"} ≠ {want}')
    o = meta(SRC[f], 'og:url')
    if o and o != want: L('B21', f'{f}: og:url {o} ≠ {want}')
    if len(re.findall(r'<h1\b', SRC[f])) != 1: L('B21', f'{f}: phải có đúng 1 thẻ H1')

# ---------- B40 Một key một trang + đủ địa danh (data/so-lieu.json → tu_khoa) ----------
TK = SO.get('tu_khoa', {})
def gon(t): return re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', ' ', norm(t).lower())).strip()
for key, f in TK.get('trang', {}).items():
    if f not in SRC: L('B40', f'câu "{key}" trỏ tới {f} không có'); continue
    s = SRC[f]
    q = re.search(r'<div class="faq-q">(.*?)</div>', s, re.S)
    if not q or not set(gon(key).split()) <= set(gon(re.sub(r'<[^>]+>', '', q.group(1))).split()):
        L('B40', f'{f}: câu hỏi FAQ đầu phải chứa đủ chữ của câu khách gõ "{key}" — đang là "{norm(q.group(1)) if q else "không có FAQ"}"')
    i = s.find('<h1'); j = s.find('<h2', i)
    if 'Nam Ban, Lâm Hà, Lâm Đồng' not in chu(s[i:j]):
        L('B40', f'{f}: đoạn mở (H1 → H2 đầu) thiếu cụm "Nam Ban, Lâm Hà, Lâm Đồng" cho câu "{key}"')
    for g in IDX:
        t = re.search(r'<title>(.*?)</title>', SRC[g], re.S)
        if g != f and t and gon(t.group(1)).startswith(gon(key)):
            L('B40', f'{g}: title mở bằng "{key}" — câu này đã giao cho {f} (một key một trang)')

# ---------- B41 Khoá title/H1 trang theo key tới ngày chốt ----------
if TK.get('khoa_title_toi') and __import__('datetime').date.today().isoformat() < TK['khoa_title_toi']:
    for f in TK.get('trang', {}).values():
        b = base(f)
        if not b or f not in SRC: continue
        for tag in ('title', 'h1'):
            x = re.search(r'<%s\b[^>]*>(.*?)</%s>' % (tag, tag), SRC[f], re.S); y = re.search(r'<%s\b[^>]*>(.*?)</%s>' % (tag, tag), b, re.S)
            if x and y and norm(x.group(1)) != norm(y.group(1)):
                L('B41', f'{f}: đổi {tag} khi đang khoá tới {TK["khoa_title_toi"]} ("{norm(y.group(1))}" → "{norm(x.group(1))}")')

if LOI:
    print(f'✗ {len(LOI)} lỗi:')
    for x in LOI: print('  ' + x)
    sys.exit(1)
print(f'✓ Sạch — {len(PAGES)} trang, {len(IDX)} trang lập chỉ mục.')
