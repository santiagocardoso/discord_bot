import discord
from discord import app_commands
from discord.ext import commands
import random
from server import server
import asyncio

def run_discord_bot():
    TOKEN = "YOUR_TOKEN"
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        activity = discord.Game(name="waffle maker | !ajuda", type=3)
        await bot.change_presence(activity=activity)
        print("Wafflinho está rodando!")
        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} command's")
        except Exception as e:
            print(e)
    
    @bot.command()
    async def oie(ctx):
        await ctx.send("Oie!")
    
    @bot.command()
    async def ajuda(ctx):
        await ctx.send("``` ```")
        await ctx.send("```👋 Oie eu sou o Wafflinho, o novo Bot oficial do Waffle!\n\nMeus comandos são:\n\nMostra esse menu                  ┃ [!ajuda]\nConsigo somar dois números        ┃ [!soma]\nSei somar vários números          ┃ [!somas]\nRoda um dado                      ┃ [!dado]\nConsigo apagar várias mensagens   ┃ [!clear]\nConsigo falar algo que você mande ┃ [/fale], [!fale]```")
        await ctx.send("``` ```")
    
    @bot.command()
    async def soma(ctx, x, y):
        result = int(x) + int(y)
        await ctx.send(f"{x} + {y} = {result}")
    
    @bot.command()
    async def somas(ctx, *arr):
        result = 0;
        for i in arr:
            result += int(i)
        await ctx.send(f"Deu {result}")
    
    @bot.command(name="dado")
    async def dado(ctx):
        await ctx.channel.send(random.randint(1, 6))
    
    @bot.command(aliases = ['purge', 'delete'])
    @commands.has_permissions(manage_messages = True)
    async def clear(ctx, amount: int = 0):
        if amount < 31:
            await ctx.message.delete()
            await ctx.channel.purge(limit = amount)
        else:
            await ctx.message.delete()
            await ctx.channel.send("Somente é possível deletar 30 mensagens por vez")
            await asyncio. sleep(2)
            await ctx.channel.purge(limit = 1)

    @bot.command()
    async def fale(ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)
    
    @bot.tree.command(name="oi")
    async def oi(interaction: discord.Interaction):
        await interaction.response.send_message(f"Oie {interaction.user.mention}!", ephemeral=True)
    
    @bot.tree.command(name="fale")
    @app_commands.describe(thing_to_say = "O que eu deveria dizer?")
    async def say(interaction: discord.Interaction, thing_to_say: str):
        await interaction.response.send_message(f"{interaction.user.name} disse: `{thing_to_say}`")
  
    server()
    bot.run(TOKEN)
    
