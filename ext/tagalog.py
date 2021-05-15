

from .lib.utils import *
from discord.ext import commands
from .lib.database import Database
import langdetect

class TagalogDetection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = Database()
        self.emb = Embed()
        self.database.afk_collection.creat
        super().__init__()


    @commands.command(name="englishonly")
    @commands.has_permissions(manage_messages = True)
    #@commands.is_owner()
    async def englishonly(self, ctx):
      
        self.database.afk_collection.update({"_id": "english_speaking_event"}, {"$set": {"english_only": True}})
        #self.database.afk_collection.update({"_id": "english_speaking_event"}, {"$set": {"english_only": False}})
        await ctx.send(embed=self.emb.create_embed(message="English Speaking Policy is now set."))

    @englishonly.error
    async def englishonly_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(embed=self.emb.create_error(message="You don't have enough permission to do that, how sad."))


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        try:
            language = langdetect.detect(message.content)
        except langdetect.LangDetectException:
            language = ""
        
        if language == 'tl':
            result = self.database.events.find_one({"_id": "english_speaking_event"})

            print(result['english_only'])
            print("Tagalog word detected: {} from {}".format(message.content, message.author.name))
            
            if result['english_only']:
                await message.channel.send("{} tagalog is not allowed".format(message.author.mention), delete_after=3.0)
            else:
                pass

            



def setup(bot):
    bot.add_cog(TagalogDetection(bot))