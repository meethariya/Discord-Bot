import discord
from discord.ext import commands
import random
import asyncio
import requests
import json

class Funny(commands.Cog):
	def __init__(self, client):
		self.client = client
		# a list of roasting lines to say
		self.roast_lines = [
			"If I throw a stick, will you leave?"

			,"You’re a gray sprinkle on a rainbow cupcake."

			,"If your brain was dynamite, there wouldn’t be enough to blow your hat off."


			,"You are more disappointing than an unsalted pretzel."

			,"Light travels faster than sound, which is why you seemed bright until you spoke."

			,"We were happily married for one month, but unfortunately, we’ve been married for 10 years."

			,"Your kid is so annoying he makes his Happy Meal cry."

			,"You have so many gaps in your teeth it looks like your tongue is in jail."

			,"Your secrets are always safe with me. I never even listen when you tell me them."

			,"I’ll never forget the first time we met. But I’ll keep trying."

			,"I forgot the world revolves around you. My apologies! How silly of me."

			,"I only take you everywhere I go just so I don’t have to kiss you goodbye."

			,"Hold still. I’m trying to imagine you with a personality."

			,"Our kid must have gotten his brain from you! I still have mine."

			,"Your face makes onions cry."


			,"The only way my husband would ever get hurt during an activity is if the TV exploded."

			,"You look so pretty. Not at all gross today."

			,"It’s impossible to underestimate you."

			,"Her teeth were so bad she could eat an apple through a fence."

			,"I’m not insulting you; I’m describing you."

			,"I’m not a nerd; I’m just smarter than you."

			,"Don’t be ashamed of who you are. That’s your parents’ job."

			,"Your face is just fine, but we’ll have to put a bag over that personality."

			,"You bring everyone so much joy… when you leave the room."

			,"I thought of you today. It reminded me to take out the trash."


			,"Don’t worry about me. Worry about your eyebrows."

			,"You are the human version of period cramps."

			,"If you’re going to be two-faced, at least make one of them pretty."

			,"You are like a cloud. When you disappear, it’s a beautiful day."

			,"I’d rather treat my baby’s diaper rash than have lunch with you."

			,"Don’t worry — the first 40 years of childhood are always the hardest."

			,"I may love to shop, but I will never buy your bull."

			,"I love what you’ve done with your hair. How do you get it to come out of your nostrils like that?"

			,"OH MY GOD! IT SPEAKS!"

			,"“Check your lipstick before you come for me.” — Naomi Smalls, RuPaul’s Drag Race"

			,"“It looks like she went into Claire’s Boutique, fell on a sale rack, and said, ‘I’ll take it!’” — Bianca Del Rio, RuPaul’s Drag Race"


			,"“Is your ass jealous of the amount of shit that comes out of your mouth?” — Jamie McGuire, Beautiful Oblivion"

			,"“Go back to Party City, where you belong!” — Phi Phi O’Hara, RuPaul’s Drag Race"

			,"“Where’d you get your outfits, girl, American Apparently Not?” — Trixie Mattel, RuPaul’s Drag Race"

			,"“Impersonating Beyoncé is not your destiny, child.” — RuPaul, RuPaul’s Drag Race"

			,"“Don’t get bitter, just get better.” — Alyssa Edwards, RuPaul’s Drag Race"

			,"Child, I’ve forgotten more than you ever knew."

			,"You just might be why the middle finger was invented in the first place."

			,"I know you are, but what am I?"

			,"I see no evil, and I definitely don’t hear your evil."


			,"You have miles to go before you reach mediocre."

			,"When you look in the mirror, say hi to the clown you see in there for me, would ya?"

			,"Bye, hope to see you never."

			,"Complete this sentence for me: “I never want to see you ____!”"

			,"Remember that time you were saying that thing I didn’t care about? Yeah… that is now."

			,"I was today years old when I realized I didn’t like you."
			,"N’Sync said it best: “BYE, BYE, BYE.”"


			,"Wish I had a flip phone so I could slam it shut on this conversation."

			,"How many licks till I get to the interesting part of this conversation?"

			,"Wow, your maker really didn’t waste time giving you a personality, huh?"

			,"You’re cute. Like my dog. He also always chases his tail for entertainment."
			,"Someday you’ll go far… and I really hope you stay there."
			,"Oh, I’m sorry. Did the middle of my sentence interrupt the beginning of yours?"
			,"You bring everyone so much joy! You know, when you leave the room. But, still."
			,"Oops, my bad. I could’ve sworn I was dealing with an adult."
			,"Did I invite you to the barbecue? Then why are you all up in my grill?"
			,"I’m an acquired taste. If you don’t like me, acquire some taste."
			,"Somewhere out there is a tree tirelessly producing oxygen for you. You owe it an apology."
			,"Yeah? Well, you smell like hot dog water."
			,"*Thumbs down*"
			,"That sounds like a you problem."
			,"Beauty is only skin deep, but ugly goes clean to the bone."
			,"Oh, you don’t like being treated the way you treat me? That must suck."
			,"“I’ve been called worse things by better men.”"
			,"Well, the jerk store called. They’re running out of you."
			,"“What, like it’s hard?” — Elle Woods, Legally Blonde"
			,"Sorry, not sorry."
			,"I’m busy right now; can I ignore you another time?"
			,"If you have a problem with me, write the problem on a piece of paper, fold it, and shove it up your ass."
			,"You have an entire life to be an idiot. Why not take today off?"
			,"No matter how much a snake sheds its skin, it’s still a snake."
			,"Some people are like slinkies — not really good for much, but they bring a smile to your face when pushed down the stairs."
			,"You’re the reason this country has to put directions on shampoo."
			,"Of course I’m talking like an idiot… how else could you understand me?"
			,"Are you almost done with all of this drama? Because I need an intermission."
			,"I’d give you a nasty look, but you’ve already got one."
			,"If I wanted to hear from an asshole, I’d fart."
			,"Your birth certificate is an apology letter from the condom factory."
			,"Your family tree must be a cactus because everybody on it is a prick."

			,"Wow, I bet you even fart glitter!"

			,"I guess if you actually ever spoke your mind, you’d really be speechless."

			,"Since you know it all, you should know when to shut up."
			,"Life is full of disappointments, and I just added you to the list."
			,"I treasure the time I don’t spend with you."
			,"I was going to make a joke about your life, but I see life beat me to the punch."
			,"The last time I saw something like you… I flushed."
			,"The only work-life balance I want is being away from you."
			,"When you start talking, I stop listening."
			,"Feed your own ego. I’m busy."
			,"You look like something that came out of a slow cooker."
			]
		

	@commands.command(brief = "Roasts the tagged person")
	async def roast(self, ctx, member:discord.Member):
		# pings member passed and selects a random roast line
		await ctx.send(f"{member.mention}\n{random.choice(self.roast_lines)}")

	@commands.command(brief = "A random joke to lighten up the room😛")
	async def joke(self, ctx):
		# gets a joke
		joke = self.get_joke()
		# just send joke if its of one line
		if joke["type"] == "single": 
			await ctx.send(joke["joke"])
		else:
			# else send the joke and reply to it after 5 seconds
			abc = await ctx.send(joke["setup"])
			await asyncio.sleep(5)
			await abc.reply(joke["delivery"])

	def get_joke(self):
		raw = requests.get("https://v2.jokeapi.dev/joke/Any")
		data = json.loads(raw.text)
		return data

def setup(client):
	# initialize cog
	client.add_cog(Funny(client))