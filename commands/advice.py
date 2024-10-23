import discord
from discord.ext import commands
import requests

class Advice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='advice')
    async def advice(self, ctx):
        """Fetch random advice from the Advice Slip API and display it in an embed."""
        try:
            response = requests.get("https://api.adviceslip.com/advice")
            data = response.json()

            advice = data['slip']['advice']

            embed = discord.Embed(
                title="Random Advice",
                description=advice,
                color=discord.Color.dark_gold()
            )
            
            await ctx.message.delete()
            await ctx.send(embed=embed)

        except Exception as e:
            print(f"Error fetching advice: {str(e)}")
            await ctx.send("An error occurred while fetching advice.")

def setup(bot):
    bot.add_cog(Advice(bot))
