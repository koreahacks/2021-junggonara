import discord
import asyncio
import time
import re
import json
from random import randrange
from utils import VoiceController
from utils import GameManager

async def musicPlay(message, bot):
    musicDir = json.load(open("music.json", encoding="utf-8"))
    numSt=str(randrange(1, 22))
    url=musicDir["mu"+numSt]["url"]
    singer=musicDir["mu"+numSt]["singer"]
    title=musicDir["mu"+numSt]["title"]
    print(url)
    url1 = re.match('(https?://)?(www\.)?((youtube\.(com))/watch\?v=([-\w]+)|youtu\.be/([-\w]+))',
                        url)  # 정규 표현식을 사용해 url 검사

    voice_client = await VoiceController.connect_bot_voice_channel(message)
    start_time = time.time()
    voice_client.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg-4.3.1-2021-01-01-full_build-shared/bin/ffmpeg.exe", source=url))
    while 1:
        if time.time()-start_time > 3.0 :
            break
    voice_client.stop()
    return [url,singer,title]

async def musicQ(message, LIST, bot):
    channel = message.channel
    embedSelect = discord.Embed(title="문제 목록")
    embedSelect.add_field(name="1. 음악이름      2. 가수", value="원하는 문제목록을 골라주세요\nex) 1 or 2")
    await channel.send(embed=embedSelect)
    channel = message.channel
    def pred(m):
        return m.channel == message.channel
    msg = await bot.wait_for('message', check=pred)

    print(msg)
    Set = await musicPlay(message, bot)
    answer=Set[2]
    if msg.content=="2":
        answer=Set[1]
    while 1:
        msg = await bot.wait_for('message', check=pred)
        if msg.content == answer:
            print(answer)
            embed=discord.Embed(title="정답자")
            embed.add_field(name="정답은 "+Set[1]+" 의 "+Set[2]+"입니다.",value=f"<@{msg.author.name}>이(가) 맞췄습니다.",inline=False)
            embed.set_footer()
            await channel.send(embed=embed)
            print(msg.author)
            await GameManager.GameManager.instance().set_game_over(message)
            return