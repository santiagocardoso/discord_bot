import asyncio
import random
import discord
from discord.ext import commands

class Divertido(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="soma", aliases=["sum", "plus"])
    async def soma(self, ctx, x, y):
        result = int(x) + int(y)
        await ctx.send(f"{x} + {y} = {result}")


    @commands.command(name="soma_varios", aliases=["somas"])
    async def somas(self, ctx, *arr):
        result = 0
        for i in arr:
            result += int(i)
        await ctx.send(f"Deu {result}")


    @commands.command(name="subtrai", aliases=["subt", "menos"])
    async def subt(self, ctx, x, y):
        result = int(x) - int(y)
        await ctx.send(f"{x} - {y} = {result}")


    @commands.command(name="subtrai_varios", aliases=["subts"])
    async def subts(self, ctx, *arr):
        result = 0
        for i in arr:
            result -= int(i)
        await ctx.send(f"Deu {result}")


    @commands.command(name="mult_varios", aliases=["mults"])
    async def mults(self, ctx, *arr):
        result = 1
        for i in arr:
            result *= int(i)
        await ctx.send(f"Deu {result}")


    @commands.command(name="dividir", aliases=["div"])
    async def div(self, ctx, x, y):
        result = float(x) / float(y)
        await ctx.send(f"{x} / {y} = {result}")


    @commands.command(name="mult")
    async def mult(self, ctx, x, y):
        result = int(x) * int(y)
        await ctx.send(f"{x} * {y} = {result}")


    @commands.command(name="dado", aliases=["roll"])
    async def dado(self, ctx):
        await ctx.channel.send(random.randint(1, 6))


    @commands.command(name="rand")
    async def rand(self, ctx, x):
        num = int(x)
        await ctx.channel.send(random.randint(1, num))


    @commands.command(name="fale", aliases=["say", "speak"])
    async def fale(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)


async def setup(bot):
    await bot.add_cog(Divertido(bot))
