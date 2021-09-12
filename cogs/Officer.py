import discord
from discord.ext import commands
from discord.utils import get
import asyncio

class Officer(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command(aliases = ["Clear"], brief = "Deletes n number of messages. Default 5msgs")
	@commands.has_permissions(manage_messages=True)
	async def clear(self, atx, count=5):
		# clears n number of messages from channel
		await atx.channel.purge(limit=int(count))

	@commands.command(brief = "Kicks a member")
	@commands.has_permissions(kick_members=True)
	async def kick(self, atx, member: discord.Member, *, reason = None):
		# kicks a member from server
		await atx.channel.purge(limit=1)
		await member.kick(reason=reason)
		await atx.send(f"{atx.author.mention} kicked {member.mention}\n`Reason`: {reason}")

	@commands.command(brief = "Bans a member")
	@commands.has_permissions(ban_members=True)
	async def ban(self, atx, member: discord.Member, *, reason = None):
		# bans a member from server
		await atx.channel.purge(limit=1)
		await member.ban(reason=reason)
		await atx.send(f"{atx.author.mention} banned {member.mention}\n`Reason`: {reason}")

	@commands.command()
	@commands.has_permissions(ban_members=True)
	async def unban(self, atx, member, *, reason=None):
		'''
		Unbans a member.
		'''
		# getting list of all banned accounts
		banned_accounts = await atx.guild.bans()
		# getting name and discriminator of the member who we want to unban
		member_name, member_discriminator = member.split('#')

		for acc in banned_accounts:
			# iterating over all banned users
			user = acc.user
			if (user.name, user.discriminator) == (member_name, member_discriminator):
				# if data matches, unban that user
				await atx.guild.unban(user)
				await atx.send(f"{atx.author.mention} unbanned {user.mention}\n`Banned reason:` {acc.reason} \n`Unbanning reason:` {reason}")
				return
		# if no account found with matching detail show message
		await atx.send("No such banned user")

	@commands.command()
	@commands.has_permissions(manage_roles=True)
	async def mute(self, ctx, member: discord.Member, time='1d', *, reason = None):
		'''
		Mutes a member for given time. Default time 1day.
		'''
		# retriving muted role
		mute_role = get(ctx.guild.roles, name = 'Muted')
		# if member is already muted, show error message
		if mute_role in member.roles:
			await ctx.reply(f"{member.mention} is already muted!")
			return
		else:
			# if member is admin, dont show cant mute message
			if member.guild_permissions.administrator:
				# creating embed message
				is_admin_embed = discord.Embed(title="Mute", description = f"You can not mute {member.mention} as he/she is Admin.", color = discord.Color.red())
				is_admin_embed.set_author(name = self.client.user.name)
				await ctx.send(embed=is_admin_embed)
			else:
				# converting time in seconds
				time_conversion = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800, "M": 2419200, "y": 29030400}
				mute_time = int(time[:-1]) * time_conversion[time[-1]]
				# adding muted role to member
				await member.add_roles(mute_role)
				# creating embed message
				mutedembed=discord.Embed(title="Mute", description=f"{member.mention} has been muted by {ctx.author.mention}. \n \nTime: {mute_time} seconds \nReason: {reason}", color=discord.Colour.red())
				mutedembed.set_author(name=self.client.user.name)
				await ctx.channel.send(embed=mutedembed)
				# sleeps for mentioned time
				await asyncio.sleep(mute_time)
				if mute_role in member.roles:
					await member.remove_roles(mute_role)
					await ctx.channel.send(f"{member.mention} has been unmuted!\n`Reason:` Mute time finished")

	@commands.command()
	@commands.has_permissions(manage_roles=True)
	async def unmute(self, ctx, member: discord.Member, *, reason=None):
		'''
		Unmutes a member
		'''
		mute_role = get(ctx.guild.roles, name = "Muted")
		if mute_role in member.roles:
			await member.remove_roles(mute_role)
			await ctx.channel.send(f"{member.mention} has been unmuted by {ctx.author.mention}!\n`Reason:` {reason}")
		else:
			await ctx.send("Member is already unmuted")



def setup(client):
	client.add_cog(Officer(client))