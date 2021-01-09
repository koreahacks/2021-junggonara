import discord
import asyncio
from discord.ext import commands
import random
import time


client = commands.Bot(command_prefix="/")

@client.event
async def on_ready():
    global LIST
    global GAME
    global alcohol
    alcohol = ['반잔😀','한잔😋', '한잔 반😮😮', '두잔...😢😢', '세잔...?😱😱😱', '네잔🤮😵🤪🤢😇']
    LIST = ['형욱', '주영', '연준', '혁준', '수현']
    GAME = '게임 종료'
    print('start')

@client.event
async def on_message(message):
    global GAME
    global LIST
    global alcohol

    if message.content.startswith('/공산당 게임'):
        GAME = '게임 시작'
        you_drink = random.choice(LIST)
        embed = discord.Embed(title="공산당 게임 시작", description="봇 맘대로 정하는 벌칙자!\n5초 후에 발표합니다!")
        await message.channel.send(embed=embed)
        try:
            await client.wait_for('대기', timeout=5.0)
        except asyncio.TimeoutError:
            embed2 = discord.Embed(title=f'{you_drink} 너 마셔 ^^', description='{0}'.format(random.choices(alcohol, weights=[50,40,30,20,5,1], k=1)))
            await message.channel.send(embed=embed2)
            GAME = '게임 종료'

client.run('Nzk3Mjg0NDI4Mjc4OTIzMjk1.X_kO_A.Dyqixtva4EfscswOtctHshsdnWc')