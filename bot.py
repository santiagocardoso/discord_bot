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
twitch_access_token_cache = None

async def run_discord_bot():
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix=["<", "w!", ">"], intents=intents, help_command=None)

    async def get_twitch_access_token():
        global twitch_access_token_cache
        if twitch_access_token_cache:
            return twitch_access_token_cache

        client_id = os.getenv("TWITCH_CLIENT_ID")
        client_secret = os.getenv("TWITCH_CLIENT_SECRET")
        url = f"https://id.twitch.tv/oauth2/token?client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials"
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url) as response:
                if response.status == 200:
                    data = await response.json()
                    twitch_access_token_cache = data["access_token"]
                    return twitch_access_token_cache
                else:
                    print(f"Erro ao gerar token: {response.status}")
                    return None

    @tasks.loop(minutes=2)
    async def check_twitch_live():
        global was_online
        global twitch_access_token_cache

        token = await get_twitch_access_token()
        if not token:
            print("Não foi possível obter o token da Twitch.")
            return

        headers = {
            "Client-ID": TWITCH_CLIENT_ID,
            "Authorization": f"Bearer {token}"
        }
        
        stream_url = f"https://api.twitch.tv/helix/streams?user_id={TWITCH_USER_ID}"

        webhooks_com_cargos = {
            os.getenv("DISCORD_WEBHOOK_URL_WAFFLE"): "1422791135738466334",
            os.getenv("DISCORD_WEBHOOK_URL_MIAU"): "1422791525980573726"
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(stream_url, headers=headers) as response:
                    if response.status == 401:
                        twitch_access_token_cache = None
                        return
                    if response.status != 200:
                        erro_msg = await response.text()
                        print(f"Erro ao verificar a Twitch. Status: {response.status} - {erro_msg}")
                        return
                    
                    data = await response.json()
                    
                    if data.get("data"):
                        if not was_online:
                            print(f"{TWITCH_USERNAME} está online! Enviando notificação...")
                            
                            stream_data = data["data"][0]
                            user_data = await get_twitch_user_data(session, headers)

                            embed = discord.Embed(
                                title=f"🔴 LIVE ON! {stream_data.get('title')}",
                                url=f"https://www.twitch.tv/{TWITCH_USERNAME}",
                                color=0x6441a5
                            )
                            embed.set_author(name=f"{stream_data.get('user_name')}", url=f"https://www.twitch.tv/{TWITCH_USERNAME}", icon_url=user_data.get('profile_image_url'))
                            embed.add_field(name="Jogando", value=f"{stream_data.get('game_name')}", inline=True)
                            embed.add_field(name="Espectadores", value=f"{stream_data.get('viewer_count')}", inline=True)
                            
                            thumbnail_url = stream_data.get('thumbnail_url').replace('{width}', '1280').replace('{height}', '720')
                            embed.set_image(url=thumbnail_url)
                            embed.set_footer(text="Clique no título para assistir!")

                            for url, role_id in webhooks_com_cargos.items():
                                if not url or not role_id:
                                    continue
                                
                                try:
                                    webhook = discord.Webhook.from_url(url, session=session)
                                    
                                    mensagem_com_cargo = f"<@&{role_id}> **santcar7** está em live, venham ver!"
                                    
                                    await webhook.send(content=mensagem_com_cargo, embed=embed)
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
        if not check_twitch_live.is_running():
            check_twitch_live.start()
        if not hasattr(bot, 'status_loop_started'):
            bot.loop.create_task(mudar_status())
            bot.status_loop_started = True
        print("Wafflinho está rodando!")


    async def mudar_status():
        await bot.wait_until_ready()

        todos_status = ["waffle maker | <help", f"em {len(bot.guilds)} servers | <help"]

        while not bot.is_closed():
            status = random.choice(todos_status)
            await bot.change_presence(activity=discord.Game(name=status))
            await asyncio.sleep(60)

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

    @bot.command()
    @commands.is_owner()
    async def sync(ctx):
        synced = await bot.tree.sync()
        await ctx.send(f"Sincronizado {len(synced)} comandos")

    @bot.tree.command(name="oi")
    async def oi(interaction: discord.Interaction):
        await interaction.response.send_message(f"Oie {interaction.user.mention}!", ephemeral=True)


    @bot.tree.command(name="fale")
    @app_commands.describe(thing_to_say="O que eu deveria dizer?")
    async def say(interaction: discord.Interaction, thing_to_say: str):
        await interaction.response.send_message(f"`{thing_to_say}`")

    # Iniciar o bot -----------------------------------------------

    server()
    await bot.start(TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(run_discord_bot())