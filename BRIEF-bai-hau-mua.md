# BRIEF DỰNG TRANG WEB — GREENSPACE (greenspacers.vn)
## Bài: "Mua đất xong rồi để đó — lô của bạn giờ ra sao?"

> Đây là brief tự chứa. Bạn (Claude Code) chưa biết gì về dự án này, nên mọi thứ cần thiết đều nằm trong tài liệu này. Đọc hết trước khi code. Mục tiêu: tạo **1 file HTML tĩnh hoàn chỉnh**, tên `dat-mua-roi-de-do-tu-xa.html`, đúng khuôn các trang đang chạy trên site.

---

## 1. BỐI CẢNH DỰ ÁN (để hiểu, không in ra web)

**GreenSpace** (greenspacers.vn) là một *landing dịch vụ* cho người sở hữu đất ở Nam Ban, Lâm Hà, Lâm Đồng nhưng sống xa (Sài Gòn, Hà Nội…). Dịch vụ: trông coi / kiểm tra / quản lý / giữ đất hộ người ở xa — kiểm tra định kỳ hàng tháng, báo cáo ảnh GPS, cảnh báo lấn chiếm, xác minh ranh mốc.

Đây là web **CÓ bán dịch vụ** (có bảng giá, có CTA tử tế), khác với một web anh em chỉ phân tích (không bán). Giọng gần gũi, tin cậy, không màu mè.

**Website là HTML tĩnh thuần** (không framework, không React, không build step). Mỗi trang là 1 file .html độc lập, tự chứa CSS trong `<style>` và JS trong `<script>`. Deploy qua Vercel tự động từ GitHub. → **Giữ nguyên kiến trúc tĩnh này.** Không thêm thư viện, không dùng localStorage/sessionStorage.

---

## 2. LANE & ĐIỀU CẤM (tuân tuyệt đối)

**Được:** nói về dịch vụ giữ/trông coi/kiểm tra đất hộ; có bảng giá; có CTA "Nhắn Zalo" / "Kiểm tra đất của tôi".

**CẤM:**
- KHÔNG bịa số liệu, vụ việc, tên người, tên khu. Chỉ dùng số ở mục 4.
- KHÔNG đổ lỗi môi giới hay hàng xóm — chỉ nêu *nỗi lo của khách* một cách nhẹ nhàng.
- KHÔNG popup, đếm ngược, "còn X suất", share ép — khách nhạy cảm, marketing lộ liễu làm mất trust.
- KHÔNG dùng ảnh stock. Nếu cần chỗ ảnh, để placeholder ghi chú "ảnh thật do chủ dự án cung cấp sau".
- KHÔNG link sang bất kỳ web tên "Panorama" nào (lý do nội bộ). Được phép link sang `nambanvillas.vn` nếu ngữ cảnh hợp.

---

## 3. GIỌNG VĂN

- Xưng hô linh hoạt: thân bài có thể dùng "bạn" hoặc giọng kể mộc mạc ("mình", "bà con"); phần CTA/FAQ trang trọng có thể "bạn". **Nhất quán trong 1 trang.** Không dùng "quý khách".
- Câu ngắn, thật, không sáo. Chạm nỗi lo bằng hình ảnh cụ thể (cỏ mọc, rào xê dịch), không hù dọa.
- Tông "im lặng mà sang": điềm đạm, ít tính từ, để sự thật tự nói.

---

## 4. SỐ THẬT ĐƯỢC PHÉP DÙNG (đã xác nhận — dùng nguyên văn, không chế thêm)

- Hơn **4 năm** hoạt động
- **50+ lô** đang quản lý
- Cảnh báo bất thường trong **24 giờ**
- **0 trường hợp mất ranh giới** (trong suốt thời gian quản lý)
- Giá gói tham khảo: **1,5 – 2,5 triệu/tháng**; gói nhiều lô (≥3 lô) **2 triệu/lô/tháng**
- SĐT / Zalo: **0978 758 788** → link Zalo: `https://zalo.me/0978758788`
- Không hợp đồng dài hạn, không phí ẩn, dừng bất kỳ lúc nào.
- 3 lời chứng (chỉ dùng nếu cần, đúng tên): Anh Tuấn, Chị Hương, Anh Minh.

**Tuyệt đối không thêm số nào ngoài danh sách này.**

---

## 5. THẨM MỸ (bắt buộc khớp site)

