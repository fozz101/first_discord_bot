import discord
import os
import requests
import json
import random
from replit import db
from discord.ext import commands

from keep_alive import keep_alive


client = discord.Client()
sad_words = ["sad","depressed","kill","unhappy","angry"]

starter_encouragements = [
  "cheer up",
  "ti jawek behi <3",
  "i am here for u",
  "i love u",
  "you are a good person"
]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] +' -'+json_data[0]['a']
  return quote

def update_encouragements(encouraging_msg):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_msg)
    db["encouragements"]= encouragements
  else:
    db["encouragements"] = [encouraging_msg]


def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"]= encouragements





@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client)) 
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="to my master Fozz - Beta version"))

@client.event
async def on_message(message):
  if message.author == client.user:
    return



  if message.content.startswith('$inspire'):
    if message.channel.id == 867880055182589975 :
      quote = get_quote()
      await message.channel.send(quote)
  
  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + list(db["encouragements"])

    if any(word in message.content for word in sad_words):
      await message.channel.send(random.choice(options))

  if message.content.startswith('$new'):
    enc_msg= message.content.split("$new ",1)[1]
    update_encouragements(enc_msg)
    await message.channel.send("new enc msg added^^")

  if message.content.startswith('$del'):
    encouragements = []
    if "encouragements" in db.keys():
      index= int(message.content.split("$del ",1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(list(encouragements))

  if message.content.startswith("$list"):
    if "encouragements" in db.keys():
      enc_list = db["encouragements"]
    await message.channel.send(list(enc_list))

  if message.content.startswith("$responding"):
    answer = message.content.split("$responding ",1)[1]
    if answer.lower() == "true":
      db["responding"]= True
      await message.channel.send("responding is ON !")
    else :
      db["responding"]= False
      await message.channel.send("responding is OFF !")


#THANK YOU https://uptimerobot.com/
keep_alive()

client.run(os.environ['TOKEN'])