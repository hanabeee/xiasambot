

from discord.ext import commands
import discord
from .lib.utils import *

class Status(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.bot.loop.create_task(self.get_user_activity())


    async def get_user_activity(self):
        print(self.bot.guilds)
        for guild in self.bot.guilds:
            for member in guild.members:
                print(len(member))
                if str(member.activity) == "hello":
                    print("Zenqi")

    # @commands.command(name='status')
    # async def status(self, ctx, member: discord.Member):
    #     await ctx.send(str(member.activity))



def setup(bot):
    bot.add_cog(Status(bot))
