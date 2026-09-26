#!/usr/bin/env python3
"""Quét tin liên quan tới GreenSpace (đất ở xa bị lấn, tranh chấp ranh, quy hoạch, pháp lý đất,
thiên tai) từ RSS báo chính thống → hàng đợi tin ứng viên data/tin-ung-vien.json.

KHÔNG tự đăng lên web. Tin ứng viên còn phải được mở nguồn kiểm, viết tóm tắt đúng luật
CLAUDE.md, rồi mới vào ô "Cập nhật" trang chủ. Thà không đăng còn hơn đăng sai.
KHÔNG quét tin rao bán đất (việc của web khác), KHÔNG quét mạng xã hội / trang sau đăng nhập.

Học từ bộ đo chỉ số giá (26/9/2026): vào đúng cửa (từng kênh), lọc địa bàn bằng danh sách
nhận + loại trừ, chạy lịch sự (robots.txt, nghỉ giữa hai lần gọi, tự giới thiệu), bị chặn thì
ghi lại và bỏ — không vượt chặn; nguồn nào về 0 thì báo, tất cả về 0 thì báo đỏ.

  python3 scripts/quet-tin.py            # quét, ghi hàng đợi
  python3 scripts/quet-tin.py --tu-kiem  # chỉ chạy phép thử bộ lọc (không mạng) — CI chạy lệnh này
"""
import email.utils, hashlib, html, json, os, re, sys, time, unicodedata
import urllib.request, urllib.robotparser, urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HANG_DOI = os.path.join(ROOT, 'data', 'tin-ung-vien.json')
UA = 'GreenSpace-tin/1.0 (+https://greenspacers.vn; Zalo 0978 758 788)'
NGHI = 1.5          # giây nghỉ giữa hai lần gọi cùng một báo
TOI_DA_MOI_KENH = 60
CUA_SO_NGAY = 45    # chỉ nhận tin trong 45 ngày gần nhất

KENH = [  # (tên, url, loại): 'dia_phuong' = báo Lâm Đồng; 'chinh_sach' = cổng/báo chính phủ; 'toan_quoc' = báo lớn
    ('Báo Lâm Đồng — Pháp luật', 'https://baolamdong.vn/rss/phap-luat', 'dia_phuong'),
    ('Báo Lâm Đồng — Nhịp cầu bạn đọc', 'https://baolamdong.vn/rss/phap-luat/nhip-cau-ban-doc', 'dia_phuong'),
    ('Báo Lâm Đồng — Thời sự Lâm Đồng', 'https://baolamdong.vn/rss/thoi-su/thoi-su-lam-dong', 'dia_phuong'),
    ('Báo Lâm Đồng — Trang địa phương', 'https://baolamdong.vn/rss/trang-dia-phuong', 'dia_phuong'),
    ('Báo Lâm Đồng — Nông nghiệp nông thôn', 'https://baolamdong.vn/rss/kinh-te/nong-nghiep-nong-thon', 'dia_phuong'),
    ('Báo Lâm Đồng — Chính sách', 'https://baolamdong.vn/rss/chinh-sach', 'dia_phuong'),
    ('Báo Chính phủ', 'https://baochinhphu.vn/rss', 'chinh_sach'),
    ('Xây dựng chính sách', 'https://xaydungchinhsach.chinhphu.vn/rss', 'chinh_sach'),
    ('Dân trí — Pháp luật', 'https://dantri.com.vn/rss/phap-luat.rss', 'toan_quoc'),
    ('Dân trí — Bất động sản', 'https://dantri.com.vn/rss/bat-dong-san.rss', 'toan_quoc'),
    ('Tuổi Trẻ — Pháp luật', 'https://tuoitre.vn/rss/phap-luat.rss', 'toan_quoc'),
    ('Thanh Niên — Pháp luật', 'https://thanhnien.vn/rss/thoi-su/phap-luat.rss', 'toan_quoc'),
]

def bo_dau(s):
    s = unicodedata.normalize('NFD', s.replace('đ', 'd').replace('Đ', 'D'))
    return ''.join(c for c in s if unicodedata.category(c) != 'Mn').lower()

