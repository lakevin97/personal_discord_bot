from utils.mysql_interface import MySql_Interface
from discord import app_commands, Interaction, Embed, Message, Reaction, User, TextChannel
from discord.ext import commands
import datetime

THUMBNAIL_URL= 'https://paspahang.org/wp-content/uploads/2019/03/get-the-marvelous-funny-looking-cat-memes-of-funny-looking-cat-memes.jpg'

class DestinyCogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
     
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

        Placeholder

        """
        token = self.generate_activity_id()
        query = f'INSERT INTO Raid (raid, player1, token_id) VALUES ("{raid_name}", "{interaction.user.name}", "{token}")'
        raid_embed = {
            "Activity_Type": "Raid",
            "Activity_Name": raid_name
            }

        if self.execute_query(query):
            message = self.generate_embed(interaction.user.name, raid_embed, token)
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

        Placeholder

        """
        token = self.generate_activity_id()

        query = f'INSERT INTO Dungeon (dungeon, player1, token_id) VALUES ("{dungeon_name}", "{interaction.user.name}", "{token}")'
        
        dungeon_embed = {
            "Activity_Type": "Dungeon",
            "Activity_Name": dungeon_name
            }
        
        if self.execute_query(query):
            message = self.generate_embed(interaction.user.name, dungeon_embed, token)
            await interaction.response.send_message(embed=message)
        else:        
            await interaction.response.send_message("An error has occured. Please contact Kevin with this error.", ephemeral=True)
   
    # Add Initial Reaction to Discord Msg
    @commands.Cog.listener()
    async def on_message(self, message:Message):
        """
        
        Placeholder

        """

        if message.author != self.bot.user:
            return
        
        if(message.embeds):
            await message.add_reaction('✅')

    # Add player name to database row
        # Read data from MySQL
        # Check if there are max users (3 players for Dungeon | 6 players for Raid)
        # Reserves (?) // Extra Credit
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction:Reaction, user:User):
        """
        
        Placeholder

        """
        message = reaction.message
        MAX_PLAYERS = None

        if user.bot == True or len(message.embeds) == 0:
            return
                
        current_activity = self.get_activity(message.embeds[0])

        if not self.update_db_add(current_activity, user):
            print(f"=== Activity Full")

        new_roster = current_activity["Roster"] + f"\n{user.name}"
        new_embed = self.generate_embed(new_roster, current_activity, current_activity["token_id"])
        
        await message.edit(embed=new_embed)

    ###############################################
    # Remove player name from database row
        # Read data from MySQL
        # Check if user that un-reacted is present in row
            # Pass if no
            # Update DB if yes
                # Update Discord Message Post
        # Ask anyone in reserves if they want to join (?) // Extra Credit
    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction:Reaction, user:User):
        """
        
        Placeholder

        """

        if user.bot == True:
            return

        print(f"{user.name} has reacted with {reaction.emoji}!")

    ### Helper functions ###
    def execute_query(self, query:str) -> bool: 
        """
        
        Placeholder

        """        
        db_client = MySql_Interface()
        result,is_successful = db_client.send_query(query=query)
        db_client.close_cnx()

        if "INSERT" in query or "UPDATE" in query and is_successful:
            return True

        return result

    def generate_activity_id(self) -> str:
        """
        
        Placeholder

        """
        return hash(str(datetime.datetime.now()))
    
    def generate_embed(self, roster: str, dict:dict, token:str):
        """
        
        Placeholder

        """
        setup = {
            "footer":{
                "text": token
            },
            "thumbnail": {
                "url": THUMBNAIL_URL
            },
            "fields":[
                {
                    "inline":True,
                    "name":"Activity",
                    "value": dict["Activity_Type"]
                },
                {
                    "inline":True,
                    "name":"Name",
                    "value": dict["Activity_Name"]
                },
                {
                    "inline":False,
                    "name":"Roster",
                    "value":f"{roster}"
                },
            ],
            "color":65280,
            "type":"rich",
            "description":"Don't be a piece of shit and join ya filthy animal by hitting that reaction!",
            "title":"Did someone schedule an activity, yes?"
            }
        
        return Embed.from_dict(setup)
    
    def get_activity(self, message:Embed):
        embed_msg = Embed.to_dict(message)
        ACTIVITY_TYPE=0
        ACTIVITY_NAME=1
        ROSTER=2

        embed_info = {
            "ID": embed_msg['footer']['text'],
            "ACTIVITY_TYPE": embed_msg['fields'][ACTIVITY_TYPE]['value'],
            "ACTIVITY_NAME": embed_msg['fields'][ACTIVITY_NAME]['value'],
            "ROSTER": embed_msg['fields'][ROSTER]['value']
        }

        query = f"SELECT * FROM {embed_info['ACTIVITY_TYPE']} WHERE token_id = {embed_info['ID']}"
        result = self.execute_query(query)
        
        result["Activity_Type"] = embed_info["ACTIVITY_TYPE"]
        result["Activity_Name"] = embed_info["ACTIVITY_NAME"]
        result["Roster"] = embed_info["ROSTER"]

        return result.iloc[0]

    def update_db_add(self, current_activity, user):        
        """
        
        Placeholder

        """
        MAX_PLAYERS = 3 if current_activity["Activity_Type"] == "Dungeon" else 6

        for num in range(1, MAX_PLAYERS+1):
            if current_activity[f'player{num}'] == None:
                query = f"UPDATE {current_activity['Activity_Type']} SET player{num} = '{user.name}' WHERE token_id='{current_activity['token_id']}';"
                
                if self.execute_query(query):
                    print(f"=== Player {num} set for {current_activity['Activity_Type']} w/ token_id = {current_activity['token_id']}")
                    return True
                
                return False
        

    def update_db_remove(self, current_activity, user):
        """
        
        Placeholder

        """
        MAX_PLAYERS = 3 if current_activity["Activity_Type"] == "Dungeon" else 6

        for num in range(1, MAX_PLAYERS+1):
                pass
            
            ### TO-DO
            # if current_activity[f'player{num}'] == None:
            #     query = f"UPDATE {current_activity['Activity']} SET player{num} = '{user.name}' WHERE token_id='{current_activity['token_id']}';"
                
            #     if self.execute_query(query):
            #         print(f"=== Player {num} set for {current_activity['Activity']} w/ token_id = {current_activity['token_id']}")
            #         return True
                
                return False