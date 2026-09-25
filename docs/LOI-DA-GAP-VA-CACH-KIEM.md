# GreenSpace — lỗi đã gặp và cách kiểm

Sổ lỗi thật của greenspacers.vn. Mỗi lỗi: **đã làm · vì sao · cách kiểm (mã bẫy)**.
Bẫy nằm trong `scripts/kiem-tra.py`, chạy trên CI mỗi lần push (`.github/workflows/kiem-tra.yml`).
Thử phá: `python3 scripts/thu-pha-bay.py` (45 lần phá, 31 bẫy — tất cả phải nổ).

## Đợt 25/9/2026 — áp bàn giao đợt 2 của Nam Ban Villas + các lỗi cùng họ

| # | Lỗi | Đã làm | Bẫy |
|---|---|---|---|
| 1 | **Nút Gọi nổi dùng ký tự ☎ (`&#9742;`) trên 19 trang** — cùng họ với lỗi nặng nhất bên Villas (nút Gọi rỗng trên 147 trang). Máy thiếu font có ký tự này sẽ hiện nút rỗng. | Đổi sang icon SVG như trang chủ, thêm `aria-label` cho cả Zalo và Gọi. | B07 (soát cả markup lẫn CSS) |
| 2 | Chữ trắng trên nút vàng ở khối cuối bài: **2,25:1** (19 trang) — đúng lỗi Villas. | Chữ tối `#1a1a1a` → 7,7:1. | B14 |
| 3 | **Viền focus vàng trên nền sáng chỉ 2,12:1** — người dùng bàn phím không thấy mình đang ở đâu. | Viền hai lớp: vòng tối sát phần tử + vòng vàng ngoài → thấy trên cả nền sáng lẫn tối. | B14 |
| 4 | Breadcrumb/chân trang `#999` (2,7:1), dòng dẫn `#777` (4,2:1), dấu `›` `#ccc`; trang chủ 14 chỗ dưới chuẩn (nhãn tối trên nền tối, tag bảng giá, chữ mờ .3–.5 trên nền đen…). | Tính lại từng màu bằng công thức WCAG, đổi tối thiểu để đạt 4,5:1. | B14 |
| 5 | **FAQ trên 18 trang chỉ mở bằng chuột** (`div onclick`). | Script bàn phím: `role=button`, `tabindex`, Enter/Space, `aria-expanded`. | B13 |
| 6 | Không có skip link trên trang bài; **trang chủ không có `<main>`**. | Thêm skip link + `<main id="main">` mọi trang. | B13 |
| 7 | Menu điện thoại không có Zalo/Gọi; hamburger thiếu `aria-expanded`; không trả focus khi đóng. | Thêm "Nhắn Zalo" + "Gọi 0978 758 788" cuối menu; aria-expanded; mở thì focus mục đầu, Esc thì trả focus về hamburger. | B08 |
| 8 | **Nút "Nhắn Zalo để chọn gói phù hợp" không mở Zalo** — chỉ cuộn xuống chân trang. Nút hero "Kiểm tra đất của tôi" và "Tư vấn ngay" cũng chỉ cuộn. | Cả ba đi thẳng Zalo. | B08 |
| 9 | Liên hệ trong trang đặt ở 64–83% chiều dài trang; khối rủi ro trang chủ (chỗ khách lo nhất) không có nút. | Cặp Zalo/Gọi ngay dưới đoạn mở của 9 trang dịch vụ; giữa trang hỏi đáp; ngay sau khối rủi ro trang chủ; khối cuối bài có thêm nút Gọi. | B08, B09 |
| 10 | Ảnh đầu bài 1200px tải cho mọi điện thoại (tới 238 KB). | Thêm bản 640/900px webp + `srcset/sizes`: điện thoại tải 20–70 KB. | B19 |
| 11 | Không có trang 404 riêng; không có Content-Security-Policy. | `404.html` (noindex, có Zalo/Gọi + link trang chính); CSP liệt kê đúng nguồn đang dùng (GA4, Google Fonts) — thử bằng máy chủ gửi header thật, 0 vi phạm, và thử phá (bỏ Google Fonts → thấy vi phạm). | — |
| 12 | Chữ máy móc: "Đất rẻ không phải món hời **tự động**". | "…không mặc nhiên là món hời." | B04 |
| 13 | Nói quá: "Đất là tài sản **duy nhất** người ta mua rồi bỏ mặc" (thân bài + og + twitter). | "…thứ tài sản người ta dễ mua rồi bỏ mặc". | B15 |
| 14 | Trang Kiểm tra đất Lâm Hà: mô tả chỉ có "Lâm Hà", không neo "Nam Ban". | Mô tả + og + JSON-LD: "Nam Ban, Lâm Hà, Lâm Đồng". Title/H1 giữ nguyên (luật giữ thứ hạng). | B05, B20 |
| 15 | 5 mô tả dài 162–165 ký tự. | Rút ở ranh ý, giữ từ khoá, đọc lại từng câu. | B05 |
| 16 | **Lịch "Tin cập nhật" có lệnh "giữ tối đa 6 mục, xoá mục cũ nhất".** | Gỡ khỏi prompt lịch; luật trong CLAUDE.md. | B16 |
| 17 | **Hai lịch tự động báo "thành công" nhưng không đăng gì** — lịch bài SEO chạy từ 25/7 mà repo chưa từng có nhánh `content/`; lịch tin chỉ có nhánh ngày 4/9 (ngày tạo). Phiên do lịch chạy không đẩy được lên GitHub. | Prompt thêm: đẩy không được thì báo THẤT BẠI. Cần chủ web cấp quyền repo cho lịch (xem báo cáo). | — (kiểm tay: có nhánh/commit mới sau mỗi lần chạy không) |