def co(t, cum): return re.search(r'(?<![a-z0-9])' + re.escape(bo_dau(cum)) + r'(?![a-z0-9])', t) is not None

# Chủ đề đúng việc GreenSpace (không phải tin rao / giá rao)
CHU_DE = ['lấn chiếm', 'lấn ranh', 'lấn đất', 'chiếm đất', 'tranh chấp đất', 'tranh chấp ranh', 'ranh giới', 'mốc giới',
          'sổ đỏ', 'giấy chứng nhận quyền sử dụng đất', 'quyền sử dụng đất', 'đất đai', 'quy hoạch', 'bảng giá đất',
          'chuyển mục đích', 'tách thửa', 'hợp thửa', 'thu hồi đất', 'cưỡng chế', 'san lấp', 'xây dựng trái phép',
          'xây dựng không phép', 'đo đạc', 'địa chính', 'trích lục', 'thuế đất', 'tiền sử dụng đất', 'sạt lở', 'sụt lún',
          'nứt đất', 'ngập', 'lũ quét', 'đất nông nghiệp', 'đất ở', 'thổ cư', 'luật đất đai']
# Địa bàn: chắc chắn là Nam Ban
NHAN_CHAC = ['Nam Ban', 'Lâm Hà']
# Tên thôn/xã cũ của Nam Ban trùng tên nơi khác (Hà Nội…) — chỉ tính khi đi kèm Nam Ban / Lâm Hà / Lâm Đồng
NHAN_KEM = ['Đông Thanh', 'Mê Linh', 'Gia Lâm', 'Buôn Chuối', 'Thăng Long', 'Chi Lăng', 'Bãi Công', 'Từ Liêm', 'Thanh Trì',
            'Linh Ẩn', 'thác Voi', 'Tổng Đội', 'Ba Đình', 'ĐT.725', 'tỉnh lộ 725']
LOAI_TRU = ['Nam Hà', 'Phi Tô', 'Tà Nung', 'Đinh Văn', 'Đạ Đờn', 'Tân Hà', 'Tân Văn', 'Phú Sơn', 'Liên Hà', 'Hoài Đức', 'Phúc Thọ',
            'Đan Phượng', 'Tân Thanh', 'Bảo Lộc', 'Di Linh', 'Đức Trọng', 'Lạc Dương', 'Đơn Dương', 'Cam Ly', 'Hà Nội']
# Tỉnh Lâm Đồng mới (từ 1/7/2025) gồm cả Đắk Nông, Bình Thuận cũ — tin ở các vùng này không liên quan chủ đất Nam Ban
LOAI_TRU_TINH = ['Đắk Nông', 'Gia Nghĩa', 'Đắk Mil', 'Đắk Song', "Đắk R'lấp", 'Krông Nô', 'Cư Jút', 'Tuy Đức', 'Đắk Lông',
                 'Bình Thuận', 'Phan Thiết', 'Hàm Thắng', 'Hàm Thuận', 'Bắc Bình', 'Tuy Phong', 'La Gi', 'Hàm Tân', 'Đức Linh',
                 'Tánh Linh', 'Phú Quý', 'Mũi Né', 'Bảo Lâm', 'Đạ Huoai', 'Đạ Tẻh', 'Cát Tiên', 'Đam Rông', 'Gia Bắc', 'Quốc lộ 55', 'Quốc lộ 28']
THIEN_TAI = ['sạt lở', 'sụt lún', 'nứt đất', 'ngập', 'lũ quét', 'sạt trượt']
# Tin chính sách đất (cấp tỉnh / toàn quốc) mà chủ đất ở xa cần biết — không gồm thiên tai
CHINH_SACH_DAT = ['bảng giá đất', 'tách thửa', 'hợp thửa', 'chuyển mục đích', 'sổ đỏ', 'giấy chứng nhận quyền sử dụng đất',
                  'thu hồi đất', 'tiền sử dụng đất', 'thuế đất', 'quy hoạch sử dụng đất', 'quy hoạch chung', 'luật đất đai',
                  'đất đai', 'lấn chiếm', 'tranh chấp đất', 'đo đạc', 'địa chính']
