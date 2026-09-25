# GreenSpace (greenspacers.vn) — luật cho mọi phiên làm việc

Web tĩnh (HTML/CSS/JS nội tuyến) trên Vercel, `cleanUrls`. Nhánh `main` = production.
Dịch vụ: trông coi / quản lý đất, nhà, vườn tại **Nam Ban, Lâm Hà, Lâm Đồng** cho người ở xa.
Liên hệ duy nhất: Zalo / điện thoại **0978 758 788**. Người sáng lập & CEO: Đoàn Quốc Duyệt.

## Trước khi đẩy bất cứ thứ gì
```
python3 scripts/kiem-tra.py --base-ref origin/main   # phải ra ✓ Sạch
```
CI chạy lại đúng lệnh này mỗi lần push. Lỗi nào bẫy báo thì sửa lỗi, không sửa bẫy —
trừ khi soát tay thấy bẫy báo nhầm (khi đó sửa bẫy + ghi vào docs/LOI-DA-GAP-VA-CACH-KIEM.md).
Sửa một lỗi mới → thêm bẫy vào `scripts/kiem-tra.py` + thêm dòng phá vào `scripts/thu-pha-bay.py`, chạy thử phá, thấy nổ mới commit.

## Luật cứng
1. **Không nhắc / không link Panorama (nambanpanorama)** ở bất kỳ đâu — kể cả comment, meta, schema, fb-queue. Được link nambanvillas.vn khi hợp ngữ cảnh.
2. **Giọng:** "chúng tôi" = đội GreenSpace; "tôi" = người sáng lập, chỉ khi kể trải nghiệm thật; khách = "bạn". Không xưng "em". Không ngôi ba lạnh.
3. **Không chữ máy móc** trong mọi chữ khách đọc (thân trang, title, meta, alt, JSON-LD, llms.txt): script, tự động, auto, bot, AI, nhập tay, thuật toán. Viết "đội ngũ tổng hợp…". Thành ngữ "không tự động là…" → "không mặc nhiên là…".
4. **Không bịa số, không nói quá.** Giá / số lô / số năm lấy từ `data/so-lieu.json` (một nguồn). Số mới phải đối chiếu với bài có sẵn trên site trước khi viết. Không "hàng đầu", "số 1", "tốt nhất", "duy nhất", "100%…".
5. **Địa danh:** "Nam Ban, Lâm Hà, Lâm Đồng". Không viết "huyện Lâm Hà" (bỏ cấp huyện từ 1/7/2025). Có "Lâm Hà" ở mô tả thì phải có "Nam Ban" cạnh đó.
6. **Không tự xoá nội dung có ngày** (tin trong ô Cập nhật, bài cũ). Cũ thì tụt xuống, không gỡ. Gỡ trang thì phải có 301 trong vercel.json.
7. **Trang đang có thứ hạng: không đổi URL / title / H1.** Chỉ sửa số sai, thêm nội dung bên dưới, chỉnh mô tả. Title/H1 không chứa ngày, số tuần.
8. **Mô tả (meta description):** ≤ 160 ký tự, cắt ở **ranh câu** rồi đọc lại (không cắt theo số ký tự), có "Nam Ban"; og/twitter/JSON-LD description cũng có "Nam Ban".
9. **FAQ:** chữ trong FAQPage schema = chữ hiển thị, nguyên văn từng chữ.
10. **Ngày:** `datePublished` = ngày đăng thật (không lùi). `dateModified` = `lastmod` trong sitemap, chỉ tiến, chỉ đổi khi chữ khách đọc thật sự đổi.
11. **Ảnh:** đường dẫn tuyệt đối `/images/…`; alt chỉ tả cái thấy trong khung (mở ảnh ra xem rồi mới viết); ảnh đầu bài có srcset 640/900/1200 (`images/articles/<slug>-640.webp`, `-900.webp`).
12. **Nói đúng sự thật trên trang:** chỉ đưa tin có nguồn chính thức; tin đồn (sáp nhập, quy hoạch…) chưa có văn bản thì không đưa.

## Khuôn một trang bài / dịch vụ mới (phiếu cho ô đăng bài)
Chép từ một bài đang chạy (vd `xu-ly-lan-chiem-dat-tu-xa.html`) — giữ đủ:
- GA4 `G-TLZVX26QHR` đầu `<head>`, canonical + og:url = `https://greenspacers.vn/<slug>`, `speculationrules`.
- `<a class="skip-link" href="#main">` ngay sau `<body>`, `<main class="wrap" id="main">`, đúng 1 H1.
- H1 = câu người ta gõ; ngay dưới là đoạn `answer-lead` 40–60 chữ trả lời thẳng.
- **Trang dịch vụ** (liệt kê trong `data/so-lieu.json` → `trang_dich_vu`): cặp nút `quick-contact` (Zalo + Gọi) ngay dưới đoạn mở.
- Khối `cta-box` cuối bài: lời mời cụ thể theo chủ đề + **cả hai** nút Zalo và `tel:` (`class="cta-call"`).
- Nút nổi: icon Gọi là **SVG** (không dùng ký tự ☎), có `aria-label` cho cả Zalo và Gọi.
- FAQ `faq-item` + script bàn phím (role=button, Enter/Space) như bài mẫu; 3 JSON-LD: BlogPosting + FAQPage + BreadcrumbList (2 cấp, mỗi mục có `item`).
- Bảng bọc `<div class="tbl-wrap">`.
- Cập nhật: `sitemap.xml` (lastmod = dateModified), `llms.txt`, `feed.xml`, 1 `insight-card` ở `#insights` trang chủ.

## Ô "Cập nhật" trên trang chủ (khối `GS-UPDATES`)
Chèn mục mới ngay dưới `<!-- GS-UPDATES:START -->`, đúng mẫu `<li class="update-item">…`. **Không xoá mục cũ.** Cập nhật `lastmod` trang chủ trong sitemap.

## Báo cáo cho chủ web
Push / tạo PR / merge không thành → báo rõ **THẤT BẠI** kèm lỗi. Không bao giờ báo "xong" khi chưa thấy commit trên remote.
