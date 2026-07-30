#!/usr/bin/env python3
"""
Script cào dữ liệu câu hỏi (JSON) và tải toàn bộ file audio
cho trang listening_question1_13 trên aptiskey.com
"""
import json
import os
import time
import requests

# ==== CẤU HÌNH ====
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NjEyMTYsImVtYWlsIjoibWlpdHN1aDI2MiIsImZ1bGxOYW1lIjoiTWlpdHN1aCIsImlzVmVyaWZpZWQiOjEsImV4cGlyZWRBdCI6IjIwMjYtMDgtMTJUMDk6MDQ6NDQuMDAwWiIsImlzQWRtaW4iOmZhbHNlLCJqdGkiOiI2MGRmZGIzYi1kNTQzLTQ2MmItODk4MC00N2UyY2NkNmI1N2EiLCJpYXQiOjE3ODQ2NTMxODgsImV4cCI6MTc4NDczOTU4OH0.mHdYzRutYHSGOY8GthMJH2QxKgOtzZiDqedWzpvd2xQ"  # giữ nguyên token của bạn

API_URL = "https://aptiskey.com/api/listening-question1-13-data"
BASE = "https://aptiskey.com/"
JSON_FILE = "listening_question16.json"
OUT_DIR = "audio_question14"

DELAY_BETWEEN_REQUESTS = 1.5   # giây, giãn cách giữa các file
DELAY_ON_403 = 15              # giây, nghỉ khi bị chặn rồi thử lại
MAX_RETRIES = 3

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36",
    "Referer": "https://aptiskey.com/listening_question1_13.html",
    "Accept": "*/*",
    "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8",
}
COOKIES = {"auth_token": AUTH_TOKEN}


def fetch_question_data(session):
    """Lấy dữ liệu JSON câu hỏi từ API và lưu ra file."""
    print("=== Bước 1: Cào dữ liệu câu hỏi (JSON) ===")
    resp = session.get(API_URL, timeout=15)
    print(f"Status code: {resp.status_code}")

    if resp.status_code != 200:
        print("❌ Lỗi request data JSON")
        print(resp.text[:500])
        return None

    try:
        data = resp.json()
        print(f"✅ Thành công! Số câu hỏi: {len(data)}")
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Đã lưu {JSON_FILE}")
        return data
    except json.JSONDecodeError:
        print("❌ Response không phải JSON, lưu raw để kiểm tra")
        with open("debug_listening_raw.txt", "w", encoding="utf-8") as f:
            f.write(resp.text)
        return None


def download_audio(session, data):
    """Tải toàn bộ file audio dựa trên audioUrl trong data JSON."""
    print("\n=== Bước 2: Tải file audio ===")
    os.makedirs(OUT_DIR, exist_ok=True)

    # Headers riêng cho request audio (giả lập trình duyệt phát audio)
    audio_headers = dict(HEADERS)
    audio_headers.update({
        "Range": "bytes=0-",
        "Sec-Fetch-Dest": "audio",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Site": "same-origin",
    })

    for item in data:
        heading = item.get("heading", "unknown")
        audio_url = item.get("audioUrl")

        if not audio_url:
            print(f"⚠️ {heading}: không có audioUrl")
            continue

        full_url = BASE + audio_url.lstrip("/")
        filename = os.path.basename(audio_url)
        out_path = os.path.join(OUT_DIR, filename)

        if os.path.exists(out_path):
            print(f"⏭️ {heading}: đã có {filename}, bỏ qua")
            continue

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                resp = session.get(full_url, headers=audio_headers, timeout=20)
                ctype = resp.headers.get("content-type", "")

                if resp.status_code in (200, 206) and ("audio" in ctype or filename.endswith(".mp3")):
                    with open(out_path, "wb") as f:
                        f.write(resp.content)
                    print(f"✅ {heading}: đã tải {filename} ({len(resp.content)} bytes)")
                    break
                elif resp.status_code == 403:
                    print(f"⚠️ {heading}: bị chặn (403), nghỉ {DELAY_ON_403}s rồi thử lại (lần {attempt}/{MAX_RETRIES})")
                    time.sleep(DELAY_ON_403)
                else:
                    print(f"⚠️ {heading}: lỗi tải {filename} (status {resp.status_code}, type {ctype})")
                    break
            except Exception as e:
                print(f"❌ {heading}: lỗi {e}")
                break

        time.sleep(DELAY_BETWEEN_REQUESTS)

    print("\nHoàn tất tải audio.")


if __name__ == "__main__":
    session = requests.Session()
    session.headers.update(HEADERS)
    session.cookies.update(COOKIES)

    # Nếu đã có sẵn file JSON rồi thì dùng lại, không cần cào lại
    if os.path.exists(JSON_FILE):
        print(f"Đã có sẵn {JSON_FILE}, dùng lại (xóa file này nếu muốn cào lại data mới)")
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = fetch_question_data(session)

    if data:
        download_audio(session, data)
    else:
        print("Không có dữ liệu để tải audio.")