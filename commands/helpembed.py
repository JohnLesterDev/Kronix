import discord

class HelpEmbed:
    """Class to generate the Help Embed"""

    @staticmethod
    def create_embed(command_prefix, bot):
        embed = discord.Embed(
            title="Help - Kronix Commands",
            description="Here is a list of commands you can use with Kronix ♡:",
            color=discord.Color.from_rgb(117, 88, 39)
        )

        embed.add_field(
            name=f"**{command_prefix}ping**",
            value="Check if the bot is alive by returning `Pong!`",
            inline=False
        )
        embed.add_field(
            name=f"**{command_prefix}bible**",
            value="Get a random Bible verse.",
            inline=False
        )
        embed.set_footer(text="Use the commands with the specified prefix '>>'.")
        embed.set_thumbnail(url=bot.user.avatar.url)

        return embed
