import asyncio
from collections import defaultdict

import discord
from discord.ext import commands
from discord.utils import get
from Music.musicClasses import Queue, Song, SongRequestError


def set_str_len(s: str, length: int):
    '''Adds whitespace or trims string to enforce a specific size'''

    return s.ljust(length)[:length]


class SesKomutlari(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.music_queues = defaultdict(Queue)

    @commands.command()
    async def play(self, ctx: commands.Context, url: str, *args: str):
        
        music_queue = self.music_queues[ctx.guild]
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        try:
            channel = ctx.message.author.voice.channel
        except:
            await ctx.send("Bir ses kanalında değilsin :face_with_raised_eyebrow:")
            return
        
        if voice is not None and not self.client_in_same_channel(ctx.message.author, ctx.guild):
            await ctx.send("Bot farklı bir ses kanalında")
            return
        
        if not url.startswith("https://"):
            url = f"ytsearch:{url} {' '.join(args)}"
        
        try:
            song = Song(url)
        except SongRequestError:
            await ctx.send(SongRequestError.args[0])
            return
        
        music_queue.append(song)
        await ctx.send(f"**{song.title}** listeye eklendi")

        if voice is None or not voice.is_connected():
            await channel.connect()
        
        await self.play_queue(ctx.guild)
    

    @commands.command()
    async def queue(self, ctx: commands.Context):
        queue = self.music_queues.get(ctx.guild)
        
        if not queue:
            await ctx.send("Liste boş")
            return
        
        for pos, song in enumerate(queue):
            title = set_str_len(song.title, 65)
            uploader = set_str_len(song.uploader, 34)
            to_send = f'{set_str_len(f"{pos + 1})", 4)}{title}| {uploader}| {song.duration_formatted}\n'
        
        await ctx.send(to_send)


    @commands.command()
    async def clear(self, ctx: commands.Context):
        voice = get(self.bot.voice_clients, guild = ctx.guild)
        queue = self.music_queues.get(ctx.guild)

        voice.stop()
        queue.clear()
        await ctx.send("Liste temizlendi.")
        await voice.disconnect()


    @commands.command()
    async def loop(self, ctx: commands.Context, mode=None):
        queue = self.music_queues.get(ctx.guild)
        if queue.current_song is None:
            await ctx.send("Bot şu anda müzik çalmıyor.")
            return

        if mode == "info":
            await ctx.send(queue.loop_mode)
        elif mode == "tek":
            queue.set_loop_mode(1)
        elif mode == "liste":
            queue.set_loop_mode(2)
        elif mode == "kapat":
            queue.set_loop_mode(0)
        else:
            await ctx.send("{0}: Doğru kullanım:\n```\nloop tek | liste | kapat\n```".format(ctx.author))

    @commands.command()
    async def skip(self, ctx: commands.Context):
        voice = get(self.bot.voice_clients, guild=ctx.guild)

        if voice is None or not voice.is_playing():
            await ctx.send("Atlanılacak şarkı yok...")
        else:
            voice.stop()
    

    @commands.command()
    async def remove(self, ctx: commands.Context, song_idx: int = None):
        if song_idx == None:
            queue = self.music_queues.get(ctx.guild)

            for index, song in reversed(list(enumerate(queue))):
                queue.pop(index)
                await ctx.send(f"{song.title} listeden kaldırıldı.")
                return
        else:
            queue = self.music_queues.get(ctx.guild)
            try:
                song = queue[song_idx -1]
            except IndexError:
                await ctx.send("Bu sırada bir şarkı yok.")
                return

            queue.pop(song_idx - 1)
            await ctx.send(f"{song.title} listeden kaldırıldı.")
    

    @commands.command()
    async def songinfo(self, ctx: commands.Context, song_index: int=0):
        queue = self.music_queues.get(ctx.guild)

        if song_index not in range(len(queue)+1):
            await ctx.send("Bu sırada bir şarkı yok")
            return
        
        embed = queue.get_embed(song_index)
        await ctx.send(embed=embed)
    

    async def play_queue(self, guild: discord.Guild):
        queue = self.music_queues.get(guild)

        while True:
            try:
                await self.wait_for_end_of_song(guild)
                song = queue.next_song()
                await self.play_song(guild, song)
            except:
                break

        await self.inactivity_disconnect(guild)
    
    async def play_song(self, guild: discord.Guild, song: Song):
        '''Downloads and starts playing a YouTube video's audio.'''

        voice = get(self.bot.voice_clients, guild=guild)
        voice.play(discord.FFmpegPCMAudio(song["formats"][0]["url"]))

    async def wait_for_end_of_song(self, guild: discord.Guild):
        voice = get(self.bot.voice_clients, guild=guild)
        while voice.is_playing():
            await asyncio.sleep(3)
    

    async def inactivity_disconnect(self, guild: discord.Guild):
        voice = get(self.bot.voice_clients, guild=guild)
        queue = self.music_queues.get(guild)
        last_song = queue.current_song

        while voice.is_playing():
            await asyncio.sleep(10)

        await asyncio.sleep(300)
        if queue.current_song == last_song:
            await voice.disconnect()
    
    def client_in_same_channel(self, author: discord.Member, guild: discord.Guild):
        voice = get(self.bot.voice_clients, guild=guild)

        try:
            channel = author.voice.channel
        except AttributeError:
            return False
        
        return voice is not None and voice.is_connected() and channel == voice.channel

    

def setup(client):
    client.add_cog(SesKomutlari(client))
