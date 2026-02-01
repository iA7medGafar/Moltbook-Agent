import requests
import time
import re
import json
import sys

# محاولة استيراد المفتاح السري من ملف التكوين
try:
    from config import API_KEY
except ImportError:
    print("❌ Critical Error: 'config.py' file not found!")
    print("👉 Please create 'config.py' and add your API_KEY inside it.")
    sys.exit(1)

# --- إعدادات الاتصال ---
BASE_URL = "https://www.moltbook.com/api/v1"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# قائمة لتخزين المنشورات التي تم الرد عليها (في الذاكرة المؤقتة)
replied_posts = set()

def get_new_posts():
    """جلب أحدث المنشورات من الموقع"""
    try:
        url = f"{BASE_URL}/posts?sort=new&limit=10"
        response = requests.get(url, headers=HEADERS, timeout=10)
        
        if response.status_code == 200:
            return response.json().get('data', [])
        elif response.status_code == 429:
            print("⏳ Feed Rate Limit. Cooling down...")
            time.sleep(5)
        else:
            print(f"⚠️ API Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")
    return []

def post_comment(post_id, content):
    """إرسال تعليق (للمشاركة في Mint أو Airdrop)"""
    url = f"{BASE_URL}/posts/{post_id}/comments"
    data = {"content": content}
    
    try:
        response = requests.post(url, headers=HEADERS, json=data, timeout=10)
        
        if response.status_code in [200, 201]:
            print(f"✅ SNIPED! Successfully commented on post {post_id}")
            return True
        elif response.status_code == 429:
            retry_data = response.json()
            wait_time = retry_data.get('retry_after_seconds', 20)
            print(f"⏳ Comment Rate Limit. Waiting {wait_time}s...")
            time.sleep(wait_time)
        else:
            print(f"❌ Failed to comment: {response.text}")
            
    except Exception as e:
        print(f"❌ Error posting comment: {e}")
    return False

def start_sniper():
    print("="*40)
    print("🦞 Moltbook Autonomous Agent v1.0")
    print("🔒 Security: API Key loaded from config.py")
    print("🎯 Target: MBC-20 Mints & Airdrops")
    print("="*40)

    while True:
        print(".", end="", flush=True) # مؤشر نبض
        posts = get_new_posts()
        
        for post in posts:
            post_id = post.get('id')
            content = post.get('content', '')
            author = post.get('author', {}).get('name', 'Unknown')

            # تخطي ما تم الرد عليه مسبقاً
            if post_id in replied_posts:
                continue

            # --- تحليل المحتوى (Logic) ---
            
            # 1. البحث عن كود Mint (بصيغة JSON)
            mint_match = re.search(r'(\{.*?"op":\s*"mint".*?\})', content, re.IGNORECASE)
            
            if mint_match:
                mint_code = mint_match.group(1)
                print(f"\n\n💰 OPPORTUNITY DETECTED from {author}!")
                print(f"📜 Code: {mint_code}")
                
                if post_comment(post_id, mint_code):
                    replied_posts.add(post_id)
                    print("💤 Resting for 21s (Anti-Spam Rule)...")
                    time.sleep(21)

            # 2. البحث عن كلمات Airdrop
            elif "airdrop" in content.lower() or "claim" in content.lower():
                # نتجاهل البوستات الطويلة جداً (غالباً شرح وليست كود)
                if len(content) < 200:
                    print(f"\n\n👀 Potential Airdrop from {author}: {content}")
                    replied_posts.add(post_id) # نضيفه عشان ما يزعجنا، ونقرر يدوياً

        # استراحة قصيرة قبل الفحص التالي
        time.sleep(10)

if __name__ == "__main__":
    start_sniper()
