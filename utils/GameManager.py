import discord
from discord.ext import commands



async def recruit(ctx, bot, GAME_NUMBER):
    global game_state
    global LIST
    global LIST_COUNT
    maxMem=0
    max=0

    game_state = "RECRUIT_GAME"
    LIST = []
    LIST.append(ctx.author.id)
    LIST_COUNT = 1

    embed = discord.Embed(title="참가자 모집 시작", description=f"이모지를 눌러주세요!\n30초 후에 음악퀴즈가 시작합니다!")
    embed.set_footer(text="명령어를 호출한 사용자는 이미 등록되었습니다")
    emoji = await ctx.send(embed=embed)
    await emoji.add_reaction(':electric_plug:')

    @bot.event
    async def on_reaction_add(reaction, user):
        global LIST_COUNT
        if user.bot:
            return
        if reaction.emoji == ':electric_plug:':
            if game_state == "RECRUIT_GAME":
                for MEMBER in LIST:
                    if MEMBER == user.id:
                        print("이미 등록된 사용자입니다")
                        return
                LIST_COUNT = LIST_COUNT + 1
                LIST.append(user.id)

