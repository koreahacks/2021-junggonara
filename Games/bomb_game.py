import discord
import asyncio
from discord.ext import commands
import random
import time

from utils import GameManager


async def bomb_game(message, bot):
    start_time = time.time()
    random_time = 0
    gm = GameManager.GameManager.instance()

    LIST = gm.users

    list_length = len(LIST)

    count = 0
    random.shuffle(LIST)
    gm.users = LIST
    gm.count = count
    embed = discord.Embed(title="폭탄게임 시작", description="제한시간은 30초 이상 5분 미만입니다!\n5초 후에 시작합니다!")
    await message.channel.send(embed=embed)

    try:
        await bot.wait_for('대기', timeout=5.0)
    except asyncio.TimeoutError:
        start_time = time.time()
        random_time = random.randint(10, 20)
        embed2 = discord.Embed(title='시작!!', description=f'{(LIST[count]).name}이 {(LIST[count+1]).name}에게 질문!')
        await message.channel.send(embed=embed2)

    while (time.time() - start_time) <= random_time:
        if gm.answer.startswith('다음'):
            count += 1
            gm.count += 1
            if count == list_length - 1:
                embed4 = discord.Embed(title='다음사람!!', description=f'{(LIST[count]).name}이 {(LIST[0]).name}에게 질문!')
                await message.channel.send(embed=embed4)
                count = 0
                gm.count = 0
            else:
                embed3 = discord.Embed(title='다음사람!!', description=f'{(LIST[count]).name}이 {(LIST[count + 1]).name}에게 질문!')
                await message.channel.send(embed=embed3)

    try:
        await bot.wait_for('대기', timeout=0.3)
    except asyncio.TimeoutError:
        embed4 = discord.Embed(title="끝!!", description=f"{LIST[count]}당첨!!")
        await message.channel.send(embed=embed4)
        await gm.set_game_over(message)




