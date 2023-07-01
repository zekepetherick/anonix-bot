import discord
from datetime import datetime
from discord.ext import commands


class Information(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Test command
    @commands.hybrid_command(name='test', description='Just a basic test command to see if the commands are working.')
    async def test(self, ctx):
        await ctx.send("Everything is working fine!")

    # Latency command
    @commands.hybrid_command(name='ping', description='Sends the bots letency/response time in ms.')
    async def ping(self, ctx):
        await ctx.send(f"Pong {round(self.client.latency * 1000)}ms")

    @commands.hybrid_command()
    async def info(self, ctx, *, member: discord.Member):
        try:
            embed = discord.Embed(title="Member Information",
                                  color=discord.Color.blue())

            # Member Details
            embed.add_field(name="Display Name",
                            value=member.display_name, inline=False)
            embed.add_field(name="User ID", value=member.id, inline=False)
            embed.add_field(name="Joined Discord", value=member.created_at.strftime(
                "%d/%m/%Y, %I:%M %p UTC"), inline=False)
            embed.add_field(name="Joined Server", value=member.joined_at.strftime(
                "%d/%m/%Y, %I:%M %p UTC"), inline=False)

            # Roles
            # Exclude @everyone role
            role_names = [role.name for role in member.roles[1:]]
            roles_text = ", ".join(role_names) if role_names else "No roles"
            embed.add_field(name="Roles", value=roles_text, inline=False)

            await ctx.send(embed=embed)
        except Exception as e:
            print(e)

    @commands.hybrid_command()
    async def serverinfo(self, ctx):
        try:
            server = ctx.guild

            # Server Details
            server_name = server.name
            server_id = server.id
            server_owner = server.owner.display_name
            server_created_at = server.created_at.strftime("%Y-%m-%d %H:%M:%S UTC")

            # Member Count
            member_count = server.member_count
            member_count_online = sum(member.status != discord.Status.offline for member in server.members)

            # Channel Count
            text_channels = len(server.text_channels)
            voice_channels = len(server.voice_channels)
            category_channels = len(server.categories)
            total_channels = text_channels + voice_channels

            # Server Verification Level
            verification_level = server.verification_level.name.capitalize()

            # Server Boost Level
            boost_level = server.premium_tier
            boost_count = server.premium_subscription_count

            # Server Emojis
            emojis = [str(emoji) for emoji in server.emojis]

            # Create Embed
            embed = discord.Embed(title="Server Information", color=0x000000)
            embed.add_field(name="Server Name", value=server_name, inline=True)
            embed.add_field(name="Server ID", value=server_id, inline=True)
            embed.add_field(name="Owner", value=server_owner, inline=True)
            embed.add_field(name="Emojis", value="\n".join(emojis) if emojis else "No emojis", inline=True)
            embed.add_field(name="Members", value=f"Total: {member_count}\nOnline: {member_count_online}", inline=True)
            embed.add_field(name="Boost Level", value=f"Tier: {boost_level}\nCount: {boost_count}", inline=True)
            embed.add_field(name="Channels", value=f"Total: {total_channels}\nText: {text_channels}\nVoice: {voice_channels}\nCategories: {category_channels}", inline=True)
            embed.add_field(name="Verification Level", value=verification_level, inline=True)
            embed.add_field(name="Created At", value=server_created_at, inline=True)

            await ctx.send(embed=embed)
        except Exception as e:
            print(e)



async def setup(client):
    await client.add_cog(Information(client))
