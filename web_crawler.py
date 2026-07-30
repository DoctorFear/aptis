#!/usr/bin/env python3
import json
import requests

AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NjEyMTYsImVtYWlsIjoibWlpdHN1aDI2MiIsImZ1bGxOYW1lIjoiTWlpdHN1aCIsImlzVmVyaWZpZWQiOjEsImV4cGlyZWRBdCI6IjIwMjYtMDgtMTJUMDk6MDQ6NDQuMDAwWiIsImlzQWRtaW4iOmZhbHNlLCJqdGkiOiI2MGRmZGIzYi1kNTQzLTQ2MmItODk4MC00N2UyY2NkNmI1N2EiLCJpYXQiOjE3ODQ2NTMxODgsImV4cCI6MTc4NDczOTU4OH0.mHdYzRutYHSGOY8GthMJH2QxKgOtzZiDqedWzpvd2xQ"  # giữ nguyên token của bạn

API_URL = "https://aptiskey.com/api/reading-question1-data"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://aptiskey.com/reading_question1.html",
    "X-Requested-With": "XMLHttpRequest",
}
COOKIES = {"auth_token": AUTH_TOKEN}

session = requests.Session()
session.headers.update(HEADERS)
session.cookies.update(COOKIES)

resp = session.get(API_URL, timeout=15)
print(f"Status code: {resp.status_code}")
print(f"Content-Type: {resp.headers.get('content-type')}")

if resp.status_code != 200:
    print("Lỗi request")
    print(resp.text[:500])
else:
    try:
        data = resp.json()
        print(f"✅ Thành công! Số câu hỏi: {len(data)}")

        with open("question1_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("Đã lưu file question1_data.json")

        # In thử câu đầu tiên để kiểm tra
        print("\nCâu đầu tiên:")
        print(json.dumps(data[0], ensure_ascii=False, indent=2))

    except json.JSONDecodeError:
        print("Response không phải JSON, lưu raw để kiểm tra")
        with open("debug_listening_raw.txt", "w", encoding="utf-8") as f:
            f.write(resp.text)
        print("Đã lưu debug_listening_raw.txt")