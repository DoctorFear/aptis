#!/usr/bin/env python3
import requests
import os
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NjEyMTYsImVtYWlsIjoibWlpdHN1aDI2MiIsImZ1bGxOYW1lIjoiTWlpdHN1aCIsImlzVmVyaWZpZWQiOjEsImV4cGlyZWRBdCI6IjIwMjYtMDgtMTJUMDk6MDQ6NDQuMDAwWiIsImlzQWRtaW4iOmZhbHNlLCJqdGkiOiI2MGRmZGIzYi1kNTQzLTQ2MmItODk4MC00N2UyY2NkNmI1N2EiLCJpYXQiOjE3ODQ2NTMxODgsImV4cCI6MTc4NDczOTU4OH0.mHdYzRutYHSGOY8GthMJH2QxKgOtzZiDqedWzpvd2xQ"
# Sửa lại URL gốc cho đúng với đường dẫn thực tế trên site

BASE_URL = "https://aptiskey.com/images/speaking/part3/{filename}"
OUT_DIR = "images_de"
HEADERS = {"User-Agent": "Mozilla/5.0"}
COOKIES = {"auth_token": AUTH_TOKEN}

TOTAL_DE = 25
IMAGES_PER_DE = 2

os.makedirs(OUT_DIR, exist_ok=True)

session = requests.Session()
session.headers.update(HEADERS)
session.cookies.update(COOKIES)

for de in range(1, TOTAL_DE + 1):
    de_str = f"{de:02d}"
    for img_num in range(1, IMAGES_PER_DE + 1):
        filename = f"de{de_str}_{img_num}.png"
        url = BASE_URL.format(filename=filename)
        out_path = os.path.join(OUT_DIR, filename)

        try:
            resp = session.get(url, timeout=15)
            ctype = resp.headers.get("content-type", "")

            if resp.status_code == 200 and ctype.startswith("image"):
                with open(out_path, "wb") as f:
                    f.write(resp.content)
                print(f"✅ Đã tải {filename} ({len(resp.content)} bytes)")
            else:
                print(f"⚠️ Bỏ qua {filename} (status {resp.status_code}, content-type {ctype})")
        except Exception as e:
            print(f"❌ Lỗi tải {filename}: {e}")

print("Hoàn tất.")