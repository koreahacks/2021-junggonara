import discord
import asyncio
from discord.ext import commands
from random import randrange

async def kingame(message, LIST, bot):
    maxMem=0
    max=0
    channel=message.channel
    try:
        await bot.wait_for('대기시간', timeout=3.0)
    except asyncio.TimeoutError :

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
        await channel.send(embed=embed3)

        try:
            await bot.wait_for("가나다", timeout=30)
        except  asyncio.TimeoutError:
            await channel.send(embed=embed2)