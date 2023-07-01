import discord
import os
from discord.ext import commands


class Administrator(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command(name='ban', description='Bans the mentioned user from the guild.')
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str):
        await discord.Member.ban(member)
        await ctx.send(f"{member} has been banned for {reason}.")

    @commands.hybrid_command(name='softban', description='Softbans the mentioned user from the guild.')
    @commands.has_permissions(administrator=True)
    async def softban(self, ctx, member: discord.Member, *, reason: str):
        await discord.Member.ban(member)
        await discord.Member.unban(member)


async def setup(client):
    await client.add_cog(Administrator(client))
