# Hướng dẫn bật "cỗ máy tự động" cho GreenSpace

Cháu đã dựng xong toàn bộ phần tự động. File này hướng dẫn 3 việc **chỉ chú làm được** (cần đăng nhập tài khoản Google/Bing của chú), mỗi việc ~5-10 phút, làm 1 lần, chạy mãi.

---

## ✅ ĐÃ TỰ ĐỘNG (cháu dựng xong, không cần chú)

| Máy | Làm gì |
|-----|--------|
| **4 trang SEO** | quan-ly-dat-nam-ban, kiem-tra-dat-lam-ha, trong-coi-dat-o-xa, ve-greenspace |
| **IndexNow** | Mỗi lần web đổi → tự báo Bing, Yandex (→ ChatGPT Search, Copilot) trong vài phút |
| **llms.txt** | Bản đồ sạch cho ChatGPT/Claude/Perplexity/Gemini trích đúng |
| **robots mở cửa AI** | Cho phép GPTBot, ClaudeBot, PerplexityBot, Google-Extended dùng web làm câu trả lời |
| **LocalBusiness + FAQ schema** | Mọi trang đều có structured data để Google + AI đọc |
| **sitemap.xml** | Bản đồ đầy đủ 5 trang |

---

## ⚠️ 3 VIỆC CHỈ CHÚ LÀM ĐƯỢC (cần tài khoản của chú)

### 1. Google Search Console (QUAN TRỌNG NHẤT — 10 phút)

Đây là "bật công tắc điện" cho cả cỗ máy.

1. Vào **search.google.com/search-console**
2. Nhấn **Add property** → chọn **URL prefix** → nhập `https://greenspacers.vn`
3. Chọn cách xác minh **HTML tag** → copy đoạn mã (dạng `<meta name="google-site-verification" content="abc123..." />`)
4. **Gửi đoạn mã đó cho cháu** → cháu dán vào web (đã chừa sẵn chỗ trong index.html)
5. Sau khi cháu dán + chú nhấn Verify → vào **Sitemaps** → nhập `sitemap.xml` → Submit

→ Xong. Google bắt đầu index toàn bộ web trong vài ngày.

### 2. Bing Webmaster Tools (nuôi ChatGPT — 5 phút)

ChatGPT Search và Copilot lấy dữ liệu từ Bing, nên đây quan trọng bất ngờ.

1. Vào **bing.com/webmasters**
2. Đăng nhập → **Add a site** → nhập `https://greenspacers.vn`
3. Có thể **Import từ Google Search Console** (nhanh nhất) hoặc xác minh bằng meta tag
4. Nếu dùng meta tag → gửi mã cho cháu dán

### 3. Google Business Profile (lên Google Maps — 10 phút)

Để khi ai search "quản lý đất Nam Ban" trên Maps → thấy GreenSpace.

1. Vào **business.google.com**
2. **Manage now** → nhập tên "GreenSpace"
3. Danh mục: **Dịch vụ quản lý bất động sản** (Property management company)
4. Khu vực phục vụ: Nam Ban, Lâm Hà, Lâm Đồng
5. SĐT: 0978 758 788 · Website: greenspacers.vn
6. Xác minh (Google gửi mã qua bưu thiếp hoặc điện thoại)

---

## 📊 (Tùy chọn) Google Analytics — xem khách tới từ đâu

1. Vào **analytics.google.com** → tạo property cho greenspacers.vn
2. Lấy **Measurement ID** (dạng `G-XXXXXXXXXX`)
3. Gửi cho cháu → cháu gắn vào toàn site

---

## 🔁 (Tùy chọn) Nối web → tự đăng Facebook

Web đã có cấu trúc để nối tự động. Nếu muốn bài/cập nhật tự bắn sang Facebook:

1. Dùng **Make.com** (miễn phí) hoặc **Zapier**
2. Tạo scenario: theo dõi web → khi có thay đổi → tự đăng Facebook Page
3. Cháu hướng dẫn chi tiết khi chú cần

---

## Tóm lại

Cỗ máy đã "cắm điện" và chạy tự động. Nhưng nó âm thầm cho tới khi chú **bật công tắc Search Console**.

**Việc duy nhất cần làm ngay:** Gửi cháu mã xác minh Google → cháu ráp nốt → sau đó chú gần như không cần đụng tay.

---

## 🔔 IndexNow — báo Bing/Yandex thủ công (tùy chọn)

Vì GitHub Actions cần quyền đặc biệt, cháu chuẩn bị script ping thủ công.

**Khi nào dùng:** Mỗi khi chú thêm nội dung mới và muốn Bing/ChatGPT Search biết ngay (thay vì đợi vài ngày).

**Cách dùng:**
- File `docs/indexnow-ping.sh` — chạy `bash docs/indexnow-ping.sh` trên máy có internet
- Hoặc dán nội dung vào bất kỳ terminal nào

**Key IndexNow:** `6adadccf3476291837bf11da2472ee5b` (file `.txt` đã ở root web)

**Lưu ý:** Google KHÔNG dùng IndexNow — Google dựa vào Search Console (việc #1 ở trên). IndexNow chủ yếu cho Bing → nuôi ChatGPT Search & Copilot.
