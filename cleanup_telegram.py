from datetime import datetime, timedelta, timezone
from telethon import TelegramClient, errors
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.types import User  # Import User class
from telethon.utils import get_display_name
import asyncio

# Replace these with your own values
API_ID = 'YOUR_API_ID'
API_HASH = 'YOUR_API_HASH'
PHONE_NUMBER = 'YOUR_PHONE_NUMBER'

# Time window to check for inactivity (6 months)
SIX_MONTHS_AGO = datetime.now(timezone.utc) - timedelta(days=180)

async def delete_inactive_chats():
    # Initialize the Telegram client
    async with TelegramClient('session_name', API_ID, API_HASH) as client:
        try:
            await client.start(phone=PHONE_NUMBER)
            me = await client.get_me()
            print(f"Logged in as: {get_display_name(me)} (@{me.username})")
        except errors.PhoneCodeRequiredError:
            print("Phone code required. Please provide it manually.")
            return
        except Exception as e:
            print(f"Failed to start client: {e}")
            return

        # Iterate over all dialogs (chats, groups, channels)
        async for dialog in client.iter_dialogs():
            chat = dialog.entity

            # Skip if there's no last message (e.g., empty chats)
            if not dialog.message:
                chat_title = get_display_name(chat)
                print(f"Skipping '{chat_title}' (no messages found)")
                continue

            last_message_date = dialog.message.date

            # Check for archived chats
            if dialog.archived:
                chat_title = get_display_name(chat)
                print(f"Archived chat found: {chat_title}")

                try:
                    if isinstance(chat, User) and chat.deleted:
                        # Delete chat with "Deleted Account" users
                        await client.delete_dialog(chat)
                        print(f"Deleted chat with 'Deleted Account'")
                    else:
                        # Delete archived chat
                        await client.delete_dialog(chat)
                        print(f"Deleted archived chat: {chat_title}")
                except Exception as e:
                    print(f"Failed to delete archived chat '{chat_title}': {e}")
                continue

            # Check for "Deleted Account" users
            if isinstance(chat, User) and chat.deleted:
                chat_title = "Deleted Account"
                try:
                    await client.delete_dialog(chat)
                    print(f"Deleted chat with: {chat_title}")
                except Exception as e:
                    print(f"Failed to delete chat with '{chat_title}': {e}")
                continue

            # Compare the last message date with six_months_ago
            if last_message_date < SIX_MONTHS_AGO:
                chat_title = get_display_name(chat)
                print(f"Inactive chat found: {chat_title} (Last message: {last_message_date})")

                try:
                    if hasattr(chat, 'broadcast') and chat.broadcast:
                        # It's a channel
                        await client(LeaveChannelRequest(chat))
                        print(f"Left channel: {chat_title}")
                    elif hasattr(chat, 'megagroup') and chat.megagroup:
                        # It's a supergroup
                        await client(LeaveChannelRequest(chat))
                        print(f"Left supergroup: {chat_title}")
                    elif hasattr(chat, 'is_group') and chat.is_group:
                        # It's a basic group
                        await client(LeaveChannelRequest(chat))
                        print(f"Left group: {chat_title}")
                    else:
                        # It's a private chat (User)
                        await client.delete_dialog(chat)
                        print(f"Deleted private chat: {chat_title}")
                except Exception as e:
                    print(f"Failed to delete '{chat_title}': {e}")

if __name__ == "__main__":
    asyncio.run(delete_inactive_chats())
