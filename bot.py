import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get

import random

from server import server
import asyncio

"""
    if needed to get emoji icon in the terminal
    print(payload.emoji.name)
"""

def run_discord_bot():
    TOKEN = "YOUR_TOKEN"
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix = "!", intents = intents)

    @bot.event
    async def on_ready():
        activity = discord.Game(name = "waffle maker | !ajuda", type=3)
        await bot.change_presence(activity=activity)
        print("Wafflinho está rodando!")
        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} command's")
        except Exception as e:
            print(e)
          
    @bot.event
    async def on_raw_reaction_add(payload): # da um cargo com reacao de emoji
        guild = discord.utils.find(lambda g: g.id == payload.guild_id, bot.guilds)

        if payload.message_id == YOUR_MESSAGE_ID:
            if payload.emoji.name == '🎲':
                role = get(guild.roles, name = "RANDOM")
                if role is not None:
                    member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                    if member is not None:
                        await member.add_roles(role)
            elif payload.emoji.name == '💨':
                role = get(guild.roles, name = "MOVER")
                if role is not None:
                    member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                    if member is not None:
                        await member.add_roles(role)
            elif payload.emoji.name == '📱':
                role = get(guild.roles, name = "CELULAR")
                if role is not None:
                    member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                    if member is not None:
                        await member.add_roles(role)
                  
    @bot.event
    async def on_raw_reaction_remove(payload): # remove um cargo com reacao de emoji
        guild = discord.utils.find(lambda g: g.id == payload.guild_id, bot.guilds)

        if payload.message_id == YOUR_MESSAGE_ID:
            if payload.emoji.name == '🎲':
                role = get(guild.roles, name = "RANDOM")
                if role is not None:
                    member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                    if member is not None:
                        await member.remove_roles(role)
            elif payload.emoji.name == '💨':
                role = get(guild.roles, name = "MOVER")
                if role is not None:
                    member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                    if member is not None:
                        await member.remove_roles(role)
            elif payload.emoji.name == '📱':
                role = get(guild.roles, name = "CELULAR")
                if role is not None:
                    member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                    if member is not None:
                        await member.remove_roles(role)
  
    @bot.event
    async def on_member_join(member):
        channel = bot.get_channel(YOUR_CHANNEL_ID)
        embed = discord.Embed(title=f"Eae {member.name}!\nBem-vindo ao {member.guild.name}, dá uma olhadinha no  📃┃regras e no  👾┃bot", color=0xf2bc66)
        await channel.send(f"{member.mention}")
        await channel.send(embed=embed)
        role = get(member.guild.roles, name = "MEMBROS")
        await member.add_roles(role)
    
    @bot.command(name = "ajuda")
    async def ajuda(ctx):
        await ctx.send("``` ```")
        await ctx.send("```👋 Oie eu sou o Wafflinho, o novo Bot oficial do Waffle!\n\nMeus comandos são:\n\nMostra esse menu                  ┃ [!ajuda]\nOperações com dois números        ┃ [!soma], [!subt], [!mult], [!div]\nOperações com vários números      ┃ [!somas], [!subts]\nRoda um dado                      ┃ [!dado], [!rand]\nConsigo apagar várias mensagens   ┃ [!clear]\nConsigo falar algo que você mande ┃ [/fale], [!fale]\nInicio uma votação                ┃ [!poll]```")
        await ctx.send("``` ```")
  
    @bot.command(name = "soma", aliases = ["sum", "plus"])
    async def soma(ctx, x, y):
        result = int(x) + int(y)
        await ctx.send(f"{x} + {y} = {result}")

    @bot.command(name = "soma_varios", aliases = ["somas"])
    async def somas(ctx, *arr):
        result = 0;
        for i in arr:
            result += int(i)
        await ctx.send(f"Deu {result}")

    @bot.command(name = "subtrai", aliases = ["subt", "menos"])
    async def subt(ctx, x, y):
        result = int(x) - int(y)
        await ctx.send(f"{x} - {y} = {result}")

    @bot.command(name = "subtrai_varios", aliases = ["subts"])
    async def subts(ctx, *arr):
        result = 0;
        for i in arr:
            result -= int(i)
        await ctx.send(f"Deu {result}")

    @bot.command(name = "dividir", aliases = ["div"])
    async def div(ctx, x, y):
        result = float(x) / float(y)
        await ctx.send(f"{x} / {y} = {result}")

    @bot.command(name = "mult")
    async def mult(ctx, x, y):
        result = int(x) * int(y)
        await ctx.send(f"{x} * {y} = {result}")
      
    @bot.command(name = "dado", aliases = ["roll"])
    async def dado(ctx):
        await ctx.channel.send(random.randint(1, 6))

    @bot.command(name = "rand")
    async def rand(ctx, x):
        num = int(x)
        await ctx.channel.send(random.randint(1, num))
    
    @bot.command(aliases = ["purge", "delete"])
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

    @bot.command(name = "fale", aliases = ["say", "speak"])
    async def fale(ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)

    @bot.command(name = "poll", aliases = ["vote", "votar"])
    async def poll(ctx, *, message):
        emb = discord.Embed(title = "VOTAÇÃO", description = f"{message}", color = 0xf2bc66)
        await ctx.message.delete()
        msg = await ctx.channel.send(embed = emb)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")
    
    @bot.tree.command(name = "oi")
    async def oi(interaction: discord.Interaction):
        await interaction.response.send_message(f"Oie {interaction.user.mention}!", ephemeral = True)
    
    @bot.tree.command(name = "fale")
    @app_commands.describe(thing_to_say = "O que eu deveria dizer?")
    async def say(interaction: discord.Interaction, thing_to_say: str):
        await interaction.response.send_message(f"{interaction.user.name} disse: `{thing_to_say}`")
  
    server()
    bot.run(TOKEN)
