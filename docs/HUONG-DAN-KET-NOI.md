# Hướng dẫn kết nối — bấm theo thứ tự

Mỗi bước là 1 link. Bấm link → làm đúng dòng mô tả → sang bước kế.

---

## PHẦN A — Cho 2 lịch tự động quyền đăng bài lên web (~5 phút)

**A1.** Nối GitHub với Claude → https://claude.ai/connect-github
- Bấm **Connect / Kết nối** → đăng nhập GitHub `doanquocduyet` → **Authorize**.

**A2.** Cài Claude cho repo web → https://github.com/apps/claude/installations/new
- Chọn tài khoản **doanquocduyet** → chọn **Only select repositories** → tick **greenspace-website** → **Install** (hoặc **Save**).
- Nếu đã cài rồi, trang sẽ mở phần cấu hình: kiểm tra **greenspace-website** có trong danh sách → **Save**.

**A3.** Mở danh sách lịch → https://claude.ai/code/routines
- Bấm lịch **"GreenSpace — Tin cập nhật tự động (2 lần/tuần)"** → **Edit**.
- Phần **Repository** → chọn **doanquocduyet/greenspace-website** → **Save**.
- Quay lại danh sách → bấm lịch **"GreenSpace — Bài SEO tự động hàng tuần"** → **Edit** → chọn repo như trên → **Save**.
- (Link không mở được thì vào https://claude.ai/code → thanh bên trái → **Routines**.)

**A4.** Chạy thử → vẫn ở trang lịch, bấm lịch **Tin cập nhật** → **Run now**.

**A5.** Đợi ~5 phút → mở https://github.com/doanquocduyet/greenspace-website/branches
- Thấy nhánh mới tên `news/2026-…` → **xong**. Nhắn Claude "đã chạy lịch" để Claude kiểm và merge.
- Không thấy → mở lại trang lịch xem lần chạy báo gì (lịch giờ sẽ ghi rõ **THẤT BẠI** + lý do), gửi Claude ảnh chụp.

---

## PHẦN B — Kết nối Facebook để tự đăng (~10 phút)

Cần: tài khoản Facebook của anh là **quản trị Trang GreenSpace**.

**B1.** Tạo app → https://developers.facebook.com/apps/creation/
- Đăng nhập Facebook nếu được hỏi (lần đầu: bấm **Get Started** đăng ký tài khoản nhà phát triển, xác nhận số điện thoại).
- Tên app: `GreenSpace Auto Post` → **Next**.
- Use case: chọn **Other** → **Next** → loại app **Business** → **Next** → **Create app** (nhập lại mật khẩu nếu hỏi).
- Không cần làm gì thêm trong app. **Không bấm Publish** — để chế độ Development là đúng.

**B2.** Lấy mã người dùng → https://developers.facebook.com/tools/explorer/
- Cột phải, ô **Meta App**: chọn **GreenSpace Auto Post**.
- Ô **User or Page**: chọn **Get User Access Token**.
- Ô **Permissions** → **Add a Permission** → gõ và tick lần lượt: `pages_show_list`, `pages_read_engagement`, `pages_manage_posts`.
- Bấm **Generate Access Token** → cửa sổ Facebook hiện ra → **Tiếp tục** → **chọn Trang GreenSpace** (quan trọng) → **Tiếp tục** → **Lưu / Xong**.
- Bấm biểu tượng **copy** cạnh ô Access Token.

**B3.** Đổi sang mã dài hạn → https://developers.facebook.com/tools/debug/accesstoken/
- Dán mã vào ô → **Debug**.
- Kéo xuống cuối → bấm **Extend Access Token** → nhập mật khẩu nếu hỏi → bấm **Debug** cạnh mã mới hiện ra → copy mã mới đó.

**B4.** Lấy mã của Trang → https://developers.facebook.com/tools/explorer/?method=GET&path=me%2Faccounts%3Ffields%3Did%2Cname%2Caccess_token
- Dán mã dài hạn (bước B3) vào ô **Access Token** ở cột phải (xoá mã cũ trong ô trước).
- Bấm **Submit**.
- Kết quả hiện dòng có `"name": "GreenSpace…"`. Copy 2 thứ ra giấy nháp / Ghi chú điện thoại:
  - số sau `"id":` → **FB_PAGE_ID**
  - chuỗi dài sau `"access_token":` (bỏ dấu ngoặc kép) → **FB_PAGE_TOKEN**

**B5.** (Kiểm mã Trang) → https://developers.facebook.com/tools/debug/accesstoken/
- Dán **FB_PAGE_TOKEN** → **Debug** → dòng **Expires** ghi **Never** là đúng. Ghi ngày giờ khác → làm lại B3–B4.

**B6.** Cất Page ID vào GitHub → https://github.com/doanquocduyet/greenspace-website/settings/secrets/actions/new
- **Name**: `FB_PAGE_ID` · **Secret**: dán số id → **Add secret**.

**B7.** Cất mã Trang vào GitHub → https://github.com/doanquocduyet/greenspace-website/settings/secrets/actions/new
- **Name**: `FB_PAGE_TOKEN` · **Secret**: dán access_token → **Add secret**.
- Xoá mã khỏi giấy nháp / Ghi chú. **Không gửi mã vào chat.**

**B8.** Kiểm kết nối (không đăng bài) → https://github.com/doanquocduyet/greenspace-website/actions/workflows/fb-autopost.yml
- Bấm **Run workflow** (nút xám bên phải) → **Run workflow** (nút xanh).
- Đợi ~30 giây, bấm vào lần chạy mới nhất → bấm **fb-post** → mở dòng **Đăng bài tới hạn**:
  - `✅ Token OK — Trang: GreenSpace…` → **xong**. Từ **29/9, 8:00 sáng** mỗi ngày tự đăng 1 bài.
  - `❌ Token hoặc Page ID không dùng được` → làm lại từ B2 (lỗi hay gặp: quên chọn Trang ở B2, hoặc dán mã người dùng thay vì mã Trang ở B7). Sửa secret: https://github.com/doanquocduyet/greenspace-website/settings/secrets/actions

---

## Sau này
- Xem lịch sử đăng: https://github.com/doanquocduyet/greenspace-website/actions/workflows/fb-autopost.yml
- Dấu đỏ ở đó = mã Trang hết hiệu lực (đổi mật khẩu Facebook, gỡ app, mất quyền admin) → làm lại B2–B8.
- Hàng đợi: 5 bài, 29/9 → 3/10. Hết bài thì nhờ Claude viết thêm vào `fb-queue/posts.json`.
