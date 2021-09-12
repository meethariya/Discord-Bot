import discord
from discord.ext import commands

class CogHandler(commands.Cog):
	def __init__(self, client):
		self.client = client

	# @commands.Cog.listener()
	# async def on_ready(self):
	# 	print("Handler Cog Ready")

	@commands.command(brief = "Loads specified cog")
	@commands.has_permissions(manage_webhooks = True, manage_guild = True)
	async def load(self, ctx, extension):
		# Loads specified cog
		self.client.load_extension(f"cogs.{extension}")
		await ctx.reply(f"{extension} loaded successfully")

	@commands.command(brief = "Unloads specified cog")
	@commands.has_permissions(manage_webhooks = True, manage_guild = True)
	async def unload(self, ctx, extension):
		# Unloads specified cog
		self.client.unload_extension(f"cogs.{extension}")
		await ctx.reply(f"{extension} unloaded successfully")
	
	@commands.command(brief = "Reloads specified cog")
	@commands.has_permissions(manage_webhooks = True, manage_guild = True)
	async def reload(self, ctx, extension):
		# Reloads specified cog
		self.client.unload_extension(f"cogs.{extension}")
		self.client.load_extension(f"cogs.{extension}")
		await ctx.reply(f"{extension} reloaded successfully")


def setup(client):
	# initializes cog
	client.add_cog(CogHandler(client))