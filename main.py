import os
import discord
from discord.ext import commands
from fastapi import FastAPI
import uvicorn

TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Bot e API rodando"}

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")

# Rodar FastAPI em thread separada
if __name__ == "__main__":
    import threading

    def start_api():
        uvicorn.run("main:app", host="0.0.0.0", port=10000, log_level="info")

    threading.Thread(target=start_api).start()
    bot.run(TOKEN)