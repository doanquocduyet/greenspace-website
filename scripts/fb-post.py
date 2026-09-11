#!/usr/bin/env python3
"""
Auto đăng Facebook cho GreenSpace / Nam Ban.

Đọc hàng đợi fb-queue/posts.json, tìm bài 'queued' đã tới ngày (theo giờ VN),
đăng bài SỚM NHẤT lên Facebook Page qua Graph API, rồi đánh dấu 'posted'.
Mỗi lần chạy chỉ đăng TỐI ĐA 1 bài (đăng đều, không spam).

Cần 2 biến môi trường (đặt trong GitHub secret) để đăng thật:
  FB_PAGE_ID     — ID của Facebook Page
  FB_PAGE_TOKEN  — Page Access Token (quyền pages_manage_posts)

CHƯA có token => chạy chế độ DRY RUN: chỉ in ra bài sẽ đăng, KHÔNG đăng,
thoát mã 0 (để workflow không báo đỏ). Xem fb-queue/README.md.

Chạy: python scripts/fb-post.py
"""
import json
import os
import sys
import datetime

try:
    from zoneinfo import ZoneInfo
except ImportError:
    ZoneInfo = None

try:
    import requests
except ImportError:
    sys.exit("Thiếu thư viện. Cài: pip install requests")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUEUE = os.path.join(ROOT, "fb-queue", "posts.json")
GRAPH = "https://graph.facebook.com/v21.0"


def today_vn(tz_name):
    if ZoneInfo:
        try:
            return datetime.datetime.now(ZoneInfo(tz_name)).date()
        except Exception:
            pass
    # fallback: UTC+7
    return (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).date()


def parse_date(s):
    return datetime.date.fromisoformat(s)


def build_message(post):
    msg = post.get("text", "").strip()
    link = post.get("link")
    if link:
        msg = msg + "\n\n👉 " + link
    return msg


def main():
    if not os.path.exists(QUEUE):
        print(f"Không thấy hàng đợi: {QUEUE}")
        return 0
    with open(QUEUE, encoding="utf-8") as f:
        data = json.load(f)

    cfg = data.get("config", {})
    tz = cfg.get("timezone", "Asia/Ho_Chi_Minh")
    today = today_vn(tz)
    posts = data.get("posts", [])

    queued = [p for p in posts if p.get("status") == "queued"]
    if not queued:
        print("Hàng đợi trống — không có bài 'queued'. Thêm bài vào fb-queue/posts.json.")
        return 0

    queued.sort(key=lambda p: p.get("scheduled", "9999-12-31"))
    due = [p for p in queued if parse_date(p["scheduled"]) <= today]

    token = os.environ.get("FB_PAGE_TOKEN")
    page = os.environ.get("FB_PAGE_ID")

    # Không có bài tới hạn -> xem trước bài kế
    if not due:
        nxt = queued[0]
        print(f"Hôm nay ({today}) chưa có bài tới hạn.")
        print(f"Bài kế: [{nxt['id']}] đăng ngày {nxt['scheduled']} (còn "
              f"{(parse_date(nxt['scheduled'])-today).days} ngày).")
        print("--- Xem trước nội dung ---")
        print(build_message(nxt))
        return 0

    post = due[0]
    message = build_message(post)

    print(f"Bài tới hạn: [{post['id']}] (lịch {post['scheduled']}, trụ {post.get('pillar','?')})")
    print("--- Nội dung ---")
    print(message)
    print("----------------")

    if not token or not page:
        print("\n⚠️  DRY RUN — chưa có FB_PAGE_TOKEN / FB_PAGE_ID nên KHÔNG đăng.")
        print("   Đặt 2 secret này trong GitHub để chuyển sang đăng thật.")
        return 0

    # Đăng thật
    resp = requests.post(
        f"{GRAPH}/{page}/feed",
        data={"message": message, "access_token": token},
        timeout=30,
    )
    if resp.status_code != 200:
        print(f"\n❌ Lỗi Facebook API ({resp.status_code}): {resp.text}")
        return 1

    fb_id = resp.json().get("id", "")
    print(f"\n✅ Đã đăng. FB post id: {fb_id}")

    # Đánh dấu posted, ghi lại DB
    for p in posts:
        if p["id"] == post["id"]:
            p["status"] = "posted"
            p["posted_at"] = datetime.datetime.now(
                ZoneInfo(tz) if ZoneInfo else None
            ).isoformat(timespec="seconds")
            p["fb_post_id"] = fb_id
            break
    with open(QUEUE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("Đã cập nhật hàng đợi.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
