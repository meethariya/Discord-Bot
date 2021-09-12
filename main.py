import discord
from discord.ext import commands
import os
import random
from replit import db
from discord.utils import get
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True
# client = discord.Client(intents=intents)
client = commands.Bot(command_prefix='.', intents = intents)

sad_words = ['sad', 'depressed', 'unhappy', 'grief', 'hurt', 'distress', 'tearful', 'upset', 'sober']

@client.event
async def on_ready():
	# when bot comes online, gives a console message
	print(f"{client.user.name} online")
	await client.change_presence(status = discord.Status.online, activity = discord.Game("with emotions"))
	# await client.get_channel(884415311430955049).send(f"{client.user.name} online")

@client.event
async def on_member_join(member):
	# sends welcome message when new member joins and asasigns them member role by default
	role = get(member.guild.roles, name='Member')
	await member.add_roles(role)
	await client.get_channel(884492043483754507).send(f"Welcome, <@{member.id}>!!🤩")

@client.event
async def on_member_remove(member):
	# sends bbye message when a member leaves
	await client.get_channel(884492825373339668).send(f"Bbye, <@{member.id}>😞")

@client.event
async def on_command_error(ctx, error):
	# throws error as message on discord
	if isinstance(error, commands.CommandNotFound):
		await ctx.send("No such command found.\nEnter `.help` to get list of all commands.")
	elif isinstance(error,commands.MissingRequiredArgument):
		await ctx.send("Enter all values for a command. For detailed command explaination enter `.help command name`")
	elif isinstance(error, commands.MissingPermissions):
		await ctx.send("You do not have permission to perform this command")
	else:
		print(error)


@client.event
async def on_message(message):
	if message.author == client.user:
		# if message is sent by bot itself, it will return from function
		return
	msg = message.content

	# if any sad words are used in message a random encouragement statement will be sent as message
	if any(word in msg for word in sad_words):
		if len(db['encouragements'])>0:
			await message.reply(random.choice(db['encouragements']))
		else:
			# else it will reply whatever dude
			await message.reply("Whatever dude")

	# if "bored" or "boring" in msg: 
	# 	await client.get_context(message).invoke(client.get_command('bored'))
	
	if msg.startswith('.'):
		# removes . from start of the string
		msg = msg.split('.',1)[1]
			
	await client.process_commands(message)

# keeps bot alive all the time by sending requests to flask backend via uptimerobot.com
keep_alive()

# loading all cogs
for filename in os.listdir("./cogs"):
	if filename.endswith(".py"):
		client.load_extension(f"cogs.{filename[:-3]}")

# Initialize bot
client.run(os.getenv('TOKEN'))