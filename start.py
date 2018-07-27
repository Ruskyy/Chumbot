import random
import os
import aiohttp
import json
from discord import *
from discord.ext.commands import Bot

BOT_PREFIX = ("?","!")

TOKEN = ''

bot = Bot(command_prefix=BOT_PREFIX)

@bot.command()
async def pergunta():
    print("Pergunta")
    respostas = [
        'Desiste logo do curso se pensas assim',
        'Pergunta ao Indiano',
        'Isso e bueda facil',
        'Ja estas chumbado',
        'Gajas... yah.. Gajas... Hmm.. qual era a pergunta mesmo ?']
    await bot.say(random.choice(respostas))

@bot.command()
async def bitcoin():
    print("Bitcoin")
    numeros = [2,5,8,7,4,1,9,6,3]
    url = 'https://api.coindesk.com/v1/bpi/currentprice/EUR.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        await bot.say("O valor e de: " + response['bpi']['EUR']['rate']+"€ \nQuero "+str(random.randint(1,10)+1)+"!")

# @client.event
# async def on_message(message):
#     # Impede que o bott entre em loop de se responder a si mesmo
#     if message.author == client.user:
#         return
#
#     if message.content.startswith('!ola'):
#         msg = 'Só fizeste uma mensagem de olá ? {0.author.mention} estás CHUMBADO'.format(message)
#         await client.send_message(message.channel, msg)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if 'chumbado' in message.content.lower():
        msg = 'Zero Bola C-H-U-M-B-A-D-O'.format(message)
        print(msg)
        await bot.send_message(message.channel,msg)

    await bot.process_commands(message)

# Comandos on boot
@bot.event
async def on_ready():
    os.system('cls' if os.name == 'nt' else 'clear') #Limpa a consola
    print('+--------------------------+')
    print('Sessao iniciada como: ' + bot.user.name )
    print('ID:' + bot.user.id)
    print('Token: ' + TOKEN)
    print('----------------------------')
    print('Lista de comandos invocados')
    print('----------------------------')
    await bot.change_presence(game=Game(name="with code"))

bot.run(TOKEN)
