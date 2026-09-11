# Hàng đợi & auto đăng Facebook

Pipeline tự đăng bài Facebook cho Nam Ban. Cùng kiểu với news/IndexNow: web tĩnh + GitHub Actions, **git làm database**.

## Cách chạy
1. **`fb-queue/posts.json`** — hàng đợi (DB). Mỗi bài có: `id`, `scheduled` (ngày đăng, YYYY-MM-DD), `status` (`queued` → `posted`), `text`, `link` (tuỳ chọn), `pillar`, `audience`.
2. **`scripts/fb-post.py`** — mỗi lần chạy tìm bài `queued` đã tới ngày (giờ VN), đăng **1 bài sớm nhất** lên Page qua Graph API, đổi `status` thành `posted`.
3. **`.github/workflows/fb-autopost.yml`** — chạy **08:00 giờ VN mỗi ngày**. Cuối tuần không có bài lịch thì tự bỏ qua. Có nút **Run workflow** để chạy tay / xem thử.

## Chưa có token = DRY RUN (an toàn)
Khi **chưa** đặt token, script chỉ **in ra** bài sẽ đăng rồi thoát — **không đăng gì cả**. Chạy thử tại máy:
```
python scripts/fb-post.py
```

## Bật đăng thật — cần 2 secret
Vào **GitHub repo → Settings → Secrets and variables → Actions → New repository secret**, thêm:

| Secret | Là gì |
|---|---|
| `FB_PAGE_ID` | ID của Facebook Page (Trang → About/Giới thiệu → Page ID) |
| `FB_PAGE_TOKEN` | Page Access Token, quyền `pages_manage_posts` |

### Lấy Page Access Token (một lần)
1. Vào **developers.facebook.com** → tạo App (loại *Business*).
2. Thêm sản phẩm **Facebook Login** hoặc dùng **Graph API Explorer**.
3. Trong **Graph API Explorer**: chọn App → chọn Page của mình → cấp quyền `pages_manage_posts`, `pages_read_engagement` → **Generate Access Token**.
4. Token đó là token ngắn hạn. Đổi sang **token dài hạn (60 ngày)** hoặc token vĩnh viễn qua System User (Business Settings) để khỏi hết hạn.
5. Dán token vào secret `FB_PAGE_TOKEN`, Page ID vào `FB_PAGE_ID`.

> Sau khi có token, bài trong hàng đợi tới ngày là tự đăng. Muốn thử ngay: đổi `scheduled` một bài về hôm nay rồi bấm **Run workflow**.

## Thêm bài mới
Chèn thêm object vào mảng `posts` trong `posts.json` (giữ `status: "queued"`, đặt `scheduled` ngày muốn đăng). Commit là xong — pipeline lo phần còn lại.

## Giới hạn hiện tại
- Chỉ đăng **chữ + link** (chưa đăng ảnh). Ảnh sẽ bổ sung sau (Graph API `/photos`).
- Mỗi lần chạy đăng tối đa 1 bài.
