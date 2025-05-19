import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    raise ValueError("DISCORD_TOKEN não está definido. Verifique suas variáveis de ambiente.")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

bot.run(TOKEN)
