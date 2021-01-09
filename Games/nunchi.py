import discord
import asyncio
from discord.ext import commands


from utils import GameManager




async def nunchi(message, bot):
    gm = GameManager.GameManager.instance()

    rankinglist = []

    gm.users.append(message.author.voice.channel.members)

    embed = discord.Embed(title="눈치게임",description=f"2초 후에 시작합니다.")
    embed.set_footer(text="반드시 숫자앞에 !를 붙여주세요 ex)!1")
    await message.channel.send(embed=embed)

    try:
        await bot.wait_for('대기', timeout=2.0)
    except asyncio.TimeoutError:
        await message.channel.send("눈치게임")
        await message.channel.send("시작!")

    cnt = gm.count
    i = 1
    while True:
        try:
            bot.wait_for(' ', timeout=0.1)
        except asyncio.TimeoutError:
            if cnt != gm.count:
                msg = gm.answer
                if msg == i-1: # 중복 숫자 검출
                    await message.channel.send(f"{rankinglist[msg-1]}님과 {gm.next_user}님이 걸렸습니다.")
                    break

                elif i == len(gm.users) - 1 or i != msg:
                    await message.channel.send(f"{gm.next_user}님이 걸렸습니다.")
                    break

                rankinglist.append(str(gm.next_user))
                i+=1
                cnt = gm.count

    gm.set_game_over(message)