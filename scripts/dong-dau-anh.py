#!/usr/bin/env python3
"""Đóng dấu bản quyền GreenSpace vào ảnh — chèn thẳng vào file, KHÔNG nén lại (ảnh giữ nguyên chất lượng).

Mỗi ảnh mang: EXIF (Artist, Copyright, ImageDescription) + XMP chuẩn IPTC mà Google Images đọc
(dc:creator, dc:rights, xmpRights:WebStatement, UsageTerms, Credit, Licensor, liên hệ).
KHÔNG ghi toạ độ GPS. Xoá mọi EXIF/XMP cũ (kể cả dấu của web khác) trước khi đóng.
Chạy lại bao nhiêu lần cũng được (idempotent).

  python3 scripts/dong-dau-anh.py              # đóng dấu mọi ảnh trong images/
  python3 scripts/dong-dau-anh.py images/a.jpg # chỉ ảnh chỉ định
Ảnh mới: nén/xuất xong → chạy lệnh này → bẫy B32 trong kiem-tra.py chặn ảnh thiếu dấu.
"""
import os, struct, sys

NAM = '2026'
EXIF_TXT = {  # EXIF chỉ nhận ASCII — chữ có dấu và © để trong XMP
    0x010E: 'GreenSpace - greenspacers.vn - Zalo 0978 758 788',                # ImageDescription
    0x013B: 'GreenSpace',                                                      # Artist
    0x8298: f'Copyright {NAM} GreenSpace - greenspacers.vn. All rights reserved.',  # Copyright
}
DAU_NHAN = b'greenspacers.vn'   # bẫy B32 tìm chuỗi này trong EXIF và XMP
XMP = f'''<?xpacket begin="﻿" id="W5M0MpCehiHzreSzNTczkc9d"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/">
 <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about=""
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:xmpRights="http://ns.adobe.com/xap/1.0/rights/"
    xmlns:photoshop="http://ns.adobe.com/photoshop/1.0/"
    xmlns:Iptc4xmpCore="http://iptc.org/std/Iptc4xmpCore/1.0/xmlns/"
    xmlns:plus="http://ns.useplus.org/ldf/xmp/1.0/"
    xmpRights:Marked="True"
    xmpRights:WebStatement="https://greenspacers.vn/"
    photoshop:Credit="GreenSpace">
   <dc:creator><rdf:Seq><rdf:li>GreenSpace</rdf:li></rdf:Seq></dc:creator>
   <dc:rights><rdf:Alt><rdf:li xml:lang="x-default">© {NAM} GreenSpace — greenspacers.vn</rdf:li></rdf:Alt></dc:rights>
   <xmpRights:UsageTerms><rdf:Alt><rdf:li xml:lang="x-default">Không dùng lại khi chưa có sự đồng ý của GreenSpace. Liên hệ Zalo 0978 758 788.</rdf:li></rdf:Alt></xmpRights:UsageTerms>
   <Iptc4xmpCore:CreatorContactInfo rdf:parseType="Resource">
    <Iptc4xmpCore:CiUrlWork>https://greenspacers.vn/</Iptc4xmpCore:CiUrlWork>
    <Iptc4xmpCore:CiTelWork>0978 758 788</Iptc4xmpCore:CiTelWork>
   </Iptc4xmpCore:CreatorContactInfo>
   <plus:Licensor><rdf:Seq><rdf:li rdf:parseType="Resource">
    <plus:LicensorName>GreenSpace</plus:LicensorName>
    <plus:LicensorURL>https://greenspacers.vn/</plus:LicensorURL>
    <plus:LicensorTelephone1>0978 758 788</plus:LicensorTelephone1>
   </rdf:li></rdf:Seq></plus:Licensor>
  </rdf:Description>
 </rdf:RDF>
</x:xmpmeta>
<?xpacket end="w"?>'''.encode('utf-8')
XMP_HDR = b'http://ns.adobe.com/xap/1.0/\x00'


