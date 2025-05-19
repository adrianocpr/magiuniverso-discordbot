
import os
import discord
from discord.ext import commands
from utils.logger import setup_logger

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

logger = setup_logger()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    logger.info(f"{bot.user} está online e pronto!")

@bot.command()
async def status(ctx):
    await ctx.send("✅ Bot está rodando normalmente.")

@bot.command()
async def log(ctx):
    try:
        with open("logs/bot.log", "r") as f:
            content = f.readlines()[-10:]
        await ctx.send("```" + "".join(content) + "```")
    except Exception as e:
        await ctx.send(f"Erro ao ler o log: {e}")

@bot.command()
async def restart(ctx):
    await ctx.send("♻️ Reiniciando bot...")
    os.execv(sys.executable, ['python'] + sys.argv)

bot.run(TOKEN)
