import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get
import random
import asyncio
# import youtube_dl

from server import server

async def run_discord_bot():
    with open("token.txt", "r") as file:
        TOKEN = file.read()
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=["w!", "<", ">"], intents=intents, help_command=None)


    @bot.event
    async def on_ready():
        bot.loop.create_task(mudar_status())
        # activity = discord.Game(name=f"waffle maker | !ajuda", type=3)
        # activity = discord.Game(name=f"waffle maker em {len(bot.guilds)} servers | !ajuda", type=3)
        # await bot.change_presence(activity=activity)
        print("Wafflinho está rodando!")
        try:
            synced = await bot.tree.sync()
            print(f"Sincronizado {len(synced)} comandos")
        except Exception as e:
            print(e)


    async def mudar_status():
        await bot.wait_until_ready()

        todos_status = ["waffle maker | w!help", f"em {len(bot.guilds)} servers | w!help"]

        while not bot.is_closed():
            status = random.choice(todos_status)
            await bot.change_presence(activity=discord.Game(name=status))
            await asyncio.sleep(10)

    # Controles de servidor -----------------------------------------------

    @bot.event
    async def on_raw_reaction_add(payload):  # Da um cargo através da reação de um emoji
        guild = discord.utils.find(lambda g: g.id == payload.guild_id, bot.guilds)

        if payload.message_id == SEU_MSG_ID_AQUI or payload.message_id == SEU_MSG_ID_AQUI:
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

        if payload.message_id == SEU_MSG_ID_AQUI or payload.message_id == SEU_MSG_ID_AQUI:
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

                if guild.id == SEU_GUILD_ID_AQUI:
                    role = get(guild.roles, name="MEMBROS")
                    if role:
                        await member.add_roles(role)
                elif guild.id == SEU_GUILD_ID_AQUI:
                    role = get(guild.roles, name="👨‍🌾 - Plebeus - 👨‍🌾")
                    if role:
                        await member.add_roles(role)
            except discord.errors.Forbidden:
                print("Bot não possui as permissões necessárias para lidar com cargos.")

    # Carregar comandos -----------------------------------------------

    await bot.load_extension('comandos_ajuda')
    await bot.load_extension('comandos_divertido')
    await bot.load_extension('comandos_utilitario')
    await bot.load_extension('comandos_economia')
    await bot.load_extension('comandos_musica')

    @bot.event
    async def on_voice_state_update(member, before, after):
        if before.channel is not None and len(before.channel.members) == 1 and before.channel.guild.voice_client is not None:
            await before.channel.guild.voice_client.disconnect()

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
    return bot, TOKEN
