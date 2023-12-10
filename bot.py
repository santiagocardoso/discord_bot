import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get
import random
# import youtube_dl
import asyncio
import json

from server import server

def run_discord_bot():
    with open("token.txt", "r") as file:
        TOKEN = file.read()
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix="w!", intents=intents, help_command=None)

    @bot.event
    async def on_ready():
        activity = discord.Game(name=f"waffle maker | !ajuda", type=3)
        # activity = discord.Game(name=f"waffle maker em {len(bot.guilds)} servers | !ajuda", type=3)
        await bot.change_presence(activity=activity)
        print("Wafflinho está rodando!")
        try:
            synced = await bot.tree.sync()
            print(f"Sincronizado {len(synced)} comandos")
        except Exception as e:
            print(e)

    '''
    async def mudar_status():
        await bot.wait_until_ready()

        todos_status = ["waffle maker | w!help", f"em {len(bot.guilds)} servers | w!help", "discord.py"]

        while not bot.is_closed():
            status = random.choice(todos_status)
            await bot.change_presence(activity=discord.Game(name=status), type=3)
            await asyncio.sleep(10)
    '''

    # Controles de servidor -----------------------------------------------

    @bot.event
    async def on_raw_reaction_add(payload):  # Da um cargo através da reação de um emoji
        guild = discord.utils.find(lambda g: g.id == payload.guild_id, bot.guilds)

        if payload.message_id == SEU_MESSAGE_ID_AQUI or payload.message_id == SEU_MESSAGE_ID_AQUI:
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

        if payload.message_id == SEU_MESSAGE_ID_AQUI or payload.message_id == SEU_MESSAGE_ID_AQUI:
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

    # Menu de ajuda -----------------------------------------------

    @bot.group(name="ajuda", aliases=["comandos", "help"])
    async def help(ctx):
        if ctx.invoked_subcommand is None:
            em = discord.Embed(title="Ajuda", description="Use w!ajuda <comandos> para mais informações.", color=0xf2bc66)
            
            em.add_field(name="Utilidade", value="clear, poll")
            em.add_field(name="Divertidos", value="dado, rand, fale, entrar, sair")
            em.add_field(name="Matemática", value="soma, subt, mult, div, somas, subts")
            em.add_field(name="Economia", value="carteira, pedir, sacar, depositar, enviar, roubar, apostar, loja, comprar, mochila, vender, ranking")

            await ctx.send(embed=em)

    @help.command()
    async def clear(ctx):
        em = discord.Embed(title="Clear", description="Limpa o chat", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!clear <quantidade>")

        await ctx.send(embed=em)

    @help.command()
    async def poll(ctx):
        em = discord.Embed(title="Poll", description="Começa uma votação", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!poll <mensagem>")

        await ctx.send(embed=em)

    @help.command()
    async def dado(ctx):
        em = discord.Embed(title="🎲 Dado", description="Gira um dado de 1 até 6", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!dado")

        await ctx.send(embed=em)

    @help.command()
    async def rand(ctx):
        em = discord.Embed(title="Random", description="Gera um número aleatório", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!rand <máximo")

        await ctx.send(embed=em)

    @help.command()
    async def fale(ctx):
        em = discord.Embed(title="Fale", description="Falo algo que você digite", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!fale <mensagem>")

        await ctx.send(embed=em)

    @help.command()
    async def entrar(ctx):
        em = discord.Embed(title="Entrar", description="Entro no voice chat", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!entrar")

        await ctx.send(embed=em)

    @help.command()
    async def sair(ctx):
        em = discord.Embed(title="Sair", description="Saio do voice chat", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!sair")

        await ctx.send(embed=em)

    @help.command()
    async def soma(ctx):
        em = discord.Embed(title="Soma", description="Somo dois números", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!soma <x> <y>")

        await ctx.send(embed=em)

    @help.command()
    async def subt(ctx):
        em = discord.Embed(title="Subtração", description="Subtraio dois números", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!subt <x> <y>")

        await ctx.send(embed=em)

    @help.command()
    async def mult(ctx):
        em = discord.Embed(title="Multiplicação", description="Multiplico dois números", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!mult <x> <y>")

        await ctx.send(embed=em)

    @help.command()
    async def div(ctx):
        em = discord.Embed(title="Divisão", description="Divido dois números", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!div <x> <y>")

        await ctx.send(embed=em)

    @help.command()
    async def somas(ctx):
        em = discord.Embed(title="Somas", description="Somo vários números", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!somas <x> <y> <z> ...")

        await ctx.send(embed=em)

    @help.command()
    async def subts(ctx):
        em = discord.Embed(title="Subtrações", description="Subtraio vários números", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!subts <x> <y> <z> ...")

        await ctx.send(embed=em)

    @help.command()
    async def carteira(ctx):
        em = discord.Embed(title="Carteira", description="Visualizar sua carteira", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!carteira")

        await ctx.send(embed=em)

    @help.command()
    async def pedir(ctx):
        em = discord.Embed(title="Pedir", description="Pedir dinheiro", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!pedir")

        await ctx.send(embed=em)

    @help.command()
    async def sacar(ctx):
        em = discord.Embed(title="📤 Sacar", description="Sacar dinheiro do cofre", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!sacar <quantia>")

        await ctx.send(embed=em)

    @help.command()
    async def depositar(ctx):
        em = discord.Embed(title="📥 Depositar", description="Depositar dinheiro do cofre", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!depositar <quantia>")

        await ctx.send(embed=em)

    @help.command()
    async def enviar(ctx):
        em = discord.Embed(title="💸 Enviar", description="Enviar dinheiro para outro membro", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!enviar <@membro> <quantia>")

        await ctx.send(embed=em)

    @help.command()
    async def roubar(ctx):
        em = discord.Embed(title="🎰 Roubar", description="Roubar dinheiro de outro membro", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!roubar <@membro> <quantia>")

        await ctx.send(embed=em)

    @help.command()
    async def apostar(ctx):
        em = discord.Embed(title="🎰 Apostar", description="Aposte dinheiro em uma máquina de cassino, igual aquelas que giram os desenhinhos", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!apostar <quantia>")

        await ctx.send(embed=em)

    @help.command()
    async def loja(ctx):
        em = discord.Embed(title="Loja", description="Abre a loja", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!loja")

        await ctx.send(embed=em)

    @help.command()
    async def comprar(ctx):
        em = discord.Embed(title="Comprar", description="Comprar itens da loja", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!comprar <item> <quantidade>")

        await ctx.send(embed=em)

    @help.command()
    async def mochila(ctx):
        em = discord.Embed(title="Mochila", description="Abre sua mochila", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!mochila")

        await ctx.send(embed=em)

    @help.command()
    async def vender(ctx):
        em = discord.Embed(title="Vender", description="Vender itens da sua mochila", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!vender <item> <quantidade>")

        await ctx.send(embed=em)

    @help.command()
    async def ranking(ctx):
        em = discord.Embed(title="Ranking", description="Mostra o ranking de economias", color=0xf2bc66)

        em.add_field(name="**Sintaxe**", value="w!ranking")

        await ctx.send(embed=em)

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

    @bot.command(aliases=["purge", "delete", "vanish", "wipe"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def clear(ctx, amount: int = 0):
        if amount < 31:
            await ctx.message.delete()
            await ctx.channel.purge(limit=amount)
        else:
            await ctx.message.delete()
            await ctx.channel.send("Somente é possível deletar 30 mensagens por vez")
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


    @bot.command(name="sair", aliases=["leave", "disconnect", "quit", "parar", "encerrar", "stop"])
    async def disconnect(ctx):
        await ctx.voice_client.disconnect()
        await ctx.send("Ok... Estou saindo \U0001F62D")


    @bot.event
    async def on_voice_state_update(member, before, after):
        if before.channel is not None and len(before.channel.members) == 1 and before.channel.guild.voice_client is not None:
            await before.channel.guild.voice_client.disconnect()

    # Tocar música -----------------------------------------------

    '''
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
    '''

    # Economia -----------------------------------------------

    @bot.command(aliases=["carteira"])
    async def dinheiro(ctx):
        await abrir_conta(ctx.author)
        
        user = ctx.author
        users = await get_banco()

        quant_carteira = users[str(user.id)]["carteira"]
        quant_cofre = users[str(user.id)]["cofre"]

        em = discord.Embed(title = f"💰 Conta do {ctx.author.name}!", color=ctx.author.color)
        em.add_field(name="Carteira 🪙", value=quant_carteira)
        em.add_field(name="Cofre 🪙", value=quant_cofre)
        await ctx.send(embed=em)


    @bot.event
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown): #  Verifica se está em cooldown
            msg = f"**Ainda tá em cooldown**, tente novamente em {error.retry_after:.2f}s"
            await ctx.send(msg)


    @bot.command()
    @commands.cooldown(5, 60, commands.BucketType.user)
    async def pedir(ctx):
        await abrir_conta(ctx.author)
        
        user = ctx.author
        users = await get_banco()

        ganhos = random.randrange(101)

        await ctx.send(f"Alguém te deu {ganhos} 🪙!!")
        
        users[str(user.id)]["carteira"] += ganhos

        with open("banco.json", "w") as f:
            json.dump(users, f)


    @bot.command()
    async def sacar(ctx, quantia = None):
        await abrir_conta(ctx.author)

        if (quantia == None):
            await ctx.send("📤 Infome a quantia que deseja sacar!")
            return

        din = await atualizar_banco(ctx.author)

        quantia = int(quantia)

        if (quantia > din[1]):
            await ctx.send("Você não é rico não!")
            return
        if (quantia < 0):
            await ctx.send("Como que tu vai sacar dinheiro negativo?")
            return
        
        await atualizar_banco(ctx.author, quantia)
        await atualizar_banco(ctx.author, -1 * quantia, "cofre")

        await ctx.send(f"Você sacou {quantia} 🪙!")


    @bot.command()
    async def depositar(ctx, quantia = None):
        await abrir_conta(ctx.author)

        if (quantia == None):
            await ctx.send("📥 Infome a quantia que deseja depositar!")
            return

        din = await atualizar_banco(ctx.author)

        quantia = int(quantia)
        if (quantia > din[0]):
            await ctx.send("Você não é rico não!")
            return
        if (quantia < 0):
            await ctx.send("Como que tu vai depositar dinheiro negativo?")
            return
        
        await atualizar_banco(ctx.author, -1 * quantia)
        await atualizar_banco(ctx.author, quantia, "cofre")

        await ctx.send(f"Você depositou {quantia} 🪙!")


    @bot.command()
    async def enviar(ctx, member:discord.Member, quantia = None):
        await abrir_conta(ctx.author)
        await abrir_conta(member)

        if (quantia == None):
            await ctx.send("💸 Infome a quantia que deseja enviar!")
            return

        din = await atualizar_banco(ctx.author, quantia)

        if (quantia  == "all"):
            quantia = din[0]

        quantia = int(quantia)

        if (quantia > din[1]):
            await ctx.send("Você não é rico não!")
            return
        if (quantia < 0):
            await ctx.send("Como que tu vai depositar dinheiro negativo?")
            return
        
        await atualizar_banco(ctx.author, -1 * quantia, "cofre")
        await atualizar_banco(member, quantia, "cofre")

        await ctx.send(f"Você deu {quantia} 🪙!")


    @bot.command()
    @commands.cooldown(1, 900, commands.BucketType.user)
    async def roubar(ctx, member:discord.Member):
        await abrir_conta(ctx.author)
        await abrir_conta(member)

        din = await atualizar_banco(member)

        if (din[0] < 100):
            await ctx.send("🔒 Não vale a pena...")
            return
        
        ganhos = random.randrange(0, din[0])
        
        await atualizar_banco(ctx.author, ganhos)
        await atualizar_banco(member, -1 * ganhos)

        await ctx.send(f"O cara roubou aqui!!! Foram {ganhos} 🪙 do {str(member)}!")


    @bot.command()
    async def apostar(ctx, quantia = None):
        await abrir_conta(ctx.author)

        if (quantia == None):
            await ctx.send("🎰 Infome a quantia que deseja apostar!")
            return

        din = await atualizar_banco(ctx.author, quantia)

        quantia = int(quantia)

        if (quantia > din[0]):
            await ctx.send("Você não é rico não!")
            return
        if (quantia < 0):
            await ctx.send("Como que tu vai apostar dinheiro negativo?")
            return
        
        final = []
        for i in range(3):
            a = random.choice(["X", "O", "Q"])

            final.append(a)

        await ctx.send(str(final))

        if (final[0] == final[1] or final[0] == final[2] or final[2] == final[1]):
            await atualizar_banco(ctx.author, 2 * quantia)
            await ctx.send("Você ganhou!!!")
        else:
            await atualizar_banco(ctx.author, -1 * quantia)
            await ctx.send("Você perdeu...")


    async def abrir_conta(user):
        users = await get_banco()

        if (str(user.id) in users):
            return False
        else:
            users[str(user.id)] = {}
            users[str(user.id)]["carteira"] = 0
            users[str(user.id)]["cofre"] = 0

        with open("banco.json", "w") as f:
            json.dump(users, f)

        return True


    async def get_banco():
        with open("banco.json", "r") as f:
            users = json.load(f)
        
        return users


    async def atualizar_banco(user, quantia=0, modo="carteira"):
        users = await get_banco()

        quantia = int(quantia)
        users[str(user.id)][modo] += quantia

        with open("banco.json", "w") as f:
            json.dump(users, f)

        din = [users[str(user.id)]["carteira"], users[str(user.id)]["cofre"]]

        return din

    # loja -----------------------------------------------

    lojinha = [{"nome":"Waffle","preco":100,"descricao":"🧇"},
               {"nome":"Chapéu","preco":10000,"descricao":"🎩"},
               {"nome":"Casa","preco":100000,"descricao":"🛖"},
               {"nome":"Mansão","preco":1000000,"descricao":"🏛️"}]
    
    
    @bot.command()
    async def loja(ctx):
        em = discord.Embed(title="🏮 Loja", color=0xf2bc66)

        for item in lojinha:
            nome = item["nome"]
            preco = item["preco"]
            desc = item["descricao"]
            em.add_field(name=nome, value=f"{preco} 🪙 | {desc}", inline=False)

        await ctx.send(embed=em)


    @bot.command()
    async def comprar(ctx, item, quantidade=1):
        await abrir_conta(ctx.author)

        res = await comprar_isso(ctx.author, item, quantidade)

        if not res[0]:
            if res[1]==1:
                await ctx.send("Não tem isso ai na vendinha!")
                return
            if res[1]==2:
                await ctx.send(f"Você não tem dinheiro suficiente na carteira para {quantidade} {item}")
                return
            
        await ctx.send(f"Você comprou {quantidade} {item}")


    @bot.command()
    async def mochila(ctx):
        await abrir_conta(ctx.author)
        user = ctx.author
        users = await get_banco()

        try:
            mochila = users[str(user.id)]["mochila"]
        except:
            mochila = []

        em = discord.Embed(title="🎒 Mochila", color=0xf2bc66)
        for item in mochila:
            nome = item["item"]
            quantidade = item["quantidade"]

            em.add_field(name=nome, value=quantidade)

        await ctx.send(embed=em)


    async def comprar_isso(user, item_nome, quantidade):
        item_nome = item_nome.lower()
        nome_ = None

        for item in lojinha:
            nome = item["nome"].lower()
            if (nome == item_nome):
                nome_ = nome
                preco = item["preco"]
                break
        
        if (nome_ == None):
            return [False, 1]
        
        custo = preco * quantidade

        users = await get_banco()

        din = await atualizar_banco(user)

        if (din[0] < custo):
            return [False, 2]

        try:
            i = 0
            t = None
            for coisa in users[str(user.id)]["mochila"]:
                n = coisa["item"]
                if n == item_nome:
                    quant_velha = coisa["quantidade"]
                    nova_quant = quant_velha + quantidade
                    users[str(user.id)]["mochila"][i]["quantidade"] = nova_quant
                    t = 1
                    break
                i += 1
            if t == None:
                obj = {"item":item_nome, "quantidade": quantidade}
                users[str(user.id)]["mochila"].append(obj)

        except:
            obj = {"item":item_nome, "quantidade": quantidade}
            users[str(user.id)]["mochila"] = [obj]

        with open("banco.json", "w") as f:
            json.dump(users, f)

        await atualizar_banco(user, custo * -1, "carteira")

        return [True, "Funcionou"]
    

    @bot.command()
    async def vender(ctx, item, quantidade=1):
        await abrir_conta(ctx.author)

        res = await vender_isso(ctx.author, item, quantidade)

        if not res[0]:
            if res[1] == 1:
                await ctx.send("Esse item não existe...")
                return
            if res[1] == 2:
                await ctx.send(f"Você não tem {quantidade} {item} na sua 🎒!")
                return
            if res[1] == 3:
                await ctx.send(f"Você não tem {item} na sua 🎒!")
                return
            
        await ctx.send(f"Você vendeu {quantidade} {item}.")

    
    async def vender_isso(user, item_nome, quantidade, preco=None):
        item_nome = item_nome.lower()
        nome_ = None
        for item in lojinha:
            nome = item["nome"].lower()
            if nome == item_nome:
                nome_ = nome
                if preco == None:
                    preco = 0.8 * item["preco"]  
                break

        if nome_ == None:
            return [False, 1]
        
        custo = preco * quantidade

        users = await get_banco()

        din = await atualizar_banco(user)

        try:
            i = 0
            f = None
            for coisa in users[str(user.id)]["mochila"]:
                n = coisa["item"]
                if n == item_nome:
                    quant_velha = coisa["quantidade"]
                    nova_quant = quant_velha - quantidade
                    if nova_quant < 0:
                        return [False, 2]
                    users[str(user.id)]["mochila"][i]["quantidade"] = nova_quant
                    f = 1
                    break
                i += 1
            if f == None:
                return [False, 3]
        except:
            return [False, 3]
        
        with open("banco.json", "w") as f:
            json.dump(users, f)

        await atualizar_banco(user, custo, "carteira")

        return [True, "Funcionou"]
    

    @bot.command(aliases=["rk"])
    async def ranking(ctx, x=3):
        users = await get_banco()
        ranking = {}
        total = []

        for user in users:
            nome = int(user)
            quant_total = users[user]["carteira"] + users[user]["cofre"]
            ranking[quant_total] = nome
            total.append(quant_total)

        total = sorted(total, reverse=True)

        em = discord.Embed(title=f"🏆 Top {x} pessoas mais ricas", description="É rankeado através da quantia total de dinheiro do usuário", color=0xf2bc66)
        i = 1

        for qtd in total:
            id_ = ranking[qtd]
            membro = bot.get_user(id_)
            nome = membro.name
            em.add_field(name=f"{i}. {nome}", value=f"{qtd}", inline=False)
            if i == x:
                break
            else:
                i += 1

        await ctx.send(embed = em)

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
    # bot.loop.create_task(mudar_status())
    bot.run(TOKEN)
