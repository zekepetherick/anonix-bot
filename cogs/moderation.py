import discord
import asyncio
import re
import json
import os
from discord.ext import commands

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}


class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for v, k in matches:
            try:
                time += time_dict[k]*float(v)
            except KeyError:
                raise commands.BadArgument(
                    "{} is an invalid time-key! h/m/s/d are valid!".format(k))
            except ValueError:
                raise commands.BadArgument("{} is not a number!".format(v))
        return time


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command(name='purge', description='Purges the given amount of messages from the channel.')
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"Successfully cleared {amount} messages!")

    @commands.hybrid_command(name='kick', description='Kicks the mentioned user from the guild.')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str):
        await discord.Member.kick(member)
        await ctx.send(f"{member} has been kicked.")

    @commands.hybrid_command(name='mute', description='Mutes the mentioned user for the given amount of time.')
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, time: TimeConverter = None, reason: str):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        memRole = discord.utils.get(ctx.guild.roles, name='Member')
        await member.remove_roles(memRole)
        await member.add_roles(role)
        await ctx.send(("Muted {} for {}s" if time else "Muted {}").format(member, time))
        if time:
            await asyncio.sleep(time)
            await member.add_roles(memRole)
            await member.remove_roles(role)

    @commands.hybrid_command(name='unmute', description='Unmutes the mentioned user.')
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        memRole = discord.utils.get(ctx.guild.roles, name='Member')
        await member.remove_roles(role)
        await member.add_roles(memRole)
        await ctx.send(f'Unmuted {member}.')

    @commands.hybrid_command(name="warn", description="Warns to mentioned user.")
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason: str):
        # Load the existing warns from the file
        with open('/Users/zekepetherick/Desktop/Home/Anonix/files/warns.json', 'r') as f:
            warns = json.load(f)

        # Add the new warn to the warns dictionary
        if str(member.id) not in warns:
            warns[str(member.id)] = []

        if len(warns[str(member.id)]) == 0:
            warns[str(member.id)].append("")
        warns[str(member.id)].append(reason)

        # Save the updated warns back to the file
        with open('/Users/zekepetherick/Desktop/Home/Anonix/files/warns.json', 'w') as f:
            json.dump(warns, f, indent=4)

        # Get the current warning count for the member
        warning_count = len(warns[str(member.id)]) - 1

        # Example: Sending a warning message with the warning count
        await ctx.send(f"{member.mention} has been warned for {reason}. This is warning number {warning_count}.")


    @commands.hybrid_command(name="listwarns", description="Shows the list of warnings the the mentioned user if they have any.")
    @commands.has_permissions(kick_members=True)
    async def listwarns(self, ctx, member: discord.Member):
        try:
            file_path = os.path.abspath('../Anonix/files/warns.json')

            with open(file_path, 'r') as f:
                warns = json.load(f)

            member_warns = warns.get(str(member.id))

            if member_warns:
                warn_list = "\n".join([f"• {warn}" for warn in member_warns[1:]])
                embed = discord.Embed(title=f"Warns for {member.display_name}", description=warn_list, color=discord.Color.orange())
                await ctx.send(embed=embed)
            else:
                await ctx.send(f"{member.mention} has no warns.")
        except Exception as e:
            print(e)
    

    @commands.hybrid_command(name="delwarn", description="Deletes the spcified warning from the mentioned user.")
    @commands.has_permissions(kick_members=True)
    async def deletewarn(self, ctx, member: discord.Member, warn: int):
        with open('/Users/zekepetherick/Desktop/Home/Anonix/files/warns.json', 'r') as f:
            warns = json.load(f)

        member_warns = warns.get(str(member.id))

        if member_warns and 0 <= warn < len(member_warns):
            removed_warn = member_warns.pop(warn)
            with open('/Users/zekepetherick/Desktop/Home/Anonix/files/warns.json', 'w') as f:
                json.dump(warns, f, indent=4)
            await ctx.send(f"Successfully removed warn #{warn} for {member.mention}: {removed_warn}")
        else:
            await ctx.send(f"Invalid warn index for {member.mention} or they have no warns.")


async def setup(client):
    await client.add_cog(Moderation(client))