# Tin chính sách chung mà chủ đất ở xa cần biết (không cần địa bàn)
CHINH_SACH = ['luật đất đai', 'nghị định', 'nghị quyết', 'thông tư', 'bảng giá đất', 'tiền sử dụng đất', 'tách thửa',
              'chuyển mục đích', 'cấp giấy chứng nhận', 'sổ đỏ']

def phan_loai(tieu_de, tom_tat, loai_kenh):
    """→ (nhom, ly_do) với nhom ∈ {'dia_ban', 'tinh', 'chinh_sach', 'mo_ho', None}."""
    t = bo_dau(tieu_de + ' ' + tom_tat)
    if not any(co(t, k) for k in CHU_DE): return None, 'không đúng chủ đề'
    chac = [k for k in NHAN_CHAC if co(t, k)]
    kem = [k for k in NHAN_KEM if co(t, k)]
    lam_dong = co(t, 'Lâm Đồng')
    loai = [k for k in LOAI_TRU if co(t, k)]
    nhan = chac or (kem if (lam_dong or chac) else [])
    if nhan and loai: return 'mo_ho', f'vừa có {nhan[0]} vừa có {loai[0]}'
    if nhan: return 'dia_ban', f'nhắc {nhan[0]}'
    if loai: return None, f'nơi khác ({loai[0]})'
    if bo_dau(tieu_de).startswith(bo_dau('Lâm Đồng hôm nay')): return None, 'bản tin tổng hợp trong ngày'
    xa = [k for k in LOAI_TRU_TINH if co(t, k)]
    if xa: return None, f'vùng khác của tỉnh mới ({xa[0]})'
    dat = [k for k in CHINH_SACH_DAT if co(t, k)]
    if lam_dong and dat: return 'tinh', f'chính sách đất Lâm Đồng ({dat[0]})'
    if lam_dong: return None, 'tin Lâm Đồng nhưng không phải chính sách đất (thiên tai chỉ nhận khi đúng Nam Ban/Lâm Hà)'
    if loai_kenh == 'chinh_sach' and any(co(t, k) for k in CHINH_SACH): return 'chinh_sach', 'chính sách đất đai chung'
    return None, 'không thuộc địa bàn'

_robots = {}
def duoc_doc(url):
    host = urllib.parse.urlsplit(url); goc = f'{host.scheme}://{host.netloc}'
    if goc not in _robots:
        rp = urllib.robotparser.RobotFileParser(goc + '/robots.txt')
        try:
            req = urllib.request.Request(goc + '/robots.txt', headers={'User-Agent': UA})
            rp.parse(urllib.request.urlopen(req, timeout=15).read().decode('utf-8', 'ignore').splitlines())
        except Exception:
            rp = None   # không đọc được robots.txt → coi như cho phép (chuẩn chung), vẫn nghỉ lịch sự
        _robots[goc] = rp
    rp = _robots[goc]
    return True if rp is None else rp.can_fetch(UA, url)

def tai(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'application/rss+xml, application/xml, text/xml'})
    return urllib.request.urlopen(req, timeout=20).read()

def lam_sach(x):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', x or ''))).strip()

def doc_ngay(x):
    """Ngày trong RSS: chuẩn RFC 822, ISO, hoặc kiểu cổng Chính phủ "9/26/2026 9:20:00 AM" (giờ VN).
    Không đọc được → None (tin vẫn giữ nhưng ghi rõ không có ngày, không đoán)."""
    x = (x or '').strip()
    if not x: return None
    try: return email.utils.parsedate_to_datetime(x)
    except Exception: pass
    try: return datetime.fromisoformat(x.replace('Z', '+00:00'))
    except Exception: pass
    for f in ('%m/%d/%Y %I:%M:%S %p', '%m/%d/%Y %H:%M:%S', '%d/%m/%Y %H:%M'):
        try: return datetime.strptime(x, f).replace(tzinfo=timezone(timedelta(hours=7)))
        except Exception: pass
    return None

