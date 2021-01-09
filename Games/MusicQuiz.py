import discord
import ffmpeg
import asyncio
from discord.ext import commands
import re
import json
from random import randrange
from utils import VoiceController

async def musicPlay(message, bot):
    musicDir = json.load(open("music.json", encoding="utf-8"))
    #numSt=str(randrange(1, 1))
    numSt=str(1)
    url=musicDir["mu"+numSt]["url"]
    singer=musicDir["mu"+numSt]["singer"]
    title=musicDir["mu"+numSt]["title"]
    print(url)
    url1 = re.match('(https?://)?(www\.)?((youtube\.(com))/watch\?v=([-\w]+)|youtu\.be/([-\w]+))',
                        url)  # 정규 표현식을 사용해 url 검사

    voice_client = await VoiceController.connect_bot_voice_channel(message)

    voice_client.play(discord.FFmpegPCMAudio(executable="C:/ffmpeg-4.3.1-2021-01-01-full_build-shared/bin/ffmpeg.exe", source="./music/IU_Good.mp3"))

    voice_client.stop()
    return [url,singer,title]

async def musicQ(message, LIST, bot):
    channel = message.channel
    embedSelect = discord.Embed(title="문제 목록")
    embedSelect.add_field(name="1. 음악이름      2. 가수", value="원하는 문제목록을 골라주세요\nex) 1.음악")
    await channel.send(embed=embedSelect)

    def pred(m):
        return m.author == message.author and m.channel == message.channel
    msg = await bot.wait_for('message', check=pred)

    print("abc2")
    print(msg)
    Set= await musicPlay(message, bot)
    answer="answer"
    #if msg.startswitch('2'):
    #    answer=Set[1]
    #    await channel.send('2')
    #else:
    #    answer=Set[2]
    #    await channel.send('1')
    #while 1:
    #    msg = await bot.wait_for('message', check=pred)
    #    if msg == answer:
    #        print(msg.author)
    #        break