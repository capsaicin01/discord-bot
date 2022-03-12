from http.client import HTTPS_PORT
import discord
import youtube_dl

class Queue(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._current_song = None
        self._loopmode = 0

    def next_song(self):
        if self._loopmode == 0:
            self._current_song = self.pop(0)
        elif self._loopmode == 1:
            pass
        elif self._loopmode == 2:
            self.append(self.current_song)
            self._current_song = self.pop(0)

        
        return self._current_song
    

    def set_loop_mode(self, mode):
        self._loopmode = mode


    def clear(self):
        super().clear()
        self._current_song = None
    
    
    @property
    def current_song(self):
        return self._current_song
    
    @property
    def loop_mode(self):
        return self._loopmode

    
    def get_embed(self, song_idx: int):
        if song_idx <= 0:
            song = self.current_song
        else:
            song = self[song_idx-1]
        
        embed = discord.Embed(title="Şarkı Bilgisi")
        embed.set_thumbnail(url=song.thumbnail)
        embed.add_field(name='Şarkı', value=song.title, inline=True)
        embed.add_field(name='Kanal', value=song.uploader, inline=True)
        embed.add_field(name='Süre', value=song.duration_formatted, inline=True)
        embed.add_field(name='Görüntülenme', value=song.views, inline=True)
        embed.add_field(name='Beğeni', value=song.likes, inline=True)

        return embed


class SongRequestError(Exception):
    pass


class Song(dict):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}

    def __init__(self, url: str):
        super().__init__()
        self.download_info(url)

        if self.get('is_live', True):
            raise SongRequestError("Geçersiz video - canlı yayın veya desteklenmeyen website.")
        elif self.url is None:
            raise SongRequestError("Geçerli bir URL girmediniz.")
        
    @property
    def url(self):
        return self.get("url", None)
    
    @property
    def source_url(self):
        return self["entries"][0]["formats"][0].get("url", None)

    @property
    def title(self):
        return self.get("title", "-")
    
    @property
    def uploader(self):
        return self.get("uploader", "-")

    @property
    def duration_raw(self):
        return self.get("duration", 0)

    @property
    def duration_formatted(self):
        dakika, saniye = self.duration_raw // 60, self.duration_raw % 60
        return f"{dakika}:{str(saniye).zfill(2)}"
    
    @property
    def views(self):
        return self.get("view_count", 0)

    @property
    def likes(self):
        return self.get("like_count", 0)

    @property
    def thumbnail(self):
        return self.get("thumbnail", "https://cdn.discordapp.com/avatars/796335968940458025/7026c49df439391745a9770a67a274fb.webp?size=1024")
    
    def download_info(self, url: str):
        with youtube_dl.YoutubeDL(self.YDL_OPTIONS) as ydl:
            
            self.update(ydl.extract_info(url, download=False))
            if url.startswith("https"):
                self["source_url"] = self["formats"][0]["url"]
            else:
                self.update(ydl.extract_info(self['entries'][0]['webpage_url'], download=False))
                self["source_url"] = self["entries"][0]["formats"][0]["url"]
            
            self["url"] = url