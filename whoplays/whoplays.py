import discord
from discord.ext import commands
import operator


class WhoPlays:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def quemjoga(self, ctx, *, game):
        if len(game) <= 2:
            await self.bot.say("Sao precisos no minimo 3 characteres para a pesquisa")
            return

        user = ctx.message.author
        server = ctx.message.server
        members = server.members

        playing_game = ""
        count_playing = 0
        for member in members:
            if not member:
                continue
            if not member.game or not member.game.name:
                continue
            if member.bot:
                continue
            if game.lower() in member.game.name.lower():
                count_playing += 1
                if count_playing <= 15:
                    playing_game += "▸ {} ({})\n".format(member.name,
                                                         member.game.name)

        if playing_game == "":
            await self.bot.say("Ninguem esta a jogar essa merda.")
        else:
            msg = playing_game
            em = discord.Embed(description=msg, colour=0x3498db)
            if count_playing > 15:
                showing = "(A mostrar 15/{})".format(count_playing)
            else:
                showing = "({})".format(count_playing)
            text = "Estes estao a jogar {} inves de trabalhar".format(game)
            text += ":\n{}".format(showing)
            em.set_author(name=text)
            await self.bot.say(embed=em)

    @commands.command(pass_context=True, no_pm=True)
    async def topgames(self, ctx):
        user = ctx.message.author
        server = ctx.message.server
        members = server.members

        freq_list = {}
        for member in members:
            if not member:
                continue
            if not member.game or not member.game.name:
                continue
            if member.bot:
                continue
            if member.game.name not in freq_list:
                freq_list[member.game.name] = 0
            freq_list[member.game.name] += 1

        sorted_list = sorted(freq_list.items(),
                             key=operator.itemgetter(1),
                             reverse=True)

        if not freq_list:
            await self.bot.say("Surpreendentemente ninguem esta a jogar nada ")
        else:
            # create display
            msg = ""
            max_games = min(len(sorted_list), 10)
            for i in range(max_games):
                game, freq = sorted_list[i]
                msg += "▸ {}: __{}__\n".format(game, freq_list[game])

            em = discord.Embed(description=msg, colour=0x3498db)
            em.set_author(name="Estes sao os jogos mais jogados neste servidor")
            await self.bot.say(embed=em)

def setup(bot):
    n = WhoPlays(bot)
    bot.add_cog(n)
