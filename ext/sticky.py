#                    Copyright (c) 2021 Zenqi.
#                 This project was created by Discord CLI
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from asyncio.runners import run
from operator import mod
import discord
import asyncio

from discord import message
from .lib.database import Database
from .lib.utils import *
from discord.ext import commands
from asyncio import run_coroutine_threadsafe


class XiasmBot(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.database = Database()
        self.emb = Embed()


    def add_sticky(self, channel, message, author, mode):
        if self.database.sticky_collection.find_one({"_id": f"{channel}"}):
            raise Exception

        return self.database.add_sticky_data({"_id": f"{channel}", "message": message, "author": author, "mode": mode})

    def edit_message(self, query: dict, message: dict):
        return self.database.sticky_collection.find_one_and_replace(query, message)

    def remove_message(self, query: dict):
        
        if self.database.sticky_collection.find_one(query):
            return self.database.sticky_collection.delete_one(query)
        else:
            raise Exception

    @commands.command(name="sticky")
    @commands.has_permissions(manage_messages=True)
    async def sticky(self, ctx, channel: discord.TextChannel, mode: str=None, *, message=None):
        
        if mode == None:
            await ctx.send(embed=self.emb.create_embed(message="Please specify mode. `(embed)` or `(text)`"), delete_after=3.0)
        
        if channel == None:
            await ctx.send(embed=self.emb.create_embed(message="Please specify `channel`"), delete_after=3.0)
    
        if message == None:
            await ctx.send(embed=self.emb.create_embed(message="Please specify `message`"), delete_after=3.0)

        if isinstance(message, str):
            if mode == "embed":
                try:
                    sticky = self.add_sticky(channel.id, message, ctx.message.author.mention, mode)
                    await self.send_sticky(channel.id, ctx.message.author.mention, message, mode)
                    await ctx.send(embed=self.emb.create_embed(message="Sticky Reminder successfully created {}".format(channel.mention)), delete_after=3.0)
                except Exception:
                    await ctx.send(embed=self.emb.create_embed(message="{} already has a sticky message. Skipping..".format(channel.mention)), delete_after=3.0)
                
                
            elif mode == "text":
                try:
                    self.add_sticky(channel.id, message, ctx.message.author.mention, mode)
                    await self.send_sticky(channel.id, ctx.message.author.mention, message, mode)
                    await ctx.send(embed=self.emb.create_embed(message="Sticky Reminder successfully created {}".format(channel.mention)), delete_after=3.0)
                except Exception:
                    await ctx.send(embed=self.emb.create_embed(message="{} already has a sticky message. Skipping..".format(channel.mention)), delete_after=3.0)

        

    @commands.command(name='unsticky')
    @commands.has_permissions(manage_messages=True)
    async def unsticky(self, ctx, channel: discord.TextChannel):
        if channel.id != None:
            try:
                remove = self.remove_message({"_id": f"{channel.id}"})
                await ctx.send(embed=self.emb.create_embed(message="Successfully removed sticky message from {}. You can now remove the bot's message manually".format(channel.mention)), delete_after=5.0)
            except Exception:
                await ctx.send(embed=self.emb.create_embed(message="{} has no sticky message. Skipping..".format(channel.mention)), delete_after=5.0)
            

        else:
            await ctx.send(embed=self.emb.create_embed(message="Please specify channel"))


    async def send_sticky(self, channelID, author, content, mode):
        if isinstance(channelID, str):
            channelID = int(channelID)
        
        channel = self.bot.get_channel(channelID)
        
        if mode == "embed":
            return await channel.send(embed=self.emb.create_sticky_embed(author, content))

        elif mode == "text":
            return await channel.send("**Sticky Reminder** from {}\n\n> {}".format(author, content))



    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return


        def is_bot(m):
            return m.author == self.bot.user

        channels_ = self.database.sticky_collection.find({})

        for channel in channels_:
            

            if str(message.channel.id) == str(channel["_id"]):
                if message.content:
                    await message.channel.purge(limit=3, check=is_bot)
                    await self.send_sticky(message.channel.id, channel['author'], channel['message'], channel['mode'])
            

    @sticky.error
    async def sticky_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You need `Manage Message` Permission in order todo that.")
    

def setup(bot):
    bot.add_cog(XiasmBot(bot))
