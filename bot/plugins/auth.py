import json
from pyrogram import Client, filters
from google.oauth2.credentials import Credentials

TOKEN_FILE = "token_store.json"

# Load stored tokens
def load_tokens():
    if not TOKEN_FILE or not os.path.exists(TOKEN_FILE):
        return {}
    with open(TOKEN_FILE, "r") as file:
        return json.load(file)

# Save tokens
def save_tokens(tokens):
    with open(TOKEN_FILE, "w") as file:
        json.dump(tokens, file)

# /auth command
@Client.on_message(filters.command("auth"))
async def authenticate_user(client, message):
    tokens = load_tokens()
    user_id = str(message.from_user.id)

    # Check if a token is provided
    if len(message.command) < 2:
        await message.reply_text("❌ Please provide a valid Google Drive credential token.\n\nUsage: `/auth <credtoken>`", parse_mode="markdown")
        return

    # Extract credential token from the command
    cred_token = " ".join(message.command[1:])

    try:
        # Parse the provided token into Google Credentials
        credentials = Credentials.from_authorized_user_info(json.loads(cred_token))
        
        # Store the credentials for the user
        tokens[user_id] = cred_token
        save_tokens(tokens)

        await message.reply_text("✅ Authentication successful! You can now upload files to your Google Drive.")
    except Exception as e:
        await message.reply_text(f"❌ Invalid token provided. Error: {str(e)}")
