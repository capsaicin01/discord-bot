import discord
import asyncio
from discord.ext import commands


class AdminKomutlari(commands.Cog):

    def __init__(self, client):
        self.client = client

    # events
    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot aktif!")

    # commands
    @commands.command(aliases=["mute"])
    @commands.has_permissions(manage_roles=True)
    async def sustur(self, ctx, member: discord.Member):
        for role in ctx.guild.roles:
            if role.name == "Muted":
                await member.add_roles(role)
                break
        await ctx.send(f"{member} sus knk")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        for role in member.roles:
            if role.name == "Mahkum":
                await member.remove_roles(role)
                await ctx.send(f"{member} kullanıcısının susturması kaldırıldı.")

    @commands.command(aliases=[], help="İstediğiniz sayıda mesajı siler (Default: 5)")
    @commands.has_permissions(administrator=True)
    async def temizle(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount + 1)
        await asyncio.sleep(1)
        await ctx.send(f"{amount} tane mesaj başarıyla silindi")

    @commands.command(help="Belirttiğiniz kişiyi sunucudan atar.")
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} savuşturuldu :shield:\nSebep: {reason}")

    @commands.command(help="Belirttiğiniz kişiyi sunucudan yasaklar")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f"{member.mention} banlandı :shield:\nSebep: {reason}")

    @commands.command(help="Belirttiğiniz kişinin yasaklamasını kaldırır. Kullanım: username#discriminator")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"{member} kullanıcısının banı kaldırıldı.")


def setup(client):
    client.add_cog(AdminKomutlari(client))