import discord
from discord.ext import commands

class Ajuda(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.group(name="ajuda", aliases=["comandos", "help"])
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:
            em = discord.Embed(title="Ajuda", description="Use w!ajuda <comandos> para mais informações.", color=0xf2bc66)

            em.add_field(name="Utilidade", value="clear, poll")
            em.add_field(name="Divertidos", value="dado, rand, fale, entrar, sair")
            em.add_field(name="Matemática", value="soma, subt, mult, div, somas, subts, mults")
            em.add_field(name="Economia", value="carteira, pedir, sacar, depositar, enviar, roubar, apostar, loja, comprar, mochila, vender, ranking")

            await ctx.send(embed=em)

    @help.command()
    async def clear(self, ctx):
        em = discord.Embed(title="Clear", description="Limpa o chat", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!clear <quantidade>")

        await ctx.send(embed=em)

    @help.command()
    async def poll(self, ctx):
        em = discord.Embed(title="Poll", description="Começa uma votação", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!poll <mensagem>")

        await ctx.send(embed=em)

    @help.command()
    async def dado(self, ctx):
        em = discord.Embed(title="🎲 Dado", description="Gira um dado de 1 até 6", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!dado")

        await ctx.send(embed=em)

    @help.command()
    async def rand(self, ctx):
        em = discord.Embed(title="Random", description="Gera um número aleatório", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!rand <máximo")

        await ctx.send(embed=em)

    @help.command()
    async def fale(self, ctx):
        em = discord.Embed(title="Fale", description="Falo algo que você digite", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!fale <mensagem>")

        await ctx.send(embed=em)

    @help.command()
    async def entrar(self, ctx):
        em = discord.Embed(title="Entrar", description="Entro no voice chat", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!entrar")

        await ctx.send(embed=em)

    @help.command()
    async def sair(self, ctx):
        em = discord.Embed(title="Sair", description="Saio do voice chat", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!sair")

        await ctx.send(embed=em)

    @help.command()
    async def soma(self, ctx):
        em = discord.Embed(title="Soma", description="Somo dois números", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!soma <x> <y>")

        await ctx.send(embed=em)

    @help.command()
    async def subt(self, ctx):
        em = discord.Embed(title="Subtração", description="Subtraio dois números", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!subt <x> <y>")

        await ctx.send(embed=em)

    @help.command()
    async def mult(self, ctx):
        em = discord.Embed(title="Multiplicação", description="Multiplico dois números", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!mult <x> <y>")

        await ctx.send(embed=em)

    @help.command()
    async def div(self, ctx):
        em = discord.Embed(title="Divisão", description="Divido dois números", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!div <x> <y>")

        await ctx.send(embed=em)

    @help.command()
    async def somas(self, ctx):
        em = discord.Embed(title="Somas", description="Somo vários números", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!somas <x> <y> <z> ...")

        await ctx.send(embed=em)

    @help.command()
    async def subts(self, ctx):
        em = discord.Embed(title="Subtrações", description="Subtraio vários números", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!subts <x> <y> <z> ...")

        await ctx.send(embed=em)

    @help.command()
    async def mults(self, ctx):
        em = discord.Embed(title="Multiplicações", description="Multiplico vários números", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!mults <x> <y> <z> ...")

        await ctx.send(embed=em)

    @help.command()
    async def carteira(self, ctx):
        em = discord.Embed(title="Carteira", description="Visualizar sua carteira", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!carteira")

        await ctx.send(embed=em)

    @help.command()
    async def pedir(self, ctx):
        em = discord.Embed(title="Pedir", description="Pedir dinheiro", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!pedir")

        await ctx.send(embed=em)

    @help.command()
    async def sacar(self, ctx):
        em = discord.Embed(title="📤 Sacar", description="Sacar dinheiro do cofre", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!sacar <quantia>")

        await ctx.send(embed=em)

    @help.command()
    async def depositar(self, ctx):
        em = discord.Embed(title="📥 Depositar", description="Depositar dinheiro do cofre", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!depositar <quantia>")

        await ctx.send(embed=em)

    @help.command()
    async def enviar(self, ctx):
        em = discord.Embed(title="💸 Enviar", description="Enviar dinheiro para outro membro", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!enviar <@membro> <quantia>")

        await ctx.send(embed=em)

    @help.command()
    async def roubar(self, ctx):
        em = discord.Embed(title="🎰 Roubar", description="Roubar dinheiro de outro membro", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!roubar <@membro> <quantia>")

        await ctx.send(embed=em)

    @help.command()
    async def apostar(self, ctx):
        em = discord.Embed(title="🎰 Apostar", description="Aposte dinheiro em uma máquina de cassino, somente aceitamos dinheiro vivo", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!apostar <quantia>")

        await ctx.send(embed=em)

    @help.command()
    async def loja(self, ctx):
        em = discord.Embed(title="Loja", description="Abre a loja", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!loja")

        await ctx.send(embed=em)

    @help.command()
    async def comprar(self, ctx):
        em = discord.Embed(title="Comprar", description="Comprar itens da loja", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!comprar <item> <quantidade>")

        await ctx.send(embed=em)

    @help.command()
    async def mochila(self, ctx):
        em = discord.Embed(title="Mochila", description="Abre sua mochila", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!mochila")

        await ctx.send(embed=em)

    @help.command()
    async def vender(self, ctx):
        em = discord.Embed(title="Vender", description="Vender itens da sua mochila", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!vender <item> <quantidade>")

        await ctx.send(embed=em)

    @help.command()
    async def ranking(self, ctx):
        em = discord.Embed(title="Ranking", description="Mostra o ranking de economias", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!ranking")

        await ctx.send(embed=em)


async def setup(bot):
    await bot.add_cog(Ajuda(bot))
