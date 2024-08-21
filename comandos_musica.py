import discord
from discord.ext import commands

class Musica(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="entrar", aliases=["join"])
    async def join(self, ctx):
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


    @commands.command(name="sair", aliases=["leave", "disconnect", "quit", "parar", "encerrar", "stop"])
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.send("Ok... Estou saindo \U0001F62D")

'''
    @bot.command(name="play", aliases=["tocar"])
    async def play(self, ctx, url):
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
    async def pause(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            await ctx.send("\u23F8 Pausando a reprodução.")
            ctx.voice_client.pause()
        else:
            await ctx.send("O bot não está reproduzindo ou não está em um canal de voz.")


    @bot.command(name="resume", aliases=["resumir", "voltar", "unpause", "despausar"])
    async def resume(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_paused():
            await ctx.send("\u25B6 Resumindo a reprodução.")
            ctx.voice_client.resume()
        else:
            await ctx.send("O bot não está pausado ou não está em um canal de voz.")
    '''


async def setup(bot):
    await bot.add_cog(Musica(bot))