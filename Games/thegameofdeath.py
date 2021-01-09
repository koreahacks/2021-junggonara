import discord
import asyncio
from discord.ext import commands
import random

from utils import GameManager

gm = GameManager.GameManager.instance()

async def thegameofdeath(message, bot):
    starter = str(message.author.name)
    embed = discord.Embed(title="더게임오브데스 시작", description=f"모든 참가자가 참여합니다")
    embed.set_footer(text="모든 멤버들은 다른 멤버 이름을 말해주세요! 중간에는 이름 수정 가능합니다.스타터분이 맨 처음 입력해주세요:)")
    await message.channel.send(embed=embed)

    gm.users.append([])
    gm.users.append({})

    gm.users[0].append(message.author.voice.channel.members)

    users = {starter: starter}
    CHOOSE = '지목 시작'
    if CHOOSE =='지목 시작':
        gm.users[str(message.author.name)] = str(message.content)

        print(users)
        print(len(users))
        print(starter)
        print(len(message.author.voice.channel.members))
        if len(users) == len(message.author.voice.channel.members): #이 부분은 나중에 수현이가 멤버 수 받으면 그 변수로 가능.
            await message.channel.send("모든 사람이 지목했습니다!")
            await message.channel.send("Starter는"+starter+"입니다.")
            await message.channel.send(users)
            await message.channel.send("Starter분은 반복할 횟수를 입력해주세요!")
            CHOOSE = '지목 종료'
    elif CHOOSE == '지목 종료':
        cnt = int(message.content)
        print(cnt)
        jimok = starter
        for i in range(cnt):
            await message.channel.send(f"{jimok} -> {users.get(jimok)}")
            try:
                await bot.wait_for('대기', timeout=1.0)
            except asyncio.TimeoutError:
                jimok = users.get(jimok)
                jimok = users.get(jimok)
                i = i + 1
        await message.channel.send(f"걸린 사람은 {jimok}입니다! 마시세요")

