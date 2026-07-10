# BRIEF THIẾT KẾ — NÂNG CẤP THẨM MỸ WEBSITE GREENSPACE
## Biến trang "sạch và đúng" thành trang "sang, tinh tế, lướt đã" như web nước ngoài đẳng cấp

> Đây là brief tự chứa. Bạn (Claude Code) chưa biết gì về dự án này. Mọi thứ cần thiết nằm trong tài liệu này, gồm cả design tokens và code mẫu thật. Đọc hết trước khi làm. Mục tiêu: **giữ nguyên toàn bộ nội dung, SEO, schema, link hiện có của website — chỉ thay lớp thẩm mỹ và chuyển động lên đẳng cấp cao.** Không xoá nội dung, không đổi text SEO, không phá schema.

---

## 0. BỐI CẢNH (để hiểu tinh thần, không in ra web)

**GreenSpace** (greenspacers.vn) là landing dịch vụ cho người sở hữu đất ở **Nam Ban, Lâm Hà, Lâm Đồng** nhưng sống xa (Sài Gòn, Hà Nội). Dịch vụ: trông coi / kiểm tra / giữ đất hộ người ở xa — kiểm tra định kỳ hàng tháng, ảnh GPS, cảnh báo lấn chiếm, xác minh ranh mốc.

Website là **HTML tĩnh thuần** (không framework, không React, không build step). Mỗi trang là 1 file .html tự chứa CSS trong `<style>` và JS thuần trong `<script>`. Deploy qua Vercel từ GitHub. **Giữ nguyên kiến trúc tĩnh này** — không thêm framework, không dùng localStorage/sessionStorage.

**Triết lý thẩm mỹ:** "im lặng mà sang" — khoảng trắng, tiết chế, không màu mè. Khách hàng nhạy cảm (người lo cho tài sản đất), nên **tuyệt đối không** popup, đếm ngược, "còn X suất", marketing lộ liễu.

---

## 1. VẤN ĐỀ CẦN GIẢI (chẩn đoán hiện trạng)

Trang hiện tại đã "sạch và đúng" nhưng chưa "sang". Sáu thiếu sót khiến nó chưa bằng web nước ngoài đẳng cấp (kiểu Aesop, Kinfolk, các studio design):

1. **Nhịp cuộn phẳng** — mọi section hiện ra cùng một kiểu, không có scroll-reveal → trang không "thở".
2. **Khoảng trắng chưa đủ dám** — padding còn khiêm tốn.
3. **Typography thiếu tương phản** — cỡ chữ hơi đều nhau → phẳng, không kịch tính.
4. **Chuyển động cơ học** — dùng `ease` mặc định, không "đắt".
5. **Thiếu micro-details** — không có underline chạy khi hover, số đếm, đường kẻ vẽ dần, ảnh zoom chậm.
6. **Thiếu "signature moment"** — không có khoảnh khắc chữ ký khiến người ta nhớ.

**Nhiệm vụ:** vá cả 6, theo đúng design system mục 3–4, áp lên trang chủ (index.html) trước.

---

## 2. NGUYÊN TẮC BẤT DI BẤT DỊCH (không được vi phạm)

- **GIỮ NGUYÊN nội dung chữ, số, SEO meta, JSON-LD schema, internal links.** Chỉ đổi lớp trình bày (CSS) + thêm chuyển động (JS nhẹ). Nếu phải đổi cấu trúc HTML, giữ nguyên text bên trong.
- **KHÔNG bịa số.** Số thật được phép: hơn **4 năm** hoạt động · **50+ lô** đang quản lý · cảnh báo **24 giờ** · **0 trường hợp mất ranh giới**. Không thêm số nào khác.
- **Màu, font: theo đúng tokens mục 3.** Không đổi bảng màu, không đổi font.
- **Mobile-first** (chủ dự án duyệt trên điện thoại). Kiểm cả điện thoại (~380px) và desktop.
- **Quality floor:** responsive tới mobile, focus bàn phím nhìn thấy được, `prefers-reduced-motion` được tôn trọng (tắt hết animation khi user bật giảm chuyển động).
- Giữ CTA chính: **Zalo 0978 758 788** → `https://zalo.me/0978758788`.

---

## 3. DESIGN TOKENS (dùng chính xác)

