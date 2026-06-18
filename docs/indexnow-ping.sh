#!/bin/bash
# IndexNow ping script — chạy thủ công khi muốn báo Bing/Yandex có web mới
# Cách dùng: bash indexnow-ping.sh

KEY="6adadccf3476291837bf11da2472ee5b"
HOST="greenspacers.vn"

curl -X POST "https://api.indexnow.org/indexnow" \
  -H "Content-Type: application/json" \
  -d "{
    \"host\": \"$HOST\",
    \"key\": \"$KEY\",
    \"keyLocation\": \"https://$HOST/$KEY.txt\",
    \"urlList\": [
      \"https://$HOST/\",
      \"https://$HOST/quan-ly-dat-nam-ban\",
      \"https://$HOST/kiem-tra-dat-lam-ha\",
      \"https://$HOST/trong-coi-dat-o-xa\",
      \"https://$HOST/ve-greenspace\"
    ]
  }"
echo ""
echo "✅ Đã báo IndexNow — Bing, Yandex sẽ crawl trong vài phút"
