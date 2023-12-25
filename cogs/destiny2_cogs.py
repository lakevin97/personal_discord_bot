from utils.mysql_interface import MySql_Interface
import discord
from typing import Optional
from discord import app_commands
from discord.ext import commands

class DestinyCogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="schedule_activity", description="To schedule an activity amongst guardians.")
    @app_commands.describe(activity="The description of activity you want to schedule.")
    @app_commands.choices(activity=[
        app_commands.Choice(name="Raid", value=1),
        app_commands.Choice(name="Dungeon", value=2)
    ])
    async def schedule(self, interaction: discord.Interaction, activity:Optional[app_commands.Choice[int]]):
        print(f"Activity Chosen: {activity}")
        await interaction.response.send_message(f" {interaction.user.id}", ephemeral=True)
    
    # @app_commands.command(name="eeek", description="parade")
    # async def hello2(self, interaction: discord.Interaction):
    #     await interaction.response.send_message(f" {interaction.user.id}", ephemeral=True)