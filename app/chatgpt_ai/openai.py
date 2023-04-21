from dotenv import load_dotenv
import openai
import os

load_dotenv()

openai.api_key = os.getenv('OPEN_AI_KEY')

def chatgpt_response(prompty):
	response = openai.Completion.create(
	      engine="text-davinci-003",
	      prompt=prompty,
	      temperature=1,
	      max_tokens=100,
	      top_p=1,
	      frequency_penalty=0.51,
	      presence_penalty=0.5,
	      #stream = False,
	      #echo = True
	    )
	response_dict = response.get("choices")
	if response_dict and len(response_dict) > 0:
		prompt_response = response_dict[0]["text"]
	return prompt_response

def chatgpt_summarize(prompty):
	response = openai.Completion.create(
	      engine="text-davinci-003",
	      prompt=prompty,
	      temperature=1,
	      max_tokens=500,
	      top_p=1,
	      frequency_penalty=0.51,
	      presence_penalty=0.5,
	      #stream = False,
	      #echo = True
	    )
	response_dict = response.get("choices")
	if response_dict and len(response_dict) > 0:
		prompt_response = response_dict[0]["text"]
	return prompt_response