def doc_rss(raw):
    root = ET.fromstring(raw); ra = []
    for it in root.iter('item'):
        link = (it.findtext('link') or '').strip()
        link = urllib.parse.urlsplit(link)._replace(query='', fragment='').geturl()
        ngay = it.findtext('pubDate') or ''
        d = doc_ngay(ngay)
        ra.append(dict(tieu_de=lam_sach(it.findtext('title')), link=link,
                       tom_tat=lam_sach(it.findtext('description'))[:400], ngay=d))
    return ra

def quet():
    q = json.load(open(HANG_DOI, encoding='utf-8')) if os.path.exists(HANG_DOI) else {'da_thay': [], 'ung_vien': [], 'nhat_ky': []}
    da_thay = set(q['da_thay']); moi = []; nk = {'luc': datetime.now(timezone(timedelta(hours=7))).isoformat(timespec='minutes'), 'kenh': {}}
    han = datetime.now(timezone.utc) - timedelta(days=CUA_SO_NGAY)
    lan_cuoi = {}
    for ten, url, loai in KENH:
        host = urllib.parse.urlsplit(url).netloc
        if host in lan_cuoi: time.sleep(max(0, NGHI - (time.time() - lan_cuoi[host])))
        if not duoc_doc(url): nk['kenh'][ten] = 'robots.txt cấm — bỏ'; continue
        try:
            items = doc_rss(tai(url))[:TOI_DA_MOI_KENH]
        except Exception as e:
            nk['kenh'][ten] = f'lỗi/bị chặn — bỏ ({type(e).__name__})'; lan_cuoi[host] = time.time(); continue
        lan_cuoi[host] = time.time(); dem = 0
        for it in items:
            if not it['link'] or (it['ngay'] and it['ngay'] < han): continue
            h = hashlib.sha1(it['link'].encode()).hexdigest()[:16]
            if h in da_thay: continue
            da_thay.add(h)
            nhom, ly_do = phan_loai(it['tieu_de'], it['tom_tat'], loai)
            if not nhom: continue
            ma_tieu_de = bo_dau(it['tieu_de'])[:60]
            if any(bo_dau(x['tieu_de'])[:60] == ma_tieu_de for x in q['ung_vien'] + moi): continue   # trùng giữa các báo
            moi.append(dict(ma=h, nhom=nhom, ly_do=ly_do, tieu_de=it['tieu_de'], link=it['link'], nguon=ten,
                            ngay=it['ngay'].date().isoformat() if it['ngay'] else '', trang_thai='cho_kiem'))
            dem += 1
        nk['kenh'][ten] = f'đọc {len(items)} tin, {dem} ứng viên mới'
    nk['ung_vien_moi'] = len(moi)
    q['ung_vien'] = sorted(q['ung_vien'] + moi, key=lambda x: x['ngay'], reverse=True)
    q['da_thay'] = sorted(da_thay); q['nhat_ky'] = ([nk] + q.get('nhat_ky', []))[:30]
    os.makedirs(os.path.dirname(HANG_DOI), exist_ok=True)
    with open(HANG_DOI, 'w', encoding='utf-8') as f:
        json.dump(q, f, ensure_ascii=False, indent=1); f.write('\n')
    for ten, tt in nk['kenh'].items(): print(f'  {ten}: {tt}')
    print(f'→ {len(moi)} ứng viên mới; hàng đợi có {sum(1 for x in q["ung_vien"] if x["trang_thai"] == "cho_kiem")} tin chờ kiểm.')
    doc_duoc = [t for t in nk['kenh'].values() if t.startswith('đọc')]
    if not doc_duoc:
        print('✗ KHÔNG đọc được nguồn nào — nghi bị chặn hết hoặc mạng lỗi. Không có gì mới là KHÔNG bình thường.')
        return 1
    return 0

