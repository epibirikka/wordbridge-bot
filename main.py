import discord
import client

from dotenv import load_dotenv
load_dotenv()


intents = discord.Intents.default()
intents.message_content = True

_client = client.WordBridge(intents=intents)
_client.bootstrap()

