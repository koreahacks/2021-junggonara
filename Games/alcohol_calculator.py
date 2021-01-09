import discord
import asyncio
from discord.ext import commands
import random

client = commands.Bot(command_prefix="/")

@client.event
async def on_ready():
    global GAME
    global alcohol_dictionary
    global glass_dictionary
    global calculation_list
    calculation_list=[]
    alcohol_dictionary = {'소주':17, '맥주':4.5, '막걸리':6, '이슬톡톡':3, '양주':40}
    glass_dictionary = {'소주잔':70, '맥주잔':200, '종이컵':180}
    GAME = '게임 종료'
    print('start')

@client.event
async def on_message(message):
    global GAME
    global alcohol_dictionary
    global glass_dictionary
    global calculation_list


    if message.content.startswith('/알코올 계산기'):
        calculation_list = []
        GAME = '게임 시작'
        embed = discord.Embed(title="알코올 계산기", description="여러 종류의 술을 소주 단위로 계산해 드립니다\n계산 가능한 술: 소주, 맥주, 막걸리, 이슬톡톡, 양주(40도로 계산)\n계산 가능한 술잔: 소주잔, 맥주잔, 종이컵")
        await message.channel.send(embed=embed)
        embed2 = discord.Embed(title='술 종류와 잔, 용량을 알려주세요', description='ex)소주,맥주잔,1.5잔\nex)맥주,종이컵,3.7잔')
        await message.channel.send(embed=embed2)

    if message.content !='/알코올 계산기' and GAME == '게임 시작':
        if message.author.bot:
            return None
        message_list = message.content.split(',')
        message_list[2] = message_list[2][:-1]
        for a in range(0,5):
            k = list(alcohol_dictionary.keys())
            if message_list[0] == k[a]:
                calculation_list.append(alcohol_dictionary[k[a]])

        for a in range(0,3):
            k = list(glass_dictionary.keys())
            if message_list[1] == k[a]:
                calculation_list.append(glass_dictionary[k[a]])
        calculation_list.append(message_list[2])
        calculation = (float(calculation_list[0])*float(calculation_list[1])*float(calculation_list[2]))/float(17*70)
        embed = discord.Embed(title='당신이 마신 술의 총량은?',description=f'소주로 {round(calculation,2)}잔입니다\n소주병으로는 {round(calculation/float(360/70),2)}병입니다')
        await message.channel.send(embed=embed)
        GAME='게임 종료'



client.run('Nzk3Mjg0NDI4Mjc4OTIzMjk1.X_kO_A.Kx1J52_gltymJpXsAh_suOQhuW0')