```css
:root{
  --ink:#1a1f1a;          /* chữ chính — gần đen ngả olive */
  --olive:#3d4a3a;        /* xanh olive đậm — màu thương hiệu */
  --olive-deep:#252e24;   /* olive tối — nền signature/hero */
  --gold:#c9a961;         /* vàng nhấn — HIẾM: chỉ dùng điểm nhấn nhỏ, vạch, chữ nhấn trên nền tối */
  --paper:#f9f8f6;        /* nền kem sáng */
  --paper-warm:#f1eee7;   /* kem ấm hơn — nền section xen kẽ */
  --mute:#8b9086;         /* chữ phụ, caption */
  --line:rgba(26,31,26,.12); /* đường kẻ mảnh */
  --ease:cubic-bezier(.22,1,.36,1); /* đường cong chuyển động "đắt" — dùng cho MỌI transition */
}
```

**Luật màu vàng (gold):** là tài nguyên hiếm. Chỉ dùng cho: vạch kẻ nhỏ, chữ nhấn *trên nền tối*, mũi tên, dấu tick, eyebrow. **Số/giá trên nền sáng phải là `--olive`** (không dùng gold trên nền sáng — không đạt tương phản). Mọi chữ đạt **WCAG contrast ≥ 4.5**.

**Fonts (Google Fonts) — nạp có preconnect để nhanh:**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Be+Vietnam+Pro:wght@300;400;500;600&display=swap" rel="stylesheet">
```
- **Display / tiêu đề:** Cormorant Garamond (serif thanh) — dùng khổ LỚN, weight 500, có thể italic cho chữ nhấn.
- **Body / UI:** Be Vietnam Pro (sans, đọc tốt tiếng Việt), weight 300–500.

---

## 4. SÁU KỸ THUẬT THẨM MỸ + CODE MẪU (làm đúng cái này)

### 4.1 — Typography tương phản mạnh
Tiêu đề rất lớn cạnh body nhỏ tinh. Type scale:
```css
.display{font-family:'Cormorant Garamond',serif;font-weight:500;line-height:.98;letter-spacing:-.01em;}
/* Hero H1 */      font-size:clamp(52px,10vw,132px);
/* Tiêu đề section */ font-size:clamp(30px,5vw,60px);
/* Signature */    font-size:clamp(38px,7.5vw,104px);
.eyebrow{font-size:12px;text-transform:uppercase;letter-spacing:.32em;color:var(--gold);font-weight:500;}
body{font-size:17px;line-height:1.75;font-weight:400;}
```
Nguyên tắc: **để chênh lệch cỡ chữ thật lớn** giữa tiêu đề và thân. Đừng để mọi thứ cùng cỡ.

### 4.2 — Khoảng trắng dám hơn
```css
section{padding:min(18vh,160px) 0;}   /* dọc rộng rãi */
.wrap{max-width:1180px;margin:0 auto;padding:0 32px;}
.wrap-narrow{max-width:720px;margin:0 auto;padding:0 32px;} /* cho khối chữ trọng tâm */
```
Cho khối chữ quan trọng đứng một mình giữa nhiều khoảng trắng.

### 4.3 — Scroll-reveal (chữ/ảnh trồi lên nhẹ khi vào khung nhìn)
```css
.reveal{opacity:0;transform:translateY(30px);transition:opacity 1s var(--ease),transform 1s var(--ease);}
.reveal.in{opacity:1;transform:none;}
.reveal.d1{transition-delay:.08s;} .reveal.d2{transition-delay:.16s;} .reveal.d3{transition-delay:.24s;}
/* đường kẻ vẽ dần */
.rule{height:1px;background:var(--line);transform:scaleX(0);transform-origin:left;transition:transform 1.2s var(--ease);}
.rule.in{transform:scaleX(1);}
```
```javascript
const io=new IntersectionObserver((es)=>{
  es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}});
},{threshold:.18});
document.querySelectorAll('.reveal,.rule,.sig-line').forEach(el=>io.observe(el));
```
Gắn class `.reveal` (kèm `.d1/.d2/.d3` để so le) cho eyebrow, tiêu đề, đoạn văn, card, số. **Không lạm dụng** — chỉ khối chính, đừng cho mọi dòng nhỏ đều bay.

### 4.4 — Chuyển động "đắt" (cubic-bezier)
Dùng `var(--ease)` cho **mọi** transition (đã định nghĩa ở tokens). Không để `ease`/`linear` mặc định.

### 4.5 — Micro-details
**a) Số đếm nhảy lên khi cuộn tới** (cho khối số 4 / 50+ / 0):
```html
<div class="num" data-count="50" data-suffix="+">0</div>
```
```javascript
const co=new IntersectionObserver((es)=>{
  es.forEach(e=>{
    if(!e.isIntersecting)return;
    const el=e.target,end=+el.dataset.count,suf=el.dataset.suffix||'';
    if(matchMedia('(prefers-reduced-motion:reduce)').matches){el.textContent=end+suf;co.unobserve(el);return;}
    let cur=0,step=Math.max(1,Math.round(end/40));
    const t=setInterval(()=>{cur+=step;if(cur>=end){cur=end;clearInterval(t);}el.textContent=cur+suf;},28);
    co.unobserve(el);
  });
},{threshold:.6});
document.querySelectorAll('[data-count]').forEach(el=>co.observe(el));
```
**b) Gạch chân link chạy khi hover:**
```css
.nav-cta{position:relative;padding-bottom:3px;text-decoration:none;}
.nav-cta::after{content:"";position:absolute;left:0;bottom:0;width:100%;height:1px;background:currentColor;transform:scaleX(0);transform-origin:right;transition:transform .5s var(--ease);}
.nav-cta:hover::after{transform:scaleX(1);transform-origin:left;}
```
**c) Ảnh zoom rất chậm khi hover** (cho card ảnh):
```css
.svc-img{transform:scale(1);transition:transform 1.4s var(--ease);}
.svc:hover .svc-img{transform:scale(1.06);}
```
**d) Nút có mũi tên nhích:**
```css
.btn{display:inline-flex;align-items:center;gap:14px;transition:background .5s var(--ease),transform .5s var(--ease),gap .4s var(--ease);}
.btn:hover{transform:translateY(-2px);gap:20px;}
.btn .arrow{color:var(--gold);transition:transform .4s var(--ease);}
.btn:hover .arrow{transform:translateX(4px);}
```

### 4.6 — Signature moment (cú "nín thở")
Một section riêng, nền olive tối, một câu chữ ký khổng lồ giữa khoảng trắng, có vạch gold rơi xuống:
```css
.signature{background:var(--olive-deep);color:var(--paper);min-height:88vh;display:flex;align-items:center;justify-content:center;text-align:center;}
.signature .big{font-family:'Cormorant Garamond',serif;font-weight:500;font-size:clamp(38px,7.5vw,104px);line-height:1.05;max-width:16ch;}
.signature .big em{font-style:italic;color:var(--gold);}
.signature .sig-line{width:1px;height:64px;background:var(--gold);margin:0 auto 44px;transform:scaleY(0);transform-origin:top;transition:transform 1.1s var(--ease);}
.signature .sig-line.in{transform:scaleY(1);}
```
```html
<section class="signature">
  <div class="wrap-narrow">
    <div class="sig-line"></div>
    <p class="big">Đất không mất trong một ngày. Nó mất <em>dần</em> — cho tới lúc bạn về thì đã khác.</p>
  </div>
