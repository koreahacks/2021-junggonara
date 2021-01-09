import discord
from discord.ext import commands

import asyncio
from utils import VoiceController

bot = commands.Bot(command_prefix='!')
channel_ids = []
users = {}

game_state = "WAIT_GAME"


@bot.event
async def on_ready():
    activity = discord.Activity(name=".help", type=discord.ActivityType.playing)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print('start')


@bot.command()
async def test(ctx: commands.Context, *args):
    print(ctx.author)
    await VoiceController.set_speaker(ctx.author, True)

@bot.command()
async def 게임목록(ctx):
    em = discord.Embed(title='게임 목록', description='폭탄')
    for user in bot.get_all_channels():
        await ctx.send(user)


bot.run('Nzk2NzI1OTQ4MDMxOTU5MDcy.X_cG3A.PS1RgrMgwqGWjRrehgrkY-mP86w')
