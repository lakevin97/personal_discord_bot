from utils.mysql_interface import MySql_Interface
from typing import Optional
from discord import app_commands, Interaction, Embed
from discord.ext import commands
import textwrap

THUMBNAIL_URL= 'https://assetsio.reedpopcdn.com/destiny-2-the-witness.jpg?width=1920&height=1920&fit=bounds&quality=80&format=jpg&auto=webp'

class DestinyCogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
     
    @app_commands.command(
            name="schedule_activity", 
            description="To schedule an activity amongst guardians.")
    @app_commands.describe(
        activity="The description of activity you want to schedule."
        )
    @app_commands.choices(
        activity=[
            app_commands.Choice(name="Crota's End", value="CROTAS_END"),
            app_commands.Choice(name="Garden of Salvation", value="GARDEN_OF_SALVATION"),
            app_commands.Choice(name="Root of Nightmares", value="ROOT_OF_NIGHTMARES"),
            app_commands.Choice(name="King's Fall", value="KINGS_FALL"),
            app_commands.Choice(name="Vow of the Desciple", value="VOW_OF_THE_DECIPLE"),
            app_commands.Choice(name="Vault of Glass", value="VAULT_OF_GLASS"),
            app_commands.Choice(name="Deep Stone Crypt", value="DEEP_STONE_CRYPT"),
            app_commands.Choice(name="Last Wish", value="LAST_WISH"),
            app_commands.Choice(name="Warlord's Ruin", value="WARLORDS_RUIN"),
            app_commands.Choice(name="Ghost of the Deep", value="GHOST_OF_THE_DEEP"),
            app_commands.Choice(name="Spire of the Watcher", value="SPIRE_OF_THE_WATCHER"),
            app_commands.Choice(name="Duality", value="DUALITY"),            
            app_commands.Choice(name="Grasp of Avarice", value="GRASP_OF_AVARICE"),         
            app_commands.Choice(name="Prophecy", value="PROPHECY"),
            app_commands.Choice(name="Pit of Heresy", value="PIT_OF_HERESY"),
            app_commands.Choice(name="Shattered Throne", value="SHATTERED_THRONE")
        ])
    async def schedule(self, interaction: Interaction, activity:str):
        # Send the embed to the same channel where the command was used
        message = self.generate_embed(interaction, activity)
        
        await interaction.response.send_message(embed=message)
        # Process user input and return a discord channel message

    def generate_embed(self, interaction: str, activity:str):
        setup = {
            "footer":{
                "text":"created by " + interaction.user.display_name
            },
            "thumbnail": {
                "url": THUMBNAIL_URL
            },
            "fields":[
                {
                    "inline":True,
                    "name":"Activity",
                    "value": activity
                },
                {
                    "inline":True,
                    "name":"Players",
                    "value":"Another Value\nValue2\nValue3\nValue4\nValue5"
                },
            ],
            "color":65280,
            "type":"rich",
            "description":"Don't be a piece of shit and join ya filthy animal by hitting that reaction!",
            "title":"Did someone schedule an activity, yes?"
            }
        
        return Embed.from_dict(setup)
    
    async def get_user_reactions(self):
        # Get notified who is joining up to 5 other players and update to DB
        pass

    async def add_reactions(self):
        # Create a reaction button so people can just press and sign up
        pass

    async def update_db(self):
        # Update the database on activity
        pass