import discord
from discord.ext import commands
import os
import asyncio
import subprocess

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def logs(ctx):
    try:
        with open("logs.txt", "r") as f:
            conteudo = f.read()
            if not conteudo.strip():
                await ctx.send("Arquivo de log está vazio.")
            else:
                if len(conteudo) > 1900:
                    await ctx.send("Log muito grande para exibir.")
                else:
                    await ctx.send(f"```\n{conteudo}\n```")
    except FileNotFoundError:
        await ctx.send("Arquivo de log não encontrado.")

@bot.command()
async def verificar(ctx):
    try:
        result = subprocess.run(["python", "verificador_integridade.py"], capture_output=True, text=True)
        output = result.stdout.strip()
        if not output:
            await ctx.send("Sem resposta do verificador.")
        elif len(output) > 1900:
            await ctx.send("Saída muito grande para exibir.")
        else:
            await ctx.send(f"```\n{output}\n```")
    except Exception as e:
        await ctx.send(f"Erro ao executar verificação: {e}")

async def periodic_integrity_check(interval=300):
    while True:
        try:
            print("[Verificador] Iniciando verificação de integridade...")
            result = subprocess.run(["python", "verificador_integridade.py"], capture_output=True, text=True)
            print(result.stdout.strip())
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
