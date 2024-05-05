#Chat-DPT Overview

## Kevin Zhang (wfs7bk) and Albert Huang (kfa7fg)

1. Create app on Discord Developer Interface, create a bot in the app and add its token to the .env file
2. Invite bot to desired server through OAuth2 service
3. Pip install dependencies (including openai==0.28) and include all included files in the same directory as main.py
  1. Create a .env file with a CHAT_KEY variable with Chat-GPT API key and BOT_TOKEN variable with bot token
5. Use !help to see usage and available commands
6. Spootify database is incomplete:
  1. only contains the following users: gojo53, sukuna13, sinbad47, kingcrimson2, zipperman3
  2. only contains the following artists: SZA, Metro Boomin, Drake, Don Toliver, The Weeknd, Kali Uchis, Travis Scott, Lil Tecca
  3. Possible questions: a user's favorite artist, how many songs an artist has in the database, how many listeners an artist has, total length of songs of a user's favorite artist in the spootify.db.
