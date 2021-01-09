import discord
import asyncio
from discord.ext import commands
import random

from utils import GameManager


async def thegameofdeath(message, bot):
    gm = GameManager.GameManager.instance()

    starter = str(message.author.name)
    embed = discord.Embed(title="더게임오브데스 시작", description=f"모든 참가자가 참여합니다")
    embed.set_footer(text="모든 멤버들은 다른 멤버 이름을 말해주세요! 중간에는 이름 수정 가능합니다.스타터분이 맨 처음 입력해주세요:)")
    await message.channel.send(embed=embed)

    gm.users.append([])
    gm.users.append({})

    gm.users[0].append(message.author.voice.channel.members)

    while True:
        try:
            bot.wait_for(timeout=0.5)
        except asyncio.TimeoutError:
            if len(gm.users[0]) == len(gm.users[1]):
                break

    await message.channel.send("모든 사람이 지목했습니다!")
    await message.channel.send("Starter는"+starter+"입니다.")
    await message.channel.send(gm.users[1])
    await message.channel.send("Starter분은 반복할 횟수를 입력해주세요!")

    while True:
        try:
            bot.wait_for(timeout=0.5)
        except asyncio.TimeoutError:
            if len(gm.users) == 3:
                break

    print(gm.users[2])
    jimok = starter
    for i in range(gm.users[2]):
        await message.channel.send(f"{jimok} -> {gm.users[1].get(jimok)}")
        try:
            await bot.wait_for('대기', timeout=1.0)
        except asyncio.TimeoutError:
            jimok = gm.users[1].get(jimok)
            i = i + 1
    await message.channel.send(f"걸린 사람은 {jimok}입니다! 마시세요")

    gm.set_game_over(message)

