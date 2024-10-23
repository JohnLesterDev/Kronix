import discord
from discord.ext import commands
from dotenv import load_dotenv
from config import TOKEN
from loggers import logger

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='>>', intents=intents, help_command=None)

logger.setup_logging(bot)

bot.load_extension('commands.help')
bot.load_extension('commands.ping')
bot.load_extension('commands.bible')
bot.load_extension('commands.music')
bot.load_extension('commands.advice')

bot.run(TOKEN)
