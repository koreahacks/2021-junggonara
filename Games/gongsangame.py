import discord
import asyncio
from discord.ext import commands
import random

from utils import GameManager


gm = GameManager.GameManager.instance()

async def gongsan(message, bot):
    alcohol = ['반잔😀','한잔😋', '한잔 반😮😮', '두잔...😢😢', '세잔...?😱😱😱', '네잔🤮😵🤪🤢😇']
    LIST = gm.users

    you_drink = random.choice(LIST)
    embed = discord.Embed(title="공산당 게임 시작", description="봇 맘대로 정하는 벌칙자!\n5초 후에 발표합니다!")
    await message.channel.send(embed=embed)
    try:
        await bot.wait_for('대기', timeout=5.0)
    except asyncio.TimeoutError:
        embed2 = discord.Embed(title=f'{you_drink} 너 마셔 ^^', description='{0}'.format(random.choices(alcohol, weights=[50,40,30,20,5,1], k=1)))
        await message.channel.send(embed=embed2)

    gm.set_game_over(message)

