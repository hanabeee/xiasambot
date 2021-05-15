
# All fun command here. 
# WARNING: MESSY CODE!
# (c) 2021, Zenqi. All rights reserved

import discord
from discord import embeds
from discord.ext import commands
from discord.ext.commands.core import command, is_nsfw
from .lib.utils import *
from .lib.database import Database
from PIL import Image, ImageFilter, ImageDraw
from io import BytesIO
import requests
import json

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


    def check_if_nsfw(self, dict: dict) -> bool:
        return dict['memes'][0]['nsfw']

    @commands.command(name='cat')
    async def cat(self, ctx):
        pass

    @commands.command(name="dog")
    async def dog(self, ctx):
        pass

    @commands.command(name="wanted")
    async def wanted(self, ctx, user: discord.Member=None):
        if user == None:
            user = ctx.author
    
    @commands.command(name="slap")
    async def slap(self, ctx, user: discord.Member=None):
        if user == None:
            user = ctx.author
        
        img = Image.open("ext/img/slap.png")
        pos = (110, 227)
        avatar = Image.open(BytesIO(await user.avatar_url_as(size=128).read()))

        img_bin = BytesIO()
        img.paste(avatar, (pos))
        img.save(img_bin, "PNG")
        img_bin.seek(0)

        file = discord.File(img_bin, filename="image.png")
        author = ctx.author.mention if user != ctx.author else "himself"

        await ctx.send(file=file, embed=self.emb.create_fun_image(user=user.mention, author=author, image="image.png"))
       

    @commands.command()
    async def avatar(self, ctx, user: discord.User=None):
        if user == None:
            user = ctx.author
        

        await ctx.send(embed=self.emb.create_avatar_embed(user=user.mention, avatar=user.avatar_url))

    @commands.command()
    async def meme(self, ctx):
        def generate_meme(url) -> dict:
            try:
                result = requests.get(url).json()
                
                _ = self.check_if_nsfw(result)

                if _:
                    return generate_meme(url)
                else:
                    return result

            except Exception as e:
                raise e

        meme = generate_meme("https://meme-api.herokuapp.com/gimme/1")
        
        title = meme['memes'][0]['title']
        author = meme['memes'][0]['author']
        url    = meme['memes'][0]['url']

        await ctx.send(embed=self.emb.create_meme_embed(title, author, url))

    @commands.command()
    async def distort(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author
        
        avatar = Image.open(BytesIO(await user.avatar_url.read()))
        img = Image.open(avatar)


def setup(bot):
    bot.add_cog(ImageFun(bot))