**Màu (CSS variables):**
```
--green:#3d4a3a;   /* olive đậm, màu chủ */
--green-dark:#2d3a2d;
--gold:#c9a961;    /* vàng nhấn — HIẾM, chỉ dùng cho điểm nhấn nhỏ / trên nền tối */
--bg:#f9f8f6;      /* nền kem */
--dark:#1a1a1a;    /* chữ */
--border:rgba(61,74,58,.1);
```
**Quy tắc màu:** gold là tài nguyên hiếm — chỉ dùng cho dấu tick, gạch chân nhỏ, nút trên nền tối. **Số/giá trên nền sáng phải là màu xanh olive đậm (`--green`)**, không dùng gold trên nền sáng (không đạt tương phản). Mọi chữ đạt WCAG contrast ≥ 4.5.

**Font (Google Fonts):**
- Tiêu đề: **Cormorant Garamond** (serif, thanh)
- Body: **Be Vietnam Pro** (sans, dễ đọc tiếng Việt)
```html
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=Be+Vietnam+Pro:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

**Nhịp thiết kế:** khoảng trắng rộng, tiết chế, mỗi section một tính cách riêng (đừng lặp y hệt khuôn header cho mọi section). **Mobile ưu tiên số 1** — chủ dự án duyệt trên điện thoại. Body `font-size:18px`, container bài viết `max-width:720px`, padding thoáng.

---

## 6. CẤU TRÚC TRANG (thứ tự khối)

1. `<header>` sticky: logo chữ "GREENSPACE" (Cormorant, letter-spacing rộng) bên trái + link "← Trang chủ" bên phải.
2. Breadcrumb: Trang chủ › Hiểu đất › [tên bài]
3. `<main class="wrap">` (max-width 720px):
   - **H1** (xem mục 7)
   - **Đoạn answer-first** (khối nền nhạt, viền trái xanh) — 40–60 từ trả lời thẳng, xem mục 7. Đây là khối AI/Google trích, phải nằm ngay dưới H1.
   - Thân bài: các H2 (mục 7) + đoạn văn, xen 1 bảng và 1 checklist.
   - 1 khối "highlight" (câu chốt, in nghiêng, nền nhạt viền trái).
   - Dòng xref sang nambanvillas.vn (nếu hợp).
   - **CTA box** (nền olive đậm, chữ trắng, nút gold): 1 tiêu đề + 1 dòng + nút "Nhắn Zalo: 0978 758 788".
   - **Khối FAQ** (accordion, bấm mở): 4 câu (mục 7).
4. `<div class="related">`: 3 link bài liên quan (dùng link mục 9).
5. `<footer>`: © 2026 GreenSpace · Nam Ban, Lâm Hà, Lâm Đồng.
6. Thanh progress đọc mảnh trên cùng (gold, chạy theo scroll) — chi tiết mục 8.

---

## 7. NỘI DUNG BÀI (viết sẵn — dựng đúng, có thể tinh chỉnh câu chữ cho mượt, KHÔNG đổi ý/số)

**Chủ đề & góc riêng:** nhắm người **đã mua đất xong** nhưng ở xa, giờ lo "lô mình để đó không ai ngó thì ra sao". Đây là khoảnh khắc *hậu-mua* — khác với "cách tự giữ đất" và khác "bảng giá dịch vụ" (2 bài đã có trên site). Trọng tâm: **mua xong không phải hết việc, mà là lúc dễ bỏ bê nhất.**

**Slug/tên file:** `dat-mua-roi-de-do-tu-xa.html`
**URL:** `https://greenspacers.vn/dat-mua-roi-de-do-tu-xa`

**Title (thẻ `<title>`):**
`Mua đất xong để đó — lô của bạn ở xa giờ ra sao? | GreenSpace`

**Meta description:**
`Mua đất Nam Ban xong, ở xa, để đó không ai trông — lô của bạn có bị lấn ranh, mọc cỏ, sai mốc không? Vì sao hậu-mua là lúc đất dễ bị bỏ bê nhất, và cách theo dõi từ xa.`

**Keywords (đặt trong meta + rải tự nhiên trong FAQ/heading):**
`đất mua rồi để không có sao không`, `đất ở xa không ai trông coi`, `mua đất xong cần làm gì`, `đất bỏ hoang bị lấn chiếm`, `kiểm tra đất mình mua còn nguyên không`

**H1:**
`Mua đất xong rồi — đó mới là lúc lô đất của bạn dễ bị bỏ quên nhất`

**Answer-first (40–60 từ, khối nền nhạt ngay dưới H1):**
> Mua đất xong không phải là hết việc. Với người ở xa, đây thường là lúc lô đất bắt đầu bị bỏ quên: môi giới đã xong phần của họ, còn bạn thì không ở gần để ngó. Cỏ mọc, rào có thể xê dịch, mốc ranh mờ dần — mà bạn không hay. Việc cần làm là lập hồ sơ hiện trạng ngay và theo dõi định kỳ.

**Các H2 (heading = câu người thật nghĩ/gõ):**

