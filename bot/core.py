import discord
from discord.ext import commands
from bot.config import ADMIN_USER_IDS

class MagiUniversoBot(commands.Bot):
    async def on_ready(self):
        print(f"Conectado como {self.user}")

    async def on_command_error(self, ctx, error):
        await ctx.send(f"Ocorreu um erro: {str(error)}")

bot = MagiUniversoBot(command_prefix="!")

@bot.command()
async def status(ctx):
    await ctx.send("O sistema está funcionando normalmente.")

@bot.command()
async def helpme(ctx):
    await ctx.send("Comandos disponíveis: !status, !logs, !repositorio, !modificar")
