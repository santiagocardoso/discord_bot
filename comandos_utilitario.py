import asyncio
import discord
from discord.ext import commands

class Utilitario(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["purge", "delete", "vanish", "wipe"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 0):
        if amount < 6 + 1:
            await ctx.message.delete()
            await ctx.channel.purge(limit=amount)
        else:
            await ctx.message.delete()
            await ctx.channel.send("Somente é possível deletar 30 mensagens por vez")
            await asyncio.sleep(2)
            await ctx.channel.purge(limit=1)


    @commands.command(name="poll", aliases=["vote", "votar"])
    async def poll(self, ctx, *, message):
        emb = discord.Embed(title="VOTAÇÃO", description=f"{message}", color=0xf2bc66)
        await ctx.message.delete()
        msg = await ctx.channel.send(embed=emb)
        await msg.add_reaction("👍")
        await msg.add_reaction("👎")


async def setup(bot):
    await bot.add_cog(Utilitario(bot))