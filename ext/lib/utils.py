

import discord
import datetime


HELP_COMMAND = """
**General Commands**

> `x!sticky <channel> <mode> <message>`: **Send sticky reminder on specific channel.**
> `x!unsticky <channel>`: **Unsticky sticky reminder from specific channel.**
> `x!afk <reason>`: **Set your status to afk with reason.**
> `x!avatar <user>`: **Get user avatar**

**Fun Commands**

> soon
"""


class Embed:
    """
    Main class for handling embeds. To avoid messy codes
    """
    current_date = datetime.date.today()
    current_year = current_date.year

    date = f"2021-{current_year}" if current_year != 2021 else "2021"

    def create_sticky_embed(self, author, message: str=None) -> discord.Embed:
        
        current_date = datetime.date.today()
        current_year = current_date.year

        date = f"2021-{current_year}" if current_year != 2021 else "2021"
        
        
        embed = discord.Embed(
            description="**Sticky Reminder** from {}\n\n> <:dot_0:841856719974039572> **{}** ".format(author, message),
            color=0xb85e19
        )
        embed.set_footer(text=f"Zodiacs Gaming © {date}. All rights reserved ")
        
        return embed


    def create_help_embed(self) -> discord.Embed:
        embed = discord.Embed(
            description=HELP_COMMAND,
            color=0xb85e19
        )
        embed.set_footer(text=f"Zodiacs Gaming © {self.date}. All rights reserved ")

        return embed

    def create_afk_embed(self, user, avatar_url, status) -> discord.Embed:
        embed = discord.Embed(
            description=f"**{user}'s Status**\n\n<:dot_0:841856719974039572> This user is currently AFK.\n\n> ❝ {status} ❞\n",
            color=0xb85e19
        )
        embed.set_thumbnail(url=avatar_url)
        embed.set_footer(text=f"Zodiacs Gaming © {self.date}. All rights reserved ")

        return embed

    def create_avatar_embed(self, user, avatar) -> discord.Embed:
        embed = discord.Embed(
            description="**{}**'s avatar".format(user),
            color=0xb85e19
        )
        embed.set_image(url=avatar)
        embed.set_footer(text=f"Zodiacs Gaming © {self.date}. All rights reserved ")

        return embed

    def create_embed(self,title: str=None, message: str=None) -> discord.Embed:

        
        embed = discord.Embed(
            description=f"> {message}",
            color=0xb85e19
        )
        
        if title != None:
            embed.title = title

        embed.set_footer(text=f"Zodiacs Gaming © {self.date}. All rights reserved ")
        
        return embed


    
