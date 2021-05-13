
import discord
from discord.ext import commands
from.lib.utils import *

class Help(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.emb = Embed()

    @commands.command()
    async def help(self, ctx):
        await ctx.send(embed=self.emb.create_help_embed())

def setup(bot):
    bot.add_cog(Help(bot))
