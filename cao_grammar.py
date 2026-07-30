#!/usr/bin/env python3
import json
import os
import time
import requests

AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NjEyMTYsImVtYWlsIjoibWlpdHN1aDI2MiIsImZ1bGxOYW1lIjoiTWlpdHN1aCIsImlzVmVyaWZpZWQiOjEsImV4cGlyZWRBdCI6IjIwMjYtMDgtMTJUMDk6MDQ6NDQuMDAwWiIsImlzQWRtaW4iOmZhbHNlLCJqdGkiOiI2MGRmZGIzYi1kNTQzLTQ2MmItODk4MC00N2UyY2NkNmI1N2EiLCJpYXQiOjE3ODQ2NTMxODgsImV4cCI6MTc4NDczOTU4OH0.mHdYzRutYHSGOY8GthMJH2QxKgOtzZiDqedWzpvd2xQ"  # giữ nguyên token của bạn

BASE_URL = "https://aptiskey.com/api/grammar-data/{id}"
OUT_DIR = "grammar_data"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
    "Referer": "https://aptiskey.com/",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8",
    "X-Requested-With": "XMLHttpRequest",
}
COOKIES = {"auth_token": AUTH_TOKEN}

TOTAL_IDS = 5
DELAY_BETWEEN_REQUESTS = 1.0
DELAY_ON_403 = 15
MAX_RETRIES = 3

os.makedirs(OUT_DIR, exist_ok=True)

session = requests.Session()
session.headers.update(HEADERS)
session.cookies.update(COOKIES)

all_data = {}

for i in range(1, TOTAL_IDS + 1):
    url = BASE_URL.format(id=i)
    out_path = os.path.join(OUT_DIR, f"grammar_{i}.json")

    if os.path.exists(out_path):
        print(f"⏭️ ID {i}: đã có sẵn, bỏ qua")
        with open(out_path, "r", encoding="utf-8") as f:
            all_data[i] = json.load(f)
        continue

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = session.get(url, timeout=15)
            ctype = resp.headers.get("content-type", "")

            if resp.status_code == 200 and "json" in ctype:
                data = resp.json()
                with open(out_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                all_data[i] = data
                print(f"✅ ID {i}: đã tải")
                break
            elif resp.status_code == 403:
                print(f"⚠️ ID {i}: bị chặn (403), nghỉ {DELAY_ON_403}s rồi thử lại (lần {attempt}/{MAX_RETRIES})")
                time.sleep(DELAY_ON_403)
            else:
                print(f"⚠️ ID {i}: lỗi (status {resp.status_code}, type {ctype})")
                break
        except Exception as e:
            print(f"❌ ID {i}: lỗi {e}")
            break

    time.sleep(DELAY_BETWEEN_REQUESTS)

combined_path = os.path.join(OUT_DIR, "grammar_all.json")
with open(combined_path, "w", encoding="utf-8") as f:
    json.dump(all_data, f, ensure_ascii=False, indent=2)

print(f"\nHoàn tất. Đã gộp vào {combined_path}")