import discord
import asyncio
from discord.ext import commands
import random

client = commands.Bot(command_prefix="/")


@client.event
async def on_ready():
    global GAME
    global count
    global playerlist
    global munjang
    global quiz
    playerlist = []
    count = 0
    GAME = "게임 종료"
    munjangfile = open('hancome.txt', 'r', encoding='utf8')  # 문장 데이터 불러오기
    munjanglist = []
    while True:
        i = munjangfile.readline()
        if not i:
            break
        munjanglist.append(i[0:-2])  # 데이터 문자열로 저장
    munjangfile.close()
    munjang = random.choice(munjanglist)  # 랜덤뽑기

    quizfile = open('nunsense.txt', 'r', encoding='utf8') #문장 데이터 불러오기
    quizlist = []
    while True:
        i = quizfile.readline()
        if not i:
            break
        quizlist.append(i)
    quizfile.close()
    wait = random.choice(quizlist) #랜덤뽑기
    quiz = wait.split(':')
    quiz[1]=quiz[1][0:-1]
    print('go!')


@client.event
async def on_message(message):
    global count
    global munjang
    global GAME
    global count
    global quiz
    global GAME

    if message.content.startswith('/한컴타자연습'):
        GAME = '게임 시작'
        embed = discord.Embed(title="한컴타자연습 시작", description=f"5초 후에 문장이 공개됩니다")
        await message.channel.send(embed=embed)
        try:
            await client.wait_for('대기', timeout=5.0)
        except asyncio.TimeoutError:
            embed2 = discord.Embed(title=munjang, description=f'위의 문장을 토씨 하나 틀리지 않고 정확히 입력해주세요!')
            await message.channel.send(embed=embed2)

    if message.content.startswith(munjang) and GAME == '게임 시작':
        await message.channel.send("{0} 정답!".format(str(message.author.name)))
        count +=1
        print(count)
        playerlist.append(str(message.author.name))
        if count>=3:
            print(playerlist)
            count1 = 0
            embed3 = discord.Embed(title='최종 순위')
            for a in playerlist:
                count1 += 1
                embed3.add_field(name='{0}등'.format(count1), value=a, inline=False)
            await message.channel.send(embed=embed3)
            GAME = '게임 종료'
            count = 0

    if message.content.startswith('/넌센스퀴즈'):
        GAME = '게임 시작'
        embed = discord.Embed(title="넌센스퀴즈 시작", description="5초 후에 퀴즈가 공개됩니다")
        await message.channel.send(embed=embed)
        try:
            await client.wait_for('대기', timeout=5.0)
        except asyncio.TimeoutError:
            embed2 = discord.Embed(title=quiz[0], description='정답은..?')
            await message.channel.send(embed=embed2)

    if message.content.startswith(quiz[1]) and GAME == '게임 시작':
        await message.channel.send("{0} 정답!".format(str(message.author.name)))
        GAME = '게임 종료'




client.run('Nzk3Mjg0NDI4Mjc4OTIzMjk1.X_kO_A.8ycQ53fCfDZOxgDPk3OtG2tSOp0')