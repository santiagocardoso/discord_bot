import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get
import random
import asyncio
import json

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
                embed = discord.Embed(
                    title=f"Eae {member.name}!\nBem-vindo ao {guild.name}, dá uma olhadinha nas 📃┃regras",
                    color=0xf2bc66,
                )
                await guild.system_channel.send(f"{member.mention}")
                await guild.system_channel.send(embed=embed)

                if guild.id == 344610042756202496:
                    role = get(guild.roles, name="MEMBROS")
                    if role:
                        await member.add_roles(role)
                elif guild.id == 768848870419333180:
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


    @bot.command(name="sair", aliases=["leave", "disconnect", "quit"])
    async def disconnect(ctx):
        await ctx.voice_client.disconnect()
        await ctx.send("Ok... Estou saindo \U0001F62D")


    @bot.event
    async def on_voice_state_update(member, before, after):
        if before.channel is not None and len(before.channel.members) == 1 and before.channel.guild.voice_client is not None:
            await before.channel.guild.voice_client.disconnect()

    # Economia -----------------------------------------------

    @bot.command()
    async def dinheiro(ctx):
        await abrir_conta(ctx.author)
        
        user = ctx.author
        users = await get_banco()

        quant_carteira = users[str(user.id)]["carteira"]
        quant_cofre = users[str(user.id)]["cofre"]

        em = discord.Embed(title = f"Conta do {ctx.author.name}!", color=0xf2bc66)
        em.add_field(name="Carteira", value=quant_carteira)
        em.add_field(name="Cofre", value=quant_cofre)
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

        await ctx.send(f"Alguém te deu {ganhos} moedas!!")
        
        users[str(user.id)]["carteira"] += ganhos

        with open("banco.json", "w") as f:
            json.dump(users, f)


    @bot.command()
    async def sacar(ctx, quantia = None):
        await abrir_conta(ctx.author)

        if (quantia == None):
            await ctx.send("Infome a quantia que deseja sacar!")
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

        await ctx.send(f"Você sacou {quantia} moedas!")


    @bot.command()
    async def depositar(ctx, quantia = None):
        await abrir_conta(ctx.author)

        if (quantia == None):
            await ctx.send("Infome a quantia que deseja depositar!")
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

        await ctx.send(f"Você depositou {quantia} moedas!")


    @bot.command()
    async def enviar(ctx, member:discord.Member, quantia = None):
        await abrir_conta(ctx.author)
        await abrir_conta(member)

        if (quantia == None):
            await ctx.send("Infome a quantia que deseja sacar!")
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

        await ctx.send(f"Você deu {quantia} moedas!")


    @bot.command()
    @commands.cooldown(1, 900, commands.BucketType.user)
    async def roubar(ctx, member:discord.Member):
        await abrir_conta(ctx.author)
        await abrir_conta(member)

        din = await atualizar_banco(member)

        if (din[0] < 100):
            await ctx.send("Não vale a pena...")
            return
        
        ganhos = random.randrange(0, din[0])
        
        await atualizar_banco(ctx.author, ganhos)
        await atualizar_banco(member, -1 * ganhos)

        await ctx.send(f"O cara roubou aqui!!! Foram {ganhos} moedas do {str(member)}!")


    @bot.command()
    async def apostar(ctx, quantia = None):
        await abrir_conta(ctx.author)

        if (quantia == None):
            await ctx.send("Infome a quantia que deseja apostar!")
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

    lojinha = [{"nome":"Waffle","preco":100,"descricao":"Yummy"},
               {"nome":"Chapéu","preco":10000,"descricao":"Chapéu estilo Fedora"},
               {"nome":"Casa","preco":100000,"descricao":"Casinha simples"},
               {"nome":"Mansão","preco":1000000,"descricao":"Mansão colossal na praia"}]
    
    
    @bot.command()
    async def loja(ctx):
        em = discord.Embed(title="Loja", color=0xf2bc66)

        for item in lojinha:
            nome = item["nome"]
            preco = item["preco"]
            desc = item["descricao"]
            em.add_field(name=nome, value=f"R${preco} | {desc}", inline=False)

        await ctx.send(embed=em)


    @bot.command()
    async def comprar(ctx, item, quantia=1):
        await abrir_conta(ctx.author)

        res = await comprar_isso(ctx.author, item, quantia)

        if not res[0]:
            if res[1]==1:
                await ctx.send("Não tem isso ai na vendinha!")
                return
            if res[1]==2:
                await ctx.send(f"Você não tem dinheiro suficiente na carteira para {quantia} {item}")
                return
            
        await ctx.send(f"Você comprou {quantia} {item}")


    @bot.command()
    async def mochila(ctx):
        await abrir_conta(ctx.author)
        user = ctx.author
        users = await get_banco()

        try:
            mochila = users[str(user.id)]["mochila"]
        except:
            mochila = []

        em = discord.Embed(title="Mochila", color=0xf2bc66)
        for item in mochila:
            nome = item["item"]
            quantia = item["quantia"]

            em.add_field(name=nome, value=quantia)

        await ctx.send(embed=em)


    async def comprar_isso(user, item_nome, quantia):
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
        
        custo = preco * quantia

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
                    quant_velha = coisa["quantia"]
                    nova_quant = quant_velha + quantia
                    users[str(user.id)]["mochila"][i]["quantia"] = nova_quant
                    t = 1
                    break
                i += 1
            if t == None:
                obj = {"item":item_nome, "quantia": quantia}
                users[str(user.id)]["mochila"].append(obj)

        except:
            obj = {"item":item_nome, "quantia": quantia}
            users[str(user.id)]["mochila"] = [obj]

        with open("banco.json", "w") as f:
            json.dump(users, f)

        await atualizar_banco(user, custo * -1, "carteira")

        return [True, "Funcionou"]

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
