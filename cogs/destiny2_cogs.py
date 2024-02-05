from utils.mysql_interface import MySql_Interface
from discord import app_commands, Interaction, Embed, Message, Reaction, User
from discord.ext import commands
import datetime
import pandas as pd
import random

class DestinyCogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.description_list = []
        self.thumbnail_list = []

        with open("./description.txt", "r") as file:
            for line in file:
                self.description_list.append(line.strip())

        with open("./thumbnail.txt", "r") as file:
            for line in file:
                self.thumbnail_list.append(line.strip())
        
    @app_commands.command(
        description="To schedule a raid amongst Absolutely Chaotic."
        )
    @app_commands.describe(
        raid_name="Enter the name of the raid you want to run."
        )
    @app_commands.choices(
        raid_name=[
            app_commands.Choice(name="Crota's End", value="CROTAS_END"),
            app_commands.Choice(name="Garden of Salvation", value="GARDEN_OF_SALVATION"),
            app_commands.Choice(name="Root of Nightmares", value="ROOT_OF_NIGHTMARES"),
            app_commands.Choice(name="King's Fall", value="KINGS_FALL"),
            app_commands.Choice(name="Vow of the Desciple", value="VOW_OF_THE_DECIPLE"),
            app_commands.Choice(name="Vault of Glass", value="VAULT_OF_GLASS"),
            app_commands.Choice(name="Deep Stone Crypt", value="DEEP_STONE_CRYPT"),
            app_commands.Choice(name="Last Wish", value="LAST_WISH")
        ])
    async def schedule_raid(self, interaction: Interaction, raid_name:str):
        """
        This function the implementation of the slash command schedule_raid. Once
        a user selects which raid name, it will generate an insert query to the MySQL
        database and return a visual message for others to queue up.

        Parameters
        -----------
        interaction: :class:`discord.Interaction`
            The interaction that occurred.

        raid_name: :class:`string`
            The name of the raid the user selects when using the slash command.
        """

        if not self.is_registered(interaction.user.name):
            await interaction.response.send_message("Seems like you aren't registered in the database. Goddamn it Kevin, you had one job.\n\nPlease use the command !register with your bungie username.", ephemeral=True)
            return

        token = self.generate_activity_id()
        query = f'INSERT INTO raid (raid, player1, token_id) VALUES ("{raid_name}", "{interaction.user.name}", "{token}")'
        raid_embed = {
            "Activity_Type": "raid",
            "Activity_Name": raid_name
            }
    
        if self.execute_query(query):
            message = self.generate_embed(interaction.user.name, raid_embed, token)
            print("Waiting for response...")
            await interaction.response.send_message(embed=message)
        else:
            await interaction.response.send_message("An error has occured. Please contact Kevin with this error.", ephemeral=True)

    @app_commands.command(
        description="To schedule a dungeon amongst Absolutely Chaotic."
        )
    @app_commands.describe(
        dungeon_name="Enter the name of the dungeon you want to run."
        )
    @app_commands.choices(
        dungeon_name=[
            app_commands.Choice(name="Warlord's Ruin", value="WARLORDS_RUIN"),
            app_commands.Choice(name="Ghost of the Deep", value="GHOST_OF_THE_DEEP"),
            app_commands.Choice(name="Spire of the Watcher", value="SPIRE_OF_THE_WATCHER"),
            app_commands.Choice(name="Duality", value="DUALITY"),            
            app_commands.Choice(name="Grasp of Avarice", value="GRASP_OF_AVARICE"),         
            app_commands.Choice(name="Prophecy", value="PROPHECY"),
            app_commands.Choice(name="Pit of Heresy", value="PIT_OF_HERESY"),
            app_commands.Choice(name="Shattered Throne", value="SHATTERED_THRONE")
        ])
    async def schedule_dungeon(self, interaction: Interaction, dungeon_name:str):
        """
        This function the implementation of the slash command schedule_dungeon. Once
        a user selects which dungeon name, it will generate an insert query to the MySQL
        database and return a visual message for others to queue up.

        Parameters
        -----------
        interaction: :class:`discord.Interaction`
            The interaction that occurred.

        dungeon_name: :class:`string`
            The name of the dungeon the user selects when using the slash command.
        """
        if not self.is_registered(interaction.user.name):
            await interaction.response.send_message("Seems like you aren't registered in the database. Goddamn it Kevin, you had one job.\n\nPlease use the command !register with your bungie username.", ephemeral=True)
            return
        
        token = self.generate_activity_id()

        query = f'INSERT INTO dungeon (dungeon, player1, token_id) VALUES ("{dungeon_name}", "{interaction.user.name}", "{token}")'
        
        dungeon_embed = {
            "Activity_Type": "dungeon",
            "Activity_Name": dungeon_name
            }

        if self.execute_query(query):
            message = self.generate_embed(interaction.user.name, dungeon_embed, token)
            await interaction.response.send_message(embed=message)
        else:        
            await interaction.response.send_message("An error has occured. Please contact Kevin with this error.", ephemeral=True)
   
    @commands.command(
            name='register',
            help="Pairs Discord user with their associated Bungie username into the database."
    )
    async def register_user(self, ctx):
        bungie_username=str(ctx.message.content).split()[1]

        check_query = f'select * from user where id="{ctx.author}";'

        if self.execute_query(check_query).empty:
            insert_query=f'INSERT INTO user VALUES("{ctx.author}", "{bungie_username}");'
            
            if self.execute_query(insert_query) == True:
                print(f"=== Successfully inserted ({ctx.author},{bungie_username}) into user table.")
                await ctx.send(f"{ctx.author} registered with bungie user: {bungie_username}")
            else:
                print(f"=== Unable to insert ({ctx.author},{bungie_username}) into user table.")
        else:
            update_query=f'UPDATE user SET bungie_name="{bungie_username}" WHERE id="{ctx.author}";'

            if self.execute_query(update_query) == True:
                print(f"=== Successfully updated ({ctx.author}, {bungie_username}) in user table.")
                await ctx.send(f"{ctx.author} updated with bungie user: {bungie_username}")
            else:
                print(f"=== Unable to update ({ctx.author}, {bungie_username}) in user table.")        
                

    # Add initial reaction for users to interact with
    @commands.Cog.listener()
    async def on_message(self, message:Message):
        """
        This function will set the initial green check reaction for users to react to join
        the roster in the scheduled activity. 

        Parameters
        -----------
        message: :class:`discord.Message`
            Message class from discord.py library to retrieve the initial activity message.

        """

        if message.author != self.bot.user:
            return
        
        if(message.embeds):
            await message.add_reaction('✅')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction:Reaction, user:User):
        """

        This function will trigger an update to the database, if room permits, to the
        corresponding activity the user chooses to react the message to.

        Parameters
        -----------
        reaction: :class:`discord.Reaction`
            Reaction class from discord.py library to retrieve the message information that was reacted.

        user: :class:`discord.User`
            User class from discord.py library to retrieve the corresponding user information that reacted.
        """

        if user.bot == True or reaction.message.author != self.bot.user:
            return

        if not self.is_registered(user.name):
            member = reaction.message.guild.get_member(user.id)
            await member.send("Seems like you aren't registered in the database. Goddamn it Kevin, you had one job.\n\nPlease use the command !register with your bungie username in the server.")
            return

        message = reaction.message

        activity_snapshot, embed_info = self.get_activity(message.embeds[0])

        if self.update_db_add(activity_snapshot, embed_info, user):
            new_roster = embed_info["Roster"] + f"\n{user.name}"
            new_embed = self.generate_embed(new_roster, embed_info, embed_info["token_id"])
            await message.edit(embed=new_embed)
            
    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction:Reaction, user:User):
        """
        This function will trigger an update to the database, if participating, to the
        corresponding activity to remove themselves from the roster if partcipating.

        Parameters
        -----------
        reaction: :class:`discord.Reaction`
            Reaction class from discord.py library to retrieve the message information that got a reaction removed.

        user: :class:`discord.User`
            User class from discord.py library to retrieve the corresponding user information that reacted.
        """

        message = reaction.message

        if user.bot == True or message.author != self.bot.user:
            return
                
        activity_snapshot, embed_info = self.get_activity(message.embeds[0])

        if not self.update_db_remove(activity_snapshot, embed_info, user):
            print(f"=== Player is not recorded on file.")
        else:
            new_roster = embed_info["Roster"].replace(user.name, "")
            new_embed = self.generate_embed(new_roster, embed_info, embed_info["token_id"])
            await message.edit(embed=new_embed)
    
    ########################
    ### Helper functions ###
    ########################
            
    def is_registered(self, user:str) -> bool:
        query = f'select * from user where id="{user}";'

        if self.execute_query(query).empty:
            return False
        else:
            return True
        
    def execute_query(self, query:str): 
        """
        A function that is called from `on_react_add` and `on_react_remove` to execute
        a SQL query to update the database accordingly based on the user's action.

        Parameters
        -----------
        query: :class:`string`
            A pre-defined SQL query based on the called function

        Returns
        ---------
        :class:`bool`
            Determines if the query execution was succesful if running an insert or update query.
        result: :class:`pandas.dataframe` 
            Returns the "select" query result in a pandas.dataframe 
        """     
        print(f"=== Executing Query: {query}")

        db_client = MySql_Interface()
        result,is_successful = db_client.send_query(query=query)
        db_client.close_cnx()

        if "INSERT" in query or "UPDATE" in query:
            if is_successful:
                return True
            else:
                return False

        return result

    def generate_activity_id(self) -> str:
        """
        To generate a unique hash token by using the datetime value when this is called.

        Returns
        ---------
        :class:`str`
            The unique hash token based on the date and time when called.
        """

        return hash(str(datetime.datetime.now()))
    
    def generate_embed(self, roster: str, activity_info:dict, token:str) -> Embed:
        """
        Generates the associated embeded message based on the user's commands or 
        actions related to the corresponding activity.  

        Parameters
        -----------
        roster: :class:`string`
            The people who are participating based on on_reaction_add and 
            on_reaction_remove.
        activity_info: :class:`dict`
            Contains the key-value pair of the activity details.
        token: :class:`str`
            The unique token id for the corresponding activity.

        Returns
        ---------
        :class:`discord.Embed`
            Returns a discord embed object that would display the information in the text 
            channel.
        """

        setup = {
            "footer":{
                "text": token
            },
            "thumbnail": {
                "url": random.choice(self.thumbnail_list)
            },
            "fields":[
                {
                    "inline":True,
                    "name":"Activity",
                    "value": activity_info["Activity_Type"]
                },
                {
                    "inline":True,
                    "name":"Name",
                    "value": activity_info["Activity_Name"]
                },
                {
                    "inline":False,
                    "name":"Roster",
                    "value":f"{roster}"
                },
            ],
            "color":65280,
            "type":"rich",
            "description":random.choice(self.description_list),
            "title":"Did someone schedule an activity, yes?"
            }
        
        return Embed.from_dict(setup)
    
    def get_activity(self, message:Embed) -> (pd.DataFrame, dict):
        """
        Retrieves the activity information from the embeded message that was interacted with.

        Parameters
        -----------
        message: :class:`discord.Embed`
            The corresponding embed message that was intereacted with.

        Returns
        ---------
        :class:`discord.Embed`
            Returns a discord embed object that would display the information in the text 
            channel.
        """
        embed_msg = Embed.to_dict(message)
        ACTIVITY_TYPE=0
        ACTIVITY_NAME=1
        ROSTER=2

        embed_info = {
            "token_id": embed_msg['footer']['text'],
            "Activity_Type": embed_msg['fields'][ACTIVITY_TYPE]['value'],
            "Activity_Name": embed_msg['fields'][ACTIVITY_NAME]['value'],
            "Roster": embed_msg['fields'][ROSTER]['value']
        }

        query = f"SELECT * FROM {embed_info['Activity_Type']} WHERE token_id = {embed_info['token_id']}"
        result = self.execute_query(query)

        return result.iloc[0], embed_info

    def update_db_add(self, current_activity, embed_info, user):        
        """
        A function that is called when a user reacts to an embedded message wanting to participate
        in the activity and update the database if any available openings.
        
        Parameters
        -----------
        current_activity: :class:`pandas.DataFrame`
            Retrieves the activity row from MySQL to check if any user columns are null.
        embed_info: :class:`dict`
            Retrieves the associated information from the embedded message to generate
            a SQL query.
        user: :class:`discord.User`
            Retrieves the user information that initiated the react_add event.

        Returns
        ---------
        :class:`bool`
            Returns `True` if the user has been successfully added to the activity else `False`.
        """
        MAX_PLAYERS = 3 if embed_info["Activity_Type"] == "dungeon" else 6

        for num in range(1, MAX_PLAYERS+1):
            if current_activity[f'player{num}'] == user.name:
                print("=== User is already part of the activity.")
                return False
            
            if current_activity[f'player{num}'] == None:
                query = f"UPDATE {embed_info['Activity_Type']} SET player{num} = '{user.name}' WHERE token_id='{embed_info['token_id']}';"
                
                if self.execute_query(query):
                    print(f"=== Player {num} set for {embed_info['Activity_Type']} w/ token_id = {embed_info['token_id']}")
                    return True

        print(f"=== Activity Full")        
        return False
        
    def update_db_remove(self, current_activity,embed_info, user):
        """
        A function that is called when a user removes their react from an embedded message
        to remove themselves from participating.
        
        Parameters
        -----------
        current_activity: :class:`pandas.DataFrame`
            Retrieves the activity row from MySQL to check if the specified 
            user is part of the roster
        embed_info: :class:`dict`
            Retrieves the associated information from the embedded message to generate
            a SQL query.
        user: :class:`discord.User`
            Retrieves the user information that initiated the react_remove event.

        Returns
        ---------
        :class:`bool`
            Returns `True` if the user has been successfully removed else `False`.
        """
        MAX_PLAYERS = 3 if embed_info["Activity_Type"] == "dungeon" else 6

        for num in range(1, MAX_PLAYERS+1):
            if current_activity[f'player{num}'] == user.name:
                query = f"UPDATE {embed_info['Activity_Type']} SET player{num} = NULL WHERE token_id='{embed_info['token_id']}';"
                
                if self.execute_query(query):
                    print(f"=== Player {num} removed from {embed_info['Activity_Type']} w/ token_id = {embed_info['token_id']}")
                    return True
                    
        return False
