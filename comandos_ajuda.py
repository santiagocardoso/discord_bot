import discord
from discord.ext import commands

class Ajuda(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.group(name="ajuda", aliases=["comandos", "help", "h"])
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:
            em = discord.Embed(title="Ajuda", description="Não utilize comandos muito depressa, pois eu posso não entender o que você quis fazer.\n\nUse ''<ajuda nome_comando'' para mais informações.", color=0xf2bc66)

            em.add_field(name="Utilidade", value="clear, poll, sort, sync") # , entrar, sair")
            em.add_field(name="Divertidos", value="dado, rand, fale")
            em.add_field(name="Matemática", value="soma, subt, mult, div, somas, subts, mults")
            em.add_field(name="Economia", value="carteira, pedir, cavar, sacar, depositar, enviar, roubar, furtar, apostar, minerar, pescar, loja, comprar, mochila, vender, ranking")
            em.add_field(name="Nível", value="xp")

            await ctx.send(embed=em)

    @help.command()
    async def clear(self, ctx):
        em = discord.Embed(title="🗑️ Clear", description="Limpa o chat", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="<clear <quantidade>")

        await ctx.send(embed=em)

    @help.command()
    async def poll(self, ctx):
        em = discord.Embed(title="📋 Poll", description="Começa uma votação", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="<poll <mensagem>")

        await ctx.send(embed=em)

    @help.command()
    async def sort(self, ctx):
        em = discord.Embed(title="🗑️ Sort", description="Sorteia um mapa", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="<sort")

        await ctx.send(embed=em)

    @help.command()
    async def sync(self, ctx):
        em = discord.Embed(title="🌀 Sync", description="Sincronizar comandos de barra", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="<sync")

        await ctx.send(embed=em)

    @help.command()
    async def dado(self, ctx):
        em = discord.Embed(title="🎲 Dado", description="Gira um dado de 1 até 6", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="<dado")

        await ctx.send(embed=em)

    @help.command()
    async def rand(self, ctx):
        em = discord.Embed(title="🎲 Random", description="Gera um número aleatório", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="<rand <máximo")

        await ctx.send(embed=em)

    @help.command()
    async def fale(self, ctx):
        em = discord.Embed(title="🗣️ Fale", description="Falo algo que você digite", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="<fale <mensagem>")

        await ctx.send(embed=em)

    @help.command()
    async def entrar(self, ctx):
        em = discord.Embed(title="🟢 Entrar", description="Entro no voice chat", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="<entrar")

        await ctx.send(embed=em)

    @help.command()
    async def sair(self, ctx):
        em = discord.Embed(title="🔴 Sair", description="Saio do voice chat", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="<sair")

        await ctx.send(embed=em)

    @help.command()
    async def soma(self, ctx):
        em = discord.Embed(title="➕ Soma", description="Somo dois números", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="<soma <x> <y>")

        await ctx.send(embed=em)

    @help.command()
    async def subt(self, ctx):
        em = discord.Embed(title="➖ Subtração", description="Subtraio dois números", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="<subt <x> <y>")

        await ctx.send(embed=em)

    @help.command()
    async def mult(self, ctx):
        em = discord.Embed(title="✖️ Multiplicação", description="Multiplico dois números", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="<mult <x> <y>")

        await ctx.send(embed=em)

    @help.command()
    async def div(self, ctx):
        em = discord.Embed(title="➗ Divisão", description="Divido dois números", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="<div <x> <y>")

        await ctx.send(embed=em)

    @help.command()
    async def somas(self, ctx):
        em = discord.Embed(title="➕ Somas", description="Somo vários números", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="<somas <x> <y> <z> ...")

        await ctx.send(embed=em)

    @help.command()
    async def subts(self, ctx):
        em = discord.Embed(title="➖ Subtrações", description="Subtraio vários números", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="<subts <x> <y> <z> ...")

        await ctx.send(embed=em)

    @help.command()
    async def mults(self, ctx):
        em = discord.Embed(title="✖️ Multiplicações", description="Multiplico vários números", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="<mults <x> <y> <z> ...")

        await ctx.send(embed=em)

    @help.command()
    async def carteira(self, ctx):
        em = discord.Embed(title="💵 Carteira", description="Visualizar a carteira de um usuário", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="<carteira [@membro]")

        await ctx.send(embed=em)

    @help.command()
    async def pedir(self, ctx):
        em = discord.Embed(title="💵 Pedir", description="Pedir dinheiro", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="<pedir")

        await ctx.send(embed=em)

    @help.command()
    async def cavar(self, ctx):
        em = discord.Embed(title="🪨 Cavar", description="Cavar itens", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="<cavar")

        await ctx.send(embed=em)

    @help.command()
    async def sacar(self, ctx):
        em = discord.Embed(title="📤 Sacar", description="Sacar dinheiro do cofre", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="<sacar <quantia>")

        await ctx.send(embed=em)

    @help.command()
    async def depositar(self, ctx):
        em = discord.Embed(title="📥 Depositar", description="Depositar dinheiro do cofre", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="<depositar <quantia>")

        await ctx.send(embed=em)

    @help.command()
    async def enviar(self, ctx):
        em = discord.Embed(title="💸 Enviar", description="Enviar dinheiro para outro membro", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="<enviar <@membro> <quantia>")

        await ctx.send(embed=em)

    @help.command()
    async def roubar(self, ctx):
        em = discord.Embed(title="🐱‍👤 Roubar", description="Roubar dinheiro do cofre de outro membro, possui um cooldown de 24h", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="<roubar <@membro>")

        await ctx.send(embed=em)

    @help.command()
    async def furtar(self, ctx):
        em = discord.Embed(title="🐱‍👤 Furtar", description="Furtar dinheiro da carteira de outro membro, possui um cooldown de 15min", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="<furtar <@membro>")

        await ctx.send(embed=em)

    @help.command()
    async def apostar(self, ctx):
        em = discord.Embed(title="🎰 Apostar", description="Aposte dinheiro em uma máquina de cassino, somente aceitamos dinheiro vivo", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="<apostar <quantia>")

        await ctx.send(embed=em)

    @help.command()
    async def minerar(self, ctx):
        em = discord.Embed(title="⛏️ Minerar", description="Utilize suas picaretas para encontrar itens", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="<minerar")

        await ctx.send(embed=em)

    @help.command()
    async def pescar(self, ctx):
        em = discord.Embed(title="🎣 Pescar", description="Utilize suas varas de pesca para encontrar itens", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="<pescar")

        await ctx.send(embed=em)

    @help.command()
    async def loja(self, ctx):
        em = discord.Embed(title="🛍️ Loja", description="Abre a loja", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="<loja")

        await ctx.send(embed=em)

    @help.command()
    async def comprar(self, ctx):
        em = discord.Embed(title="🛍️ Comprar", description="Comprar itens da loja", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="<comprar <item> <quantidade>")

        await ctx.send(embed=em)

    @help.command()
    async def mochila(self, ctx):
        em = discord.Embed(title="🎒 Mochila", description="Abre a mochila de um usuário", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="<mochila [@membro]")

        await ctx.send(embed=em)

    @help.command()
    async def vender(self, ctx):
        em = discord.Embed(title="🛍️ Vender", description="Vender itens da sua mochila", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="<vender <item> <quantidade>")

        await ctx.send(embed=em)

    @help.command()
    async def usar(self, ctx):
        em = discord.Embed(title="🎫 Usar", description="Usar itens da sua mochila, possui um cooldown de 8h", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="<usar <item> <quantidade>")

        await ctx.send(embed=em)

    @help.command()
    async def ranking(self, ctx):
        em = discord.Embed(title="🏆 Ranking", description="Mostra o ranking de economias", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="<ranking [tamanho]")

        await ctx.send(embed=em)

    @help.command()
    async def xp(self, ctx):
        em = discord.Embed(title="🍀 XP", description="Mostra o XP de um usuário", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="<xp [@membro]")

        await ctx.send(embed=em)


async def setup(bot):
    await bot.add_cog(Ajuda(bot))
