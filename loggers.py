import logging
import discord
from discord.ext import commands

class Logger:
    """Logger class for handling bot events and commands."""

    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format='[%(asctime)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=[
                logging.FileHandler('HISTORY.log', mode='a', encoding='utf-8'),  # Use UTF-8 encoding
                logging.StreamHandler()  # Also log to console
            ]
        )


    def log_command(self, ctx, status):
        """Log command execution status."""
        guild = ctx.guild.name if ctx.guild else "DM"
        channel = ctx.channel.name if isinstance(ctx.channel, discord.TextChannel) else "DM"
        user = f"{ctx.author.name}#{ctx.author.discriminator}"
        command = ctx.command.name if ctx.command else "Unknown Command"

        log_message = (
            f"[Guild: {guild}] "
            f"[Channel: {channel}] "
            f"[User: {user}] "
            f"[Command: {command}] "
            f"[Status: {status}]"
        )
        logging.info(log_message)

    def log_event(self, event_type, user, details):
        """Log general bot events."""
        log_message = (
            f"[Event: {event_type}] "
            f"[User: {user}] "
            f"[Details: {details}]"
        )
        logging.info(log_message)

    def setup_logging(self, bot: commands.Bot):
        """Setup event logging with the bot."""
        @bot.event
        async def on_command(ctx):
            self.log_command(ctx, "Success")

        @bot.event
        async def on_command_error(ctx, error):
            self.log_command(ctx, f"Failed ({error})")

        @bot.event
        async def on_ready():
            self.log_event("INIT", bot.user, f"'Bot is ready! Logged in as {bot.user}'")

        @bot.event
        async def on_message(message):
            logging.info(f'Message received from {message.author} in {message.guild.name}#{message.channel.name}: {message.content}')
            await bot.process_commands(message)

        @bot.event
        async def on_message_edit(before, after):
            logging.info(f"Message edited in {before.guild.name}#{before.channel.name} by {before.author}: '{before.content}' -> '{after.content}'")

        @bot.event
        async def on_message_delete(message):
            logging.info(f"Message deleted in {message.guild.name}#{message.channel.name} by {message.author}: '{message.content}'")

        @bot.event
        async def on_member_join(member):
            logging.info(f'Member {member} has joined {member.guild.name}')

        @bot.event
        async def on_member_remove(member):
            logging.info(f'Member {member} has left {member.guild.name}')

        @bot.event
        async def on_member_update(before, after):
            logging.info(f'Member update in {after.guild.name}: {before} -> {after}')

        @bot.event
        async def on_role_create(role):
            logging.info(f'Role created: {role.name} in {role.guild.name}')

        @bot.event
        async def on_role_delete(role):
            logging.info(f'Role deleted: {role.name} in {role.guild.name}')

        @bot.event
        async def on_role_update(before, after):
            logging.info(f'Role updated in {after.guild.name}: {before.name} -> {after.name}')

        @bot.event
        async def on_guild_update(before, after):
            logging.info(f'Guild update: {before.name} -> {after.name}')

        @bot.event
        async def on_guild_channel_create(channel):
            logging.info(f'Channel created: {channel.name} in {channel.guild.name}')

        @bot.event
        async def on_guild_channel_delete(channel):
            logging.info(f'Channel deleted: {channel.name} in {channel.guild.name}')

        @bot.event
        async def on_guild_channel_update(before, after):
            logging.info(f'Channel updated in {after.guild.name}: {before.name} -> {after.name}')

        @bot.event
        async def on_user_update(before, after):
            logging.info(f'User updated: {before.name}#{before.discriminator} -> {after.name}#{after.discriminator}')

logger = Logger()
