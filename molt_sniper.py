import requests
import time
import re
import os
import threading
from flask import Flask

# --- إعداد السيرفر الوهمي (عشان Render يرضى يشغله) ---
app = Flask('')

@app.route('/')
def home():
    return "I am alive! Moltbook Sniper is running."

def run_http():
    # Render بيحدد البورت تلقائياً، لو مش موجود نستخدم 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = threading.Thread(target=run_http)
    t.start()

# --- إعدادات البوت ---
# المحاولة الأولى: قراءة المفتاح من ملف config (لو على اللابتوب)
# المحاولة الثانية: قراءة المفتاح من Environment Variables (لو على Render)
try:
    from config import API_KEY
except ImportError:
    API_KEY = os.environ.get("API_KEY")

if not API_KEY:
    print("❌ Error: API_KEY not found in config.py or Environment Variables!")
    exit()

BASE_URL = "https://www.moltbook.com/api/v1"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

replied_posts = set()

def get_new_posts():
    try:
        response = requests.get(f"{BASE_URL}/posts?sort=new&limit=10", headers=HEADERS, timeout=10)
        if response.status_code == 200:
            return response.json().get('data', [])
        elif response.status_code == 429:
            time.sleep(5)
    except Exception as e:
        print(f"❌ Connection Error: {e}")
    return []

def post_comment(post_id, content):
    try:
        url = f"{BASE_URL}/posts/{post_id}/comments"
        requests.post(url, headers=HEADERS, json={"content": content}, timeout=10)
        print(f"✅ SNIPED! Commented on {post_id}")
        return True
    except:
        return False

def start_sniper():
    print("🦞 Moltbook Agent Started on Cloud!")
    while True:
        print(".", end="", flush=True)
        posts = get_new_posts()
        for post in posts:
            post_id = post.get('id')
            if post_id in replied_posts: continue
            
            content = post.get('content', '')
            mint_match = re.search(r'(\{.*?"op":\s*"mint".*?\})', content, re.IGNORECASE)
            
            if mint_match:
                if post_comment(post_id, mint_match.group(1)):
                    replied_posts.add(post_id)
                    time.sleep(21)
        time.sleep(10)

if __name__ == "__main__":
    keep_alive()  # تشغيل السيرفر الوهمي
    start_sniper() # تشغيل البوت
