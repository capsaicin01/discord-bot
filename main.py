# image editing
import asyncio
import os
import platform
import sqlite3
import time
from io import BytesIO
from pathlib import Path

import discord
from discord.ext import commands
from PIL import Image

from functions import *

isletim_sistemi = platform.system()
intents = discord.Intents.all()
client = commands.Bot(command_prefix="",
                      case_insensitive=True,
                      intents=intents)

# Cogs Setup
cog_list = [p.stem for p in Path(".").glob("./cogs/*.py")]
for cog in cog_list:
    client.load_extension(f"cogs.{cog}")
    print(f"Loaded '{cog}' cog.")

with open("token.txt", "r", encoding="utf-8") as file:
    token = file.read()

async def members():
    activeGuilds = client.guilds
    channel = client.get_channel(940660296748515358)
    sum = 0
    for s in activeGuilds:
        sum += len(s.members)
    await channel.edit(name='❎ KİŞİ SAYISI: {} ❎'.format(int(sum)))
    await asyncio.sleep(1)


@client.event
async def on_ready():
    activity = discord.Game(name="Made by capsaicin#0129", type=3)
    await client.change_presence(status=discord.Status.online, activity=activity)
    print(client.guilds)



@client.event
async def on_member_join(member):
    sv = client.get_guild(757259257421889617)
    id = client.get_channel(801033615176892446)
    embed = discord.Embed(
        title="SUNUCUYA HOŞGELDİN!",
        description=f"Hosgeldin {member.mention} kardes <:sumichan:792039166467899403>"
    )
    embed.set_author(name=member, icon_url=member.avatar_url)
    embed.set_image(
        url="https://cdn.discordapp.com/attachments/802104550608994334/938014849865244682/resim_2022-02-01_131525.png")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text="Serverda {} kişi var.".format(
        sv.member_count), icon_url=sv.icon_url)

    await id.send(embed=embed)
    await members()


@client.event
async def on_member_remove(member):
    await members()


@client.command()
async def botping(ctx):
    await ctx.send(f"{round(client.latency * 1000)} ms")


@client.command(name="kisisayisi", aliases=["kişisayısı"])
async def _kisisayisi(ctx):
    id = client.get_guild(757259257421889617)
    await ctx.send(f"Serverda şuan {id.member_count} kişi bulunmakta.")


@client.command(aliases=["işletimsistemi"])
async def isletimsistemi(ctx):
    await ctx.send("Botun çalıştırıldığı işletim sistemi: " + isletim_sistemi)


@client.command()
async def oyun(ctx, *args):
    if "zar" in args:
        if "komik" in args:
            await ctx.send("Zar attım, 31 geldi :rofl:")
        else:
            await ctx.send(f"Zar attım, {Game.zar_at()} geldi")
    else:
        await ctx.send("Oyunlar: zar")


@client.command()
async def avatar(ctx, *member: discord.Member):
    if not member:
        await ctx.send(ctx.author.avatar_url)
    else:
        for user in member:
            await ctx.send(user.avatar_url)


@client.command()
async def chad(ctx, user: discord.Member = None, ):
    os.chdir("./images")
    my_image = Image.open("chad.jpg")
    if not user:
        asset = ctx.author.avatar_url_as(size=512)
    else:
        asset = user.avatar_url_as(size=512)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((360, 360))
    my_image.paste(pfp, (165, 95))

    my_image.save("profile.png")

    await ctx.send(file=discord.File("profile.png"))


client.run(token)
