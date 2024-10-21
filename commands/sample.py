import discord
from discord.ext import commands

class ExampleEmbed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def embed_example(self, ctx):
        # Create an embed object
        embed = discord.Embed(
            title="This is the Title",  # The main title
            description="This is the **main body** (description) with some *italic text* and a [masked link](https://example.com).",  # Main body (description)
            color=discord.Color.blue()  # Embed color
        )

        # Author details (appears at the top of the embed)
        embed.set_author(
            name="Author Name", 
            icon_url="https://example.com/author-avatar.png"  # Optional author image
        )

        # Adding fields (Field title and field value)
        embed.add_field(name="Field Title 1", value="Field Value 1", inline=False)  # Not inline
        embed.add_field(name="Field Title 2", value="Field Value 2", inline=True)   # Inline field
        embed.add_field(name="Field Title 3", value="Field Value 3", inline=True)   # Another inline field

        # Set an image (appears below the description)
        embed.set_image(url="https://example.com/image.png")  # Main image below the body

        # Add a thumbnail (appears in the top right corner)
        embed.set_thumbnail(url="https://example.com/thumbnail.png")

        # Footer (appears at the bottom of the embed)
        embed.set_footer(
            text="This is the footer text", 
            icon_url="https://example.com/footer-icon.png"  # Optional footer icon
        )

        # Send the embed to the channel
        await ctx.send(embed=embed)

# Setup function to add the cog to the bot
def setup(bot):
    bot.add_cog(ExampleEmbed(bot))
