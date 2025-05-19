import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True  # Adiciona permissão para ler conteúdo das mensagens

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
