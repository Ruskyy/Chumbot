import random
import os
import io
import aiohttp
import json
import asyncio
import time
import datetime
import discord
import youtube_dl
import safygiphy
import requests
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient

BOT_PREFIX = ("!")

#Cria uma timestamp durante o boot para o sobre()
ts = time.time()
lastboot = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

#Nao te esquecas de adicionar o token ANA
TOKEN = 'NDcxNDk4MzAzNDMxNzcwMTIy.Dj0Yuw.g6KumUnYWn-A7P-mREODg1Fd1OQ'

#Incicaliza a framework do bot
bot = commands.Bot(command_prefix=BOT_PREFIX)

#Instancia a API do Giphy
g = safygiphy.Giphy()


if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')

def __init__(self, bot):
        self.bot = bot

class VoiceEntry:
    def __init__(self, message, player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

    def __str__(self):
        fmt = ' {0.title} - pedida por {1.display_name}'
        duration = self.player.duration
        if duration:
            fmt = fmt + ' [duracao: {0[0]}m {0[1]}s]'.format(divmod(duration, 60))
        return fmt.format(self.player, self.requester)

class VoiceState:
    def __init__(self, bot):
        self.current = None
        self.voice = None
        self.bot = bot
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skip_votes = set()
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    @property
    def player(self):
        return self.current.player

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing():
            self.player.stop()

    def toggle_next(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    async def audio_player_task(self):
        while True:
            self.play_next_song.clear()
            self.current = await self.songs.get()
            await self.bot.send_message(self.current.channel, 'A bombar :' + str(self.current))
            self.current.player.start()
            await self.play_next_song.wait()
class Music:

    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state

        return state

    async def create_voice_client(self, channel):
        voice = await self.bot.join_voice_channel(channel)
        state = self.get_voice_state(channel.server)
        state.voice = voice

    def __unload(self):
        for state in self.voice_states.values():
            try:
                state.audio_player.cancel()
                if state.voice:
                    self.bot.loop.create_task(state.voice.disconnect())
            except:
                pass

    @commands.command(pass_context=True, no_pm=True)
    async def summon(self, ctx):

        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            await self.bot.say('Puto... para fazer isso tens de estar num voice chat chavalo...')
            return False

        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            state.voice = await self.bot.join_voice_channel(summoned_channel)
        else:
            await state.voice.move_to(summoned_channel)

        return True

    @commands.command(pass_context=True, no_pm=True)
    async def play(self, ctx, *, song : str):

        request_user_channel=ctx.message.author.voice.voice_channel
        server=ctx.message.server

        state = self.get_voice_state(ctx.message.server)
        opts = {
            'default_search': 'auto',
            'quiet': False,
        }
        if request_user_channel is None:
            print("Erro : User do Request nao estava em voice")
            await bot.say('Puto... para fazer isso tens de estar num voice chat chavalo...')
            return False

        if state.voice is None:
            print("Playing")
            success = await ctx.invoke(self.summon)
            await self.bot.say("A preparar a festa...")
            if not success:
                return

        try:
            player = await state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next)
        except Exception as e:
            fmt = 'Occoreu um erro: ```py\n{}: {}\n```'
            await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
        else:
            player.volume = 0.6
            entry = VoiceEntry(ctx.message, player)
            await self.bot.say('Adicionada a lista de reproducao' + str(entry))
            await state.songs.put(entry)

    @commands.command(pass_context=True, no_pm=True)
    async def volume(self, ctx, value : int):

        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            if value >= 0 and value <= 300:
                print("Volume para : " + str(value))
                player = state.player
                player.volume = value / 100
                await self.bot.say('Volume a : {:.0%}'.format(player.volume))
            else:
                await self.bot.say('Deves achar que sou otario... (0-300)')
                return
        else:
            await self.bot.say('Mas estas burro ou que ? Nao estou a passar musica')

    @commands.command(pass_context=True, no_pm=True)
    async def pause(self, ctx):
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.pause()

    @commands.command(pass_context=True, no_pm=True)
    async def resume(self, ctx):
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.resume()

    @commands.command(pass_context=True, no_pm=True)
    async def stop(self, ctx):
        #Stops playing e sai o server apagando a queue

        server = ctx.message.server
        state = self.get_voice_state(server)

        if state.is_playing():
            player = state.player
            player.stop()

        try:
            state.audio_player.cancel()
            del self.voice_states[server.id]
            await state.voice.disconnect()
            await self.bot.say("Pronto acabou maltinha ... xau")
            await self.bot.say("Bernardo arranjas-me um cigarrinho ?")
        except:
            pass

    @commands.command(pass_context=True, no_pm=True)
    async def skip(self, ctx):

        state = self.get_voice_state(ctx.message.server)
        if not state.is_playing():
            await self.bot.say('Mas estas burro ou que ? Nao estou a passar musica')
            return

        voter = ctx.message.author
        if voter == state.current.requester:
            await self.bot.say('Foda-se decide-te...')
            state.skip()
        elif voter.id not in state.skip_votes:
            state.skip_votes.add(voter.id)
            total_votes = len(state.skip_votes)
            if total_votes >= 3:
                await self.bot.say('Okay.. vou mudar entao...')
                state.skip()
            else:
                await self.bot.say('Ok.. Mais alguem ? [{}/3]'.format(total_votes))
        else:
            await self.bot.say('Ja votaste para passar chavalo...')


    @commands.command(pass_context=True, no_pm=True)
    async def playing(self, ctx):
        #Shows info about the currently played song.
        state = self.get_voice_state(ctx.message.server)
        if state.current is None:
            await self.bot.say('Mas estas burro ou que ? Nao estou a passar musica')
        else:
            skip_count = len(state.skip_votes)
            await self.bot.say('A bombar {} [skips: {}/3]'.format(state.current, skip_count))

#Lista de comandos
@bot.command()
async def comandos():
    message = discord.Embed(
        title = 'Lista de comandos:',
        colour = 0x3498db,
        description=" \n !sobre         informacoes sobre o bot \n‍\n"
                    " !comandos         apresenta lista de todos os comandos \n‍\n"
                    " !pergunta         basicamente uma 8-Ball \n‍\n"
                    " !bitcoin          apresenta o valor das bitcoin em EUR\n‍\n"
                    " !escolhe [list]   escolhe uma das opcoes \n‍\n"
                    " !gif [search]     procura e seleciona ao acaso um gif \n‍\n"
                    " !pedra            pedra/papel/tesoura \n‍\n"
                    " !role             aplica roles a users \n‍\n"
                    "\n\n"
                    " !play [arg]       Inicia a reproducao de um link/pesquisa \n‍\n"
                    " !volume           permite alterar o volume do bot \n‍\n"
                    " !playing          identifica a musica actual \n‍\n"
                    " !skip             votacao para passar 'a frente' \n‍\n"
                    " !pause            pausa a musica actual \n‍\n"
                    " !resume           retoma a musica actual \n‍\n"
                    " !stop             informacoes sobre o bot \n‍\n"
                    " !pause            informacoes sobre o bot \n‍\n"
    )
    await bot.say(embed=message)

@bot.command()
async def pergunta():
    print("Pergunta")
    respostas = [
        'Desiste logo do curso se pensas assim',
        'Pergunta ao Indiano',
        'Isso e bueda facil',
        'Ja estas chumbado',
        'Gajas... yah.. Gajas... Hmm.. qual era a pergunta mesmo ?',
        'Ja chumbaste o modulo',
        'Estas é com saudades das minhas musicas']
    await bot.say(random.choice(respostas))

@bot.command()
async def escolhe(*choices : str):
    await bot.say(random.choice(choices))

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
    embed = discord.Embed(title="Chumbot", description="Basicamente o dario no corpo de um bot.", color=0x3498db, type="rich")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/471500310133604352/471500693539258386/qw.png")
    embed.add_field(name="Autores", value="Rusky#0001 and AnaG#2174")
    embed.add_field(name="Online desde:", value=lastboot);
    embed.add_field(name="Convite:", value="[Link](https://discordapp.com/oauth2/authorize?&client_id=471498303431770122&scope=bot&permissions=0)")
    embed.set_footer(text="Chumbados")
    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def gif(ctx,search):
    msgserver=ctx.message.channel
    gif_search = search
    resultquerrygif = g.random(tag=str(gif_search))
    resposta = requests.get(
    str(resultquerrygif.get('data',{}).get('image_original_url')),stream=True
    )
    await bot.send_file(msgserver,io.BytesIO(resposta.raw.read()),filename='isto_e_um_jpeg.gif')

@bot.event
async def on_message(message):
    global mesagee_id
    global msg_user


    if message.author == bot.user:
        return
    if 'chumbado' in message.content.lower():
        msg = 'Zero Bola C-H-U-M-B-A-D-O'.format(message)
        print(msg)
        await bot.send_message(message.channel,msg)
        await asyncio.sleep(2) # espera 2 segundos para enviar a proxima mensagem
        await bot.add_reaction(message,"👍")
    if message.content == "!role":
        embid = discord.Embed(
            title = 'Futuro depois da atec:',
            colour = 808080,
            description=" - McDonalds = 🍔‍\n‍\n"
                        " - Agricultor = 🥕\n‍\n"
                        " - Perito em codigo = 👳‍\n"
        )
        mebotmsg = await bot.send_message(message.channel, embed=embid)
        await bot.add_reaction(mebotmsg, "🍔")
        await bot.add_reaction(mebotmsg, "🥕")
        await bot.add_reaction(mebotmsg, "👳")

        mesagee_id = mebotmsg.id
        msg_user = message.author

    if message.content == "!pedra":
        embeed = discord.Embed(
            title = 'Escolhe:',
            colour = 0x3498db,
            description=" - Pedra = ✊‍\n‍\n"
                        " - Papel = 🖐\n‍\n"
                        " - Tesoura = 🖖"
        )
        botppt = await bot.send_message(message.channel, embed=embeed)
        await bot.add_reaction(botppt, "✊")
        await bot.add_reaction(botppt, "🖐")
        await bot.add_reaction(botppt, "🖖")

        ppt = ["Pedra","Papel","Tesoura"]
        global chosen
        chosen = random.choice(ppt)
        global played
        played = 1

    await bot.process_commands(message)


# quando for colocado um emoji, o bot reage á mensagem que postou o emoticon
@bot.event
async def on_reaction_add(reaction,user):
    channel = reaction.message.channel
    r_mnsg = reaction.message
    on_role = "off"
    game_status="off"


    if user == bot.user:
        return

    if reaction.emoji == "🍔" and mesagee_id==r_mnsg.id:
        on_role = "on"
        role = discord.utils.find(lambda r: r.name == "empregado do McDonalds", r_mnsg.server.roles)
        await bot.add_roles(user,role)
    if reaction.emoji == "🥕" and mesagee_id==r_mnsg.id:
        on_role = "on"
        role = discord.utils.find(lambda r: r.name == "Agricultor XPTO", r_mnsg.server.roles)
        await bot.add_roles(user,role)
    if reaction.emoji == "👳" and mesagee_id==r_mnsg.id:
        on_role = "on"
        role = discord.utils.find(lambda r: r.name == "indiano senpai", r_mnsg.server.roles)
        await bot.add_roles(user,role)

    if played == 1 :
        played = 0
        if reaction.emoji == "✊" and chosen == "Tesoura" or reaction.emoji=="🖐" and chosen == "Pedra" or reaction.emoji == "🖖" and chosen == "Papel":
            game_status="on"
            await bot.send_message(channel, "Ganhas-te")

        if reaction.emoji == "✊" and chosen == "Papel" or reaction.emoji=="🖐" and chosen == "Tesoura" or reaction.emoji == "🖖" and chosen == "Pedra":
            game_status="on"
            await bot.send_message(channel,'Perdes-te')

        if reaction.emoji == "✊" and chosen == "Pedra" or reaction.emoji=="🖐" and chosen == "Papel" or reaction.emoji == "🖖" and chosen == "Tesoura":
            game_status="on"
            await bot.send_message(channel,'Empate')

    if user != bot.user and game_status!="on" and on_role!="on":
        await bot.send_message(channel, '{} colocar {} é bué gay'.format(user.name, reaction.emoji))



@bot.event
async def on_reaction_remove(reaction,user):
    r_mnsg = reaction.message
    if reaction.emoji == "🍔" and mesagee_id==r_mnsg.id:
        role = discord.utils.find(lambda r: r.name == "empregado do McDonalds", r_mnsg.server.roles)
        await bot.remove_roles(user,role)
    if reaction.emoji == "🥕" and mesagee_id==r_mnsg.id:
        role = discord.utils.find(lambda r: r.name == "Agricultor XPTO", r_mnsg.server.roles)
        await bot.remove_roles(user,role)
    if reaction.emoji == "👳" and mesagee_id==r_mnsg.id:
        role = discord.utils.find(lambda r: r.name == "indiano senpai", r_mnsg.server.roles)
        await bot.remove_roles(user,role)

# quando alguem se junta ao servidor procura o channel com o nome 'general' e envia a mensagem
@bot.event
async def on_member_join(member):
    for channel in member.server.channels:
        if channel.name == 'general':
            msg = "{} juntou-se á lista de espera para comprar o kit da staples".format(member.mention)
            await bot.send_message(channel, msg)

# quando alguem sai procura o channel com o nome 'general' e envia a mensagem
@bot.event
async def on_member_remove(member):
    for channel in member.server.channels:
        if channel.name == 'general':
            msg = "{} desistiu.".format(member.mention)
            await bot.send_message(channel, msg)

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

bot.add_cog(Music(bot))
bot.run(TOKEN)
