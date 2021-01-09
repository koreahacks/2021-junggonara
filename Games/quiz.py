import discord
import asyncio
from discord.ext import commands
import random

from utils import GameManager


async def quiz(message, bot):
    gm = GameManager.GameManager.instance()

    playerlist = []
    munjangfile = open('hancome.txt', 'r', encoding='utf8')  # 문장 데이터 불러오기
    munjanglist = []
    while True:
        i = munjangfile.readline()
        if not i:
            break
        munjanglist.append(i[0:-2])  # 데이터 문자열로 저장
    munjangfile.close()
    munjang = random.choice(munjanglist)  # 랜덤뽑기

    embed = discord.Embed(title="한컴타자연습 시작", description=f"5초 후에 문장이 공개됩니다")
    await message.channel.send(embed=embed)
    try:
        await bot.wait_for('대기', timeout=5.0)
    except asyncio.TimeoutError:
        embed2 = discord.Embed(title=munjang, description=f'위의 문장을 토씨 하나 틀리지 않고 정확히 입력해주세요!')
        await message.channel.send(embed=embed2)

    while len(gm.users) < 3:
        try:
            await bot.wait_for('', timeout=0.2)
        except asyncio.TimeoutError:
            if gm.answer == munjang:
                gm.answer = ""
                gm.users.append(gm.next_user)
                await message.channel.send("{0} 정답!".format(str(message.author.name)))
                playerlist.append(str(message.author.name))

    print(playerlist)
    count1 = 0
    embed3 = discord.Embed(title='최종 순위')
    for a in playerlist:
        count1 += 1
        embed3.add_field(name='{0}등'.format(count1), value=a, inline=False)

    await message.channel.send(embed=embed3)

    await gm.set_game_over(message)


async def nunsence(message, bot):
    gm = GameManager.GameManager.instance()

    quizfile = open('nunsense.txt', 'r', encoding='utf8')  # 문장 데이터 불러오기
    quizlist = []
    while True:
        i = quizfile.readline()
        if not i:
            break
        quizlist.append(i)
    quizfile.close()
    wait = random.choice(quizlist)  # 랜덤뽑기
    quiz = wait.split(':')
    quiz[1] = quiz[1][0:-1]
    print('go!')

    embed = discord.Embed(title="넌센스퀴즈 시작", description="5초 후에 퀴즈가 공개됩니다")
    await message.channel.send(embed=embed)
    try:
        await bot.wait_for('대기', timeout=5.0)
    except asyncio.TimeoutError:
        embed2 = discord.Embed(title=quiz[0], description='정답은..?')
        await message.channel.send(embed=embed2)

    while True:
        try:
            await bot.wait_for('', timeout=0.2)
        except asyncio.TimeoutError:
            if gm.answer == quiz[1]:
                await message.channel.send("{0} 정답!".format(str(message.author.name)))
                break

    await gm.set_game_over(message)
