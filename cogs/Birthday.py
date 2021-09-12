import discord
from discord.ext import commands
import json
from replit import db
from datetime import datetime
from dateutil.relativedelta import relativedelta

class Birthday(commands.Cog):
	def __init__(self,client):
		self.client = client

	# events
	# @commands.Cog.listener()
	# async def on_ready(self):
	# 	print("Birthday Cog Ready")

	@commands.command(brief="set your birthday/ view birthday/ del your birthday")
	async def birthday(self,ctx, *, msg=None):
		if msg.startswith('set'):
			await ctx.invoke(self.client.get_command('birthday_set'), msg=msg[3:])
		elif msg.startswith('del'):
			await ctx.invoke(self.client.get_command('birthday_del'))
		elif msg.startswith('view'):
			await ctx.invoke(self.client.get_command('birthday_view'), msg=msg[4:])

	@commands.command(aliases = ["birthday set"], brief = "Sets birthday in format dd-mm-yyyy")
	async def birthday_set(self, ctx, *, msg):
		'''
		Sets birthday of the member who sends the birthday. 
		Birthday should be in dd-mm-yyyy format only.
		'''

		# default response
		response = "Enter date as dd-mm-yyyy"
		# fetching date
		b_day = msg[1:]
		# fetching all records
		records = json.loads(db['birthdays'])
		try:
			# setting member id as key and birthday as value in type str(Datetime(str()))
			records[ctx.author.id] = str(datetime.strptime(b_day,"%d-%m-%Y"))
			# loading data back to database
			db['birthdays'] = json.dumps(records)
			# modifing response
			response = f"<@{ctx.author.id}> your birthday is set to _{b_day}_"
		except Exception as e:
			# if date is not formatted correctly, shows message
			print(e)
		await ctx.send(response)

	@commands.command(brief = "Deletes birthday of user")
	async def birthday_del(self, ctx):
		'''
		Deletes birthday of the member sending the message.
		'''

		# loading data
		data = json.loads(db['birthdays'])
		# storing member id
		mem_id = ctx.author.id
		# if member in data
		if str(mem_id) in data:
			# deleting member birthday
			del data[str(mem_id)]
			# dumping data back to database
			db['birthdays'] = json.dumps(data)
			await ctx.send(f"<@{mem_id}>'s birthday deleted successfully!")
			return
		await ctx.send(f"<@{mem_id}> You have not set your birthday.")

	@commands.command(brief="Displays birthdays in n months. Default user's birthday")
	async def birthday_view(self, ctx, *, msg=None):
		'''
		Given message and the atx, it will show all upcoming birthdays in n months.
		If n is not given it will show personal birthday
		'''
		if not msg:
			# show personal birthday
			data = json.loads(db['birthdays'])
			# if birthday is not set, request them to set
			if str(ctx.author.id) not in data.keys():
				await ctx.reply("Set your birthday before viewing 😐")
				return
			b_day = datetime.strftime(datetime.strptime(data[str(ctx.author.id)],"%Y-%m-%d %H:%M:%S"),"%d %B")
			await ctx.reply(f"<@{ctx.author.id}> Dont worry everyone will wish you on _{b_day}_ 😉.")
			return
		try:
			# if entered month is valid or not
			months = msg
			if int(months) > 12: return "Enter months in range 0-12"
		except ValueError:
			# if invalid month is given
			await ctx.reply("Enter valid number of months")
			return
		
		# retriving today's date
		today_date = datetime.today()
		# generating date after n months
		end_date = today_date + relativedelta(months=int(months))
		
		# retriving all birthdays
		all_birthdays = json.loads(db['birthdays'])
		
		# creating response
		response = f">>> All birthdays between `{datetime.strftime(today_date.date(),'%d-%m-%Y')}` and `{datetime.strftime(end_date.date(),'%d-%m-%Y')}`:\n"
		i = 1
		for j in all_birthdays.items():
			# temp is birthday with year of today date and temp2 is birthday with year of end date
			temp = datetime.strptime(j[1],"%Y-%m-%d %H:%M:%S").replace(year=today_date.year)
			temp2 = datetime.strptime(j[1],"%Y-%m-%d %H:%M:%S").replace(year=end_date.year)
		
			# if temp between current date and end date add it to response
			if (temp >= today_date and temp <= end_date) or (temp2 >= today_date and temp2 <= end_date):
				# formatting birthday
				b = datetime.strftime(datetime.strptime(j[1],"%Y-%m-%d %H:%M:%S"),"%d %B %Y")
				response += "`"+str(i)+"`" + f"   <@{int(j[0])}>    {b}"+"\n"
				i += 1
		# returning response	
		await ctx.reply(response)
	
def setup(client):
	# initializes cog
	client.add_cog(Birthday(client))