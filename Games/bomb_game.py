import discord
import asyncio
from discord.ext import commands
import random
import time


client = commands.Bot(command_prefix="/")


@client.event
async def on_ready():
    global GAME
    global count
    global LIST
    global random_time
    global start_time
    start_time = time.time()
    random_time = 1000000000
    count = 0
    LIST = ['형욱', '주영', '연준', '혁준', '수현']
    GAME = '게임 종료'
    print('start')


@client.event
async def on_message(message):
    global start_time
    global GAME
    global random_time
    global count
    global LIST

    list_length = len(LIST)


    if message.content.startswith('/폭탄게임'):
        GAME = '게임 시작'
        count = 0
        random.shuffle(LIST)
        embed = discord.Embed(title="폭탄게임 시작", description="제한시간은 30초 이상 5분 미만입니다!\n5초 후에 시작합니다!")
        await message.channel.send(embed=embed)
        try:
            await client.wait_for('대기', timeout=5.0)
        except asyncio.TimeoutError:
            start_time = time.time()
            random_time = random.randint(10, 20)
            embed2 = discord.Embed(title='시작!!', description=f'{LIST[count]}이 {LIST[count+1]}에게 질문!')
            await message.channel.send(embed=embed2)

    if (time.time() - start_time) > random_time and GAME == '게임 시작':
        try:
            await client.wait_for('대기', timeout=0.3)
        except asyncio.TimeoutError:
            embed4 = discord.Embed(title="끝!!", description=f"{LIST[count]}당첨!!")
            await message.channel.send(embed=embed4)
            GAME = '게임 종료'

    if message.content.startswith('다음') and GAME == '게임 시작':
        count += 1
        if count == list_length-1:
            embed4 = discord.Embed(title='다음사람!!', description=f'{LIST[count]}이 {LIST[0]}에게 질문!')
            await message.channel.send(embed=embed4)
            count = 0
        else:
            embed3 = discord.Embed(title='다음사람!!', description=f'{LIST[count]}이 {LIST[count + 1]}에게 질문!')
            await message.channel.send(embed=embed3)




client.run('Nzk3Mjg0NDI4Mjc4OTIzMjk1.X_kO_A.Dyqixtva4EfscswOtctHshsdnWc')