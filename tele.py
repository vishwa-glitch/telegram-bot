import os
import asyncio
import random
import requests
from bs4 import BeautifulSoup
from telegram import Bot

# Configuration
WEBSITES = [
    "https://www.pornpics.com/tags/hot-milf/",
    "https://www.pornpics.com/tags/teen/",
    "https://www.pornpics.com/tags/amateur/",
    "https://www.pornpics.com/tags/anal/", 
    "https://www.pornpics.com/tags/asian/"
]
TELEGRAM_BOT_TOKEN = "7630710110:AAE1jWMiWhDnUjqKIo2lgWY2Yc_McbM2wpY"
TELEGRAM_CHANNEL_ID = "-1002501159798"
DOWNLOAD_FOLDER = "temp_images"
NUM_IMAGES = 6

# Headers configuration
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "https://www.google.com/",
    "Upgrade-Insecure-Requests": "1",
}

# Create download directory
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

async def main():
    # Randomly select a website
    target_url = random.choice(WEBSITES)
    print(f"Selected website: {target_url}")

    # Scrape image URLs
    try:
        response = requests.get(target_url, headers=HEADERS, timeout=30)  # Increased timeout
        response.raise_for_status()  # Raise HTTP errors
        soup = BeautifulSoup(response.content, "html.parser")
        items = soup.find_all("li", class_="thumbwook")
        
        all_images = []
        for item in items:
            img_tag = item.find("img")
            if img_tag and (src := img_tag.get("src")):
                if src.startswith("/"):
                    src = f"{target_url}{src}"
                all_images.append(src)

        # Select random 6 images
        selected_images = random.sample(all_images, min(NUM_IMAGES, len(all_images)))
        print(f"Found {len(selected_images)} images")

    except requests.exceptions.ProxyError:
        print("Proxy error: Unable to connect to proxy.")
        return
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return

    # Download and send images
    bot = Bot(TELEGRAM_BOT_TOKEN)
    for idx, img_url in enumerate(selected_images):
        try:
            # Download image
            response = requests.get(img_url, headers=HEADERS, proxies=PROXIES, stream=True, timeout=30)
            response.raise_for_status()
            file_path = os.path.join(DOWNLOAD_FOLDER, f"img_{idx}.jpg")
            
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)

            # Send to Telegram
            with open(file_path, "rb") as f:
                await bot.send_photo(chat_id=TELEGRAM_CHANNEL_ID, photo=f)
            
            # Cleanup
            os.remove(file_path)
            print(f"Sent and deleted: {file_path}")

        except requests.exceptions.ProxyError:
            print("Proxy error while downloading image.")
        except requests.exceptions.RequestException as e:
            print(f"Failed to process image: {e}")
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

if __name__ == "__main__":
    asyncio.run(main())
