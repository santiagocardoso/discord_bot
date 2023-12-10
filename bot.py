import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get
import random
import asyncio

from server import server

def run_discord_bot():
    with open("token.txt", "r") as file:
        TOKEN = file.read()
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

    @bot.event
    async def on_ready():
        activity = discord.Game(name="waffle maker | !ajuda", type=3)
        await bot.change_presence(activity=activity)
        print("Wafflinho está rodando!")
        try:
            synced = await bot.tree.sync()
            print(f"Sincronizado {len(synced)} comandos")
        except Exception as e:
            print(e)

    # Controles de servidor -----------------------------------------------

    @bot.event
    async def on_raw_reaction_add(payload):  # Da um cargo através da reação de um emoji
        guild = discord.utils.find(lambda g: g.id == payload.guild_id, bot.guilds)

        if payload.message_id == SUA_MESSAGE_ID or payload.message_id == SUA_MESSAGE_ID:
            if payload.emoji.name == '💨':
                role = get(guild.roles, name="MOVER")
                if role is not None:
                    member = discord.utils.find(lambda m: m.id == payload.user_id,
                                        guild.members)
                    if member is not None:
                        await member.add_roles(role)

    @bot.event
    async def on_raw_reaction_remove(payload):  # Remove um cargo através da reação de um emoji
        guild = discord.utils.find(lambda g: g.id == payload.guild_id, bot.guilds)

        if payload.message_id == SUA_MESSAGE_ID or payload.message_id == SUA_MESSAGE_ID:
            if payload.emoji.name == '💨':
                role = get(guild.roles, name="MOVER")
                if role is not None:
                    member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                    if member is not None:
                        await member.remove_roles(role)

    @bot.event
    async def on_member_join(member):
        guild = member.guild
        if guild.system_channel is not None:
            try:
                embed = discord.Embed(
                    title=f"Eae {member.name}!\nBem-vindo ao {guild.name}, dá uma olhadinha nas 📃┃regras",
                    color=0xf2bc66,
                )
                await guild.system_channel.send(f"{member.mention}")
                await guild.system_channel.send(embed=embed)

                if guild.id == SUA_GUILD_ID:
                    role = get(guild.roles, name="MEMBROS")
                    if role:
                        await member.add_roles(role)
                elif guild.id == SUA_GUILD_ID:
                    role = get(guild.roles, name="👨‍🌾 - Plebeus - 👨‍🌾")
                    if role:
                        await member.add_roles(role)
            except discord.errors.Forbidden:
                print("Bot não possui as permissões necessárias para lidar com cargos.")

    # Menu de ajuda -----------------------------------------------

    @bot.command(name="ajuda", aliases=["comandos"])
    async def ajuda(ctx):
        await ctx.send("``` ```")
        await ctx.send(
        "```👋 Oie eu sou o Wafflinho, o Bot oficial do Waffle!\n\nMeus comandos são:\n\nMostrar esse menu                 ┃ [!ajuda]\nOperações com dois números        ┃ [!soma], [!subt], [!mult], [!div]\nOperações com vários números      ┃ [!somas], [!subts]\nRoda um dado                      ┃ [!dado], [!rand]\nConsigo apagar várias mensagens   ┃ [!clear]\nConsigo falar algo que você mande ┃ [/fale], [!fale]\nInicio uma votação                ┃ [!poll]\nEntrar no canal de voz            ┃ [!join]\nSair do canal de voz              ┃ [!sair]```"
        )
        await ctx.send("``` ```")

    # Comandos divertidos -----------------------------------------------

    @bot.command(name="soma", aliases=["sum", "plus"])
    async def soma(ctx, x, y):
        result = int(x) + int(y)
        await ctx.send(f"{x} + {y} = {result}")

    @bot.command(name="soma_varios", aliases=["somas"])
    async def somas(ctx, *arr):
        result = 0
        for i in arr:
            result += int(i)
        await ctx.send(f"Deu {result}")

    @bot.command(name="subtrai", aliases=["subt", "menos"])
    async def subt(ctx, x, y):
        result = int(x) - int(y)
        await ctx.send(f"{x} - {y} = {result}")

    @bot.command(name="subtrai_varios", aliases=["subts"])
    async def subts(ctx, *arr):
        result = 0
        for i in arr:
            result -= int(i)
        await ctx.send(f"Deu {result}")

    @bot.command(name="dividir", aliases=["div"])
    async def div(ctx, x, y):
        result = float(x) / float(y)
        await ctx.send(f"{x} / {y} = {result}")

    @bot.command(name="mult")
    async def mult(ctx, x, y):
        result = int(x) * int(y)
        await ctx.send(f"{x} * {y} = {result}")

    @bot.command(name="dado", aliases=["roll"])
    async def dado(ctx):
        await ctx.channel.send(random.randint(1, 6))

    @bot.command(name="rand")
    async def rand(ctx, x):
        num = int(x)
        await ctx.channel.send(random.randint(1, num))

    @bot.command(name="fale", aliases=["say", "speak"])
    async def fale(ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)

    # Comandos úteis -----------------------------------------------

    @bot.command(aliases=["purge", "delete"])
    @commands.has_permissions(manage_messages=True)
    async def clear(ctx, amount: int = 0):
        if amount < 11:
            await ctx.message.delete()
            await ctx.channel.purge(limit=amount)
        else:
            await ctx.message.delete()
            await ctx.channel.send("Somente é possível deletar 10 mensagens por vez")
            await asyncio.sleep(2)
            await ctx.channel.purge(limit=1)

    @bot.command(name="poll", aliases=["vote", "votar"])
    async def poll(ctx, *, message):
        emb = discord.Embed(title="VOTAÇÃO", description=f"{message}", color=0xf2bc66)
        await ctx.message.delete()
        msg = await ctx.channel.send(embed=emb)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")

    @bot.command(name="entrar", aliases=["join"])
    async def join(ctx):
        if ctx.author.voice is None:
            await ctx.send("Você não está em um canal de voz!")
        else:
            voice_channel = ctx.author.voice.channel
            if ctx.voice_client is None:
                await voice_channel.connect()
                await ctx.send("Já já eu entro \U0001F61D")
            else:
                await ctx.voice_client.move_to(voice_channel)
                await ctx.send("Já já eu entro \U0001F61D")

    @bot.command(name="sair", aliases=["leave", "disconnect", "quit"])
    async def disconnect(ctx):
        await ctx.voice_client.disconnect()
        await ctx.send("Ok... Estou saindo \U0001F62D")

    # Comandos com barra -----------------------------------------------

    @bot.tree.command(name="oi")
    async def oi(interaction: discord.Interaction):
        await interaction.response.send_message(f"Oie {interaction.user.mention}!", ephemeral=True)

    @bot.tree.command(name="fale")
    @app_commands.describe(thing_to_say="O que eu deveria dizer?")
    async def say(interaction: discord.Interaction, thing_to_say: str):
        await interaction.response.send_message(f"`{thing_to_say}`")

    # Iniciar o bot -----------------------------------------------

    server()
    bot.run(TOKEN)

