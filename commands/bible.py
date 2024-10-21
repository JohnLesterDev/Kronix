import discord
from discord.ext import commands
import requests

class BibleCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bible(self, ctx):
        user_name = ctx.author.name

        try:
            response = requests.get("https://bible-api.com/?random=verse")
            response.raise_for_status()  # Raise an error for bad responses
            data = response.json()

            # Extract the data from the JSON response
            reference = data.get('reference', 'Unknown Reference')
            verse_text = data.get('text', 'No verse text found.')
            translation_name = data.get('translation_name', 'Unknown Translation')

            # Create the embed
            embed = discord.Embed(
                title=reference,
                description=verse_text,
                color=discord.Color.from_rgb(117, 88, 39)
            )

            embed.set_author(name=translation_name)
            embed.set_footer(text=f"Source: Bible API | Requested by: {user_name}")
            embed.set_image(url="https://picsum.photos/400/600")  # Consider using a more relevant image URL

            # Send the embed to the channel
            await ctx.send(embed=embed)

        except requests.RequestException as e:
            await ctx.send(f"An error occurred while fetching the verse: {str(e)}")

# Setup function to add the cog to the bot
def setup(bot):
    bot.add_cog(BibleCommand(bot))
