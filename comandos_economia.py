import asyncio
import discord
from discord.ext import commands
import json
import random

class Economia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=["carteira", "conta", "din"])
    async def dinheiro(self, ctx, member: discord.Member=None):
        await self.abrir_conta(ctx.author)

        if member is None:
            member = ctx.author

        users = await self.get_banco()

        quant_carteira = users[str(member.id)]["carteira"]
        quant_cofre = users[str(member.id)]["cofre"]

        em = discord.Embed(title=f"💰 Conta de {member.name}!", color=member.color)
        em.add_field(name="Carteira 🪙", value=quant_carteira)
        em.add_field(name="Cofre 🪙", value=quant_cofre)
        await ctx.send(embed=em)



    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):  # Verifica se está em cooldown
            msg = f"**Ainda tá em cooldown**, tente novamente em {error.retry_after:.2f}s"
            await ctx.send(msg)


    @commands.command(aliases=["implorar", "p"])
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def pedir(self, ctx):
        await self.abrir_conta(ctx.author)

        user = ctx.author
        users = await self.get_banco()

        ganhos = random.randint(100, 300)

        await ctx.send(f"Alguém te deu {ganhos} 🪙!!")

        users[str(user.id)]["carteira"] += ganhos

        with open("banco.json", "w") as f:
            json.dump(users, f)


    @commands.command(aliases=["dig"])
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def cavar(self, ctx):
        await self.abrir_conta(ctx.author)

        user = ctx.author
        users = await self.get_banco()

        din = await self.atualizar_banco(ctx.author)

        perdeu_carteira = int(20/100 * din[0])
        perdeu_cofre = int(40/100 * din[1])

        item = random.choice(["🪨", "🪨", "🪨", "🪨", "🪨", "🪨", "💎", "💎", "🌌", "💣", "🦖"]) 

        await ctx.send(f"Você encontrou {item}!!")

        if item == "🪨":
            obj = {"item":"pedra", "quantidade": 1}

            try:
                i = 0
                t = None
                for coisa in users[str(user.id)]["mochila"]:
                    n = coisa["item"]
                    if n == obj["item"]:
                        quant_velha = coisa["quantidade"]
                        nova_quant = quant_velha + obj["quantidade"]
                        users[str(user.id)]["mochila"][i]["quantidade"] = nova_quant
                        t = 1
                        break
                    i += 1
                if t == None:
                    obj = {"item":obj["item"], "quantidade": obj["quantidade"]}
                    users[str(user.id)]["mochila"].append(obj)

            except:
                obj = {"item":obj["item"], "quantidade": obj["quantidade"]}
                users[str(user.id)]["mochila"] = [obj]

        if item == "💎":
            obj = {"item":"diamante", "quantidade": 1}

            try:
                i = 0
                t = None
                for coisa in users[str(user.id)]["mochila"]:
                    n = coisa["item"]
                    if n == obj["item"]:
                        quant_velha = coisa["quantidade"]
                        nova_quant = quant_velha + obj["quantidade"]
                        users[str(user.id)]["mochila"][i]["quantidade"] = nova_quant
                        t = 1
                        break
                    i += 1
                if t == None:
                    obj = {"item":obj["item"], "quantidade": obj["quantidade"]}
                    users[str(user.id)]["mochila"].append(obj)

            except:
                obj = {"item":obj["item"], "quantidade": obj["quantidade"]}
                users[str(user.id)]["mochila"] = [obj]

        if item == "🌌":
            await ctx.send("Você encontrou um portal dimensional... Deseja investigar? Digite (sim/nao)")

            async def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            try:
                response = await self.bot.wait_for('message', check=check, timeout=15)  # Aguarda a resposta por 15 segundos
            except asyncio.TimeoutError:
                await ctx.send("Tempo esgotado. A investigação foi cancelada.")

            if response.content.lower() == "sim":
                await ctx.send("Você entrou no portal e encontrou um 👽")

                destino = random.choice(["❌", "💎"])

                if destino == "❌":
                    await ctx.send(f"Ele não gostou de você e fez experimentos 😱\nVocê perdeu **(-{perdeu_cofre} 🪙)** para pagar suas cirurgias após os danos causados!")

                    if users[str(user.id)]["carteira"] > perdeu_cofre:
                        users[str(user.id)]["carteira"] -= perdeu_cofre
                    else:
                        users[str(user.id)]["carteira"] = 0
                else:
                    await ctx.send(f"Ele gostou de você e como viu que estava procurando diamantes te deu um 💎!")

                    obj = {"item":"diamante", "quantidade": 1}

                    try:
                        i = 0
                        t = None
                        for coisa in users[str(user.id)]["mochila"]:
                            n = coisa["item"]
                            if n == obj["item"]:
                                quant_velha = coisa["quantidade"]
                                nova_quant = quant_velha + obj["quantidade"]
                                users[str(user.id)]["mochila"][i]["quantidade"] = nova_quant
                                t = 1
                                break
                            i += 1
                        if t == None:
                            obj = {"item":obj["item"], "quantidade": obj["quantidade"]}
                            users[str(user.id)]["mochila"].append(obj)

                    except:
                        obj = {"item":obj["item"], "quantidade": obj["quantidade"]}
                        users[str(user.id)]["mochila"] = [obj]

            elif response.content.lower() == "nao":
                await ctx.send("Você decidiu não investigar a pegada.")
            else:
                await ctx.send("Resposta inválida. A investigação foi cancelada.")

        if item == "💣":
            await ctx.send(f"Você acertou uma bomba!!!! 💥💥💥\nPerdeu **(-{perdeu_carteira} 🪙)**")

            if users[str(user.id)]["carteira"] > perdeu_carteira:
                users[str(user.id)]["carteira"] -= perdeu_carteira
            else:
                users[str(user.id)]["carteira"] = 0

        if item == "🦖":
            await ctx.send(f"Você encontrou um fóssil raro de um T-Rex e vendeu ele para um museu\nGanhou **(1500 🪙)**")
            users[str(user.id)]["carteira"] += 1500

        with open("banco.json", "w") as f:
            json.dump(users, f)


    # Mine: ⛏️🪨💎💰🪙🪙🪙🌋🐾

    @commands.command(aliases=["mine", "m", "search"])
    @commands.cooldown(1, 0.8, commands.BucketType.user)
    async def minerar(self, ctx):
        await self.abrir_conta(ctx.author)

        user = ctx.author
        users = await self.get_banco()

        din = await self.atualizar_banco(ctx.author)

        n = None
        for coisa in users[str(user.id)]["mochila"]:
            n = coisa["item"]
            if n == "picareta":
                if coisa["quantidade"] > 0:
                    coisa["quantidade"] -= 1
                else:
                    await ctx.send("Você não tem uma ⛏️, compre uma na loja!")
                    return

        if n == None:
            await ctx.send("Você não tem uma ⛏️, compre uma na loja!")
            return

        perdeu = int(10/100 * din[0])

        item = random.choice(["🪨", "🪨", "🪨", "🪨", "💎", "💎", "💰", "🪙", "🌋", "🐾"])

        await ctx.send(f"Você encontrou {item}!!")

        if item == "🪨":
            obj = {"item":"pedra", "quantidade": 1}

            try:
                i = 0
                t = None
                for coisa in users[str(user.id)]["mochila"]:
                    n = coisa["item"]
                    if n == obj["item"]:
                        quant_velha = coisa["quantidade"]
                        nova_quant = quant_velha + obj["quantidade"]
                        users[str(user.id)]["mochila"][i]["quantidade"] = nova_quant
                        t = 1
                        break
                    i += 1
                if t == None:
                    obj = {"item":obj["item"], "quantidade": obj["quantidade"]}
                    users[str(user.id)]["mochila"].append(obj)

            except:
                obj = {"item":obj["item"], "quantidade": obj["quantidade"]}
                users[str(user.id)]["mochila"] = [obj]

        if item == "💎":
            obj = {"item":"diamante", "quantidade": 1}

            try:
                i = 0
                t = None
                for coisa in users[str(user.id)]["mochila"]:
                    n = coisa["item"]
                    if n == obj["item"]:
                        quant_velha = coisa["quantidade"]
                        nova_quant = quant_velha + obj["quantidade"]
                        users[str(user.id)]["mochila"][i]["quantidade"] = nova_quant
                        t = 1
                        break
                    i += 1
                if t == None:
                    obj = {"item":obj["item"], "quantidade": obj["quantidade"]}
                    users[str(user.id)]["mochila"].append(obj)

            except:
                obj = {"item":obj["item"], "quantidade": obj["quantidade"]}
                users[str(user.id)]["mochila"] = [obj]

        if item == "💰":
            users[str(user.id)]["carteira"] += 1000
            await ctx.send("Ganhou **(1000 🪙)**")

        if item == "🪙":
            users[str(user.id)]["carteira"] += 500
            await ctx.send("Ganhou **(400 🪙)**")

        if item == "🌋":
            await ctx.send(f"Você iniciou a erupção de um vulcão! Parece que queimou um pouco do seu dinheiro 😱\n**(-{perdeu} 🪙)**")
            if users[str(user.id)]["carteira"] > perdeu:
                users[str(user.id)]["carteira"] -= perdeu
            else:
                users[str(user.id)]["carteira"] = 0

        if item == "🐾":
            await ctx.send("Você encontrou uma pegada estranha... Deseja investigar? Digite (sim/nao)")

            async def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            try:
                response = await self.bot.wait_for('message', check=check, timeout=15)  # Aguarda a resposta por 15 segundos
            except asyncio.TimeoutError:
                await ctx.send("Tempo esgotado. A investigação foi cancelada.")

            if response.content.lower() == "sim":
                await ctx.send("Você decidiu investigar a pegada.")

                animal = random.choice(["🦤", "🦍"])

                if animal == "🦍":
                    await ctx.send(f"Você encontrou um 🦍 malvado. Parece que ele roubou um pouco do seu dinheiro 😱\n**(-{perdeu} 🪙)**")

                    if users[str(user.id)]["carteira"] > perdeu:
                        users[str(user.id)]["carteira"] -= perdeu
                    else:
                        users[str(user.id)]["carteira"] = 0
                else:
                    await ctx.send(f"Você encontrou um {animal} bonzinho. Foi para a sua mochila!")
                    if animal == "🦤":
                        obj = {"item":"dodo", "quantidade": 1}

                    try:
                        i = 0
                        t = None
                        for coisa in users[str(user.id)]["mochila"]:
                            n = coisa["item"]
                            if n == obj["item"]:
                                quant_velha = coisa["quantidade"]
                                nova_quant = quant_velha + obj["quantidade"]
                                users[str(user.id)]["mochila"][i]["quantidade"] = nova_quant
                                t = 1
                                break
                            i += 1
                        if t == None:
                            obj = {"item":obj["item"], "quantidade": obj["quantidade"]}
                            users[str(user.id)]["mochila"].append(obj)

                    except:
                        obj = {"item":obj["item"], "quantidade": obj["quantidade"]}
                        users[str(user.id)]["mochila"] = [obj]

            elif response.content.lower() == "nao":
                await ctx.send("Você decidiu não investigar a pegada.")
            else:
                await ctx.send("Resposta inválida. A investigação foi cancelada.")

        with open("banco.json", "w") as f:
            json.dump(users, f)


    #  Pesca: 🎣🐟🐠🐡🦈🐙🪼🦀🦑🐳

    @commands.command(aliases=["fish", "fishing", "f", "pesca"])
    @commands.cooldown(1, 0.8, commands.BucketType.user)
    async def pescar(self, ctx):
        await self.abrir_conta(ctx.author)

        user = ctx.author
        users = await self.get_banco()

        din = await self.atualizar_banco(ctx.author)

        n = None
        for coisa in users[str(user.id)]["mochila"]:
            n = coisa["item"]
            if n == "vara":
                if coisa["quantidade"] > 0:
                    coisa["quantidade"] -= 1
                else:
                    await ctx.send("Você não tem uma 🎣, compre uma na loja!")
                    return

        if n == None:
            await ctx.send("Você não tem uma 🎣, compre uma na loja!")
            return

        dano = int(10/100 * din[0])
        tuba = int(30/100 * din[0])

        item = random.choice(["🐟", "🐟", "🐟", "🐟", "🐟", "🐟", "🐟", "🐟", "🐟", "🐠", "🐠", "🐠", "🐠", "🐠", "🐡", "🦈", "🐙","🐙", "🐙", "🪼", "🦀", "🦀", "🦀", "🦑", "🦑", "🐳"])
        await ctx.send(f"Você pescou {item}!!")

        if item == "🐟" or item == "🐠" or item == "🐙" or item == "🦀" or item == "🦑" or item == "🐳" or item == "🐡":
            obj = {"item":"peixe", "quantidade": 1}

            try:
                i = 0
                t = None
                for coisa in users[str(user.id)]["mochila"]:
                    n = coisa["item"]
                    if n == obj["item"]:
                        quant_velha = coisa["quantidade"]
                        nova_quant = quant_velha + obj["quantidade"]
                        users[str(user.id)]["mochila"][i]["quantidade"] = nova_quant
                        t = 1
                        break
                    i += 1
                if t == None:
                    obj = {"item":obj["item"], "quantidade": obj["quantidade"]}
                    users[str(user.id)]["mochila"].append(obj)

            except:
                obj = {"item":obj["item"], "quantidade": obj["quantidade"]}
                users[str(user.id)]["mochila"] = [obj]

        bonus_mapping = {
            "🐠": 600,
            "🐙": 800,
            "🦀": 400,
            "🦑": 1000,
        }

        if item in bonus_mapping:
            bonus = bonus_mapping[item]
            await ctx.send(f"Você ganhou **{bonus}** 🪙 de bônus da pesca desse peixe")
            users[str(user.id)]["carteira"] += bonus

        if item == "🐳":
            await ctx.send("Você encontrou a baleia da sorte!! Ela dobrou seu dinheiro da carteira!")
            users[str(user.id)]["carteira"] = 2 * users[str(user.id)]["carteira"]

        if item == "🐡":
            await ctx.send(f"O baiacu acabou furando um pouco do seu dinheiro 😱\n**(-{dano} 🪙)**")
            if users[str(user.id)]["carteira"] > dano:
                users[str(user.id)]["carteira"] -= dano
            else:
                users[str(user.id)]["carteira"] = 0

        if item == "🪼":
            await ctx.send(f"Você acabou levando um choque e curto circuitou seu cofre 😱\n**(-{dano} 🪙)**")
            if users[str(user.id)]["cofre"] > dano:
                users[str(user.id)]["cofre"] -= dano
            else:
                users[str(user.id)]["cofre"] = 0

        if item == "🦈":
            await ctx.send(f"O tubarão comeu sua perna!!! Parece que a sua carteira também...\n**(-{tuba} 🪙)**")
            if users[str(user.id)]["cofre"] > tuba:
              users[str(user.id)]["cofre"] -= tuba
            else:
              users[str(user.id)]["cofre"] = 0

        with open("banco.json", "w") as f:
            json.dump(users, f)


    @commands.command(aliases=["positar"])
    async def sacar(self, ctx, quantia=None):
        await self.abrir_conta(ctx.author)

        if quantia is None:
            await ctx.send("📤 Infome a quantia que deseja sacar!")
            return

        din = await self.atualizar_banco(ctx.author)

        if quantia == "all" or quantia == "tudo":
            quantia = din[1]

        quantia = int(quantia)

        if quantia > din[1]:
            await ctx.send("Você não é rico não!")
            return
        if quantia < 0:
            await ctx.send("Como que tu vai sacar dinheiro negativo?")
            return
        if quantia == 0:
            await ctx.send("Não tem como sacar nada...")
            return

        await self.atualizar_banco(ctx.author, quantia)
        await self.atualizar_banco(ctx.author, -1 * quantia, "cofre")

        await ctx.send(f"Você sacou {quantia} 🪙!")


    @commands.command(aliases=["cofre"])
    async def depositar(self, ctx, quantia=None):
        await self.abrir_conta(ctx.author)

        if quantia is None:
            await ctx.send("📥 Infome a quantia que deseja depositar!")
            return

        din = await self.atualizar_banco(ctx.author)

        if quantia == "all" or quantia == "tudo":
            quantia = din[0]

        quantia = int(quantia)

        if quantia > din[0]:
            await ctx.send("Você não é rico não!")
            return
        if quantia < 0:
            await ctx.send("Como que tu vai depositar dinheiro negativo?")
            return
        if quantia == 0:
            await ctx.send("Não tem como depositar nada...")
            return

        await self.atualizar_banco(ctx.author, -1 * quantia)
        await self.atualizar_banco(ctx.author, quantia, "cofre")

        await ctx.send(f"Você depositou {quantia} 🪙!")


    @commands.command(aliases=["send", "give"])
    async def enviar(self, ctx, member: discord.Member, quantia=None):
        await self.abrir_conta(ctx.author)
        await self.abrir_conta(member)

        if quantia is None:
            await ctx.send("💸 Infome a quantia que deseja enviar!")
            return

        din = await self.atualizar_banco(ctx.author)

        if quantia == "all" or quantia == "tudo":
            quantia = din[0]

        quantia = int(quantia)

        if quantia > din[1]:
            await ctx.send("Você não é rico não!")
            return
        if quantia < 0:
            await ctx.send("Como que tu vai enviar dinheiro negativo?")
            return
        if quantia == 0:
            await ctx.send("Não tem como enviar nada...")
            return

        await self.atualizar_banco(ctx.author, -1 * quantia, "cofre")
        await self.atualizar_banco(member, quantia, "cofre")

        await ctx.send(f"Você deu {quantia} 🪙!")


    @commands.command(aliases=["furto", "steal", "assaltar"])
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def furtar(self, ctx, member: discord.Member):
        await self.abrir_conta(ctx.author)
        await self.abrir_conta(member)

        din = await self.atualizar_banco(member)

        if din[0] < 100:
            await ctx.send("🔒 Não vale a pena...")
            return

        range = int((60/100) * din[0])
        ganhos = random.randrange(0, range)

        await self.atualizar_banco(ctx.author, ganhos)
        await self.atualizar_banco(member, -1 * ganhos)

        await ctx.send(f"O cara roubou aqui!!! Foram {ganhos} 🪙 do {member.mention}!")


    @commands.command(aliases=["saquear", "rob"])
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def roubar(self, ctx, member: discord.Member):
        await self.abrir_conta(ctx.author)
        await self.abrir_conta(member)

        meu = await self.atualizar_banco(ctx.author)
        din = await self.atualizar_banco(member)

        if din[1] < 100:
            await ctx.send("🔒 Não vale a pena...")
            return

        if meu[1] < din[1] / 2:
            await ctx.send("🔒 Você precisa ter pelo menos metade dos ganhos de quem está tentando roubar o cofre...")
            return

        range = int((20/100) * din[1])
        ganhos = random.randrange(0, range)

        await self.atualizar_banco(ctx.author, ganhos)
        await self.atualizar_banco(member, -1 * ganhos, "cofre")

        await ctx.send(f"O cara roubou aqui!!! Foram {ganhos} 🪙 do cofre do {member.mention}!")


    @commands.command(aliases=["gambling", "roletar", "gamble", "g", "bet"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def apostar(self, ctx, quantia=None):
        await self.abrir_conta(ctx.author)

        if quantia is None:
            await ctx.send("🎰 Infome a quantia que deseja apostar!")
            return

        din = await self.atualizar_banco(ctx.author)

        if quantia == "all" or quantia == "tudo":
            quantia = din[0]

        quantia = int(quantia)

        if quantia > din[0]:
            await ctx.send("Você não é rico não!")
            return
        if quantia < 0:
            await ctx.send("Como que tu vai apostar dinheiro negativo?")
            return
        if quantia == 0:
            await ctx.send("Não tem como apostar nada...")
            return

        final = []

        for _ in range(3):
            # a = random.choice(["🔔", "🧲", "🧶", "🧸", "7️⃣", "💎", "🍒", "🍀"])
            a = random.choice(["🔔", "🧲", "7️⃣", "💎", "🍒", "🍀"])

            final.append(a)

        await ctx.send(str(final))

        if final[0] == final[1] and final[1] == final[2]:
            await self.atualizar_banco(ctx.author, 5 * quantia)
            await ctx.send(f"Você ganhou {5 * quantia} 🪙!!!")
        elif final[0] == final[1] or final[0] == final[2] or final[2] == final[1]:
            await self.atualizar_banco(ctx.author, 2 * quantia)
            await ctx.send(f"Você ganhou {2 * quantia} 🪙!!!")
        else:
            await self.atualizar_banco(ctx.author, -1 * quantia)
            await self.atualizar_banco(self.bot.user, quantia, "cofre")
            await ctx.send("Você perdeu... 🤣")


    async def abrir_conta(self, user):
        users = await self.get_banco()

        if str(user.id) in users:
            return False
        else:
            users[str(user.id)] = {}
            users[str(user.id)]["carteira"] = 0
            users[str(user.id)]["cofre"] = 0
            users[str(user.id)]["mochila"] = []

        with open("banco.json", "w") as f:
            json.dump(users, f)

        return True


    async def get_banco(self):
        with open("banco.json", "r") as f:
            users = json.load(f)

        return users


    async def atualizar_banco(self, user, quantia=0, modo="carteira"):
        users = await self.get_banco()

        quantia = int(quantia)
        users[str(user.id)][modo] += quantia

        with open("banco.json", "w") as f:
            json.dump(users, f)

        din = [users[str(user.id)]["carteira"], users[str(user.id)]["cofre"]]

        return din


    lojinha = [
        {"nome": "Waffle", "preco": 100, "emoji": "🧇", "descricao": "comida"},
        {"nome": "Picareta", "preco": 200, "emoji": "⛏️", "descricao": "ferramenta"},
        {"nome": "Vara", "preco": 200, "emoji": "🎣", "descricao": "ferramenta"},
        {"nome": "Pedra", "preco": 200, "emoji": "🪨", "descricao": "recurso"},
        {"nome": "Diamante", "preco": 5000, "emoji": "💎", "descricao": "recurso"},
        {"nome": "Dodo", "preco": 3000, "emoji": "🦤", "descricao": "recurso"},
        {"nome": "Peixe", "preco": 200, "emoji": "🐟", "descricao": "recurso"},
        {"nome": "Castigo1", "preco": 250000, "emoji": "😝 60s **(🚧)**", "descricao": "utilitario"},
        {"nome": "Castigo2", "preco": 1250000, "emoji": "🤔 5min **(🚧)**", "descricao": "utilitario"},
        {"nome": "Castigo3", "preco": 2500000, "emoji": "😭 10min **(🚧)**", "descricao": "utilitario"},
        {"nome": "Castigo4", "preco": 15000000, "emoji": "😱 1h **(🚧)**", "descricao": "utilitario"},
        {"nome": "Castigo5", "preco": 360000000, "emoji": "🥵 1 dia **(🚧)**", "descricao": "utilitario"},
        {"nome": "Castigo6", "preco": 2520000000, "emoji": "💀 1 semana **(🚧)**", "descricao": "utilitario"},
        {"nome": "Milionario", "preco": 1000000, "emoji": "💵 Cargo no **Waffle** **(🚧)**", "descricao": "cargo"},
        {"nome": "Bilionario", "preco": 1000000000, "emoji": "💶 Cargo no **Waffle** **(🚧)**", "descricao": "cargo"}
    ]


    @commands.command(aliases=["store", "mercado", "lojinha", "market", "l"])
    async def loja(self, ctx):
        em = discord.Embed(title="Loja 🛍️", color=0xf2bc66)

        em.add_field(name="**------------------**\nProduto", value=f"Preço 🪙 | Emoji\n**------------------**\n🚧 Em obras\n**------------------**\n")

        for item in self.lojinha:
            nome = item["nome"]
            preco = item["preco"]
            emoji = item["emoji"]
            em.add_field(name=nome, value=f"{preco} | {emoji}", inline=False)

        await ctx.send(embed=em)


    @commands.command(aliases=["buy"])
    async def comprar(self, ctx, item, quantidade=1):
        await self.abrir_conta(ctx.author)

        res = await self.comprar_isso(ctx.author, item, quantidade)

        if not res[0]:
            if res[1] == 1:
                await ctx.send("Não tem isso ai na vendinha!")
                return
            if res[1] == 2:
                await ctx.send(f"Você não tem dinheiro suficiente na carteira para {quantidade} {item}")
                return

        await ctx.send(f"Você comprou {quantidade} {item}")


    async def comprar_isso(self, user, item_nome, quantidade):
        item_nome = item_nome.lower()
        nome_ = None

        for item in self.lojinha:
            nome = item["nome"].lower()
            if (nome == item_nome):
                nome_ = nome
                preco = item["preco"]
                break

        if (nome_ == None):
            return [False, 1]

        custo = preco * quantidade

        din = await self.atualizar_banco(user)

        if (din[0] < custo):
            return [False, 2]

        users = await self.get_banco()

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

        await self.atualizar_banco(user, custo * -1, "carteira")

        return [True, "Funcionou"]


    @commands.command(aliases=["bag", "itens", "inventario"])
    async def mochila(self, ctx, member: discord.Member=None):
        await self.abrir_conta(ctx.author)
        if member is None:
            member = ctx.author

        users = await self.get_banco()

        try:
            mochila = users[str(member.id)]["mochila"]
        except:
            mochila = []

        em = discord.Embed(title="🎒 Mochila", color=0xf2bc66)
        for item in mochila:
            nome = item["item"]
            quantidade = item["quantidade"]

            em.add_field(name=nome, value=quantidade)

        await ctx.send(embed=em)


    @commands.command(aliases=["utilizar", "use"])
    @commands.cooldown(1, 28800, commands.BucketType.user)
    async def usar(self, ctx, item, quantidade=1, member=None):
        await self.abrir_conta(ctx.author)

        res = await self.usar_isso(ctx.author, item, quantidade)

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

        if res[2]["descricao"] == "comida":
            await ctx.send(f"Você comeu {quantidade} {item}")
        elif res[2]["descricao"] == "utilitario":
            await ctx.send(f"Você aplicou {quantidade} {res[2]['nome']} em {member}!")
        else:
            await ctx.send(f"Você usou {quantidade} {res[2]['nome']}!")


    async def usar_isso(self, user, item_nome, quantidade):
        item_nome = item_nome.lower()
        item_usar = None
        for item in self.lojinha:
            nome = item["nome"].lower()
            if nome == item_nome:
                item_usar = item
                break

        if item_usar is None:
            return [False, 1]

        users = await self.get_banco()

        try:
            i = 0
            f = None
            for coisa in users[str(user.id)]["mochila"]:
                n = coisa["item"]
                if n == item_nome:

                    if item_usar["descricao"] == "utilitario":
                        quantidade = 1

                    quant_velha = coisa["quantidade"]
                    nova_quant = quant_velha - quantidade

                    if nova_quant < 0:
                        return [False, 2, item_usar]

                    users[str(user.id)]["mochila"][i]["quantidade"] = nova_quant
                    f = 1

                    break
                i += 1
            if f is None:
                return [False, 3, item_usar]
        except:
            return [False, 3, item_usar]

        with open("banco.json", "w") as f:
            json.dump(users, f)

        return [True, "Funcionou", item_usar]


    @commands.command(aliases=["sell"])
    async def vender(self, ctx, item, quantidade=1):
        await self.abrir_conta(ctx.author)

        res = await self.vender_isso(ctx.author, item, quantidade)

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

        await ctx.send(f"Você vendeu {quantidade} {item}")


    async def vender_isso(self, user, item_nome, quantidade, preco=None):
        item_nome = item_nome.lower()
        nome_ = None
        for item in self.lojinha:
            nome = item["nome"].lower()
            if nome == item_nome:
                nome_ = nome
                if preco is None:
                    preco = 0.9 * item["preco"]  
                break

        if nome_ is None:
            return [False, 1]

        custo = preco * quantidade

        users = await self.get_banco()

        din = await self.atualizar_banco(user)

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
            if f is None:
                return [False, 3]
        except:
            return [False, 3]

        with open("banco.json", "w") as f:
            json.dump(users, f)

        await self.atualizar_banco(user, custo, "carteira")
        await self.atualizar_banco(self.bot.user, custo, "cofre")

        return [True, "Funcionou"]


    @commands.command(aliases=["rk"])
    async def ranking(self, ctx, x=3):
        users = await self.get_banco()
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
            membro = self.bot.get_user(id_)
            nome = membro.name
            em.add_field(name=f"{i}. {nome}", value=f"{qtd}", inline=False)
            if i == x:
                break
            else:
                i += 1

        await ctx.send(embed=em)


async def setup(bot):
    await bot.add_cog(Economia(bot))
