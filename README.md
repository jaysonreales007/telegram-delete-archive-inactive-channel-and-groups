
# Telegram Inactive Chats Cleaner

This Python script helps you automatically delete or leave inactive Telegram chats, channels, and groups based on inactivity. It identifies chats with no activity in the last 6 months or with deleted users and removes them accordingly. The script uses the Telethon library to interact with Telegram's API.




## Features

- Detects and removes chats with deleted accounts.
- Leaves inactive channels and supergroups.
- Deletes archived and inactive chats older than 6 months.
- Logs actions and errors to the console.


# Prerequisites

Before using this script, you must create a Telegram API account and obtain your API credentials:


## Edit the script to include your API_ID, API_HASH, and PHONE_NUMBER:

- API_ID = 'YOUR_API_ID'
- API_HASH = 'YOUR_API_HASH'
- PHONE_NUMBER = 'YOUR_PHONE_NUMBER'
- Logs actions and errors to the console.

You must replace the placeholders (YOUR_API_ID, YOUR_API_HASH, YOUR_PHONE_NUMBER) with your actual Telegram API credentials.


## Setup

Clone the project

```bash
  https://github.com/jaysonreales007/telegram-delete-archive-inactive-channel-and-groups.git
```

Go to the project directory

```bash
  cd telegram-delete-archive-inactive-channel-and-groups
```

Install dependencies

```bash
  pip install telethon
```

Run the script

```bash
  python cleanup_telegram.py
```


## The script will:

- Log in to your Telegram account.
- Iterate through all your chats, checking for inactivity.
- Remove or leave chats with deleted users, inactive channels, and inactive groups older than 6 months.

## How It Works

- Inactivity Check: The script compares the last message date in each chat with the current date minus 6 months (SIX_MONTHS_AGO).
- Archived Chats: Archived chats are automatically deleted if they are inactive.
- Deleted Accounts: If a chat is with a deleted account, it is deleted automatically.
- Groups and Channels: The script will leave inactive supergroups, channels, and basic groups based on their last message date.
- Error Handling
- The script logs any issues (e.g., if it fails to delete a chat) to the console.
- It gracefully handles missing messages or archived chats with deleted users, ensuring no interruption in execution.
