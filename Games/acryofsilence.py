import asyncio

import discord
from discord.ext import commands

import random

from utils import GameManager
from utils import VoiceController

gm = GameManager.GameManager.instance()


async def acryofsilence(message: discord.Message, bot: commands.Bot, words: str, count = 30):
    users = gm.users.copy()
    word = random.choice(words.split(' '))
    targets = random.choices(users, k=2)

    while targets[0] == targets[1]:
        targets[1] = random.choice(users)

    users.remove(targets[0])
    users.remove(targets[1])

    #print(targets)

    em = discord.Embed(title='고요속의 외침', description="제출자는 " + targets[0].name + "\n정답을 맞추는 사람은 " + targets[1].name
                                                    + "입니다!", colour=0x888833)

    await message.channel.send(embed=em)

    await VoiceController.set_speaker(targets[0], False)
    await VoiceController.set_speaker(targets[1], False)

    await message.channel.send('총 3번의 기회가 주어집니다! \n그러면 문제를 내겠습니다!')

    await targets[0].send(word)

    gm.next_user = targets[1]

    isClear = False

    befCnt = 3
    gm.count = 3
    cnt = 0
    while cnt < count and gm.count > 0:
        try:
            await bot.wait_for('대기시간', timeout=0.25)
        except asyncio.TimeoutError:
            cnt += 0.25
            if befCnt != gm.count:
                befCnt = gm.count
                if gm.answer == word:
                    isClear = True
                else:
                    await message.channel.send("기회가 "+ befCnt + "번 남았습니다!")

        if isClear:
            await message.channel.send(targets[0].name + ', ' + targets[1].name + "팀이 맞췄습니다!")
            gm.next_user = random.choice(users)
            break

    if cnt >= count:
        await message.channel.send("시간 초과!")
        gm.next_user = random.choice(targets)

    await message.channel.send('술을 마실 사람은 ' + gm.next_user.name + '입니다!')
    await gm.set_game_over(message)