### Đã rà nhưng không phải lỗi ở GreenSpace
- Trùng ý định giữa các trang: cao nhất 15% (5-gram), dưới xa ngưỡng gộp 50% → không gộp.
- Số trong title/mô tả sai do gõ tay: giá, "50+ lô", "hơn 4 năm" khớp nhau toàn site. "2.490.000đ" là giá gói nhà vườn riêng (có từ PR #20), khớp trong trang → đưa vào `data/so-lieu.json`.
- `speakable` trỏ phần tử có thật; link nội bộ không có `.html`/`/` cuối; lastmod = dateModified 20/20 trang; không ô nhập nào < 16px (web không có form).
- Trang đang có > 1.800 chữ: không có (dài nhất ~1.300) → luật "khối giữa bài" không áp.
- Cache CSS/JS: web không có file CSS/JS ngoài (đều nội tuyến); ảnh đã `immutable`.
- Hamburger 44×44 (đạt).

### Bẫy tự viết sai (đã sửa trước khi tin)
- B06 bắt nhầm "đ" trong "**đ**ến" thành đơn vị tiền → thêm `(?!\w)`.
- B12 báo ảnh `founder.jpg` không tồn tại — nó nằm trong comment chừa chỗ ảnh → bỏ comment trước khi dò.
- B02 báo 4 câu FAQ lệch chữ — do bóc thẻ `<a>` chèn thêm dấu cách → thẻ trong dòng bỏ không chèn cách.
- B15 bắt "cách rẻ nhất để giữ" (câu tự nhiên trong tin) → bỏ "rẻ nhất" khỏi danh sách.
- Tự gây: chọn màu `›` #767676 tính trên nền trắng (4,54) nhưng nền trang là kem #f9f8f6 (4,28) — bẫy B14 bắt → đổi #6b6b6b.

## Đợt 25/9/2026 (tối) — đóng dấu bản quyền ảnh (theo cách Nam Ban Villas)
- 54 ảnh trước đó trống thông tin chủ ảnh. `scripts/dong-dau-anh.py` chèn EXIF (Artist, Copyright, ImageDescription — chỉ ASCII) + XMP chuẩn IPTC (dc:rights "© 2026 GreenSpace — greenspacers.vn", creator, WebStatement, UsageTerms, Credit, Licensor, liên hệ) **thẳng vào file JPEG/WebP, không nén lại**.
- Đã kiểm: 54/54 ảnh giữ nguyên từng điểm ảnh; chạy lại không đổi thêm (idempotent); XMP đọc được bằng trình phân tích XML; Chromium hiển thị 54/54; mọi trang tải đủ ảnh. Thêm ~1,8 KB/ảnh. Không ghi GPS.
- B32 đổi từ "không metadata" → "phải có dấu GreenSpace, không GPS". Thử phá: xoá dấu → nổ; gắn GPS (giữ nguyên XMP) → nổ đúng lý do GPS.

## Đợt 25/9/2026 (chiều) — lộ tên web thứ ba + file nội bộ công khai

| # | Lỗi | Đã làm | Bẫy |
|---|---|---|---|
| 26 | **Ảnh founder mang metadata bản quyền ghi tên + tên miền web thứ ba** (EXIF Copyright + XMP), đang phục vụ trên greenspacers.vn — Google Images đọc được. Không có GPS. | Xoá sạch EXIF/XMP. Bẫy quét cả byte trong ảnh. | B03, B32 |
| 27 | **Không có `.vercelignore`** → CLAUDE.md (có tên web thứ ba), scripts/, data/, fb-queue/ nằm công khai trên greenspacers.vn. | Thêm `.vercelignore`. | B33 |
| 28 | Tên web thứ ba viết thẳng trong CLAUDE.md, kiem-tra.py, thu-pha-bay.py (repo công khai). | Bỏ tên; bẫy giữ tên ở dạng ghép ngược. Lịch sử git cũ vẫn còn — không viết lại lịch sử repo công khai. | B03 |
| 29 | **Báo cáo sai của chính người sửa:** nói `docs/LOI-DA-GAP…` và `docs/HUONG-DAN…` đã vào repo ở PR #31–33, thực ra `docs/` bị `.gitignore` nên chưa từng lên. | `git add -f` sau khi soát chữ. Luật: sau commit phải `git ls-files` kiểm file có thật trong repo. | — |

## Đợt 25/9/2026 (tiếp) — áp sổ lỗi đợt 2 của Nam Ban Villas (40 lỗi + 6 bài học gốc)

| # | Lỗi | Đã làm | Bẫy |
|---|---|---|---|
| 18 | **Lỗi tự gây ở PR #31:** đổi `style` nội tuyến thành `class="xref"` ở trang giá mà trang đó không có CSS `.xref` → dòng chữ mất kiểu. Đúng bài học gốc "chép tay nhiều trang thì có trang sai" + "chỉ kiểm cái vừa sửa là sót". | Thêm CSS; bẫy soát mọi class dùng mà trang không định nghĩa. | B22 |
| 19 | Bậc tiêu đề nhảy cóc: trang chủ h2→h4 (tên khách, khối Chuyện thật, cột chân trang), kiem-tra h1→h3. | Đổi h4→h3 kèm đổi selector CSS (cỡ chữ đã ghi rõ nên không đổi giao diện); kiem-tra thêm H2 dạng câu hỏi "Mỗi lần kiểm tra thực địa gồm những gì?". | B24 |
| 20 | **91 câu FAQ trên 19 trang đóng sẵn**; FAQ trang chủ giới hạn `max-height:300px` (câu dài có thể bị cắt) và mở câu này thì đóng câu khác. | Mở sẵn hết (luật Villas #29), vẫn gập được; bỏ giới hạn chiều cao; không đóng câu khác; `aria-expanded`. | B25 |
| 21 | **Số thống kê không nguồn nằm trong chuỗi JS**: "80% trường hợp mọi thứ ổn" (câu xoay vòng trang chủ, cả bản EN). Máy quét chỉ đọc HTML nên bỏ sót. | "Phần lớn các lần kiểm tra, mọi thứ vẫn ổn." Bẫy đọc cả chữ trong chuỗi JS. | B28 (+ B04 cho chuỗi JS) |
| 22 | Tên hành chính đã bỏ: "bộ phận một cửa **cấp huyện**" (trích lục, cả trong FAQ schema), "nộp ở đúng **huyện**", "ở xã, **huyện**". | Theo quy định hiện hành: bộ phận một cửa của UBND xã / Văn phòng đăng ký đất đai; sửa cả chữ hiện và schema cùng lúc. | B27 |
| 23 | Lặp từ gõ nhầm "nên nên làm cả hai" (thân + schema). | "vì vậy nên làm cả hai". | B29 |
| 24 | **3 bài pháp lý (quy hoạch, thuế đất, trích lục) mỗi bài chỉ 1 link vào**; khảo sát, xử lý lấn chiếm, bán đất, về GreenSpace chỉ 2 (đếm đúng, không tính trang noindex). | Nối vào khối "Bài liên quan" của bài cùng cụm, chữ neo là câu hỏi bài đích trả lời (21 link). Bài ít nhất giờ có 3 link vào. | B30 |
| 25 | Nút VI/EN là nút bật/tắt mà thiếu `aria-pressed`. | Thêm và cập nhật khi đổi. | B26 |

### Rà theo sổ đợt 2 nhưng không phải lỗi ở GreenSpace
- #1 canonical ra ngoài: 0. #9 ảnh gãy: 0. #14 nút gọi hàm không có: 0. #13 cache CSS: web không có file CSS/JS ngoài.
- #6 thẻ trỏ sai bài: máy báo 5, soát tay đều đúng (neo là cụm từ trong câu trả lời; tiêu đề thẻ khớp bài).
- #17 thì tương lai: các chữ "sắp" đều là "sắp mua/sắp xây/sắp bán" — cách nói thường, không phải mốc đã qua.
- #19 hub: 3 trang không có trong ô "Hiểu đất" (hỏi đáp, nhà vườn, về GreenSpace) không phải bài "hiểu đất" và đã có link từ khối khác trên trang chủ.
- Lặp từ: "đo đo ngó ngó", "từ từ", "xa xa", "bằng bằng chứng" là tiếng Việt đúng.
- Thuế suất 0,03% / 0,07–0,15%, "30–50%" (NQ 254): có văn bản nguồn.
- Độ sâu bấm: mọi trang cách trang chủ 1 lần bấm; không trang mồ côi.
- #7, #8, #10, #11, #20–23, #26, #27: web không có danh sách hàng / bộ lọc / hub sản phẩm.

### Tự cắn từ khoá — chủ web đã quyết (25/9): trùng thì cùng lên, không gộp
"Về GreenSpace" ↔ "Quản lý đất Nam Ban" trùng 41% chữ (title + mô tả + H2). Chủ web chốt: `/ve-greenspace` là trang **góc nhìn / GreenSpace là ai**, `/quan-ly-dat-nam-ban` là trang **dịch vụ**. Đã viết lại mô tả (meta/og/twitter) của trang Về GreenSpace theo vai góc nhìn; title/H1 giữ nguyên (luật trang đang có thứ hạng). Luật ghi trong CLAUDE.md.

### Bẫy tự viết sai trong đợt (đã sửa trước khi tin)
- B30 đếm cả link từ trang noindex `anh-da-dung` → tưởng đủ link vào; đếm đúng thì 2 trang còn thiếu.
- Mẫu phá B30 ban đầu bỏ 1 link khỏi bài có 5 link vào → vẫn ≥3 nên không nổ; mẫu phá sai, không phải bẫy sai → chọn bài có đúng 3.
- Script sửa suýt cắt hàm `toggleFaq` ở dấu `}` của khối `if` (cắt khối mù) → neo vào `</script>`, kiểm cú pháp JS bằng node sau khi sửa.

## Các đợt trước (tóm tắt)
- 25/9 (sổ rà soát web anh em): datePublished lùi; mô tả thiếu "Nam Ban"; ảnh đường dẫn tương đối; 10 alt tả sai ảnh (6 cái do người rà tự viết mà không mở ảnh); bảng không cuộn; tin NQ 254 nói quá "giảm 70%"; trang mồ côi; fb-queue nói Làng Gà ở Nam Ban (sai) và link web thứ ba.
- 12/9: 85 luật CSS chết; thiếu skip link trang chủ; og:title vỡ vì dấu nháy; header bảo mật.

## Bẫy — bảng tra
| Mã | Kiểm gì |
|---|---|
| B01 | JSON-LD đọc được |
| B02 | FAQ schema = chữ hiển thị (nguyên văn) |
| B03 | Không có tên web thứ ba ở mọi file trong repo (kể cả metadata ảnh) |
| B32 | Ảnh mang dấu bản quyền GreenSpace (EXIF + XMP), không GPS |
| B33 | .vercelignore giữ file nội bộ không lên web |
| B04 | Không chữ máy móc (thân, khung, llms.txt) |
| B05 | Mô tả ≤160, hết câu, ngoặc đủ, có "Nam Ban" (meta/og/twitter/JSON-LD) |
| B06 | Giá /tháng, "N+ lô", "hơn N năm" khớp `data/so-lieu.json` |
| B07 | Nút Gọi nổi có SVG + aria-label, và CSS nút nổi có thật |
| B08 | Mỗi trang có Zalo + Gọi trong trang; cta-box đủ cặp; menu điện thoại có Zalo/Gọi; nút chính trang chủ đi thẳng Zalo |
| B09 | Trang dịch vụ có quick-contact trước H2 đầu |
| B10 | speculationrules |
| B11 | Sitemap đủ trang; lastmod = dateModified; lastmod chỉ tiến; dateModified ≥ datePublished |
| B12 | Ảnh tuyệt đối + tồn tại; link nội bộ không `.html`, không `/` cuối, không chết |
| B13 | Skip link, `<main id="main">`, FAQ bàn phím, không chặn zoom, bảng bọc cuộn, ảnh có alt |
| B14 | Tương phản (công thức WCAG) trong cùng luật CSS + breadcrumb/footer/xref trên nền trang; cấm viền focus chỉ vàng |
| B15 | Không nói quá |
| B16 | Không mất tin có ngày trong ô Cập nhật; không mất URL sitemap mà thiếu 301 |
| B17 | Title/H1 không chứa ngày/tuần |
| B19 | Ảnh đầu bài có srcset nhiều cỡ |
| B20 | Mô tả có "Lâm Hà" phải neo "Nam Ban" |
| B21 | canonical/og:url đúng; đúng 1 H1 |
| B22 | Mọi class dùng trên trang phải có CSS trên trang đó |
| B23 | onclick gọi hàm có thật; JS tìm id có thật |
| B24 | Bậc tiêu đề không nhảy cóc |
| B25 | Câu hỏi FAQ mở sẵn |
| B26 | Nút bật/tắt có aria-pressed |
| B27 | Không "huyện/thị trấn" (bỏ từ 1/7/2025) — thân, khung, chuỗi JS |
| B28 | Không số thống kê không nguồn — thân, khung, chuỗi JS |
| B29 | Không lặp từ gõ nhầm |
| B30 | Mỗi trang ≥ 3 link vào từ trang lập chỉ mục khác |
