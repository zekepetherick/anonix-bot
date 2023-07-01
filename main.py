import discord
import asyncio
import re
from discord.ext import commands
from discord.ext.commands import *
import os

client = commands.Bot(command_prefix="!", help_command=commands.MinimalHelpCommand(), intents=discord.Intents.all())
client.remove_command("help")


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Anonix.xyz"))
    print('Logged in as {0.user}'.format(client))
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have the required permissions to use this command!")
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Uh-oh, That command does not exist!")

@client.event
async def on_message(message):
    await client.process_commands(message)


@client.command(name='load', description='Loads the given cog')
@has_permissions(administrator=True)
async def load(ctx, extension):
    await client.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension}.")
    print(f"Loaded {extension}.py")


@client.command(name='unload', description='Unloads the given cog')
@has_permissions(administrator=True)
async def unload(ctx, extension):
    await client.unload_extension(f"cogs.{extension}")
    await ctx.send(f"Unloaded {extension}.")
    print(f"Unloaded {extension}.py")


@client.command(name='reload', description='Re-loads the given cog')
@has_permissions(administrator=True)
async def reload(ctx, extension):
    await client.reload_extension(f"cogs.{extension}")
    await ctx.send(f"Re-loaded {extension}.")
    print(f"Re-loaded {extension}.py")


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with client:
        await load_extensions()
        await client.start("TOKEN")

asyncio.run(main())
