import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get
import random
import youtube_dl
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

        if payload.message_id == SEU_ID_DA_MENSAGEM or payload.message_id == SEU_ID_DA_MENSAGEM:
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

        if payload.message_id == SEU_ID_DA_MENSAGEM or payload.message_id == SEU_ID_DA_MENSAGEM:
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

                if guild.id == SEU_ID_DA_GUILDA:
                    role = get(guild.roles, name="MEMBROS")
                    if role:
                        await member.add_roles(role)
                elif guild.id == SEU_ID_DA_GUILDA:
                    role = get(guild.roles, name="👨‍🌾 - Plebeus - 👨‍🌾")
                    if role:
                        await member.add_roles(role)
            except discord.errors.Forbidden:
                print("Bot does not have the necessary permissions to manage roles.")

    # Menu de ajuda -----------------------------------------------

    @bot.command(name="ajuda", aliases=["comandos"])
    async def ajuda(ctx):
        await ctx.send("``` ```")
        await ctx.send(
        "```👋 Oie eu sou o Wafflinho, o Bot oficial do Waffle!\n\nMeus comandos são:\n\nMostrar esse menu                 ┃ [!ajuda]\nOperações com dois números        ┃ [!soma], [!subt], [!mult], [!div]\nOperações com vários números      ┃ [!somas], [!subts]\nRoda um dado                      ┃ [!dado], [!rand]\nConsigo apagar várias mensagens   ┃ [!clear]\nConsigo falar algo que você mande ┃ [/fale], [!fale]\nInicio uma votação                ┃ [!poll]```"
        )
        await ctx.send("```\U0001F3B5 Música:\n\nEntrar no canal de voz ┃ [!join]\nTocar uma música       ┃ [!play]\nPausar                 ┃ [!pausar]\nDespausar              ┃ [!despausar]\nSair do canal de voz   ┃ [!stop]```")
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

    # Tocar música -----------------------------------------------

    @bot.command(name="join", aliases=["entrar"])
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

    @bot.command(name="play", aliases=["tocar"])
    async def play(ctx, url):
        ctx.voice_client.stop()
        FFMPEG_OPTIONS={'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        YDL_OPTIONS = {'format': 'bestaudio'}

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            if 'formats' in info:
                best_audio = min(info['formats'], key=lambda x: int(x.get('abr', 0)))
                url2 = best_audio['url']
                source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
                ctx.voice_client.play(source)
            else:
                await ctx.send("Não foi possível encontrar o formato de áudio adequado para este vídeo.")

    @bot.command(name="stop", aliases=["leave", "disconnect", "sair", "parar"])
    async def disconnect(ctx):
        await ctx.voice_client.disconnect()
        await ctx.send("Ok!! Estou desligando \U0001F62D")

    @bot.command(name="pause", aliases=["pausar"])
    async def pause(ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            await ctx.send("\u23F8 Pausando a reprodução.")
            ctx.voice_client.pause()
        else:
            await ctx.send("O bot não está reproduzindo ou não está em um canal de voz.")

    @bot.command(name="resume", aliases=["resumir", "voltar", "unpause", "despausar"])
    async def resume(ctx):
        if ctx.voice_client and ctx.voice_client.is_paused():
            await ctx.send("\u25B6 Resumindo a reprodução.")
            ctx.voice_client.resume()
        else:
            await ctx.send("O bot não está pausado ou não está em um canal de voz.")

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
