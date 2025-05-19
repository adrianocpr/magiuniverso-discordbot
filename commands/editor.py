from discord.ext import commands
import os

SUGGESTIONS_PATH = "logs/suggestions.txt"

class Editor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sugerir(self, ctx, *, code):
        with open(SUGGESTIONS_PATH, "a") as f:
            f.write(f"--- SUGESTÃO DE {ctx.author} ---\n{code}\n\n")
        await ctx.send("📬 Sugestão de código recebida. Será revisada em breve.")

    @commands.command()
    async def revisar(self, ctx):
        if ctx.author.guild_permissions.administrator:
            try:
                with open(SUGGESTIONS_PATH, "r") as f:
                    content = f.read()[-1800:]
                await ctx.send(f"📝 Sugestões pendentes:\n```{content}```")
            except FileNotFoundError:
                await ctx.send("❌ Nenhuma sugestão encontrada.")
        else:
            await ctx.send("❌ Você não tem permissão para revisar sugestões.")

def setup(bot):
    bot.add_cog(Editor(bot))