def tiff():
    """Khối TIFF/EXIF tối giản (big-endian), chỉ IFD0 với 3 thẻ chữ — không GPS."""
    tags = sorted(EXIF_TXT.items())
    n = len(tags); data_off = 8 + 2 + n * 12 + 4
    ent, data = b'', b''
    for tag, val in tags:
        v = val.encode('ascii') + b'\x00'
        if len(v) <= 4:
            ent += struct.pack('>HHI', tag, 2, len(v)) + v.ljust(4, b'\x00')
        else:
            ent += struct.pack('>HHII', tag, 2, len(v), data_off + len(data))
            data += v + (b'\x00' if len(v) % 2 else b'')
    return b'MM\x00\x2a' + struct.pack('>I', 8) + struct.pack('>H', n) + ent + b'\x00\x00\x00\x00' + data


def dong_jpeg(b):
    assert b[:2] == b'\xff\xd8', 'không phải JPEG'
    i, giu, sau_app0 = 2, [], 0
    while i < len(b) and b[i] == 0xFF:
        m = b[i + 1]
        if not (0xE0 <= m <= 0xEF or m == 0xFE): break          # hết đoạn APPn/COM đầu file
        ln = struct.unpack('>H', b[i + 2:i + 4])[0]; seg = b[i:i + 2 + ln]; body = seg[4:]
        cu = m == 0xE1 and (body.startswith(b'Exif\x00\x00') or body.startswith(XMP_HDR))
        if not cu:
            giu.append(seg)
            if m == 0xE0: sau_app0 = len(giu)
        i += 2 + ln
    def app1(p): return b'\xff\xe1' + struct.pack('>H', len(p) + 2) + p
    moi = [app1(b'Exif\x00\x00' + tiff()), app1(XMP_HDR + XMP)]
    giu[sau_app0:sau_app0] = moi
    return b'\xff\xd8' + b''.join(giu) + b[i:]


def chunks(b):
    i = 12
    while i + 8 <= len(b):
        cid = b[i:i + 4]; sz = struct.unpack('<I', b[i + 4:i + 8])[0]
        yield cid, b[i + 8:i + 8 + sz]
        i += 8 + sz + (sz & 1)


def chunk(cid, p): return cid + struct.pack('<I', len(p)) + p + (b'\x00' if len(p) & 1 else b'')


def dong_webp(b):
    assert b[:4] == b'RIFF' and b[8:12] == b'WEBP', 'không phải WebP'
    cs = [(c, p) for c, p in chunks(b) if c not in (b'EXIF', b'XMP ')]
    if cs[0][0] == b'VP8X':
        p = bytearray(cs[0][1]); p[0] |= 0x08 | 0x04; cs[0] = (b'VP8X', bytes(p))
    else:
        c, p = cs[0]; alpha = 0
        if c == b'VP8 ':
            assert p[3:6] == b'\x9d\x01\x2a', 'khung VP8 lạ'
            w = struct.unpack('<H', p[6:8])[0] & 0x3FFF; h = struct.unpack('<H', p[8:10])[0] & 0x3FFF
        elif c == b'VP8L':
            bits = int.from_bytes(p[1:5], 'little')
            w = (bits & 0x3FFF) + 1; h = ((bits >> 14) & 0x3FFF) + 1; alpha = 0x10 if (bits >> 28) & 1 else 0
        else:
            raise ValueError(f'chunk đầu lạ {c}')
        vp8x = bytes([0x08 | 0x04 | alpha, 0, 0, 0]) + (w - 1).to_bytes(3, 'little') + (h - 1).to_bytes(3, 'little')
        cs.insert(0, (b'VP8X', vp8x))
    body = b'WEBP' + b''.join(chunk(c, p) for c, p in cs) + chunk(b'EXIF', tiff()) + chunk(b'XMP ', XMP)
    return b'RIFF' + struct.pack('<I', len(body)) + body


def dong(path):
    b = open(path, 'rb').read()
    ext = path.lower().rsplit('.', 1)[-1]
    nb = dong_jpeg(b) if ext in ('jpg', 'jpeg') else dong_webp(b) if ext == 'webp' else None
    if nb is None: return None
    if nb != b: open(path, 'wb').write(nb)
    return len(nb) - len(b)


if __name__ == '__main__':
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ds = sys.argv[1:] or sorted(os.path.join(d, f) for d, _, fs in os.walk(os.path.join(root, 'images')) for f in fs)
    tong = n = 0
    for p in ds:
        r = dong(p)
        if r is not None: n += 1; tong += r
    print(f'Đã đóng dấu {n} ảnh, tổng thay đổi {tong:+,} byte.')
