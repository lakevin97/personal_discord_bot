from utils.mysql_interface import MySql_Interface
from discord.ext import commands

class DestinyCogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Hi!")
    
    @commands.command(name="PeePee")
    async def hello_command(self,ctx):
        await ctx.send("I am a cog machine")