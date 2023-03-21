import discord
from discord import app_commands
from discord.ext import commands
import random

def run_discord_bot():
    TOKEN = "MTA4NzIwMTg5NTYyMzQ0MjQ2Mg.GJ9aka.Tr3Lz_lKl4iv2g8Ze0AOyS8_Wt2lgRl-GCIfPI"
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print("Wafflinho está rodando!")
        try:
            synced = await bot.tree.sync()
            print(f"Synced {len(synced)} command's")
        except Exception as e:
            print(e)

    @bot.command()
    async def oie(ctx):
        await ctx.send("Oie!")

    @bot.command()
    async def ajuda(ctx):
        await ctx.send("`Oie eu sou o Wafflinho, o novo Bot oficial do Waffle!`")
        await ctx.send("`Meus comandos são:\n[!ajuda] Mostra esse menu;\n[!add] Consigo somar dois números;\n[!add_list] Sei somar vários números;\n[!dado] Roda um dado;\n[/fale] Consigo falar algo que você mande;\n[!clear] Consigo apagar várias mensagens.`")

    @bot.command()
    async def add(ctx, x, y):
        result = int(x) + int(y)
        await ctx.send(f"{x} + {y} = {result}")

    @bot.command()
    async def add_list(ctx, *arr):
        result = 0;
        for i in arr:
            result += int(i)
        await ctx.send(f"Deu {result}!")
    
    @bot.command(name="dado")
    async def dado(ctx):
        await ctx.channel.send(random.randint(1, 6))

    @bot.command(aliases = ['purge', 'delete'])
    @commands.has_permissions(manage_messages = True)
    async def clear(ctx, amount: int = 0):
        if amount < 100:
            await ctx.channel.purge(limit = amount + 1)
            await ctx.channel.send(f"Foram limpadas {amount} mensagens!")
            await ctx.channel.purge(limit = 1)
        else:
            await ctx.channel.send("Somente é possível deletar 100 mensagens por vez")

    @bot.tree.command(name="oi")
    async def oi(interaction: discord.Interaction):
        await interaction.response.send_message(f"Oie {interaction.user.mention}!", ephemeral=True)

    @bot.tree.command(name="fale")
    @app_commands.describe(thing_to_say = "O que eu deveria dizer?")
    async def say(interaction: discord.Interaction, thing_to_say: str):
        await interaction.response.send_message(f"{interaction.user.name} disse: `{thing_to_say}`")

    bot.run(TOKEN)
