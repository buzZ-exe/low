import discord
from discord.ext import commands
import random, asyncio

class listeners(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Logged in as " + self.client.user.name)
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="with my battery."))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return

        elif message.content.startswith('!guess'):
            await message.channel.send('Alright. I have a number between 1 and 10 in mind. Guess it')

            def guess_check(m):
                return m.content.isdigit() and m.author == message.author and m.channel == message.channel

            try:
                guess = await self.client.wait_for('message', timeout=5.0, check=guess_check)
            except asyncio.TimeoutError:
                await message.channel.send("You took too long...")

            answer = random.randint(1, 10)
            if guess is None:
                response = 'Sorry, you took too long. It was {}.'
                await message.channel.send(response.format(answer))
                return
            if int(guess.content) == answer:
                await message.channel.send('Right on the money. Here, have a candy :)')
            else:
                await message.channel.send("It's actually {}. You suck.".format(answer))    

def setup(client):
    client.add_cog(listeners(client))