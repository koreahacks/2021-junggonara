import asyncio

import discord
from discord.ext import commands

import random

from utils import GameManager
from utils import VoiceController

gm = GameManager.GameManager.instance()


async def acryofsilence(message: discord.Message, bot: commands.Bot, count = 30):
    users = gm.users

    targets = random.choices(users, k=2)

    while targets[0] == targets[1]:
        targets[1] = random.choice(users)

    print(targets)
    await message.channel.send("제출자는 " +targets[0].name + "\n정답을 맞추는 사람은 " + targets[1].name + "입니다!")

    await VoiceController.set_speaker(targets[0], False)
    await VoiceController.set_speaker(targets[1], False)

    await targets[0].send("테스트")

    isClear = False

    cnt = 0
    while cnt < count:
        try:
            await bot.wait_for('대기시간', timeout=0.5)
        except asyncio.TimeoutError:
            cnt += 0.5
            if gm.answer == '테스트':
                isClear = True

        if isClear:
            await message.channel.send(gm.next_user.name + "이(가) 맞췄습니다!")
            break

    if cnt >= count:
        await message.channel.send("시간 초과!")
    await gm.set_game_over(message)
