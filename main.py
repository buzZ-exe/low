#main.py

#For main bot functionality
from discord.ext.commands import Bot
import cogs.config as config

global status_state                 #Unused variable for future commands - Don't delete       
status_state = 'with Humans'        #Probably never gonna use

BOT_PREFIX = "!"
client = Bot(command_prefix = BOT_PREFIX)
client.remove_command('help')

#Loading cogs
client.load_extension("cogs.redditCommands")
client.load_extension("cogs.commands")
client.load_extension("cogs.listeners")
client.load_extension("cogs.helpCommand")

client.run(config.token)