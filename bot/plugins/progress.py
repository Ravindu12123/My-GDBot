from pyrogram.types import Message

async def progress(current, total, message: Message):
    percent = (current / total) * 100
    await message.edit(f"Progress: {percent:.2f}%")
