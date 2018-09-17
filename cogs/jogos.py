import random
from random import randint

class Jogo:
    def __init__(self, players):
        self.players = players

    async def comeco(self, bot, message):
        pass

    async def partida(self, bot, message):
        pass

    def quem_joga(self):
        pass

    async def player_jogada(self, bot, message):
        pass

    def end_game(self):
        pass


class JogodaGalinha(Jogo):
    def __init__(self, players):
        Jogo.__init__(self, players)
        self.tabuleiro = [' ']*9
        self.vez = players[0]
        self.final = False
        self.player = 0
        self.repeat = 0

    async def comeco(self, bot, message):
        await self.partida(bot, message)

    async def partida(self, bot, message):
        tabuleiro = self.tabuleiro

        l = ''
        l += str(self.players[0]) + ' vs ' + str(self.players[1])

        l += '\n```'
        l += '   |   |' + '\n'
        l += ' ' + tabuleiro[0] + ' | ' + tabuleiro[1] + ' | ' + tabuleiro[2] + '\n'
        l += '   |   |' + '\n'
        l += '-----------' + '\n'
        l += '   |   |' + '\n'
        l += ' ' + tabuleiro[3] + ' | ' + tabuleiro[4] + ' | ' + tabuleiro[5] + '\n'
        l += '   |   |' + '\n'
        l += '-----------' + '\n'
        l += '   |   |' + '\n'
        l += ' ' + tabuleiro[6] + ' | ' + tabuleiro[7] + ' | ' + tabuleiro[8] + '\n'
        l += '   |   |' + '\n'
        l += '```\n'


        if not self.final:
            l +=  "{} é a tua vez de jogar".format(message.author.mention)


        await bot.send_message(message.channel, l)



    async def player_jogada(self, bot, message):
        i = int(message.content.split()[1])

        if i > 9 or i < 1 or self.tabuleiro[i - 1] != ' ' :
            await bot.send_message(message.channel, 'Não sabes contar? O que estas a fazer na atec então?')
            return


        if self.vez == self.players[0]:
            self.tabuleiro[i - 1] = 'X'
            self.player = 1
            self.repeat=0

        w = self.check_win()
        if self.player == 1  and w == False:
            for i in range(0,9):
                print(i)
                if self.tabuleiro[i] == 'O':

                    if i == 4 or i == 1 or i == 7:
                        print("b")
                        if self.tabuleiro[i+1] == 'O' and self.tabuleiro[i-1] == ' ':
                            print("v")
                            self.tabuleiro[i-1] = 'O'
                            break

                        if self.tabuleiro[i-1] == 'O' and self.tabuleiro[i+1] == ' ':
                            print("t")
                            self.tabuleiro[i+1] = 'O'
                            break


                        if i == 3 or i == 1 or i == 6 or i == 2 or i == 5 or i == 8:
                            if self.tabuleiro[i-2] == 'O' and self.tabuleiro[i-1] == ' ':
                                self.tabuleiro[i-1] = 'O'
                                print("f")
                                break

                            if self.tabuleiro[i+2] == 'O' and self.tabuleiro[i+1] == ' ':
                                print("m")
                                self.tabuleiro[i+1] = 'O'
                                break


                    if i==4:
                        print("a")
                        if self.tabuleiro[i-4] == 'O' and self.tabuleiro[i+4] == ' ':
                            print("z")
                            self.tabuleiro[i+4] = 'O'
                            break

                        if self.tabuleiro[i+4] == 'O' and self.tabuleiro[i-4] == ' ':
                            print("x")
                            self.tabuleiro[i-4] = 'O'
                            break

                        if self.tabuleiro[i-2] == 'O' and self.tabuleiro[i+2] == ' ':
                            print("y")
                            self.tabuleiro[i+2] = 'O'
                            break

                        if self.tabuleiro[i+2] == 'O' and self.tabuleiro[i-2] == ' ':
                            print("w")
                            self.tabuleiro[i-2] = 'O'
                            break

                        else:
                            continue

                if self.tabuleiro[i] == 'X':


                    if i == 3 or i ==4 or i ==5:

                        if self.tabuleiro[i-3] == 'X' and i+3<9 and self.tabuleiro[i+3] == ' ':
                            print("u")
                            self.tabuleiro[i+3] = 'O'
                            break

                        if i+3<9:
                            print("c")
                            if self.tabuleiro[i+3] == 'X' and i+3<=8 and i-3>0 and self.tabuleiro[i-3] == ' ':
                                self.tabuleiro[i-3] = 'O'
                                break

                    if i == 4 or i == 1 or i == 7:
                        print("b")
                        if self.tabuleiro[i+1] == 'X' and self.tabuleiro[i-1] == ' ':
                            print("v")
                            self.tabuleiro[i-1] = 'O'
                            break

                        if self.tabuleiro[i-1] == 'X' and self.tabuleiro[i+1] == ' ':
                            print("t")
                            self.tabuleiro[i+1] = 'O'
                            break


                        if self.tabuleiro[i-2] == 'X' and self.tabuleiro[i+2] == ' ':
                            self.tabuleiro[i+2] = 'O'
                            print("f")
                            break

                        if self.tabuleiro[i+2] == 'X' and self.tabuleiro[i-2] == ' ':
                            print("m")
                            self.tabuleiro[i-2] = 'O'
                            break


                    if i==4:
                        print("a")
                        if self.tabuleiro[i-4] == 'X' and self.tabuleiro[i+4] == ' ':
                            print("z")
                            self.tabuleiro[i+4] = 'O'
                            break

                        if self.tabuleiro[i+4] == 'X' and self.tabuleiro[i-4] == ' ':
                            print("x")
                            self.tabuleiro[i-4] = 'O'
                            break

                        if self.tabuleiro[i-2] == 'X' and self.tabuleiro[i+2] == ' ':
                            print("y")
                            self.tabuleiro[i+2] = 'O'
                            break

                        if self.tabuleiro[i+2] == 'X' and self.tabuleiro[i-2] == ' ':
                            print("w")
                            self.tabuleiro[i-2] = 'O'
                            break

                        else:
                            continue

                    if i!=0 or i!=1:
                        if self.tabuleiro[i-2] == 'X' and self.tabuleiro[i-1] == ' ':
                            print("l")
                            self.tabuleiro[i-1] = 'O'
                            break

                    if i!=8 and i!=7:
                        if self.tabuleiro[i+2] == 'X' and self.tabuleiro[i+1] == ' ':
                            print("q")
                            self.tabuleiro[i+1] = 'O'
                            break


                if i==8:
                    while self.repeat==0:
                        bot_space = randint(0,8)
                        if self.tabuleiro[bot_space] != ' ':
                           self.repeat=0
                           self.player =1
                        else:
                            print("paras aqui")
                            self.repeat=1
                            self.player=0
                            self.tabuleiro[bot_space] = 'O'



        await self.partida(bot, message)

        w = self.check_win()
        if w != False:
            self.final = True
            if w == 'X' or w == 'O': await bot.send_message(message.channel, w + ' wins.')
            else: await bot.send_message(message.channel, 'Tie.')

    def check_win(self):
        t = self.tabuleiro
        if t[0] == t[1] and t[0] == t[2]:
            if t[0] == 'X': return 'X'
            elif t[0] == 'O': return 'O'
        if t[3] == t[4] and t[3] == t[5]:
            if t[3] == 'X': return 'X'
            elif t[3] == 'O': return 'O'
        if t[6] == t[7] and t[6] == t[8]:
            if t[6] == 'X': return 'X'
            elif t[6] == 'O': return 'O'

        if t[0] == t[3] and t[0] == t[6]:
            if t[0] == 'X': return 'X'
            elif t[0] == 'O': return 'O'
        if t[1] == t[4] and t[1] == t[7]:
            if t[1] == 'X': return 'X'
            elif t[1] == 'O': return 'O'
        if t[2] == t[5] and t[2] == t[8]:
            if t[2] == 'X': return 'X'
            elif t[2] == 'O': return 'O'

        if t[0] == t[4] and t[0] == t[8]:
            if t[4] == 'X': return 'X'
            elif t[4] == 'O': return 'O'
        if t[2] == t[4] and t[2] == t[6]:
            if t[4] == 'X': return 'X'
            elif t[4] == 'O': return 'O'

        if ' ' not in t: return 'T' # tie

        return False

    def quem_joga(self):
        return self.vez

    def end_game(self):
        return self.final
