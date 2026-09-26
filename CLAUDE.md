# GreenSpace (greenspacers.vn) — luật cho mọi phiên làm việc

Web tĩnh (HTML/CSS/JS nội tuyến) trên Vercel, `cleanUrls`. Nhánh `main` = production.
Dịch vụ: trông coi / quản lý đất, nhà, vườn tại **Nam Ban, Lâm Hà, Lâm Đồng** cho người ở xa.
Liên hệ duy nhất: Zalo / điện thoại **0978 758 788**. Người sáng lập & CEO: Đoàn Quốc Duyệt.

## Repo công khai + web tĩnh
- Repo GitHub **public**: mọi file commit ai cũng đọc được. Không đưa bí mật, token, tên web thứ ba.
- `.vercelignore` giữ CLAUDE.md, docs/, scripts/, data/, fb-queue/, .github/ **không lên greenspacers.vn** (bẫy B33).
- `docs/` bị `.gitignore` — tài liệu nội bộ chỉ nằm máy; muốn đưa lên repo thì `git add -f` và soát chữ trước.
- Ảnh đưa lên: chạy `python3 scripts/dong-dau-anh.py` — xoá metadata cũ (GPS, tên, bản quyền web khác) và **đóng dấu bản quyền GreenSpace** (EXIF + XMP chuẩn IPTC: © GreenSpace, greenspacers.vn, Zalo 0978 758 788, không dùng lại khi chưa đồng ý). Chèn thẳng, không nén lại. Bẫy B32 chặn ảnh thiếu dấu hoặc có GPS.

## Trước khi đẩy bất cứ thứ gì
```
python3 scripts/kiem-tra.py --base-ref origin/main   # phải ra ✓ Sạch
```
CI chạy lại đúng lệnh này mỗi lần push. Lỗi nào bẫy báo thì sửa lỗi, không sửa bẫy —
trừ khi soát tay thấy bẫy báo nhầm (khi đó sửa bẫy + ghi vào docs/LOI-DA-GAP-VA-CACH-KIEM.md).
Sửa một lỗi mới → thêm bẫy vào `scripts/kiem-tra.py` + thêm dòng phá vào `scripts/thu-pha-bay.py`, chạy thử phá, thấy nổ mới commit.

## Luật cứng
1. **Luật link: không nhắc / không link web thứ ba của chủ web** ở bất kỳ đâu — kể cả comment, meta, schema, fb-queue, **metadata ảnh**. Tên web đó không viết ra trong repo (repo công khai); bẫy B03 giữ tên ở dạng ghép ngược. Được link nambanvillas.vn khi hợp ngữ cảnh.
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
12. **FAQ mở sẵn** (đáp án hiện thẳng, vẫn gập được). **Bậc tiêu đề không nhảy cóc** (h1→h2→h3). Mỗi trang ≥ 3 link vào; khối "Bài liên quan" dùng chữ neo là **câu hỏi** bài đích trả lời, cấm "xem thêm / tại đây".
13. **Chữ trong chuỗi JS (câu xoay vòng, bản dịch) cũng là chữ khách đọc** — cùng luật số liệu, chữ máy móc, địa danh.
14. **Sửa hàng loạt:** JSON-LD sửa bằng `json.loads` → sửa cây → `json.dumps`, không regex. Khối HTML cắt bằng chỉ số (thẻ mở → thẻ đóng đúng), không `.*?` mù. Thay chữ hàng loạt xong thì chạy bẫy (lặp từ B29, ngoặc B05). Sửa một thứ thì kiểm **cả loại đó trên mọi trang**.
16. **Nói dịch vụ phải nói ở đâu** (chủ web chốt 26/9): câu mô tả việc GreenSpace làm, giá gói, lời mời liên hệ phải gắn "Nam Ban, Lâm Hà" tự nhiên trong câu — không viết chung chung "GreenSpace kiểm tra hàng tháng". Khối lời mời cuối trang bắt buộc có (bẫy B38). **Không nhồi**: "Nam Ban" ≤ 4% số chữ trang (bẫy B39); tiêu đề mục ("Tại sao là GreenSpace"), câu mà câu kề đã có địa danh thì để nguyên.
15. **Nói đúng sự thật trên trang:** chỉ đưa tin có nguồn chính thức; tin đồn (sáp nhập, quy hoạch…) chưa có văn bản thì không đưa.

## Vai của từng trang (chủ web chốt 25/9 — trùng chữ thì cùng lên, KHÔNG gộp)
- `/quan-ly-dat-nam-ban` = trang **dịch vụ** (gói, cách làm, chi phí, liên hệ).
- `/ve-greenspace` = trang **góc nhìn / GreenSpace là ai** (đội ngũ, điều chúng tôi tin, số liệu). Mô tả viết theo vai này, không viết như trang dịch vụ.
- Trang chủ và các bài khác trùng chữ với hai trang trên cũng giữ riêng; chỉ cần mỗi trang nói đúng vai và nối link qua lại.

