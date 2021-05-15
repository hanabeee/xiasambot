

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


    def convert_seconds_to_min(self, seconds):
        pass

    def convert_mins_to_h(self, minutes):
        pass

    def convert_h_to_day(self, minutes):
        pass

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

        if message.author == self.bot.user:
            return

        if message.mentions:
            
            # I just moved the result here because you were looking for the author's message id
            # not the mentioned id. 
            # - hanabeee

            result = self.database.afk_collection.find_one({"_id": f"{message.mentions[0].id}"})
            if result:
                if message.mentions[0].id == int(result["_id"]):
                    await message.channel.send(embed=self.emb.create_afk_embed(message.mentions[0].mention, message.mentions[0].avatar_url, result['status']), delete_after=15.0)


    # This event used to check if the afk user is back then removed it.
    # - hanabeee
    
    @commands.Cog.listener()
    async def on_typing(self, channel, user, when):
        result = self.database.afk_collection.find_one({"_id": f"{user.id}"})

        if result:
            if user.id == int(result['_id']):
                try:
                    self.database.afk_collection.delete_one({"_id": f"{user.id}"})
                except:
                    return
                
                await channel.send(embed=self.emb.create_embed(message="<:dot_1:841856785291804733> Welcome back {}! Your status **AFK** is now removed".format(user.mention)))


def setup(bot):
    bot.add_cog(AfkCommand(bot))
