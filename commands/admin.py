from discord.ext import commands
import os

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def reiniciar(self, ctx):
        if ctx.author.guild_permissions.administrator:
            await ctx.send("♻️ Reiniciando o bot...")
            os._exit(0)
        else:
            await ctx.send("❌ Você não tem permissão para isso.")

def setup(bot):
    bot.add_cog(Admin(bot))