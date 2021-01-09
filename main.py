import discord
from discord.ext import commands

import asyncio
import json

from utils import GameManager
from utils import VoiceController
from Games import acryofsilence


bot = commands.Bot(command_prefix='!')

gm = GameManager.GameManager.instance()
game_info = json.load(open('game_data.json', encoding='utf-8'))

print(game_info.keys())


@bot.event
async def on_ready():
    activity = discord.Activity(name=".help", type=discord.ActivityType.playing)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print('start')


@bot.event
async def on_message(message):
    words = message.content.split(' ')

    if gm.game_state == 'WAIT_GAME':
        if words[0].startswith('!'):
            if message.author.bot:
                return
            gm.game_state = "RECRUIT"
            game_name = words[0][1:]

            if game_name in game_info.keys():
                gm.initialize()
                gm.game_name = game_name
                print('현재 게임은 ' + gm.game_name + '입니다')
                if game_info[gm.game_name]['recruit']:
                    await gm.recruit(message, bot, 10.0, gm.game_name,
                                     game_info[gm.game_name]['min_member'],
                                     game_info[gm.game_name]['max_member'])
                    await message.channel.send("참가자: " + str(len(gm.users)))
                else:
                    gm.game_state = "GAMING"

                if gm.game_state == 'WAIT_GAME':
                    return

                if gm.game_name == "고요속의외침":
                    await acryofsilence.acryofsilence(message, bot, game_info[gm.game_name]['words'])

            else:
                await message.channel.send("해당 게임은 없습니다.")
                gm.game_state = "WAIT_GAME"

    elif gm.game_state == 'GAMING':
        if gm.game_name == '고요속의외침':
            if message.author == gm.next_user:
                gm.next_user = message.author
                gm.answer = message.content
                gm.count -= 1
        else:
            await gm.set_game_over(message)

    elif gm.game_state == 'GAME_OVER':
        if message.content.startswith('!게임종료!'):
            await message.channel.send("게임종료 인식 성공!!")
        gm.game_state = "WAIT_GAME"

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
