

import discord
from discord import message
from discord.ext import commands
from discord.ext.commands import bot
from discord.ext.commands.core import command
from .lib.utils import *
from .lib.database import Database

class AfkCommand(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.database = Database()
        self.emb = Embed()

    @commands.command()
    async def afk(self, ctx, *, msg: str=None):
        if msg == None:
            await ctx.send(embed=self.emb.create_embed(message="Specify your afk reson / message"))
        
        else:
            try:
                self.database.afk_collection.insert_one({"_id": f"{ctx.author.id}", "status": f"{msg}"})
            except Exception:
                self.database.afk_collection.update_one({"_id": f"{ctx.author.id}"}, {"$set": { "status": f"{msg}"}})
            await ctx.send(embed=self.emb.create_embed(message="Your status is now set to afk: **{}**".format(msg)), delete_after=10.0)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        result = self.database.afk_collection.find_one({"_id": f"{message.author.id}"})

        if message.author == self.bot.user:
            return
            
        #if message.channel.is_private:
        #    return

        if message.mentions:
            if result:
                if message.mentions[0].id == int(result["_id"]):
                    await message.channel.send(embed=self.emb.create_afk_embed(message.author.mention, message.author.avatar_url, result['status']), delete_after=15.0)

        #print(message.content)
        if message.content:
            if result:
               if message.author.id == int(result["_id"]):
                    self.database.afk_collection.delete_one(result)
                    await message.channel.send(embed=self.emb.create_embed(message="<:dot_1:841856785291804733> Welcome back {}, Your afk status is now removed".format(message.author.mention)), delete_after=10.0)

        


def setup(bot):
    bot.add_cog(AfkCommand(bot))
