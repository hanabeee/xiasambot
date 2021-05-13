

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


from discord.ext import commands
import discord
import json
import os
import asyncio as asyncio

try:

    with open("config.json", "r") as f:
        data = json.load(f)

except FileNotFoundError:
    print("config.json is missing")


intents = discord.Intents.default()

if data['debug']['is_debug']:
    bot = commands.Bot(command_prefix=data['debug']['debug_prefix'], intents=intents)
else:
    bot = commands.Bot(command_prefix="{}".format(data["prefix"]), intents=intents)


bot.remove_command("help")

def get_cogs(bot):
    try:
        print("cogs found")
        for filename in os.listdir("./ext"):
            if filename.endswith(".py"):
                bot.load_extension(f"ext.%s"%(filename[:-3]))
            else:
                print("unable to load %s"%(filename[:-3]))
    except FileNotFoundError:
        print("cogs not found")

@bot.event
async def on_ready():

    print("Discord Bot template by discli")
    print("-"*50)
    print("Logged in as: %s" %(bot.user.name)) 

    serverlist = []
    for server in bot.guilds:
        serverlist.append(server.name)

    # set the presence of the bot

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="%s servers"%(len(serverlist))))


print("-"*50)
print("Loading Cogs")
get_cogs(bot)


if data['debug']['is_debug']:
    bot.run(data['debug']['debug_token'])

# print("Running Debug mode")
# bot.run("{}".format(data['debug']['debug_token']))
else:
    bot.run("{}".format(data["token"]))
