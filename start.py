import random
import os
import aiohttp
import json
import time
import datetime
import discord
import youtube_dl
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient

BOT_PREFIX = ("?","!")

#Cria uma timestamp durante o boot para o sobre()
ts = time.time()
lastboot = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

#Nao te esque'cas de adicionar o token ANA
TOKEN = 'NDcxNDk4MzAzNDMxNzcwMTIy.Dj6qVg.JHoP-UQOBperAOnuRO0XT4dCUnU'

bot = commands.Bot(command_prefix=BOT_PREFIX)

players={}

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

@bot.command()
async def sobre():
    print("Sobre")
    embed = discord.Embed(title="Chumbot", description="Basicamente o dario no corpo de um bot", color=0x3498db, type="rich")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/471500310133604352/471500693539258386/qw.png")
    embed.add_field(name="Autores", value="Rusky#0001 and AnaG#2174")
    embed.add_field(name="Online desde:", value=lastboot);
    embed.add_field(name="Convite:", value="[Link](https://discordapp.com/api/oauth2/authorize/471498303431770122)")
    embed.set_footer(text="Chumbados")
    await bot.say(embed=embed)


@bot.command(pass_context=True)
async def entra(ctx):
    print("Entra")
    channel=ctx.message.author.voice.voice_channel
    await bot.join_voice_channel(channel)


@bot.command(pass_context=True)
async def sai(ctx):
    print("Sai")
    server=ctx.message.server
    voice_client = bot.voice_client_in(server)
    await voice_client.disconnect()

@bot.command(pass_context=True)
async def play(ctx,url):
    print("Playing")
    server=ctx.message.server
    voice_client = bot.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url)
    players[server.id] = player
    player.start()

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
    print('ID:' + str(bot.user.id))
    print('Token: ' + TOKEN)
    print('----------------------------')
    print('Lista de comandos invocados')
    print('----------------------------')
    await bot.change_presence(game=discord.Game(name="with code"))

bot.run(TOKEN)
