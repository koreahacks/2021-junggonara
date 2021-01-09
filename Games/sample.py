import discord
import asyncio
from discord.ext import commands
from random import randrange

client = commands.Bot(command_prefix="/")

@client.event
async def on_ready():
    global GAME
    GAME = "게임 종료"

@client.command()
async def 왕게임(ctx):
    global GAME
    global LIST
    global LIST_COUNT

    if GAME == "게임 종료":
        GAME = "게임 시작"
        LIST = []
        LIST.append(ctx.author.id)
        LIST_COUNT = 1

        embed = discord.Embed(title="왕게임 시작", description=f"이모지를 눌러주세요!\n30초 후에 왕게임이 시작합니다!")
        embed.set_footer(text="명령어를 호출한 사용자는 이미 등록되었습니다")
        emoji = await ctx.send(embed=embed)
        await emoji.add_reaction('🔌')

        try:
            await client.wait_for('대기시간', timeout=10.0)
        except asyncio.TimeoutError :
            if int(LIST_COUNT) <= int(2):
                await emoji.delete()
                await ctx.send("3명 이하는 게임을 시작할 수 없어요!")
                GAME = "게임 종료"
            else:
                embed2 = discord.Embed(title="왕게임 분배 목록")
                embed3= discord.Embed(title="왕게임 점수분배목록")
                i = 1
                for MEMBER in LIST:
                    i += 1
                    RANDOM = randrange(0, 100)
                    embed3.add_field(name=f"해당 대상자는 {RANDOM}점을 분배 받았습니다", value=f"{i}번 ???")
                    embed2.add_field(name=f"해당 대상자는 {RANDOM}점을 분배 받았습니다", value=f"{i}번 <@{MEMBER}>", inline=False)

                embed3.set_footer(text="30초 후에 번호를 공개합니다")
                embed2.set_footer(text="가장 많은 점수를 분배 받은 사람이 왕입니다!")
                await emoji.delete()
                await ctx.send(embed=embed3)

                try:
                    await client.wait_for("간나다", timeout=30)
                except  asyncio.TimeoutError:
                    await ctx.send(embed=embed2)
                    GAME = "게임 종료"
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