</section>
```
Đây là câu thật của thương hiệu — giữ nguyên chữ này.

---

## 5. HEADER & HERO (nâng cấp)

**Header** cố định, tối giản, dùng `mix-blend-mode:difference` để chữ tự đổi màu theo nền phía sau (trắng trên nền tối, tối trên nền sáng):
```css
header{position:fixed;top:0;left:0;right:0;z-index:50;display:flex;align-items:center;justify-content:space-between;padding:22px 40px;mix-blend-mode:difference;}
.logo{font-family:'Cormorant Garamond',serif;font-weight:600;font-size:19px;letter-spacing:.36em;color:#fff;}
```
Logo chữ "GREENSPACE" (letter-spacing rộng). Bên phải: link "Kiểm tra đất của tôi" với gạch chân chạy (4.5b).

**Hero** full màn hình, nền gradient olive, tiêu đề Cormorant khổng lồ, chữ nhấn italic màu gold, phụ đề nhỏ mờ, và một chỉ báo "cuộn xuống" với vạch gold co giãn:
```css
.hero{min-height:100vh;display:flex;flex-direction:column;justify-content:center;background:linear-gradient(160deg,var(--olive-deep),var(--olive));color:var(--paper);padding:0 40px;position:relative;}
.hero h1{font-size:clamp(52px,10vw,132px);max-width:15ch;}
.hero h1 em{font-style:italic;color:var(--gold);font-weight:400;}
```
Giữ đúng câu hero hiện có của trang: **"Đất của bạn đang ra sao?"** (có thể mở rộng thành *"Đất của bạn đang ra sao khi bạn không ở đây?"* với vế sau italic gold, nếu hợp — nhưng đừng đổi ý câu).

---

## 6. BỐ CỤC TỔNG TRANG CHỦ (thứ tự khối — giữ nội dung cũ, sắp lại theo nhịp này)

1. Header cố định (mix-blend).
2. **Hero** full màn — eyebrow "Nam Ban · Lâm Hà · Lâm Đồng" + H1 lớn + phụ đề + chỉ báo cuộn.
3. **Intro + Stats** — 1 câu triết lý lớn ("Đất là tài sản duy nhất người ta mua rồi để mặc ngoài trời…") + hàng 3 số đếm (4 năm / 50+ lô / 0 mất ranh).
4. **Dịch vụ** — lưới card ảnh (mỗi card có số thứ tự 01–04, tiêu đề Cormorant, ảnh zoom chậm khi hover). Nội dung 4 việc: ra tận đất / canh ranh mốc / cảnh báo 24h / báo cáo hàng tháng.
5. **Signature moment** (mục 4.6).
6. **Bảng giá / gói** (giữ nội dung giá hiện có: 1,5–2,5 triệu/tháng; ≥3 lô: 2 triệu/lô) — trình bày tiết chế, số bằng `--olive`.
7. **Lời chứng** (3 lời chứng thật: Anh Tuấn TP.HCM, Chị Hương Hà Nội, Anh Minh Hải Phòng — giữ nguyên nội dung + giữ Review schema).
8. **Bài viết** (khối "Hiểu đất, giữ đất" — các card link tới bài, grid tự co giãn `repeat(auto-fit,minmax(240px,1fr))`).
9. **Form liên hệ / CTA** — giữ form hiện có (gửi email qua FormSubmit + mở Zalo). Nút CTA theo mục 4.5d.
10. **Footer** tối giản.

**Xen kẽ nền:** section sáng (`--paper`) và section tối (`--olive-deep`, cho hero + signature) luân phiên để tạo nhịp. Đừng để toàn bộ cùng một nền.

---

## 7. GIỮ NGUYÊN (không đụng)

- Toàn bộ thẻ `<meta>` SEO, `<title>`, canonical, og tags.
- Toàn bộ khối `<script type="application/ld+json">` (LocalBusiness + Review + AggregateRating + FAQPage schema). Nếu di chuyển vị trí HTML của phần lời chứng, **giữ text khớp 100% với reviewBody trong schema**.
- Form liên hệ và JS gửi email/Zalo hiện có.
- Sitemap, robots, llms.txt.

---

## 8. CHECKLIST QA TRƯỚC KHI COI LÀ XONG

- [ ] Mở ở **380px (điện thoại)** và **desktop**: không tràn ngang, không vỡ, chữ không dính mép. Bảng cuộn ngang được.
- [ ] CSS: số `{` = số `}` (cân). Thẻ `<section>`, `<div>`, `<picture>`, `<script>` mở/đóng cân.
- [ ] Mọi JSON-LD parse hợp lệ; text lời chứng khớp schema.
- [ ] `prefers-reduced-motion`: bật lên thì mọi animation/số đếm/reveal tắt, nội dung vẫn hiện đầy đủ (không có khối nào kẹt ở `opacity:0`).
- [ ] Focus bàn phím (Tab) nhìn thấy được viền focus (`outline` gold).
- [ ] Không số nào ngoài: 4 năm, 50+, 24 giờ, 0 mất ranh, giá 1,5–2,5 triệu / 2 triệu.
- [ ] Gold không dùng làm chữ trên nền sáng. Tương phản ≥ 4.5.
- [ ] Ảnh dùng WebP có fallback (nếu đang có `<picture>` thì giữ).
- [ ] Reduced-motion khối `.reveal` phải có fallback `opacity:1` (nếu không, người tắt chuyển động sẽ thấy trang trắng).

```css
@media(prefers-reduced-motion:reduce){
  *,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important;}
  .reveal{opacity:1!important;transform:none!important;}
  .rule,.sig-line{transform:none!important;}
}
```

---

## 9. TINH THẦN CUỐI

Spend boldness in one place: **để signature moment là thứ duy nhất "to tiếng", mọi thứ quanh nó giữ im lặng và kỷ luật.** Bớt một chi tiết còn hơn thừa. Web này bán sự yên tâm cho người lo xa — nên nó phải *tĩnh, chắc, đáng tin*, và sang một cách kín đáo, không phô trương. "Im lặng mà sang."

*Hết brief. Nếu chỗ nào chưa rõ: chọn phương án tối giản hơn, tĩnh hơn, nhiều khoảng trắng hơn.*
