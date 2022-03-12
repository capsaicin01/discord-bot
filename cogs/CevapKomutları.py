from http import client
import discord
import asyncio
from discord.ext import commands

responses = {"sa":"Aleyküm selam mümin aga",
             "aaaaaaaaa":"SUUPRAAAAAAAAAAAAAAA",
             "napim":"Lafı koydu :sunglasses:",
             "kes":"Kesersem içinde kalır :sunglasses:",
             "fıratabiözlüsöz":"https://cdn.discordapp.com/attachments/906985365083144312/937812589818302525/firatabi.jpg",
             "galio":"https://cdn.discordapp.com/attachments/906985365083144312/937812590128660530/galio.png"
             }

class CevapKomutlari(commands.Cog):
    
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_message(self, msg):
        lowered_message = msg.content.lower()
        if lowered_message in responses.keys():
            await msg.channel.send(responses.get(lowered_message))

def setup(client):
    client.add_cog(CevapKomutlari(client))