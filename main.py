import discord
from discord.ext import commands
import os
import asyncio
from verificador_integridade_periodico import verificar_integridade

TOKEN = os.getenv("DISCORD_TOKEN")
CANAL_LOG_ID = 1371601665169428501

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def verificar(ctx):
    alertas = verificar_integridade()
    log = "\n".join(alertas)
    await ctx.send(f"🛡️ Verificação de integridade:\n```{log}```")

async def periodic_integrity_check(canal, interval=300):
    await bot.wait_until_ready()
    while not bot.is_closed():
        alertas = verificar_integridade()
        log = "\n".join(alertas)
        if canal:
            await canal.send(f"🛡️ Verificação de integridade:\n```{log}```")
        else:
            print("[Verificação] Canal não disponível.")
        await asyncio.sleep(interval)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    canal_log = bot.get_channel(CANAL_LOG_ID)
    if canal_log:
        await canal_log.send("✅ Bot iniciado com sucesso e verificação periódica ativada.")
    else:
        print("⚠️ Canal de log não encontrado. Verifique o ID.")
    bot.loop.create_task(periodic_integrity_check(canal_log))

if TOKEN:
    bot.run(TOKEN)
else:
    print("⚠️ Token do Discord não definido. Verifique a variável de ambiente 'DISCORD_TOKEN'.")
