from utils import DEBUG
from cogs.destiny2_cogs import DestinyCogs
import discord
import json

with open("credentials.json", "r") as file:
    token = json.load(file)["discord_oauth"]

intents = discord.Intents.default()
intents.message_content = True
intents.typing = False

#client = discord.Client(intents=intents)
client = discord.ext.commands.Bot(command_prefix="/", intents=intents)

@client.event
async def on_ready():
    print("=== Addings Cogs")
    await client.add_cog(DestinyCogs(client))

client.run(token)