import discord
from discord.ext import commands

import asyncio
import json


bot = commands.Bot(command_prefix='!')
users = []

game_state = "WAIT_GAME"
game_name= ""

@bot.event
async def on_ready():
    activity = discord.Activity(name=".help", type=discord.ActivityType.playing)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print('start')

@bot.event
async def on_message(message):
    global game_state
    global game_name

    if game_state == 'WAIT_GAME':
        if message.content.startswith('!'):
            game_state = "RECRUIT"
            game_name = message.content[1:]
            print(game_name)
            if message.content == "!왕게임":
                await recruit(message, 10.0, game_name)
                game_state="GAMEING"
                await message.channel.send("참가자: " + str(len(users)))
                #await KingGame.왕게임(message, users)

            elif message.content.startswith("!한컴타자연습"):
                await recruit(message, 10.0, game_name)
                #await 한컴타자연습

            elif message.content.startswith("!더게임오브데스"):
                await recruit(message, 10.0, game_name)
                # await 더게임오브데스

    elif game_state == 'GAMING':
        pass

    elif game_state == 'GAME_OVER':
        pass


async def recruit(message: discord.Message, count: float, game_title: str, min = 0):
    global game_state
    global users

    users=[]
    users.append(message.author)

    channel=message.channel

    embed = discord.Embed(title="참가자 모집 시작", description=f"이모지를 눌러주세요!\n" + str(count) + "초 후에 " + game_title + "가 시작합니다!")
    embed.set_footer(text="명령어를 호출한 사용자는 이미 등록되었습니다")
    emoji = await channel.send(embed=embed)
    await emoji.add_reaction('🔌')

    try:
        await bot.wait_for('대기시간', timeout=count)
    except asyncio.TimeoutError:
        if len(users) <= min:
            await emoji.delete()
            await channel.send(str(min)+"명 이하는 게임을 시작할 수 없어요!")
            game_state = "GAME_OVER"
        else:
            await channel.send("게임을 시작합니다")


@bot.event
async def on_reaction_add(reaction, user):
    global users

    print("hello")

    if user.bot:
        return
    if reaction.emoji == '🔌':
        if game_state == "RECRUIT":
            for MEMBER in users:
                if MEMBER == user.id:
                    print("이미 등록된 사용자입니다")
                    return
            users.append(user)

bot.run(json.load(open("tok.json"))['tok'])
