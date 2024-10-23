import discord
from discord.ext import commands
import yt_dlp

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='join')
    async def join(self, ctx):
        """Join the voice channel."""
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            if ctx.voice_client and ctx.voice_client.channel == channel:
                await ctx.send(f"I'm already in {channel}!")
                return
            await channel.connect()
            await ctx.send(f"Joined {channel}!")
        else:
            await ctx.send("You need to be in a voice channel to use this command :>")

    @commands.command(name='leave')
    async def leave(self, ctx):
        """Leave the voice channel."""
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Disconnected from the voice channel.")
        else:
            await ctx.send("I'm not in a voice channel.")

    @commands.command(name='play')
    async def play(self, ctx, *, url):
        """Play a song from a URL."""
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            if ctx.voice_client is None:
                await channel.connect()
            elif ctx.voice_client.channel != channel:
                await ctx.voice_client.move_to(channel)
        else:
            await ctx.send("You need to be in a voice channel to use this command.")
            return

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        await ctx.message.delete()

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
            'noplaylist': True,
            'quiet': False,
            'nocheckcertificate': True  
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(url, download=False)
                audio_url = info['url']
                title = info.get('title', 'Unknown Title')

            except KeyError as e:
                print(f"KeyError: {str(e)} while extracting info for URL: {url}")
                await ctx.send("An error occurred while extracting the audio.")
                return
            except Exception as e:
                print(f"Unexpected error: {str(e)} while extracting info for URL: {url}")
                await ctx.send("An unexpected error occurred.")
                return

        voice_client = ctx.voice_client
        print(f'Playing URL: {audio_url}')

        try:
            before_options = '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
            voice_client.play(
                discord.FFmpegPCMAudio(
                    audio_url,
                    before_options=before_options,
                    options="-vn -loglevel quiet",
                ),
                after=lambda e: print(f'Finished playing: {e}') if e else None
            )
            await ctx.send(f'Now playing: {title}')
        except Exception as e:
            print(f"Error during playback: {str(e)}")
            await ctx.send(f"An error occurred while trying to play the song: {title}")

    @commands.command(name='pause')
    async def pause(self, ctx):
        """Pause the currently playing song."""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("Paused the music.")
        else:
            await ctx.send("No music is currently playing.")

    @commands.command(name='resume')
    async def resume(self, ctx):
        """Resume the currently paused song."""
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("Resumed the music.")
        else:
            await ctx.send("No music is currently paused.")

    @commands.command(name='stop')
    async def stop(self, ctx):
        """Stop the currently playing song."""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Stopped the music.")
        else:
            await ctx.send("No music is currently playing.")

def setup(bot):
    bot.add_cog(Music(bot))
