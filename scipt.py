import asyncio
from telethon import TelegramClient

# Replace these with your actual API credentials
API_ID = 24393293 # Your API ID
API_HASH = "ec1d4354a6aa9d1201819176fe3d2b5d"  # Your API Hash

# Source chat/channel and message ID
SOURCE_CHAT = "bot98765432123456"  # Extracted from your link
MESSAGE_ID = 4  # Message number

# List of target channels/groups where you want to forward the message
DESTINATION_CHATS = ["@freepromotion15", "@ObmenGolosamiTG", "@tgchannel_freepromo", "@ArTifiCiaL_GaMeR01"]
INTERVAL = 30 * 60  # 30 minutes in seconds

async def forward_post():
    async with TelegramClient('session_name', API_ID, API_HASH) as client:
        while True:
            for chat in DESTINATION_CHATS:
                try:
                    # Forward the message from SOURCE_CHAT to each target channel
                    await client.forward_messages(chat, MESSAGE_ID, SOURCE_CHAT)
                    print(f"✅ Forwarded message to {chat}")
                except Exception as e:
                    print(f"❌ Failed to forward to {chat}: {e}")
            await asyncio.sleep(INTERVAL)  # Wait 15 minutes before repeating

# Run the script
asyncio.run(forward_post())
