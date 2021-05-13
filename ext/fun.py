
# All fun command here. 
# WARNING: MESSY CODE!
# (c) 2021, Zenqi. All rights reserved

import discord
from discord import embeds
from discord.ext import commands
from .lib.utils import *
from .lib.database import Database
from PIL import Image, ImageFilter, ImageDraw
import requests


class ImageFun(commands.Cog):

    """
    A fun command that handles all image processing commands.

    Summary of commands:
        !wanter <user>      - send wanted poster of a specific person
        !slap   <user>      - send a picture of slapped user.
        !cat                - send random cat image.
        !dog                - send random dog image.
        !tweet <text>       - send a picture of tweeted tet.

    """

    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.emb = Embed()
        self.database = Database()


    @commands.command(name='cat')
    async def cat(self, ctx):
        pass

    @commands.command(name="dog")
    async def dog(self, ctx):
        pass

    @commands.command(name="wanted")
    async def wanted(self, ctx, user: discord.User=None):
        if user == None:
            user = ctx.author
    
    @commands.command()
    async def avatar(self, ctx, user: discord.User=None):
        if user == None:
            user = ctx.author
        

        await ctx.send(embed=self.emb.create_avatar_embed(user=user.mention, avatar=user.avatar_url))


def setup(bot):
    bot.add_cog(ImageFun(bot))