**H2: "Mua xong là xong?" — không, là mới bắt đầu**
Nội dung: giao dịch khép lại thì ai cũng thở phào, cất sổ, rồi thôi. Nhưng miếng đất thật vẫn nằm ngoài trời. Sổ trong két thì mười năm vẫn nguyên; đất ngoài kia thì tháng nào cũng đổi. Người ở gần còn tạt qua; người ở xa thì tin đồ đang "yên" — trong khi chẳng ai kiểm.

**H2: Lô đất để không, mấy tháng đầu thường gặp gì**
Đưa 1 **checklist** (mỗi dòng 1 nỗi lo cụ thể, giọng mộc):
- Cỏ và cây bụi phủ nhanh, mốc ranh khuất dần.
- Hàng rào hoặc cọc ranh bị xê dịch mà không ai để ý.
- Người quanh đó canh tác lấn qua vài mét — lâu thành quen.
- Đường vào bị lấn, bị rào, tự nhiên đất "kẹt" trong.
- Có biến động quy hoạch, đường mới — người ở xa biết trễ vài tháng.

**H2: Vì sao "để vài tháng cho ổn định rồi tính" là cái bẫy**
Nội dung: đất càng để lâu không mốc, không hồ sơ, thì khi có chuyện càng khó cãi — vì không có gì làm bằng chứng "lúc mua nó thế này". Cái nên làm ngay sau mua là **lập hồ sơ hiện trạng gốc** (ảnh có tọa độ, ngày giờ, mốc ranh) để về sau còn cái mà so.

**H2: Ở xa thì theo dõi lô mới mua bằng cách nào**
Đưa 1 **bảng** so sánh 2 cột: *"Để mặc, thỉnh thoảng nhờ người quen ngó"* vs *"Có người theo dõi định kỳ"* — trên các dòng: tần suất ra đất / có hồ sơ gốc không / phát hiện lấn sớm hay muộn / bằng chứng khi tranh chấp / chi phí. Cột phải nghiêng về "có hệ thống" nhưng không nói quá.
Sau bảng, giới thiệu nhẹ: đây là việc GreenSpace làm — ra đất định kỳ, chụp ảnh GPS, cảnh báo trong 24h, giữ hồ sơ từng lô. Dẫn số thật: hơn 4 năm, 50+ lô, 0 trường hợp mất ranh.

**Khối highlight (in nghiêng, câu chốt):**
> Đất không mất trong một ngày. Nó mất dần — từng centimet ranh, từng tháng không ai ngó — cho tới lúc bạn về thì đã khác.

**Dòng xref (nếu hợp):**
> → Đang tính mua thêm lô nữa ở Nam Ban? Xem đất đang bán bên [nambanvillas.vn](https://nambanvillas.vn).

**CTA box (nền olive đậm):**
- Tiêu đề: `Mới mua đất, muốn có người ở Nam Ban theo dõi giúp?`
- Dòng nhỏ: `Nhắn cho tôi, kể lô của bạn ở đâu — tôi phản hồi trong 24 giờ.`
- Nút (gold): `Nhắn Zalo: 0978 758 788` → `https://zalo.me/0978758788`

**FAQ (4 câu — câu trả lời phải THẲNG ngay câu đầu, khớp 100% với schema mục 8):**

1. **Đất mua rồi để không có sao không?**
   Để không thì đất không tự mất, nhưng ở xa mà không ai theo dõi thì rủi ro âm thầm: cỏ phủ mốc ranh, hàng xóm canh tác lấn, cọc ranh xê dịch, đường vào bị lấn. Cái nguy không phải mất ngay, mà là mất dần đến lúc khó cãi vì không có hồ sơ gốc. Nên lập hồ sơ hiện trạng ngay sau mua và kiểm tra định kỳ.

2. **Mới mua đất xong nên làm gì đầu tiên?**
   Việc đầu tiên nên làm là lập hồ sơ hiện trạng: ra tận lô, chụp ảnh có tọa độ và ngày giờ, ghi lại mốc ranh, hàng rào, đường vào, cây cối. Đây là bản gốc để sau này so sánh khi có bất thường. Người ở xa không tự ra được thì nhờ dịch vụ khảo sát hiện trạng làm hộ.

3. **Ở xa, làm sao biết lô đất mình vẫn còn nguyên?**
   Cách chắc nhất là có người ra đất định kỳ chụp ảnh gắn tọa độ gửi về, so với hồ sơ gốc để phát hiện thay đổi. GreenSpace kiểm tra hàng tháng, cảnh báo bất thường trong 24 giờ, giữ hồ sơ riêng từng lô — hơn 4 năm quản lý 50+ lô, chưa để xảy ra trường hợp nào mất ranh giới.

4. **Chi phí theo dõi một lô đất là bao nhiêu?**
   Gói tham khảo từ 1,5 đến 2,5 triệu đồng một tháng cho một lô, gồm kiểm tra định kỳ, báo cáo ảnh GPS và cảnh báo bất thường. Từ 3 lô trở lên tính 2 triệu mỗi lô mỗi tháng. Không hợp đồng dài hạn, không phí ẩn, dừng bất kỳ lúc nào.

---

## 8. SCHEMA & AEO (bắt buộc)

Chèn **3 khối JSON-LD** trong `<head>`, mỗi khối một thẻ `<script type="application/ld+json">`:

**a) BlogPosting** — có: `headline`, `description`, `inLanguage:"vi"`, `datePublished:"2026-07-07"`, `dateModified:"2026-07-07"`, `author` là `Person` tên **"Đoàn Quốc Duyệt"**, jobTitle "Người sáng lập GreenSpace", `worksFor` Organization "GreenSpace", `knowsAbout` gồm các chủ đề trông coi/kiểm tra đất; `publisher` Organization "GreenSpace"; `mainEntityOfPage` là URL bài; `spatialCoverage` Place "Nam Ban, Lâm Hà, Lâm Đồng".

