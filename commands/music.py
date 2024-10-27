import discord
from discord.ext import commands
import yt_dlp

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queues = {}

    def get_guild_queue(self, guild_id):
        if guild_id not in self.queues:
            self.queues[guild_id] = []
        return self.queues[guild_id]

    async def play_next(self, ctx):
        queue = self.get_guild_queue(ctx.guild.id)
        
        if queue:
            next_song = queue.pop(0)
            await self.start_playback(ctx, next_song)
        else:
            await ctx.voice_client.disconnect()

    async def start_playback(self, ctx, song_url):
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
                info = ydl.extract_info(song_url, download=False)
                audio_url = info['url']
                title = info.get('title', 'Unknown Title')
            except KeyError as e:
                print(f"KeyError: {str(e)} while extracting info for URL: {song_url}")
                await ctx.send("An error occurred while extracting the audio.")
                return
            except Exception as e:
                print(f"Unexpected error: {str(e)} while extracting info for URL: {song_url}")
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
                after=lambda e: self.bot.loop.create_task(self.play_next(ctx))
            )
            await ctx.send(f'Now playing: {title}')
        except Exception as e:
            print(f"Error during playback: {str(e)}")
            await ctx.send(f"An error occurred while trying to play the song: {title}")

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
        """Play a song from a URL or a playlist."""
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            if ctx.voice_client is None:
                await channel.connect()
            elif ctx.voice_client.channel != channel:
                await ctx.voice_client.move_to(channel)
        else:
            await ctx.send("You need to be in a voice channel to use this command.")
            return

        queue = self.get_guild_queue(ctx.guild.id)

        ydl_opts = {'extract_flat': 'in_playlist', 'quiet': True}
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        if 'entries' in info:
            for entry in info['entries']:
                queue.append(entry['url'])
            await ctx.send(f"Added {len(info['entries'])} songs to the queue from the playlist!")
        else:
            queue.append(info['url'])
            await ctx.send(f"Added {info.get('title', 'Unknown Title')} to the queue!")

        if not ctx.voice_client.is_playing():
            await self.play_next(ctx)

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

    @commands.command(name='skip')
    async def skip(self, ctx):
        """Skip the currently playing song."""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Skipped the current song.")
        else:
            await ctx.send("No song is currently playing.")

    @commands.command(name='queue')
    async def show_queue(self, ctx):
        """Show the current music queue."""
        queue = self.get_guild_queue(ctx.guild.id)
        if queue:
            await ctx.send("\n".join(f"{idx+1}. {url}" for idx, url in enumerate(queue)))
        else:
            await ctx.send("The queue is empty.")

def setup(bot):
    bot.add_cog(Music(bot))
