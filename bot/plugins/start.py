from pyrogram import Client, filters

@Client.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "👋 Hi! Send me a video, and I’ll upload it to Google Drive!"
    )
