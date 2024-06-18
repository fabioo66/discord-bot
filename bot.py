import discord
from discord.ext import commands
import os

# Import all of the cogs
from help_cog import help_cog
from music_cog import music_cog

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Remove the default help command so that we can write our own
bot.remove_command('help')

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if "hello" in message.content.lower() or "hola" in message.content.lower():
        await message.channel.send(f"Hello {message.author.name}!")

    await bot.process_commands(message)

# Add cogs
@bot.event
async def on_ready():
    await bot.add_cog(help_cog(bot))
    await bot.add_cog(music_cog(bot))
    print(f'Logged in as {bot.user.name}')

# Run the bot
bot.run(os.getenv('token'))