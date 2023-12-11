import asyncio
import discord
from discord.ext import commands
import json
import random

class Economia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    
    @commands.command(aliases=["carteira", "conta"])
    async def dinheiro(self, ctx):
        await self.abrir_conta(ctx.author)

        user = ctx.author
        users = await self.get_banco()

        quant_carteira = users[str(user.id)]["carteira"]
        quant_cofre = users[str(user.id)]["cofre"]

        em = discord.Embed(title=f"💰 Conta do {ctx.author.name}!", color=ctx.author.color)
        em.add_field(name="Carteira 🪙", value=quant_carteira)
        em.add_field(name="Cofre 🪙", value=quant_cofre)
        await ctx.send(embed=em)


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):  # Verifica se está em cooldown
            msg = f"**Ainda tá em cooldown**, tente novamente em {error.retry_after:.2f}s"
            await ctx.send(msg)


    @commands.command(aliases=["implorar"])
    @commands.cooldown(5, 60, commands.BucketType.user)
    async def pedir(self, ctx):
        await self.abrir_conta(ctx.author)

        user = ctx.author
        users = await self.get_banco()

        ganhos = random.randrange(201)

        await ctx.send(f"Alguém te deu {ganhos} 🪙!!")

        users[str(user.id)]["carteira"] += ganhos

        with open("banco.json", "w") as f:
            json.dump(users, f)


    @commands.command()
    async def sacar(self, ctx, quantia=None):
        await self.abrir_conta(ctx.author)

        if quantia is None:
            await ctx.send("📤 Infome a quantia que deseja sacar!")
            return

        din = await self.atualizar_banco(ctx.author)

        quantia = int(quantia)

        if quantia > din[1]:
            await ctx.send("Você não é rico não!")
            return
        if quantia < 0:
            await ctx.send("Como que tu vai sacar dinheiro negativo?")
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

        quantia = int(quantia)
        if quantia > din[0]:
            await ctx.send("Você não é rico não!")
            return
        if quantia < 0:
            await ctx.send("Como que tu vai depositar dinheiro negativo?")
            return

        await self.atualizar_banco(ctx.author, -1 * quantia)
        await self.atualizar_banco(ctx.author, quantia, "cofre")

        await ctx.send(f"Você depositou {quantia} 🪙!")


    @commands.command()
    async def enviar(self, ctx, member: discord.Member, quantia=None):
        await self.abrir_conta(ctx.author)
        await self.abrir_conta(member)

        if quantia is None:
            await ctx.send("💸 Infome a quantia que deseja enviar!")
            return

        din = await self.atualizar_banco(ctx.author)

        if quantia == "all":
            quantia = din[0]

        quantia = int(quantia)

        if quantia > din[1]:
            await ctx.send("Você não é rico não!")
            return
        if quantia < 0:
            await ctx.send("Como que tu vai depositar dinheiro negativo?")
            return

        await self.atualizar_banco(ctx.author, -1 * quantia, "cofre")
        await self.atualizar_banco(member, quantia, "cofre")

        await ctx.send(f"Você deu {quantia} 🪙!")


    @commands.command()
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def roubar(self, ctx, member: discord.Member):
        await self.abrir_conta(ctx.author)
        await self.abrir_conta(member)

        din = await self.atualizar_banco(member)

        if din[0] < 100:
            await ctx.send("🔒 Não vale a pena...")
            return

        ganhos = random.randrange(0, din[0])

        await self.atualizar_banco(ctx.author, ganhos)
        await self.atualizar_banco(member, -1 * ganhos)

        await ctx.send(f"O cara roubou aqui!!! Foram {ganhos} 🪙 do {member.mention}!")


    @commands.command(aliases=["gambling", "roletar"])
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

        final = []

        for _ in range(3):
            a = random.choice(["🔔", "🧲", "🧶", "🧸", "7️⃣", "💎", "🍒", "🍀"])

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
            await ctx.send("Você perdeu...")


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
        {"nome": "Castigo 60s", "preco": 25000, "emoji": "😝", "descricao": "utilitario"},
        {"nome": "Castigo 5min", "preco": 100000, "emoji": "🤔", "descricao": "utilitario"},
        {"nome": "Castigo 10min", "preco": 500000, "emoji": "😭", "descricao": "utilitario"},
        {"nome": "Castigo 1h", "preco": 1000000, "emoji": "😱", "descricao": "utilitario"},
        {"nome": "Castigo 1 semana", "preco": 100000000, "emoji": "🥵", "descricao": "utilitario"},
        {"nome": "Cargo milionário **(Waffle)**", "preco": 1000000, "emoji": "💵", "descricao": "cargo"},
        {"nome": "Cargo bilionário **(Waffle)**", "preco": 1000000000, "emoji": "💶", "descricao": "cargo"},
    ]

    @commands.command(aliases=["store", "mercado", "lojinha", "market"])
    async def loja(self, ctx):
        em = discord.Embed(title="Loja 🛍️", color=0xf2bc66)

        em.add_field(name="------------------\nProduto", value=f"Preço 🪙 | Emoji\n**------------------**")

        for item in self.lojinha:
            nome = item["nome"]
            preco = item["preco"]
            emoji = item["emoji"]
            em.add_field(name=nome, value=f"{preco} | {emoji}", inline=False)

        await ctx.send(embed=em)


    @commands.command()
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

        users = await self.get_banco()

        din = await self.atualizar_banco(user)

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

        await self.atualizar_banco(user, custo * -1, "carteira")

        return [True, "Funcionou"]


    @commands.command(aliases=["bag", "itens", "inventario"])
    async def mochila(self, ctx):
        await self.abrir_conta(ctx.author)
        user = ctx.author
        users = await self.get_banco()

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


    @commands.command(aliases=["utilizar"])
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
            await ctx.send(f"Você aplicou {res[2]['nome']} em {member}!")


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


    @commands.command()
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
                    preco = 0.8 * item["preco"]  
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