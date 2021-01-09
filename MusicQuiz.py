import discord
import asyncio
from discord.ext import commands
import youtube_dl
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
    numSt=str(randrange(1, 20))
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


async def musicQ(message,LIST):
    channel = message.channel
    global GAME
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
client.run("Nzk3MjgzOTUwODk2MDg3MTAx.X_kOig.CxW5s99YbgOo6RWS6qE7XGj0yIE")