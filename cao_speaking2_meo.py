#!/usr/bin/env python3
import json
import json5
import re
import requests

AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NjEyMTYsImVtYWlsIjoibWlpdHN1aDI2MiIsImZ1bGxOYW1lIjoiTWlpdHN1aCIsImlzVmVyaWZpZWQiOjEsImV4cGlyZWRBdCI6IjIwMjYtMDgtMTJUMDk6MDQ6NDQuMDAwWiIsImlzQWRtaW4iOmZhbHNlLCJqdGkiOiI2MGRmZGIzYi1kNTQzLTQ2MmItODk4MC00N2UyY2NkNmI1N2EiLCJpYXQiOjE3ODQ2NTMxODgsImV4cCI6MTc4NDczOTU4OH0.mHdYzRutYHSGOY8GthMJH2QxKgOtzZiDqedWzpvd2xQ"  # giữ nguyên token của bạn

API_URL = "https://aptiskey.com/js/speaking/speaking_question2_meo.js"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
    "Referer": "https://aptiskey.com/",
}
COOKIES = {"auth_token": AUTH_TOKEN}


def js_to_json(text: str):
    # Thử tìm biến "const questions = [...]"
    match = re.search(r'const\s+questions\s*=\s*(\[[\s\S]*?\]);', text)
    if not match:
        # Thử tìm biến khác nếu tên biến không phải "questions"
        match = re.search(r'const\s+\w+\s*=\s*(\[[\s\S]*?\]);', text)
    if not match:
        print("⚠️ Không tìm thấy mảng dữ liệu dạng 'const xxx = [...]'")
        return None

    array_str = match.group(1)
    try:
        return json5.loads(array_str)
    except Exception as e:
        print(f"❌ json5 parse lỗi: {e}")
        with open("debug_speaking2_array.txt", "w", encoding="utf-8") as f:
            f.write(array_str)
        print("Đã lưu debug_speaking2_array.txt để kiểm tra")
        return None


def fetch_data():
    session = requests.Session()
    session.headers.update(HEADERS)
    session.cookies.update(COOKIES)

    resp = session.get(API_URL, timeout=15)
    print(f"Status code: {resp.status_code}")

    if resp.status_code != 200:
        print("Lỗi request")
        return None

    with open("debug_speaking2_raw.js", "w", encoding="utf-8") as f:
        f.write(resp.text)

    data = js_to_json(resp.text)
    if data:
        print(f"✅ Thành công! Tìm thấy {len(data)} mục.")
        with open("speaking_question2_meo.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("Đã lưu speaking_question2_meo.json")
        return data
    else:
        print("Không parse được, xem debug_speaking2_raw.js")
        return None


if __name__ == "__main__":
    fetch_data()