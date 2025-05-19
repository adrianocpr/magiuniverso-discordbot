import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    bot.loop.create_task(keep_alive())

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

async def keep_alive():
    while True:
        print("Bot ativo...")
        await asyncio.sleep(300)  # 5 minutos

if __name__ == "__main__":
    try:
        bot.run(TOKEN)
    except Exception as e:
        import logging
        logging.exception("Erro ao rodar o bot:")
