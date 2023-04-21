import requests
import sys
import os

import openai
import discord
from dotenv import load_dotenv
from app.chatgpt_ai.openai import chatgpt_response, chatgpt_summarize
from llama_index import GPTListIndex, DiscordReader

load_dotenv()
openai.api_key = os.getenv('OPEN_AI_KEY')
openai.api_base =  os.getenv('OPEN_AI_ENDPOINT')
openai.api_type = 'azure'
openai.api_version = '2022-12-01'

discord_token = os.getenv('DISCORD_TOKEN')

class MyClient(discord.Client):
	async def on_ready(self):
		print("successfully logged in as: ", self.user)
	async def on_message(self, message):
		channel_message = message.channel
		print(message.content)
		if message.author == self.user:
			return
		command, user_message=None, None

		for text in ['/ai', '/gptsummaryc']:
			if message.content.startswith(text):
				command=message.content.split(' ')[0]
				user_message=message.content.replace(text, '').lstrip()
				print(command, user_message)
		if command == '/ai':
			bot_response = chatgpt_response(prompty=user_message)
			await channel_message.send(f"Answer: {bot_response}")

		if command == '/gptsummaryc':
			#based on number they input read in that many past messages?
			
			src_channel_name=user_message.split(' ')[0]
			num_messages = user_message.split(' ')[1]
			src_channel = discord.utils.get(client.get_all_channels(), name=src_channel_name)

			target_channel = client.get_channel(src_channel)
			messages = [message async for message in src_channel.history(limit=int(num_messages))]
			text_length = 0
			for message in messages:
				text_length += len(message.content)
			if text_length > 4000:
				to_summarize = ""
				responses = []
				for message in messages:
					if not len(to_summarize) > 4000:
						to_summarize += message.content
					else:
						to_summarize = "summarize this segment of a long body of text" + to_summarize
						response = chatgpt_summarize(to_summarize)
						responses.append(response)
						to_summarize = message.content
				bot_response = ''.join(responses)
				await channel_message.send(f"{bot_response}")
			else:
				#errorhandling here
				messages = [message async for message in src_channel.history(limit=int(num_messages))]
				text_corpus = ""
				for message in messages:
					print(f"{message.author}: {message.content}")
					text_corpus += f"{message.author}: {message.content}"
				to_summarize = "summarize this:" + text_corpus 
				bot_response = chatgpt_summarize(to_summarize)
				await channel_message.send(f"Here's a summary: {bot_response}")

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

client= MyClient(intents=intents)


# TOKEN = os.getenv('DISCORD_TOKEN')
# CHANNEL = os.getenv('DISCORD_CHANNEL')
# client = discord.Client()
# print(discord.__version__)
# @client.event
# async def on_ready():
	
# 	print('We have logged in as {0.user}'.format(client))

# 	await client.wait_until_ready()
# 	channel = client.get_channel(int(CHANNEL))
# 	#if date in pickle of dates read then don't post it in discord


# client.run(TOKEN)


