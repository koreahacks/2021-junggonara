import discord
from discord.ext import commands

import asyncio
import json

from utils import GameManager


bot = commands.Bot(command_prefix='!')

gm = GameManager.GameManager.instance()

@bot.event
async def on_ready():
    activity = discord.Activity(name=".help", type=discord.ActivityType.playing)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print('start')


@bot.event
async def on_message(message):

    if gm.game_state == 'WAIT_GAME':
        if message.content.startswith('!'):
            gm.game_state = "RECRUIT"
            game_name = message.content[1:]
            print(game_name)
            if message.content == "!왕게임":
                await gm.recruit(message, bot, 10.0, game_name)
                game_state="GAMEING"
                await message.channel.send("참가자: " + str(len(gm.users)))
                await gm.set_game_over(message, gm.users[0])
                #await KingGame.왕게임(message, users)

            elif message.content.startswith("!한컴타자연습"):
                await gm.recruit(message, bot, 10.0, game_name)

                #await 한컴타자연습

            elif message.content.startswith("!더게임오브데스"):
                await gm.recruit(message, bot, 10.0, game_name)

                # await 더게임오브데스

    elif gm.game_state == 'GAMING':
        pass

    elif gm.game_state == 'GAME_OVER':
        if message.content.startswith('!게임종료!'):
            await message.channel.send("게임종료 인식 성공!!")
            gm.game_state = "WAIT_GAME"
        pass




@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    if reaction.emoji == '🔌':
        if gm.game_state == "RECRUIT":
            for MEMBER in gm.users:
                if MEMBER == user:
                    print("이미 등록된 사용자입니다")
                    return
            gm.users.append(user)

bot.run(json.load(open("tok.json"))['tok'])
