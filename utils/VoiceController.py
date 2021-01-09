import discord
from discord.ext import commands


async def set_speaker(member: discord.Member, state: bool):
    await member.edit(deafen=not state)


async def set_mic(member: discord.Member, state: bool):
    await member.edit(mute=not state)