**b) FAQPage** — `mainEntity` là 4 câu hỏi ở mục 7, **text câu trả lời trong schema phải khớp 100% text hiển thị trên trang** (nếu lệch, Google phạt rich result). Thêm `speakable` (SpeakableSpecification, cssSelector trỏ `.faq-q`, `.faq-a`).

**c) BreadcrumbList** — 3 cấp: Trang chủ (`https://greenspacers.vn/`) › Hiểu đất › [bài này].

**Quy tắc AEO khác:**
- Answer-first 40–60 từ ngay dưới H1 (đã cho ở mục 7).
- Heading là câu hỏi thật, không văn vẻ.
- Số luôn kèm đơn vị + mốc ("24 giờ", "50+ lô", "1,5–2,5 triệu/tháng").
- 1 trang = 1 ý định (hậu-mua/trông coi). Không lan sang chủ đề mua bán hay pháp lý giao dịch.

---

## 9. KỸ THUẬT & KIỂM TRA

**Kiến trúc:** 1 file HTML tĩnh, CSS trong `<style>`, JS thuần trong `<script>`. Không framework, không thư viện ngoài (trừ Google Fonts). **Không dùng localStorage/sessionStorage.**

**Link bài liên quan (khối `.related`) — dùng đúng đường dẫn nội bộ:**
- `/quan-ly-dat-nam-ban` — Dịch vụ quản lý đất Nam Ban
- `/cach-giu-dat-an-toan-tu-xa` — Cách giữ đất an toàn từ xa
- `/quan-ly-tai-san-dat-tu-xa` — Quản lý tài sản đất từ xa (nhiều lô)

**JS cần có:**
- Progress bar theo scroll (thanh mảnh gold trên cùng).
- FAQ accordion: bấm câu hỏi thì mở/đóng câu trả lời (toggle class `open`; CSS ẩn `.faq-a` mặc định, hiện khi có `.open`).

**FAVICON:** dùng 1 favicon PNG base64 nhỏ hoặc bỏ trống — không bắt buộc.

**Mobile-first:** kiểm ở bề rộng ~380px: chữ không tràn, bảng cuộn ngang được (`overflow-x:auto`), nút CTA cao ≥44px, không vỡ layout. Kiểm cả desktop.

**Checklist tự QA trước khi coi là xong:**
- [ ] CSS: số dấu `{` = số dấu `}` (cân).
- [ ] Tag `<div>`, `<script>`, `<section>`… mở/đóng cân.
- [ ] 3 khối JSON-LD parse hợp lệ (không lỗi cú pháp), `@type` đúng.
- [ ] Text 4 câu trả lời FAQ trong schema **khớp y hệt** text hiển thị.
- [ ] Answer-first 40–60 từ, nằm ngay dưới H1.
- [ ] Không có số nào ngoài danh sách mục 4.
- [ ] Chữ đạt tương phản WCAG ≥ 4.5; gold không dùng làm chữ trên nền sáng.
- [ ] Test mobile 380px + desktop, không tràn/vỡ.

**Sau khi tạo xong file:** đây là 1 trang mới của site, cần thêm URL `https://greenspacers.vn/dat-mua-roi-de-do-tu-xa` vào `sitemap.xml` (priority 0.8) và vào `llms.txt` (mục danh sách bài viết) nếu 2 file đó có trong repo.

---

*Hết brief. Nếu có chỗ nào brief chưa nói rõ, cứ theo tinh thần: tĩnh, sạch, tiết chế, mobile-first, số thật, không marketing lộ liễu.*
