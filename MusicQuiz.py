import discord
import asyncio
from discord.ext import commands
import re
import json
from random import randrange
from util import VoiceController

client = commands.Bot(command_prefix='!')

que = {}
playerlist = {}
playlist = list() #재생목록 리스트

def queue(id): #음악 재생용 큐
	if que[id] != []:
		player = que[id].pop(0)
		playerlist[id] = player
		del playlist[0]
		player.start()

@client.event
async def on_ready():
    global GAME
    GAME = "게임 종료"
    print("is ready")

async def musicPlay(message):
    musicDir = json.load(open("music.json",encoding="utf-8"))
    numSt=str(randrange(1, 1))
    url=musicDir["mu"+numSt]["url"]
    singer=musicDir["mu"+numSt]["singer"]
    title=musicDir["mu"+numSt]["title"]
    url1 = re.match('(https?://)?(www\.)?((youtube\.(com))/watch\?v=([-\w]+)|youtu\.be/([-\w]+))',
                        url)  # 정규 표현식을 사용해 url 검사

    channel = message.author.voice.channel
    server = message.server

    if client.is_connected():  # 봇이 음성채널에 접속해있으나 음악을 재생하지 않을 때
        await VoiceController.disconnect_bot_voice_channel(message)
    voice_client = await VoiceController.connect_bot_voice_channel(message)

    voice_client.play(discord.FFmpegPCMAudio(url), after=lambda e: print('done', e))
    client.wait_for("노래시간", timeout=4)
    voice_client.stop()
    return [url,singer,title]


async def musicQ(message,LIST):
    channel = message.channel
    embedSelect = discord.Embed(title="문제 목록")
    embedSelect.add_field(name="1. 음악이름      2. 가수", value="원하는 문제목록을 골라주세요\nex) 1.음악")
    await channel.send(embed=embedSelect)

    def pred(m):
        return m.author == message.author and m.channel == message.channel
    msg = await client.wait_for('message', check=pred)

    Set=musicPlay(message)
    answer="answer"
    if msg.startswitch('2'):
        answer=Set[1]
        await channel.send('2')
    else:
        answer=Set[2]
        await channel.send('1')
    while 1:
        msg = await client.wait_for('message', check=pred)
        if msg == answer:
            print(msg.author)
            break

@client.event
async def on_message(message):
    # 메세지를 보낸 사람이 봇일 경우 무시한다
    if message.author.bot:
        return None
    if message.

client.run("Nzk3MjgzOTUwODk2MDg3MTAx.X_kOig.-WdQ2wtMOaB3tlFB1RK6DRpFjWk")