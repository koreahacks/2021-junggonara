import discord
import asyncio
from discord.ext import commands
from random import randrange

client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    global GAME
    GAME = "게임 종료"
    print("is ready")

async def join(message):
    channel = message.author.voice.channel
    #channel = message.author.voice.channel
    await channel.connect()

    #await channel.connect()

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

async def musicQ(message,LIST):
    channel = message.channel
    if GAME == "게임 종료":
        GAME = "게임 시작"
        LIST = []
        LIST.append(message.author.id)
        LIST_COUNT = 1

        embed = discord.Embed(title="음악퀴즈 시작", description=f"이모지를 눌러주세요!\n10초 후에 음악퀴즈가 시작합니다!")
        embed.set_footer(text="명령어를 호출한 사용자는 이미 등록되었습니다")
        emoji = await channel.send(embed=embed)
        await emoji.add_reaction('🔌')

        try:
            await client.wait_for('대기시간', timeout=10.0)
        except asyncio.TimeoutError:
            if int(LIST_COUNT) <= int(0):
                await emoji.delete()
                await channel.send("3명 이하는 게임을 시작할 수 없어요!")
                GAME = "게임 종료"
            else:
                embedSelect = discord.Embed(title="문제 목록")
                embedSelect.add_field(name="1. 음악      2. 가수", value="원하는 문제목록을 골라주세요\nex) 1.음악")
                await channel.send(embed=embedSelect)
                await emoji.delete()
                msg = await client.wait_for_message(timeout=15.0, author=message.author)
                musicNum = randrange(0, 100)
                if msg.startswitch('2'):
                    await channel.send('2')
                else:
                    await channel.send('1')
    else:
        await channel.send("Game Start Status")

@client.event
async def on_message(message):
    # 메세지를 보낸 사람이 봇일 경우 무시한다
    if message.author.bot:
        return None
    if message.content.startswith("!join"):
        await join(message)
