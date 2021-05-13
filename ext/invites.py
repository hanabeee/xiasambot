
# Cog by: Quill (quillfires).
# i'm to tired to rewrite everything from scratch, lol

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


import discord
from discord import invite
from discord import message
from discord.ext import commands
import datetime

class InviteTracker(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.channel_id = 0 # enter your channel id
        self.invites = {}
        current_date = datetime.date.today()
        current_year = current_date.year
        self.date = f"2021-{current_year}" if current_year != 2021 else "2021"

        #self.load_invites()
        self.bot.loop.create_task(self.load_invites())

    def find_invite_by_code(self, inv: list=None, code: str=None):
        for i in inv:
            if i.code == code:
                return i

    async def get_user_invites(self, ctx, user):
        totalInvites = 0
        for i in await ctx.guild.invites():
            if i.inviter == user:
                totalInvites += i.uses

        return totalInvites


    async def load_invites(self):
        # wait until the bot to be ready to avoid some errors
        await self.bot.wait_until_ready()
    
        for guild in self.bot.guilds:
            try:
                self.invites[guild.id] = await guild.invites()

            except Exception:
                pass
    
    @commands.Cog.listener()
    async def on_member_join(self, member):

        print("Joined")
        logs = self.bot.get_channel(self.channel_id)
        eme = discord.Embed(description="Just joined the server", color=0x03d692)
        eme.set_author(name=str(member), icon_url=member.avatar_url)
        eme.set_footer(text=f"Zodiacs Gaming © {self.date}.")
        eme.timestamp = member.joined_at

        try:
            invs_before = self.invites[member.guild.id]
            invs_after = await member.guild.invites()
            self.invites[member.guild.id] = invs_after
            for invite in invs_before:
                if invite.uses < self.find_invite_by_code(invs_after, invite.code).uses:
                    eme.add_field(name="Inviter Information",
                                  value=f"Inviter: {invite.inviter.mention}\nTotal Invites by {invite.inviter.mention}: **{await self.get_user_invites(member, invite.inviter)}**", inline=False)
        except:
            pass
        await logs.send(embed=eme)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        
        
        logs = self.bot.get_channel(self.channel_id)
        eme = discord.Embed(description="Just left the server", color=0xff0000, title=" ")
        eme.set_author(name=str(member), icon_url=member.avatar_url)
        eme.set_footer(text=f"Zodiacs Gaming © {self.date}.")
        eme.timestamp = member.joined_at
        try:
            invs_before = self.invites[member.guild.id]
            invs_after = await member.guild.invites()
            self.invites[member.guild.id] = invs_after
            for invite in invs_before:
                if invite.uses > self.find_invite_by_code(invs_after, invite.code).uses:
                    eme.add_field(name="Inviter Information",
                                  value=f"Inviter: {invite.inviter.mention}\nTotal Invites by {invite.inviter.mention}: **{await self.get_user_invites(member, invite.inviter)}**", inline=False)
        except:
            pass
        await logs.send(embed=eme)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        try:
            self.invites[guild.id] = await guild.invites()
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        try:
            self.invites.pop(guild.id)
        except:
            pass

def setup(bot):
    bot.add_cog(InviteTracker(bot))
