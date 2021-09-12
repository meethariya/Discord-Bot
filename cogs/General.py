import discord
from discord.ext import commands
import random
import asyncio
import requests
from requests.utils import unquote
import os
import json

class General(commands.Cog):
	def __init__(self, client):
		self.client = client

	
	@commands.command(aliases = ["hi","Hi","Hello"], brief = "Greets User")
	async def hello(self, atx):
		# Greets user by a pleasent hello
		options = ["Greetings", "Hi", "Howdy", "Welcome", "bonjour", "Hey", "How are you", "Sup"]
		await atx.send(f"{random.choice(options)} "+atx.author.mention + " 😊.")

	@commands.command(brief = "R2D2's ping")
	async def ping(self, atx):
		# returns ping of bot
		await atx.send(f'{self.client.user.name} has {round(self.client.latency * 1000)}ms')

	@commands.command(aliases = ["Ask","8ball"], brief = "Ask a yes/no question for expert's advice")
	async def ask(self, atx, *, msg):
		# gives random yes/no/maybe opinion
		# * will make all text as one text for parameter msg
		decision_responses = ["It is certain.",
		"It is decidedly so.",
		"Without a doubt.",
		"Yes - definitely.",
		"You may rely on it.",
		"As I see it, yes.",
		"Most likely.",
		"Outlook good.",
		"Yes.",
		"Signs point to yes.",
		"Reply hazy, try again.",
		"Ask again later.",
		"Better not tell you now.",
		"Cannot predict now.",
		"Concentrate and ask again.",
		"Don't count on it.",
		"My reply is no.",
		"My sources say no.",
		"Outlook not so good.",
		"Very doubtful."]
		# op = message.author.mention+'\n _'+random.choice(decision_responses)+'_'
		op = '_'+random.choice(decision_responses)+'_'
		await atx.reply(op)

	@commands.command(aliases = ["Quote"], brief = "Gives a random positive quote")
	async def quote(self, atx):
		# message a random quote
		await atx.reply(self.get_quote())

	@commands.command(aliases = ["Weather"], brief = "Enter place name to get its weather")
	async def weather(self, atx, *, place):
		# gives weather for the given location
		response = self.get_weather(place)
		if isinstance(response,str):
			await atx.reply(response)
		else:
			await atx.reply(embed=response[0], file=response[1])


	@commands.command(aliased = ["quiz"])
	async def trivia(self, ctx):
		'''
		Whats more brainstorming then a fun quiz
		'''
		# building trivia
		triviaembed, options, correct_option = self.get_trivia(ctx.author)
		# sending message
		quiz = await ctx.send(embed=triviaembed)
		# adding option reactions on emoji
		emojis = ["1️⃣","2️⃣","3️⃣","4️⃣"]
		for emoji in emojis:
			await quiz.add_reaction(emoji)
		
		def check_answer(reaction,user):
			# simple function to check if the person who has sent the ans is the author of the person who requested the trivia
			return ctx.author == user

		while True:
			# waits for 30sec for user to add reaction
			try:
				# triggers when user reacts to quiz
				reaction, user = await self.client.wait_for("reaction_add", timeout=30, check=check_answer)
				# if reaction is one of the ans, then verify ans
				if reaction.emoji in emojis:
					# if selected option is correct
					if options[emojis.index(reaction.emoji)]==correct_option:
						await ctx.send("Congratulations! Its correct 🥳")
						break
					else:
						# if selected option is wrong
						await ctx.send("Better Luck next time _noob_ 😏")
						await ctx.send(f"Correct answer is {unquote(correct_option)}")
						break
			
			except asyncio.TimeoutError:
				# if time exceeds than timeout seconds
				await ctx.send("Time's up you. Even my pet turtle's faster then you 🤦🏻‍♂️")
				break

	@commands.command(brief = "Gets list of all users of a role")
	async def getuser(self, ctx,role:discord.Role):
		# returns all members of a specific role
		response = ">>> "
		for i, j in enumerate(role.members):
			response += str(i+1)+ j.mention+"\n"
		await ctx.send(response)

	@commands.command(brief = "Returns a space image of the day with information")
	async def space(self, ctx):
		# gives info abt space image
		embed, file = self.get_space()
		await ctx.send(embed=embed, file=file)

	@commands.command(brief = "Bored? Try this! Give number of bored people. Default 1")
	async def bored(self, ctx, n=1):
		# gives task to perform 
		await ctx.reply(embed=self.get_bored(n))

	def get_bored(self, n):
		'''
		Return embed message as some task to perform
		'''
		participants = n
		raw = requests.get(f"http://www.boredapi.com/api/activity?participants={participants}")
		data = json.loads(raw.text)

		#gathering data
		try:
			activity = data['activity']
			activity_type = data['type']
			link = data['link']
			access = int(data['accessibility']) * 100
		except KeyError:
			activity = "Reduce participants"
			activity_type = ""
			link = ""
			access = ""


		# building description
		description = ""
		description += f"`Type:` {activity_type}\n" if activity_type else ""
		description += f"`Link:` {link}\n" if link else ""
		description += f"`Accessibility required:` {access}%\n" if access else ""
		description += f"`Participants required:` {participants}"

		# building embed messsage
		boredembed = discord.Embed(title = activity, description = description, color = discord.Color.random())
		boredembed.set_author(name = "Try This!")
		return boredembed

	def get_space(self):
		'''
		Returns image of the day via NASA which has its details, image url and HD image url
		'''
		# fetching data
		url = f"https://api.nasa.gov/planetary/apod?api_key={os.getenv('nasa_api')}"
		raw = requests.get(url)
		data = json.loads(raw.text)
		
		# gathering data
		explaination = data['explanation']
		image_url = data['url']
		title = data['title']

		# downloading image
		image = requests.get(image_url)
		file = open("space_image.jpg","wb")
		file.write(image.content)
		file.close()

		# preparing embed message
		spaceembed = discord.Embed(title = title, description = explaination, color = discord.Color.dark_blue())
		spaceembed.set_author(name = "NASA's image of the day")
		file = discord.File("space_image.jpg", "space_image.jpg")
		spaceembed.set_image(url = "attachment://space_image.jpg")
		
		#returning embed message and file
		return spaceembed, file

	def get_weather(self, place):
		''' 
		Takes name of a place as string and sends request to weatherapi.com with that place. The API returns JSON object with current weather of that place and returns organised data as string
		'''

		try:
			# requesting data
			raw = requests.get(f"http://api.weatherapi.com/v1/current.json?key={os.getenv('weather_api')}&q={place}&aqi=no")
			# formatting data
			data = json.loads(raw.text)

			# preparing address
			address = data['location']['name']+', '+data['location']['region']+', '+data['location']['country']
			# last updated status
			last_updated = data['current']['last_updated']
			# feel like temperature
			feels_like_temperature = str(data['current']['feelslike_c'])+' C'
			# actual temperature
			temperature = str(data['current']['temp_c'])+' C'
			# condition of place
			condition = data['current']['condition']['text']
			# wind speed and wind direction of place
			wind_speed, wind_dir = str(data['current']['wind_kph'])+' kph', data['current']['wind_dir']
			# humidity
			humidity = str(data['current']['humidity'])

			# preparing final message by concatinating above data
			response = ">>> `Last Updated:` " + last_updated + "\n" + "`Feels Like:` " + feels_like_temperature + "\n" + "`Temperature:` " + temperature + "\n" + "`Condition:` " + condition + "\n" + "`Wind Speed:` " + wind_speed + "\t" + "`Direction:` " + wind_dir + "\n" + "`Humidity:` " + humidity
			weatherembed = discord.Embed(title = address, description = response, color = discord.Color.green())
			weatherembed.set_author(name="Weather")
			# downloading image and embeding it to message
			image = requests.get("https:"+data['current']['condition']['icon'])
			file = open("weather_image.png", "wb")
			file.write(image.content)
			file.close()
			# loading image as discord image
			file = discord.File("weather_image.png","weather_image.png")
			# attaching image to embed
			weatherembed.set_image(url = "attachment://weather_image.png")
			# returning image file and embed
			response = (weatherembed, file)
		except KeyError:
			# location may not be found, so requesting for valid location
			response = "Enter Valid Location"
		# returning message
		return response
	
	def get_trivia(self, author):
		# return a trivia embed question, list of options and the correct option
		raw = requests.get('https://opentdb.com/api.php?amount=1&difficulty=easy&type=multiple&encode=url3986')
		data = json.loads(raw.text)
		data = data['results'][0]
		# extracting question and decoding it
		question = unquote(data['question'])
		# joining all options and sorting them to mix correct answer
		options = sorted([data['correct_answer']]+data['incorrect_answers'])
		options_text = ''
		# iterating thro all options
		for i,j in enumerate(options):
			options_text += f"`{str(i+1)}`   {unquote(j)}\n"
		# building message
		options_text += f"{author.mention} You have `30 seconds` to answers the trivia.\nSelect the reaction that you want to select as answer.\nGood Luck!"
		# creating embed message
		triviaembed=discord.Embed(title=question, description=options_text, color=discord.Colour.random())
		triviaembed.set_author(name='Trivia')
		# returning embed message, options and correct option
		return (triviaembed, options, data['correct_answer'])
	
	def get_quote(self):
		''' 
		Gets a random quote along with author name from zenquotes.io
		Return a message as string
		'''

		# requesting quote
		raw = requests.get('https://zenquotes.io/api/random')
		# fetching json data
		data = json.loads(raw.text)
		# creating useful string
		quote, author = data[0]['q'], data[0]['a']
		op = quote+'\n\t\t-'+author
		# returning readable message
		return op


def setup(client):
	client.add_cog(General(client))