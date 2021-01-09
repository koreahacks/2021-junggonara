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

async def kingame(message, LIST):
    maxMem=0
    max=0
    channel=message.channel
    try:
        await client.wait_for('대기시간', timeout=30.0)
    except asyncio.TimeoutError :
        if int(LIST.len()) <= int(2):
            await emoji.delete()
            await channel.send("3명 이하는 게임을 시작할 수 없어요!")
        else:
            embed2 = discord.Embed(title="왕게임 점수 분배 목록")
            embed3= discord.Embed(title="who is the new King")
            i = 0
            for MEMBER in LIST:
                i += 1
                RANDOM = randrange(0, 100)
                embed2.add_field(name=f"해당 대상자는 {RANDOM}점을 분배 받았습니다", value=f"{i}번 <@{MEMBER}>", inline=False)
                if max < RANDOM:
                    maxMem=MEMBER
            embed3.add_field(name= "왕은 다른 번호들에게 명령을 내리세요", value=f"왕은 <@{maxMem}> 입니다.")
            embed3.set_footer(text="60초 뒤에 멤버들의 번호가 공개됩니다.")

            embed2.set_footer(text="가장 많은 점수를 분배 받은 사람이 왕입니다!")
            await emoji.delete()
            await channel.send(embed=embed3)

            try:
                await client.wait_for("가나다", timeout=30)
            except  asyncio.TimeoutError:
                await channel.send(embed=embed2)


@client.event
async def on_message(message):
    if message.content.startswitch("/왕게임"):
        KingGame(message,LIST)

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