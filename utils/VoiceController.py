import discord
from discord.ext import commands


async def set_speaker(member: discord.Member, state: bool):
    await member.edit(deafen=not state)


async def set_mic(member: discord.Member, state: bool):
    await member.edit(mute=not state)


async def connect_bot_voice_channel(message: discord.Message):
    channel = message.author.voice.channel
    return await channel.connect()

async def disconnect_bot_voice_channel(message: discord.Message):
    channel = message.author.voice.channel
    return await channel.disconnect()
