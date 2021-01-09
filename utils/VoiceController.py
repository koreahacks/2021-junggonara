import discord
from discord.ext import commands

class VoiceController:
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    def setSpeaker(self, voicechannel:discord.VoiceChannel, user_id:int, state):
        user = ''
        for u in voicechannel.members:
            if discord.Member(u).id == user_id:
                u.voice.deaf = state
                return

    def setMic(self, voicechannel:discord.VoiceChannel, user_id:int, state):
        user = ''
        for u in voicechannel.members:
            if discord.Member(u).id == user_id:
                u.voice.mute = state
                return

