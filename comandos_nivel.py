import asyncio
import discord
import json
import math
import random
from discord.ext import commands

class nvl(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.canais_especificos = {
            ID_DO_SERVER: ID_DO_CANAL,
            ID_DO_SERVER: ID_DO_CANAL,
        }


    async def level_up(self, user, users):
        current_experience = users[str(user.id)]["xp"]
        current_level = users[str(user.id)]["nvl"]

        required_experience = math.ceil((6 * (current_level ** 4)) / 2.5)

        if current_experience >= required_experience:
            users[str(user.id)]["nvl"] += 1
            return True
        
        return False


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.bot.user.id:
           return

        user = message.author
        await self.abrir_niveis(user)

        async with asyncio.Lock():
            users = await self.get_niveis()

            random_exp = random.randint(5, 15)
            users[str(user.id)]["xp"] += random_exp

            if await self.level_up(user, users):
                level_up_embed = discord.Embed(title="Ebaaa você subiu de nível!", color=discord.Color.green())
                level_up_embed.add_field(name="Parabéns 🎉", value=f"{message.author.mention} subiu para o nível {users[str(user.id)]['nvl']}!")

                guild_id = message.guild.id
                if guild_id in self.canais_especificos:
                    canal_id = self.canais_especificos[guild_id]
                    canal = self.bot.get_channel(canal_id)
                    if canal:
                        await canal.send(embed=level_up_embed)

            with open("usuarios.json", "w") as f:
                json.dump(users, f)


    @commands.command(aliases=["lvl", "nvl", "xp"])
    async def level(self, ctx, member: discord.Member = None):
        await self.abrir_niveis(ctx.author)
        if member is None:
            member = ctx.author

        users = await self.get_niveis()

        level_card = discord.Embed(title=f"XP do {member.name}", color=discord.Color.random())
        level_card.add_field(name="Nível:", value=users[str(member.id)]["nvl"])
        level_card.add_field(name="Experiência:", value=users[str(member.id)]["xp"])
        level_card.set_footer(text=f"Requisitado por {ctx.author.name}", icon_url=ctx.author.avatar)
        await ctx.send(embed=level_card)
    

    async def abrir_niveis(self, user):
        users = await self.get_niveis()

        if str(user.id) in users:
            return False
        else:
            users[str(user.id)] = {
                "nvl": 1,
                "xp": 0
            }

            with open("usuarios.json", "w") as f:
                json.dump(users, f)

        return True
    

    async def get_niveis(self):
        with open("usuarios.json", "r") as f:
            users = json.load(f)
        return users


async def setup(bot):
    await bot.add_cog(nvl(bot))
