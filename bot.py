import os
import discord
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands, tasks
from discord.utils import get
import random
import asyncio
import aiohttp
# import youtube_dl
from server import server

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
TWITCH_APP_TOKEN = os.getenv("TWITCH_APP_TOKEN")
TWITCH_USER_ID = os.getenv("TWITCH_USER_ID")
TWITCH_USERNAME = "santcar7"
DISCORD_WEBHOOK_URL_WAFFLE = os.getenv("DISCORD_WEBHOOK_URL_WAFFLE")
DISCORD_WEBHOOK_URL_MIAU = os.getenv("DISCORD_WEBHOOK_URL_MIAU")

was_online = False

async def run_discord_bot():
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=["<", "w!", ">"], intents=intents, help_command=None)

    @tasks.loop(minutes=2)
    async def check_twitch_live():
        global was_online
        
        webhook_urls = []
        if DISCORD_WEBHOOK_URL_WAFFLE:
            webhook_urls.append(DISCORD_WEBHOOK_URL_WAFFLE)
        if DISCORD_WEBHOOK_URL_MIAU:
            webhook_urls.append(DISCORD_WEBHOOK_URL_MIAU)
        
        if not webhook_urls:
            return
        
        stream_url = f"https://api.twitch.tv/helix/streams?user_id={TWITCH_USER_ID}"
        headers = { "Client-ID": TWITCH_CLIENT_ID, "Authorization": f"Bearer {TWITCH_APP_TOKEN}" }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(stream_url, headers=headers) as response:
                    if response.status != 200:
                        print(f"Erro ao verificar a Twitch. Status: {response.status}")
                        return
                    
                    data = await response.json()
                    
                    if data.get("data"):
                        if not was_online:
                            print(f"{TWITCH_USERNAME} está online! Enviando notificação para {len(webhook_urls)} canais.")
                            
                            stream_data = data["data"][0]
                            user_data = await get_twitch_user_data(session, headers)

                            embed = discord.Embed(
                                title=f"🔴 LIVE ON! {stream_data.get('title')}",
                                url=f"https://www.twitch.tv/{TWITCH_USERNAME}",
                                color=0x0047ab
                            )
                            embed.set_author(name=f"{stream_data.get('user_name')}", url=f"https://www.twitch.tv/{TWITCH_USERNAME}", icon_url=user_data.get('profile_image_url'))
                            embed.add_field(name="Jogando", value=f"{stream_data.get('game_name')}", inline=True)
                            embed.add_field(name="Espectadores", value=f"{stream_data.get('viewer_count')}", inline=True)
                            
                            thumbnail_url = stream_data.get('thumbnail_url').replace('{width}', '1280').replace('{height}', '720')
                            embed.set_image(url=thumbnail_url)
                            embed.set_footer(text="Clique no título para assistir!")

                            for url in webhook_urls:
                                try:
                                    webhook = discord.Webhook.from_url(url, session=session)
                                    await webhook.send(content="@everyone O Santi está em live, venham ver!", embed=embed)
                                except Exception as e:
                                    print(f"Falha ao enviar para o webhook {url[:30]}... Erro: {e}")
                            
                            was_online = True
                    else:
                        if was_online:
                            print(f"{TWITCH_USERNAME} ficou offline.")
                            was_online = False

            except Exception as e:
                print(f"Ocorreu um erro ao checar a Twitch: {e}")

    async def get_twitch_user_data(session, headers):
        user_url = f"https://api.twitch.tv/helix/users?id={TWITCH_USER_ID}"
        async with session.get(user_url, headers=headers) as response:
            if response.status == 200:
                user_data = await response.json()
                if user_data.get("data"):
                    return user_data["data"][0]
        return {}

    @check_twitch_live.before_loop
    async def before_check():
        await bot.wait_until_ready()


    @bot.event
    async def on_ready():
        check_twitch_live.start()
        bot.loop.create_task(mudar_status())
        print("Wafflinho está rodando!")
        try:
            synced = await bot.tree.sync()
            print(f"Sincronizado {len(synced)} comandos")
        except Exception as e:
            print(e)


    async def mudar_status():
        await bot.wait_until_ready()

        todos_status = ["waffle maker | <help", f"em {len(bot.guilds)} servers | <help"]

        while not bot.is_closed():
            status = random.choice(todos_status)
            await bot.change_presence(activity=discord.Game(name=status))
            await asyncio.sleep(10)

    # Controles de servidor -----------------------------------------------

    @bot.event
    async def on_raw_reaction_add(payload):  # Da um cargo através da reação de um emoji
        guild = discord.utils.find(lambda g: g.id == payload.guild_id, bot.guilds)

        if payload.message_id == 774810615373365268 or payload.message_id == 1109138770479038515:
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

        if payload.message_id == 774810615373365268 or payload.message_id == 1109138770479038515:
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
                if guild.id == 344610042756202496:
                    embed = discord.Embed(
                        title=f"Eae {member.name}!\nBem-vindo ao {guild.name}, dá uma olhadinha nas 📃┃regras",
                        color=0xf2bc66,
                    )
                    await guild.system_channel.send(f"{member.mention}")
                    await guild.system_channel.send(embed=embed)
                    
                    role = get(guild.roles, name="MEMBROS")
                    if role:
                        await member.add_roles(role)
                elif guild.id == 768848870419333180:
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
    await bot.load_extension('comandos_nivel')

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

if __name__ == "__main__":
    import asyncio
    bot_instance, token = asyncio.run(run_discord_bot())
    asyncio.run(bot_instance.start(token))