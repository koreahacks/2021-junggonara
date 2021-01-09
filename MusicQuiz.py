import discord
import asyncio
from discord.ext import commands
import youtube_dl
import re
import json
from random import randrange

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

async def join(message):
    channel = message.author.voice.channel
    #channel = message.author.voice.channel
    await channel.connect()

async def disjoin(message):
    channel = message.author.voice.channel
    #channel = message.author.voice.channel
    await channel.disconnect()

async def musicPlay(message):
    try:
        musicDir = json.load(open("music.json",encoding="utf-8"))
        url=musicDir["mu"+str(randrange(1,20))]
        url1 = re.match('(https?://)?(www\.)?((youtube\.(com))/watch\?v=([-\w]+)|youtu\.be/([-\w]+))',
                        )  # 정규 표현식을 사용해 url 검사
        if url1 == None:
            await client.send_message(message.channel,
                                      embed=discord.Embed(title=":no_entry_sign: url을 제대로 입력해주세요.", colour=0x2EFEF7))
            return
    except IndexError:
        await client.send_message(message.channel,
                                  embed=discord.Embed(title=":no_entry_sign: url을 입력해주세요.", colour=0x2EFEF7))
        return

    channel = message.author.voice.voice_channel
    server = message.server
    voice_client = client.voice_client_in(server)

    if client.is_voice_connected(server) and not playerlist[server.id].is_playing():  # 봇이 음성채널에 접속해있으나 음악을 재생하지 않을 때
        await voice_client.disconnect()
    elif client.is_voice_connected(server) and playerlist[server.id].is_playing():  # 봇이 음성채널에 접속해있고 음악을 재생할 때
        player = await voice_client.create_ytdl_player(url, after=lambda: queue(server.id),
                                                       before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
        if server.id in que:  # 큐에 값이 들어있을 때
            que[server.id].append(player)
        else:  # 큐에 값이 없을 때
            que[server.id] = [player]
        await client.send_message(message.channel,
                                  embed=discord.Embed(title=":white_check_mark: 추가 완료!", colour=0x2EFEF7))
        playlist.append(player.title)  # 재생목록에 제목 추가
        return

    try:
        voice_client = await client.join_voice_channel(channel)
    except discord.errors.InvalidArgument:  # 유저가 음성채널에 접속해있지 않을 때
        await client.send_message(message.channel,
                                  embed=discord.Embed(title=":no_entry_sign: 음성채널에 접속하고 사용해주세요.", colour=0x2EFEF7))
        return

    try:
        player = await voice_client.create_ytdl_player(url, after=lambda: queue(server.id),
                                                       before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5")
        playerlist[server.id] = player
        playlist.append(player.title)
    except youtube_dl.utils.DownloadError:  # 유저가 제대로 된 유튜브 경로를 입력하지 않았을 때
        await client.send_message(message.channel,
                                  embed=discord.Embed(title=":no_entry_sign: 존재하지 않는 경로입니다.", colour=0x2EFEF7))
        await voice_client.disconnect()
        return
    player.start()

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
    if message.content.startswith("!join"):
        await join(message)
    if message.content.startswith("!disjoin"):
        await disjoin(message)
client.run("Nzk3MjgzOTUwODk2MDg3MTAx.X_kOig.CxW5s99YbgOo6RWS6qE7XGj0yIE")