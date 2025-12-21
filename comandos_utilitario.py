import asyncio
import discord
import os
import random
import json
from discord.ext import commands
from discord import ui

PASTA_IMAGENS = "img"
ARQUIVO_CONFIG = "mapas.json"

def carregar_config():
    if os.path.exists(ARQUIVO_CONFIG):
        with open(ARQUIVO_CONFIG, 'r') as f:
            return json.load(f)
    return {}

def salvar_config(config):
    with open(ARQUIVO_CONFIG, 'w') as f:
        json.dump(config, f, indent=4)

class MapButton(ui.Button):
    def __init__(self, mapa_arquivo, status_inicial):
        nome_mapa = os.path.splitext(mapa_arquivo)[0].replace("_", " ").title()
        emoji = "🟢" if status_inicial else "🔴"
        
        super().__init__(
            label=f"{nome_mapa}",
            emoji=emoji,
            style=discord.ButtonStyle.green if status_inicial else discord.ButtonStyle.danger,
            custom_id=f"map_{mapa_arquivo}"
        )
        self.mapa_arquivo = mapa_arquivo

    async def callback(self, interaction: discord.Interaction):
        view: VermintideView = self.view
        novo_status = not view.mapas_status[self.mapa_arquivo]
        view.mapas_status[self.mapa_arquivo] = novo_status
        
        salvar_config(view.mapas_status)
        
        view.atualizar_botoes()
        await interaction.response.edit_message(embed=view.criar_embed(), view=view)


class VermintideView(ui.View):
    def __init__(self, mapas):
        super().__init__(timeout=None) 
        
        config_salva = carregar_config()
        self.mapas_status = {m: config_salva.get(m, True) for m in mapas}
        
        self.lista_mapas = mapas
        self.pagina = 0
        self.itens_por_pagina = 20
        
        self.ultima_msg_sorteio = None
        
        self.atualizar_botoes()

    def criar_embed(self):
        total_ativos = sum(1 for v in self.mapas_status.values() if v)
        total_mapas = len(self.lista_mapas)
        max_paginas = (total_mapas - 1) // self.itens_por_pagina + 1
        
        emb = discord.Embed(
            title="🔮 Sorteio de Mapas Vermintide",
            description="Selecione quais mapas entrarão nas mãos do destino.",
            color=0xaa8dd8
        )
        emb.add_field(name="Status", value=f"✅ **{total_ativos}** ativos / **{total_mapas}** total", inline=True)
        emb.add_field(name="Página", value=f"📄 {self.pagina + 1} de {max_paginas}", inline=True)
        emb.set_footer(text="🟢 Incluído | 🔴 Removido")
        return emb

    def atualizar_botoes(self):
        self.clear_items()
        
        inicio = self.pagina * self.itens_por_pagina
        fim = inicio + self.itens_por_pagina
        mapas_da_pagina = self.lista_mapas[inicio:fim]

        for mapa in mapas_da_pagina:
            status = self.mapas_status.get(mapa, True)
            self.add_item(MapButton(mapa, status))

        btn_prev = ui.Button(label="⬅️", style=discord.ButtonStyle.secondary, disabled=(self.pagina == 0), row=4)
        btn_prev.callback = self.prev_page
        self.add_item(btn_prev)

        btn_sortear = ui.Button(label="🎲 SORTEAR", style=discord.ButtonStyle.primary, row=4)
        btn_sortear.callback = self.sortear_callback
        self.add_item(btn_sortear)

        max_paginas = (len(self.lista_mapas) - 1) // self.itens_por_pagina
        btn_next = ui.Button(label="➡️", style=discord.ButtonStyle.secondary, disabled=(self.pagina >= max_paginas), row=4)
        btn_next.callback = self.next_page
        self.add_item(btn_next)

    async def prev_page(self, interaction: discord.Interaction):
        self.pagina -= 1
        self.atualizar_botoes()
        await interaction.response.edit_message(embed=view.criar_embed(), view=self)

    async def next_page(self, interaction: discord.Interaction):
        self.pagina += 1
        self.atualizar_botoes()
        await interaction.response.edit_message(embed=view.criar_embed(), view=self)

    async def sortear_callback(self, interaction: discord.Interaction):
        if self.ultima_msg_sorteio:
            try:
                await self.ultima_msg_sorteio.delete()
            except:
                pass

        ativos = [m for m, status in self.mapas_status.items() if status]

        if not ativos:
            await interaction.response.send_message("❌ Nenhum mapa selecionado. Ative pelo menos um mapa!", ephemeral=True)
            return

        vencedor = random.choice(ativos)
        nome_mapa = os.path.splitext(vencedor)[0].replace("_", " ").title()
        caminho = os.path.join(PASTA_IMAGENS, vencedor)

        embed_vitoria = discord.Embed(
            title="⚔️ Mapa Sorteado!",
            description=f"O destino escolheu: **{nome_mapa}**",
            color=0xf2bc66
        )

        if os.path.exists(caminho):
            file = discord.File(caminho, filename="mapa.png")
            embed_vitoria.set_image(url="attachment://mapa.png")
            await interaction.response.send_message(file=file, embed=embed_vitoria)
        else:
            await interaction.response.send_message(embed=embed_vitoria)

        self.ultima_msg_sorteio = await interaction.original_response()


class Utilitario(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sort")
    async def sort(self, ctx):
        if not os.path.exists(PASTA_IMAGENS):
            await ctx.send(f"A pasta `{PASTA_IMAGENS}` não existe.")
            return
            
        mapas = [f for f in os.listdir(PASTA_IMAGENS) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        mapas.sort()

        if not mapas:
            await ctx.send("Nenhuma imagem encontrada na pasta.")
            return

        view = VermintideView(mapas)
        await ctx.send(embed=view.criar_embed(), view=view)

    @commands.command(aliases=["purge", "delete", "vanish", "wipe"])
    @commands.cooldown(1, 4, commands.BucketType.default)
    @commands.has_any_role("💘- Queen miau -💘", "⭐we love casting miaus⭐", "STREAMER", "MOD", "VIP")
    async def clear(self, ctx, amount: int = 0):
        quant = 10
        if amount < quant + 1:
            await ctx.message.delete()
            await ctx.channel.purge(limit=amount)
        else:
            await ctx.message.delete()
            await ctx.channel.send(f"Somente é possível deletar {quant} mensagens por vez")
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
