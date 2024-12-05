from pyrogram import Client, filters
from bot.utils.drive import upload_to_drive
import os

UPLOAD_FOLDER = "uploads/"

@Client.on_message(filters.video)
async def upload_video(client, message):
    user_id = message.from_user.id

    await message.reply_text("📥 Downloading your video...")
    video = await message.download(file_name=UPLOAD_FOLDER)
    file_name = os.path.basename(video)

    try:
        await message.reply_text("☁️ Uploading to Google Drive...")
        drive_file_id = upload_to_drive(user_id, video, file_name)
        drive_link = f"https://drive.google.com/file/d/{drive_file_id}/view"
        await message.reply_text(f"✅ Uploaded successfully!\n[View on Google Drive]({drive_link})", disable_web_page_preview=True)
    except Exception as e:
        await message.reply_text(f"❌ Failed to upload: {str(e)}")
    finally:
        os.remove(video)
