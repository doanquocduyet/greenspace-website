#!/usr/bin/env python3
"""
Tự động ping IndexNow khi có trang HTML mới/đổi lên main.
Báo Bing, Yandex, Cốc Cốc "có trang mới, vào crawl đi" (Google không dùng IndexNow).

Chạy trong GitHub Actions (on push to main). Biến môi trường:
  BEFORE, AFTER — 2 commit SHA để so ra file đổi (Actions tự đưa vào).
Nếu không có (chạy tay), sẽ ping toàn bộ trang index được.
"""
import json
import os
import subprocess
import sys
import urllib.request

HOST = "greenspacers.vn"
KEY = "6adadccf3476291837bf11da2472ee5b"
ENDPOINT = "https://api.indexnow.org/indexnow"
# Trang noindex — không ping
SKIP = {"cam-on.html", "anh-da-dung.html"}


def changed_html():
    before = os.environ.get("BEFORE", "").strip()
    after = os.environ.get("AFTER", "HEAD").strip() or "HEAD"
    # before rỗng hoặc toàn số 0 (push đầu/force) -> ping tất cả
    if not before or set(before) <= {"0"}:
        return None
    try:
        out = subprocess.check_output(
            ["git", "diff", "--name-only", "--diff-filter=ACM", before, after, "--", "*.html"],
            text=True,
        )
        return [f for f in out.split() if f.endswith(".html")]
    except subprocess.CalledProcessError:
        return None


def all_html():
    out = subprocess.check_output(["git", "ls-files", "*.html"], text=True)
    return out.split()


def to_url(fname):
    name = os.path.basename(fname)
    if name == "index.html":
        return f"https://{HOST}/"
    return f"https://{HOST}/{name[:-5]}"  # bỏ .html (cleanUrls)


def main():
    files = changed_html()
    if files is None:
        files = all_html()
        print("Chế độ: ping toàn bộ trang.")
    else:
        print(f"Chế độ: ping trang thay đổi ({len(files)} file).")

    urls = sorted({to_url(f) for f in files if os.path.basename(f) not in SKIP})
    # luôn kèm trang chủ
    home = f"https://{HOST}/"
    if home not in urls:
        urls.insert(0, home)

    if not urls:
        print("Không có URL nào để ping.")
        return

    payload = {
        "host": HOST,
        "key": KEY,
        "keyLocation": f"https://{HOST}/{KEY}.txt",
        "urlList": urls,
    }
    print("Ping", len(urls), "URL:")
    for u in urls:
        print("  -", u)

    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(f"IndexNow trả về HTTP {r.status} — OK (200/202 là thành công).")
    except urllib.error.HTTPError as e:
        print(f"IndexNow HTTP {e.code}: {e.read().decode(errors='ignore')}")
        # 200/202 mới là OK; mã khác coi như lỗi mềm, không làm hỏng cả build
        if e.code not in (200, 202):
            sys.exit(0)  # không fail workflow chỉ vì IndexNow từ chối tạm


if __name__ == "__main__":
    main()
