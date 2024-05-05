import discord
from discord.ext import commands

from dotenv import load_dotenv
import os

import openai
import requests

import sqlite3

load_dotenv()

openai.api_key = os.getenv("CHAT_KEY")

TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")


# get bot online
@bot.event
async def on_ready():
    print("Online")


# error message if command not found
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Sorry, I do not have that command")


'''@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')'''


# help command listing out commands
@bot.command()
async def help(ctx):
    help_embed = discord.Embed(title="chat-dpt's Help!")

    values = ""

    counter = 1
    for command in bot.commands:
        if command.name == "help":
            continue
        elif command.name == "translate":
            values += f"{counter}. !{command.name} [text to translate]\n"
            values += f"\t\t{command.description}\n"
        elif command.name == "weather":
            values += f"{counter}. !{command.name} [latitude] [longitude]\n"
            values += f"\t\t{command.description}\n"
        elif command.name == "query":
            values += f"{counter}. !{command.name} [query]\n"
            values += f"\t\t{command.description}\n"

        counter += 1

    # list commands
    help_embed.add_field(
        name="List of supported commands:",
        value=values,
        inline=False
    )
    await ctx.send(embed=help_embed)


# functional commands
@bot.command(description="translates input phrase into english")
async def translate(ctx, *args):
    # print("translate command")
    arguments = ' '.join(args)
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Choose the model you prefer
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Translate the following text: {arguments}"}
            ]
        )
        translated_text = response['choices'][0]['message']['content']

        await ctx.send(f"Translated text: {translated_text}")
    except Exception as e:
        print(e)
        await ctx.send(f"An error occurred. Please try again.")


@bot.command(description="gives the weather at the latitude and longitude input")
async def weather(ctx, *args):
    try:
        responseapi = requests.get(
            f"https://api.open-meteo.com/v1/forecast?latitude={args[0]}&longitude={args[1]}&current=temperature_2m,precipitation,weather_code")
        responseapi.raise_for_status()
        responsedict = responseapi.json()
        current = responsedict['current']
        # print(responsedict)
        retrieved = f"Current time: {current['time']}, Current Temperature: {current['temperature_2m']}{responsedict['current_units']['temperature_2m']}, Current Precipitation: {current['precipitation']}{responsedict['current_units']['precipitation']}, Weather Code: {current['weather_code']}"
        await ctx.send(f"At latitude {args[0]} and longitude {args[1]}: {retrieved}")
    except requests.exceptions.RequestException as errex:
        print(f"Invalid argument for latitude and longitude. Try again.")
        await ctx.send(f"Invalid argument for latitude and longitude. Try again.")


@bot.command(description="queries spootify database with a question (music related)")
async def query(ctx, *args):
    arguments = ' '.join(args)
    databaseinfo = "The spootify.db contains 5 tables: Users, Artists, Songs, Playlists, and Impact. The Users table contains user_id, username, email, favorite_artist, and favorite_artist_id. The Artists table contains artist_id, name, birthdate, and gender. The Songs table contains song_id, title, duration, artist_id, and artist_name. The Playlists table contains playlist_id, name, and user_id. The Impact table contains artist_name, mbid, popularity, and listeners. Create a SQLlite query for the following prompt (only the code without additional text): "
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Choose the model you prefer
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"{databaseinfo} {arguments}"}
            ]
        )
        sql_query = response['choices'][0]['message']['content']

        print(sql_query)

        if sql_query.startswith("```sql"):
            sql_query = sql_query[6:]
            sql_query = sql_query[:-3]

        spootconnection = sqlite3.connect('spootify.db')

        spootcursor = spootconnection.cursor()

        selection = spootcursor.execute(sql_query)
        query = selection.fetchall()

        await ctx.send(f"Query output: {query}")
    except Exception as e:
        print(e)
        await ctx.send(f"An error occurred generating SQL query. Please try again.")


bot.run(TOKEN)
