import discord
from discord.ext import commands
import os
import asyncio
import subprocess

TOKEN = os.getenv("DISCORD_TOKEN")
ALERTA_CANAL_ID = 1371601665169428501

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

async def enviar_alertas_para_discord(alertas):
    canal = bot.get_channel(ALERTA_CANAL_ID)
    if canal:
        if alertas:
            await canal.send("🚨 **Alertas de integridade detectados:**\n" + "\n".join(f"- {a}" for a in alertas))
        else:
            await canal.send("✅ Todos os arquivos estão íntegros.")

async def periodic_integrity_check(interval=300):
    while True:
        try:
            print("[Verificador] Iniciando verificação de integridade...")
            result = subprocess.run(["python", "verificador_integridade.py"], capture_output=True, text=True)
            output = result.stdout.strip()
            print(output)
            alertas = [line[2:] for line in output.splitlines() if line.startswith("- ") or "detectado" in line]
            await enviar_alertas_para_discord(alertas)
        except Exception as e:
            print(f"[Verificador] Erro na verificação: {e}")
        await asyncio.sleep(interval)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    bot.loop.create_task(periodic_integrity_check())

if TOKEN:
    bot.run(TOKEN)
else:
    print("⚠️ Token do Discord não definido. Verifique a variável de ambiente 'DISCORD_TOKEN'.")