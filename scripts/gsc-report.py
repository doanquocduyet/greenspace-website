#!/usr/bin/env python3
"""
Báo cáo trạng thái index Google Search Console cho greenspacers.vn.

Đọc danh sách URL từ sitemap.xml, hỏi Google (URL Inspection API) từng URL
đang ở trạng thái nào (đã index / đã phát hiện chưa index / redirect / chặn...),
rồi ghi báo cáo Markdown vào docs/gsc-status.md.

Cần 2 biến môi trường:
  GSC_SA_JSON  — toàn bộ nội dung file JSON của service account (dán vào GitHub secret)
  GSC_PROPERTY — property trong Search Console. Mặc định 'sc-domain:greenspacers.vn'.
                 Nếu property của chú là kiểu "tiền tố URL", đặt 'https://greenspacers.vn/'.

Chạy: python scripts/gsc-report.py
"""
import json
import os
import sys
import datetime
import xml.etree.ElementTree as ET

try:
    from google.oauth2 import service_account
    from google.auth.transport.requests import AuthorizedSession
except ImportError:
    sys.exit("Thiếu thư viện. Cài: pip install google-auth requests")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITEMAP = os.path.join(ROOT, "sitemap.xml")
OUT = os.path.join(ROOT, "docs", "gsc-status.md")

INSPECT_URL = "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect"
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]

# Ánh xạ trạng thái Google -> tiếng Việt dễ đọc
STATE_VI = {
    "Submitted and indexed": "✅ Đã index",
    "Indexed, not submitted in sitemap": "✅ Đã index (ngoài sitemap)",
    "Discovered - currently not indexed": "🟡 Đã phát hiện, chưa index",
    "Crawled - currently not indexed": "🟡 Đã crawl, chưa index",
    "Page with redirect": "↪️ Trang có chuyển hướng",
    "Duplicate without user-selected canonical": "⚠️ Trùng lặp, thiếu canonical",
    "Duplicate, Google chose different canonical than user": "⚠️ Google chọn canonical khác",
    "Excluded by 'noindex' tag": "⛔ Bị chặn bởi noindex",
    "Blocked by robots.txt": "⛔ Bị chặn bởi robots.txt",
    "Not found (404)": "❌ Không tìm thấy (404)",
    "Server error (5xx)": "❌ Lỗi server (5xx)",
    "URL is unknown to Google": "⚪ Google chưa biết URL này",
}


def load_urls():
    tree = ET.parse(SITEMAP)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return [loc.text.strip() for loc in tree.findall(".//sm:loc", ns)]


def main():
    sa_json = os.environ.get("GSC_SA_JSON", "").strip()
    if not sa_json:
        # Chưa cấu hình key = trạng thái bình thường trước khi setup.
        # Thoát ÊM (mã 0) để workflow không báo đỏ/spam email mỗi tuần.
        print("Chưa có GSC_SA_JSON — bỏ qua báo cáo tuần này. "
              "Thêm service-account JSON vào GitHub secret 'GSC_SA_JSON' để bật.")
        return
    prop = os.environ.get("GSC_PROPERTY", "").strip() or "sc-domain:greenspacers.vn"

    try:
        info = json.loads(sa_json)
    except json.JSONDecodeError:
        sys.exit("GSC_SA_JSON không phải JSON hợp lệ. Dán nguyên văn file .json.")

    creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    session = AuthorizedSession(creds)

    urls = load_urls()
    rows = []
    counts = {}
    for url in urls:
        body = {"inspectionUrl": url, "siteUrl": prop, "languageCode": "vi"}
        try:
            r = session.post(INSPECT_URL, json=body, timeout=60)
            if r.status_code != 200:
                rows.append((url, f"❌ Lỗi API {r.status_code}", "—"))
                counts["Lỗi"] = counts.get("Lỗi", 0) + 1
                continue
            res = r.json().get("inspectionResult", {}).get("indexStatusResult", {})
            state = res.get("coverageState", "—")
            last = res.get("lastCrawlTime", "—")
            if last and last != "—":
                last = last.split("T")[0]
            label = STATE_VI.get(state, state)
            rows.append((url, label, last))
            key = "Đã index" if state.startswith(("Submitted and indexed", "Indexed")) else "Chưa index"
            counts[key] = counts.get(key, 0) + 1
        except Exception as e:  # noqa: BLE001
            rows.append((url, f"❌ Lỗi: {e}", "—"))
            counts["Lỗi"] = counts.get("Lỗi", 0) + 1

    today = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    indexed = counts.get("Đã index", 0)
    total = len(urls)

    lines = []
    lines.append("# Báo cáo index Google Search Console — greenspacers.vn")
    lines.append("")
    lines.append(f"> Tự động cập nhật: **{today}** · Property: `{prop}`")
    lines.append(f"> **{indexed}/{total} trang đã được index.**")
    lines.append("")
    if counts:
        lines.append("| Nhóm | Số trang |")
        lines.append("|---|---|")
        for k, v in sorted(counts.items()):
            lines.append(f"| {k} | {v} |")
        lines.append("")
    lines.append("## Chi tiết từng trang")
    lines.append("")
    lines.append("| URL | Trạng thái | Crawl cuối |")
    lines.append("|---|---|---|")
    for url, label, last in rows:
        path = url.replace("https://greenspacers.vn", "") or "/"
        lines.append(f"| `{path}` | {label} | {last} |")
    lines.append("")
    lines.append("---")
    lines.append("*File này do workflow `.github/workflows/gsc-report.yml` tự sinh. "
                 "Đừng sửa tay — sẽ bị ghi đè lần chạy sau.*")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Đã ghi {OUT} — {indexed}/{total} trang đã index.")


if __name__ == "__main__":
    main()
