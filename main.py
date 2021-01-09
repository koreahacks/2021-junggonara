import discord
from discord.ext import commands

import asyncio
import json

from utils import GameManager
from utils import VoiceController
from Games import acryofsilence, thegameofdeath, quiz, nunchi, gongsangame, bomb_game, alcohol_calculator, KingGame


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

                elif gm.game_name == "더게임오브데스":
                    await thegameofdeath.thegameofdeath(message, bot)

                elif gm.game_name == '한컴타자연습':
                    await quiz.quiz(message, bot)

                elif gm.game_name == '넌센스퀴즈':
                    await quiz.nunsence(message, bot)

                elif gm.game_name == '눈치게임':
                    await nunchi.nunchi(message, bot)

                elif gm.game_name == '왕게임':
                    await KingGame.kingame(message, bot)

                elif gm.game_name == "공산당게임":
                    gm.users = message.author.voice.channel.members
                    await gongsangame.gongsan(message, bot)

            else:
                await message.channel.send("해당 게임은 없습니다.")
                gm.game_state = "WAIT_GAME"

    elif gm.game_state == 'GAMING':
        if gm.game_name == '고요속의외침':
            if message.author == gm.next_user:
                gm.next_user = message.author
                gm.answer = message.content
                gm.count -= 1

        elif gm.game_name == '더게임오브데스':
            if not message.author.bot:
                if len(gm.users) == 3:
                    return
                if message.content in gm.users[0]:
                    gm.users[1][message.author.name] = message.content

                if len(gm.users[0]) == len(gm.users[1]):
                    try:
                        gm.users.append(int(message.content))
                    except ValueError:
                        return

        elif gm.game_name == '한컴타자연습':
            if not message.author.bot:
                gm.next_user = message.author
                gm.answer = message.content

        elif gm.game_name == '넌센스퀴즈':
            if not message.author.bot:
                gm.next_user = message.author
                gm.answer = message.content

        elif gm.game_name == '눈치게임':
            if (not message.author.bot) and (message.content.isdigit()):
                gm.count += 1
                gm.answer = int(message.content)
                gm.next_user = message.author

        elif gm.game_name == '왕게임':
            pass

        elif gm.game_name == '공산당게임':
            pass

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
