import discord
import asyncio
from discord.ext import commands
import random

client = commands.Bot(command_prefix="/")


@client.event
async def on_ready():
    global GAME
    global munjang
    global count
    global playerlist
    playerlist = []
    count = 0
    GAME = "게임 종료"
    print("already")


#참가자 리스트가 있다는 가정 하에
@client.event
async def on_message(message):
    global count, name_list
    global munjang
    global GAME
    global count
    global LIST_COUNT
    global starter
    global final_list
    global banbok
    if message.content.startswith("/더게임오브데스"):
        starter = str(message.author.name)
        GAME = '게임 시작'
        embed = discord.Embed(title="더게임오브데스 시작", description=f"모든 참가자가 참여합니다")
        await message.channel.send(embed=embed)
        try:
            await client.wait_for('대기', timeout=5.0)
        except asyncio.TimeoutError:
            embed2 = discord.Embed(title="더게임오브데스 시작", description=f'모든 멤버들은 다른 멤버 이름을 말해주세요! 중간에는 이름 수정 가능합니다.스타터분이 맨 처음 입력해주세요:)')
            await message.channel.send(embed=embed2)
        name_list = {starter:starter}
    i=0
    while i<2:
        if message.author.bot:
            return None
        else:
            name_list[str(message.author.name)] = str(message.content)
            i=i+1
    print(name_list)
    print(len(name_list))
    print(starter)
    if len(name_list) == 2: #이 부분은 나중에 수현이가 멤버 수 받으면 그 변수로 가능.
        await message.channel.send("모든 사람이 지목했습니다!")
        await message.channel.send("Starter는"+starter+"입니다.")
        await message.channel.send(name_list)
        await message.channel.send("Starter분은 반복할 횟수를 입력해주세요!")
        banbok = int(message.content)
        print(banbok)






client.run("Nzk3Mzk5MzMzMzYwMTA3NTMw.X_l6AA.iYfVDgE6jVMUdfWmK5okny063jg")