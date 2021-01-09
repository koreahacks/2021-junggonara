import discord
import asyncio
from discord.ext import commands


client = commands.Bot(command_prefix="/")

@client.event
async def on_ready():
    global GAME
    global rankinglist
    global i
    i=1
    GAME = "게임 종료"
    rankinglist=[]
@client.event
async def on_message(message):
    global i
    global GAME
    global check
    global LIST

    if message.content.startswith('/눈치게임'):
        embed = discord.Embed(title="눈치게임",description=f"2초 후에 시작합니다.")
        embed.set_footer(text="반드시 숫자앞에 !를 붙여주세요 ex)!1")
        await message.channel.send(embed=embed)

        try:
            await client.wait_for('대기',timeout=2.0)
        except asyncio.TimeoutError:
            await message.channel.send("눈치게임")
            await message.channel.send("시작!")
            GAME='게임 시작'
    if GAME == '게임 시작':
        if message.content == "!"+str(i):
            print(1)
            rankinglist.append(str(message.author.name))
            i+=1
        elif str(message.content)[1:].isdigit()==True:
            msg=int(str(message.content)[1:])
            print(msg)
            if msg<i:
                await message.channel.send(f"{rankinglist[msg-1]}님과 {message.author.name}님이 걸렸습니다.")
                GAME ='게임 종료'

        if i==4:
            for l in LIST:
                check=0
                for r in rankinglist:
                    if str(l)==str(r):
                        check=1
                if check==0:
                    await message.channel.send(f"{l}님이 걸렸습니다.")
                    GAME = '게임 종료'