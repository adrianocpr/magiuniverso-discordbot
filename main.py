import discord
from discord.ext import commands
import os
import asyncio
import subprocess

# Carrega o token do ambiente
TOKEN = os.getenv("DISCORD_TOKEN")

# Inicializa o bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Comando de teste simples
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

# --- Função periódica de verificação de integridade ---
async def periodic_integrity_check(interval=300):
    while True:
        try:
            print("[Verificador] Iniciando verificação de integridade...")
            result = subprocess.run(["python", "verificador_integridade.py"], capture_output=True, text=True)
            print(result.stdout.strip())
        except Exception as e:
            print(f"[Verificador] Erro na verificação: {e}")
        await asyncio.sleep(interval)

# --- Evento on_ready ---
@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    # Inicia a verificação periódica
    bot.loop.create_task(periodic_integrity_check())

# --- Inicia o bot ---
if TOKEN:
    bot.run(TOKEN)
else:
    print("⚠️ Token do Discord não definido. Verifique a variável de ambiente 'DISCORD_TOKEN'.")
