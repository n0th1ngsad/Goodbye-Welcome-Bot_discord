import discord
from discord.ext import commands

import Welcome as Welcome
import Goodbye as Goodbye

intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)  

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    print(f'Bot is connected to guilds :')
    for guild in client.guilds:
        print(f'- {guild.name} (ID: {guild.id})')

    Goodbye.setup(client)
    Welcome.setup(client)

client.run("YOUR_TOKEN")   