def tu_kiem():
    """Phép thử bộ lọc — mỗi dòng là một lỗi đã/đang có thể gặp."""
    T = [
        ('Phát hiện lấn chiếm đất rừng ở xã Nam Ban', '', 'dia_phuong', 'dia_ban'),
        ('Tranh chấp ranh giới đất tại thôn Mê Linh, Lâm Hà', '', 'dia_phuong', 'dia_ban'),
        ('Mê Linh (Hà Nội) xử lý lấn chiếm đất công', '', 'toan_quoc', None),          # trùng tên Hà Nội
        ('Gia Lâm cưỡng chế công trình xây dựng trái phép', '', 'toan_quoc', None),   # Gia Lâm Hà Nội, không kèm Lâm Đồng
        ('Lâm Đồng: sạt lở đất ở Tà Nung', '', 'dia_phuong', None),                  # nơi khác trong tỉnh
        ('Sạt lở ở Nam Ban và Tà Nung sau mưa lớn', '', 'dia_phuong', 'mo_ho'),        # vừa nhận vừa loại trừ
        ('Lâm Đồng công bố bảng giá đất mới', '', 'dia_phuong', 'tinh'),
        ('Hàm Thắng chủ động di dời người dân khỏi vùng có nguy cơ ngập sâu', 'Lâm Đồng', 'dia_phuong', None),   # Bình Thuận cũ
        ('Lâm Đồng khẩn trương ứng phó sụt lún ven hồ Đắk Lông Thượng', '', 'dia_phuong', None),                # Đắk Nông cũ
        ('Lâm Đồng hôm nay 25/09', 'sạt lở, quy hoạch, đất đai', 'dia_phuong', None),                            # bản tin tổng hợp
        ('Lâm Đồng xuyên đêm khắc phục sạt lở trên đèo Prenn', '', 'dia_phuong', None),                          # thiên tai ngoài Nam Ban
        ('Sạt lở đất ở thôn Chi Lăng, Nam Ban sau mưa', '', 'dia_phuong', 'dia_ban'),                            # thiên tai đúng Nam Ban
        ('Cần cơ chế gỡ vướng nợ tiền thuê đất của công ty lâm nghiệp ở Lâm Đồng', '', 'dia_phuong', 'tinh'),
        ('Nghị định mới về cấp giấy chứng nhận quyền sử dụng đất', '', 'chinh_sach', 'chinh_sach'),
        ('Nghị định mới về cấp giấy chứng nhận quyền sử dụng đất', '', 'toan_quoc', None),   # báo toàn quốc: cần địa bàn
        ('Nam Ban mùa hoa cà phê', '', 'dia_phuong', None),                            # đúng địa bàn, sai chủ đề
        ('Bán lô đất Nam Ban view đẹp giá rẻ', '', 'dia_phuong', None),                 # tin rao: không có chủ đề pháp lý
        ('Thôn Thăng Long có hộ san lấp trái phép', 'xã Nam Ban, Lâm Hà', 'dia_phuong', 'dia_ban'),
        ('Thăng Long: xử lý san lấp trái phép', 'Hà Nội', 'toan_quoc', None),
    ]
    sai = 0
    for x, mong in [('Fri, 25 Sep 2026 10:00:00 +0700', '2026-09-25'), ('9/26/2026 9:20:00 AM', '2026-09-26'),
                    ('2026-09-24T08:00:00+07:00', '2026-09-24'), ('', None), ('hôm qua', None)]:
        d = doc_ngay(x); ra = d.date().isoformat() if d else None
        if ra != mong: sai += 1; print(f'✗ ngày "{x}" → {ra}, mong {mong}')
    for td, tt, kenh, mong in T:
        ra, ly_do = phan_loai(td, tt, kenh)
        if ra != mong: sai += 1; print(f'✗ "{td}" [{kenh}] → {ra} ({ly_do}), mong {mong}')
    print('✓ Bộ lọc đúng cả', len(T), 'phép thử.' if not sai else f'\n{sai} phép thử sai.')
    return 1 if sai else 0

if __name__ == '__main__':
    sys.exit(tu_kiem() if '--tu-kiem' in sys.argv else quet())
