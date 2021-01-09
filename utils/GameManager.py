import discord
from discord.ext import commands
import asyncio


class GameManager:
    __instance = None

    @classmethod
    def __getInstance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls.__instance = cls(*args, **kargs)
        cls.instance = cls.__getInstance
        return cls.__instance

    def __init__(self):
        self.game_state = "WAIT_GAME"
        self.game_name = ""
        self.users = []
        self.next_user = None

    async def recruit(self, message: discord.Message, bot: commands.Bot,  count: float, game_title: str, min = -1, max = -1):
        self.users = []
        self.users.append(message.author)

        channel = message.channel

        embed = discord.Embed(title="참가자 모집 시작",
                              description=f"이모지를 눌러주세요!\n" + str(count) + "초 후에 " + game_title + "가 시작합니다!")
        embed.set_footer(text="명령어를 호출한 사용자는 이미 등록되었습니다")
        emoji = await channel.send(embed=embed)
        await emoji.add_reaction('🔌')

        try:
            await bot.wait_for('대기시간', timeout=count)
        except asyncio.TimeoutError:
            if len(self.users) < min:
                await emoji.delete()
                await channel.send(str(min-1) + "명 이하는 게임을 시작할 수 없어요!")
                self.game_state = "GAME_OVER"

            elif (len(self.users) > max) and (max != -1):
                await emoji.delete()
                await channel.send(str(min) + "명 이하는 게임을 시작할 수 없어요!")
                self.game_state = "GAME_OVER"
            else:
                await channel.send("게임을 시작합니다")

    async def set_game_over(self, message: discord.Message):
        self.game_state = "GAME_OVER"
        await message.channel.send("!게임종료!")

