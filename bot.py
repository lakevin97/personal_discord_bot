from utils import DEBUG
from cogs.destiny2_cogs import DestinyCogs
import discord
import json

def get_auth_token() -> str:
    try:
        with open("credentials.json", "r") as file:
            return json.load(file)["discord_oauth"]
    except:
        print("=== 'credentials.json' file is unavailable. Please check directory and try again.")

def initialize_bot(token:str):
    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.ext.commands.Bot(command_prefix="!", intents=intents)
 
    @client.event
    async def on_ready():
        print("=== Addings Cogs")
        await client.add_cog(DestinyCogs(client))

        try:
            synced = await client.tree.sync()
            print(f"Synced {len(synced)} commands!")
        except Exception as e:
            print(e)
    
    client.run(token)

if __name__ == '__main__':
    discord_token = get_auth_token()

    if discord_token:
        initialize_bot(discord_token)
    else:
        print("=== Bot.py is unable to retrieve token. ")