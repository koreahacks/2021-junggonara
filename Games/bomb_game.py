import discord
import asyncio
from discord.ext import commands
import random
import time


client = commands.Bot(command_prefix="/")


@client.event
async def on_ready():
    global GAME
    global time_count
    global count
    time_count = 0
    count = 0
    global playerlist
    GAME = '게임 종료'
    print('start')


@client.event
async def on_message(message):
    global time_count
    global start_time
    global GAME
    global random_time
    global quiz
    global GAME
    global i
    global LIST
    global count
    LIST = ['형욱', '주영', '연준', '혁준','수현']
    list_length = len(LIST)


    if message.content.startswith('/폭탄게임'):
        GAME = '게임 시작'
        i = 0
        random.shuffle(LIST)
        embed = discord.Embed(title="폭탄게임 시작", description="제한시간은 30초 이상 5분 미만입니다!\n5초 후에 시작합니다!")
        await message.channel.send(embed=embed)
        try:
            await client.wait_for('대기', timeout=5.0)
        except asyncio.TimeoutError:
            start_time = time.time()
            random_time = random.randint(5, 10)
            embed2 = discord.Embed(title='시작!!', description=f'{LIST[i]}이 {LIST[i+1]}에게 질문!')
            await message.channel.send(embed=embed2)

    if (time.time() - start_time) > random_time and GAME == '게임 시작':
        try:
            await client.wait_for('대기', timeout=5.0)
        except asyncio.TimeoutError:
            embed4 = discord.Embed(title="끝!!", description=f"{LIST[i]}당첨!!")
            await message.channel.send(embed=embed4)
            GAME = '게임 종료'



    if message.content.startswith('다음') and GAME == '게임 시작':
        i += 1
        embed3 = discord.Embed(title='다음사람!!', description=f'{LIST[i]}이 {LIST[i+1]}에게 질문!')
        await message.channel.send(embed=embed3)



client.run('Nzk3Mjg0NDI4Mjc4OTIzMjk1.X_kO_A.8ycQ53fCfDZOxgDPk3OtG2tSOp0')