
import discord
from discord.ext import commands
import os
import asyncio
import subprocess
import sqlite3

TOKEN = os.getenv("DISCORD_TOKEN")
LOG_FILE = "logs.txt"
DB_FILE = "banco.db"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def logs(ctx):
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            content = f.read()[-1500:]
        await ctx.send(f"```
{content}
```")
    else:
        await ctx.send("Arquivo de log não encontrado.")

@bot.command()
async def bd(ctx):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
        if tables:
            await ctx.send(f"Tabelas: {', '.join(t[0] for t in tables)}")
        else:
            await ctx.send("Nenhuma tabela encontrada.")
    except Exception as e:
        await ctx.send(f"Erro ao acessar o banco: {e}")

@bot.command()
async def verificar(ctx):
    result = subprocess.run(["python", "verificador_integridade_periodico.py"], capture_output=True, text=True)
    await ctx.send(f"```
{result.stdout[:1900]}
```")

async def periodic_integrity_check(interval=300):
    while True:
        print("[Verificador] Iniciando verificação de integridade...")
        subprocess.run(["python", "verificador_integridade_periodico.py"], capture_output=True, text=True)
        await asyncio.sleep(interval)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    bot.loop.create_task(periodic_integrity_check())

if TOKEN:
    bot.run(TOKEN)
else:
    print("⚠️ Token do Discord não definido.")