## Làm theo từ khoá (một key một trang — chốt 26/9)
- Mỗi câu khách gõ chỉ có **một trang đích**. Trước khi viết trang mới: tìm trong repo xem đã có trang nào nhắm câu đó chưa → có thì làm dày trang đó, không đẻ trang trùng.
- Trang mới: title **bắt đầu đúng câu khách gõ**; FAQ đầu tiên là câu đó (hoặc biến thể có "giá/bao nhiêu"); trả lời các câu "Mọi người cũng hỏi" bằng H2 dạng câu hỏi.
- Trang đang chạy: không đổi title/H1 (luật 7) — chỉ thêm FAQ, thêm mục H2 bên dưới.
- Số lấy ở web khác (lương, giá thị trường) phải có nguồn + tháng/năm ngay trong câu, và ghi vào `data/so-lieu.json` → `gia_tham_chieu_ngoai` kèm `_nguon` (bẫy B06).
- Đọc phần tóm tắt AI của Google cho câu đó: thấy nói sai về GreenSpace (giá, địa danh cũ) thì viết đoạn nói đúng, có nguồn.
- **Khoá title tới 26/10/2026** (đang chờ Google đọc lại): `/thue-nguoi-trong-coi-dat-nam-ban`, `/gia-trong-coi-dat-bao-nhieu`, `/quan-ly-dat-nam-ban`.
- Nhắc tên hành chính cũ chỉ khi ghi rõ "cũ" ngay sau ("thị trấn Nam Ban cũ") — bẫy B27 cho qua đúng dạng đó.

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
- `<link rel="alternate" type="application/rss+xml" …feed.xml>` trong `<head>`; JSON-LD có `author` (người sáng lập) + `dateModified` (bẫy B34).
- Sửa bất kỳ trang nào xong: chạy `python3 scripts/tao-llms-full.py` (bẫy B35 chặn nếu `llms-full.txt` lệch trang).
- **Không khai sao/đánh giá trong JSON-LD** (aggregateRating, review): khách không chấm sao, Google cấm doanh nghiệp tự khai đánh giá về mình (bẫy B37). Lời khách chỉ để ở phần hiển thị.

## Ô "Cập nhật" trên trang chủ (khối `GS-UPDATES`) + quét tin
- **Nguồn tin:** `.github/workflows/quet-tin.yml` chạy 06:00 VN mỗi ngày → `scripts/quet-tin.py` đọc RSS báo chính thống (Báo Lâm Đồng, cổng Chính phủ, báo lớn), lọc đúng việc GreenSpace (lấn chiếm, ranh, quy hoạch, pháp lý đất; thiên tai chỉ khi đúng Nam Ban/Lâm Hà) → `data/tin-ung-vien.json` (trạng thái `cho_kiem`). **Không tự đăng lên web.** Không quét tin rao bán, không quét mạng xã hội/trang sau đăng nhập; robots.txt cấm thì bỏ, bị chặn thì bỏ — không vượt chặn.
- Tên thôn cũ của Nam Ban trùng tên Hà Nội (Mê Linh, Gia Lâm, Thanh Trì, Từ Liêm, Ba Đình, Thăng Long) → chỉ tính khi kèm Nam Ban/Lâm Hà/Lâm Đồng. Tỉnh Lâm Đồng mới gồm cả Đắk Nông, Bình Thuận cũ → tin vùng đó loại. Sửa bộ lọc thì thêm phép thử vào `--tu-kiem` (CI chạy).
- **Đăng:** lấy tin `cho_kiem` → mở nguồn gốc kiểm ngày, nội dung → viết 2–3 câu đúng luật (nói rõ nếu mới là dự thảo/định hướng) → chèn ngay dưới `<!-- GS-UPDATES:START -->`, đúng mẫu `<li class="update-item">…` → đổi trạng thái tin thành `da_dang` hoặc `bo` + `ghi_chu` lý do. **Không xoá mục cũ.** Cập nhật `lastmod` trang chủ + `dateModified` WebPage trang chủ (bằng nhau), chạy `tao-llms-full.py`.
- Commit chỉ đổi `data/`, `scripts/`, `docs/`, `.github/`, `fb-queue/`, `CLAUDE.md` → Vercel **bỏ qua deploy** (`ignoreCommand` trong vercel.json) — không tốn lượt deploy.

## Báo cáo cho chủ web
Push / tạo PR / merge không thành → báo rõ **THẤT BẠI** kèm lỗi. Không bao giờ báo "xong" khi chưa thấy commit trên remote.
