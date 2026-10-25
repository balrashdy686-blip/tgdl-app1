import asyncio
import os
import sys
from tg_core import TelegramDownloader

API_ID = 31558937
API_HASH = "da2bbb947a9502eaa4231b2c9957e61f"


def progress_callback(current, total):
  percent = (current / total) * 100
  print(f"📥 جاري التحميل: {percent:.1f}% مكتمل", end="\r")


async def main():
  print("=== نظام تحميل الفيديوهات من تلجرام ===")
  downloader = TelegramDownloader(API_ID, API_HASH)

  connected = await downloader.connect()
  if not connected:
    print("❌ لم يتم تسجيل الدخول بنجاح.")
    return

  print("✅ تم الاتصال بحسابك بنجاح!\n")

  while True:
    try:
      text = input('🔗 أدخل رابط الفيديو (أو اكتب "خروج"): ').strip()
      if text.lower() in ["خروج", "exit", "quit"]:
        print("إغلاق البرنامج. مع السلامة!")
        break
      if not text:
        continue

      print("⏳ جاري تحليل الرابط...")
      msg = await downloader.resolve_message(text)

      if msg and msg.media:
        print("🚀 بدء التنزيل...")
        download_dir = "/storage/emulated/0/Download/"
        if not os.path.exists(download_dir):
          download_dir = "./downloads/"
          os.makedirs(download_dir, exist_ok=True)

        path = await msg.download_media(
            file=download_dir, progress_callback=progress_callback
        )
        print(f"\n✅ تم الحفظ في: {path}\n")
      else:
        print("❌ لم يتم العثور على ملف فيديو أو المحتوى محمي.\n")
    except Exception as e:
      print(f"❌ حدث خطأ: {e}\n")


if __name__ == "__main__":
  asyncio.run(main())

