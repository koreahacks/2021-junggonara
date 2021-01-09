import discord
import asyncio
from discord.ext import commands
from random import randrange

client = commands.Bot(command_prefix="/")

@client.event
async def on_ready():
    global GAME
    GAME = "게임 종료"
    print("is ready")

@client.command()
async def 음악퀴즈(ctx):
    global GAME
    global LIST
    global LIST_COUNT
    global next_flag
    maxMem=0
    max=0

    if GAME == "게임 종료":
        GAME = "게임 시작"
        LIST = []
        LIST.append(ctx.author.id)
        LIST_COUNT = 1

        embed = discord.Embed(title="음악퀴즈 시작", description=f"이모지를 눌러주세요!\n30초 후에 음악퀴즈가 시작합니다!")
        embed.set_footer(text="명령어를 호출한 사용자는 이미 등록되었습니다")
        emoji = await ctx.send(embed=embed)
        await emoji.add_reaction('🔌')

        try:
            await client.wait_for('대기시간', timeout=30.0)
        except asyncio.TimeoutError :
            if int(LIST_COUNT) <= int(0):
                await emoji.delete()
                await ctx.send("3명 이하는 게임을 시작할 수 없어요!")
                GAME = "게임 종료"
            else :
                embedSelect=discord.Embed(title="문제 목록")
                embedSelect.add_field(name="1. 음악      2. 가수",value = "원하는 문제목록을 골라주세요\nex) 1.음악")
                await ctx.send(embed=embedSelect)
                await emoji.delete()
                msg = await client.wait_for_message(timeout=30.0,author=message.author)
                musicNum=randrange(0,100)
                if msg.startswitch('2'):
                    singer
                else:
                    music

    else:
        await ctx.send("Game Start Status")

@client.event
async def on_reaction_add(reaction, user):
    global LIST_COUNT
    if user.bot:
        return
    if reaction.emoji == '🔌' and user.id == user.id:
        if GAME == "게임 시작":
            for MEMBER in LIST:
                if MEMBER == user.id:
                    print("이미 등록된 사용자입니다")
                    return
            LIST_COUNT = LIST_COUNT + 1
            LIST.append(user.id)

@client.event
async def on_message(message):
    if message.author.bot:
        return none


client.run("Nzk3MjgzOTUwODk2MDg3MTAx.X_kOig.2xC7u1iUa6yJdy9X0IADrkR1ke4")