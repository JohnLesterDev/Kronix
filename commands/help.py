from discord.ext import commands
from .helpembed import HelpEmbed

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if self.bot.user in message.mentions:
            command_prefix = ">>"
            embed = HelpEmbed.create_embed(command_prefix, self.bot)
            await message.channel.send(embed=embed)

    @commands.command(name="help")
    async def help(self, ctx):
        command_prefix = ">>"
        embed = HelpEmbed.create_embed(command_prefix, self.bot)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(HelpCommand(bot))
