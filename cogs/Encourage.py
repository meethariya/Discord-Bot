import discord
from discord.ext import commands
from replit import db

class Encourage(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.command()
	async def encourage(self, ctx, *, msg):
		'''
		Responses to all encourage commands i.e. add, view and del.
		Adds Encouragement statement provided in msg
		Views all current Encouragement statements
		Deletes Encouragement statement provided in msg
		'''
		if msg.startswith('add'):
			# adds new encourage statement to database
			new = msg.split('add ',1)[1]
			await ctx.invoke(self.client.get_command('encourage_add'), new=new)
			

		elif msg.startswith('view'):
			# views all available encouragement statements
			await ctx.invoke(self.client.get_command('encourage_view'))
		
		elif msg.startswith('del'):
			# deletes statement from encouragements list
			statement = msg.split('del ',1)[1]
			await ctx.invoke(self.client.get_command('encourage_del'), msg=statement)
		
		else:
			await ctx.reply("Enter a valid command")
			

	@commands.command()
	async def encourage_add(self, ctx, *, new):
		''' 
		Adds new encouragement to list of encouragements.
		If no encouragements are present, it creates one
		'''

		# checks for encouregements in database
		if 'encouragements' in db.keys():
			# retrives all statements
			encouragements = db['encouragements']
			# adds new statement to existing
			encouragements.append(new)
			# updates to database
			db['encouragements'] = encouragements
		else:
			# creates new encouragements in database as list of statements
			db['encouragements'] = [new]
		await ctx.send(f"'{new}' added to list of encouragements")

	@commands.command()
	async def encourage_view(self,ctx):
		'''
		Views all encouraging statements
		'''
		op = list(db['encouragements'])
		await ctx.send(op)

	@commands.command()
	async def encourage_del(self,ctx , *, msg):
		'''
		Views all encouraging statements
		'''
		if msg in db['encouragements']:
			records = db['encouragements']
			records.remove(msg)
			db['encouragements'] = records
			await ctx.send(f"'{msg}' removed successfully!")
		else:
			await ctx.send(f"'{msg}' not found")

def setup(client):
	client.add_cog(Encourage(client))