import discord
from discord.ext import commands

#For bot functions
import random, asyncio
from datetime import datetime
import response_lists

#For ZenQuotes
import json, requests


class commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context = True,
                    aliases = ['random', 'roll'],
                    description = 'Generates a random number between one and the number you input',
                    brief = 'Random number generator')
    async def Random(self, ctx, number = 100):
        response = random.randint(1,int(number))
        await ctx.send(str(response))




    @commands.command(aliases = ['flip', 'toss'],
                    description = 'Flips a coin',
                    brief = 'Flips a coin')
    async def Flip(self, ctx):
        num = random.randint(0,1)
        response = 'Tails'
        if num == 0:
            response = 'Tails'
        elif num == 1:
            response = 'Heads'
        await ctx.send('>>> ' + response)




    @commands.command(aliases = ['quote'],
                    description = "Displays a random quote")
    async def Quote(self, ctx):
        response = requests.get('https://zenquotes.io/api/random')
        jRes = json.loads(response.text)

        embed = discord.Embed(colour = discord.Colour.red())

        embed.set_author(name = 'Quote')
        embed.add_field(name = jRes[0]['q'], value = 'By ' + jRes[0]['a'])
        
        await ctx.send(embed = embed)




    @commands.command(aliases = ['face', 'emoticon'],
                    description = "Returns a random face emoticon from the internet",
                    brief = "Sends a face ( ͡° ͜ʖ ͡°)")
    async def Face(self, ctx):
            
        num = random.randint(1,len(response_lists.face_responses)-1)
        await ctx.send(response_lists.face_responses[num])



    @commands.command(aliases = ['add', 'advertise', 'addme', 'plugme'],
                    description = "Sends the link you need to add this bot to your server.",
                    breif = "Sends the link you need to add this bot.")
    async def Add(self, ctx):
        response = 'https://discordapp.com/oauth2/authorize?client_id=730435329420689428&scope=bot'
        await ctx.send(response)




    @commands.command(aliases = ['poll', 'vote'],
                    description = 'Creates a poll on the spot',
                    brief = 'Creates a poll on the spot')
    async def Poll(self, ctx, ques, *args:str):

        PollList = ['🇦', '🇧', '🇨',
                    '🇩', '🇪', '🇫']

        PollList2 = [':regional_indicator_a:', ':regional_indicator_b:', ':regional_indicator_c:',
                    ':regional_indicator_d:', ':regional_indicator_e:', ':regional_indicator_f:']
        
        if len(args) <= 1:
            await ctx.send('A poll cannot have less than or 1 option.')

        elif len(args) > 6:
            await ctx.send('A poll cannot have more than 6 options.')

        else:

            embed = discord.Embed(title = ques, colour = discord.Colour.red())

            for i in range(1,len(args)+1):
                embed.add_field(name = PollList2[i-1] + ' ' + args[i-1], value = '\u200b', inline = False)

            embed.set_footer(text = 'React with the corresponding option to vote.')

            msg = await ctx.send(embed = embed)

            for i in range(0,len(args)):
                await msg.add_reaction(PollList[i])    


    @commands.command(aliases = ['guess'],
                    description = 'Play a guess game with the bot',
                    brief = 'Play a simple guess game with the bot.')
    async def Guess(self):
        pass


    @commands.command(aliases = ['remind', 'remindme'],
                    pass_context = True)
    async def Remind(self, ctx, sec = None):

        if sec is None:

            embed = discord.Embed(colour = discord.Colour.red())

            embed.set_author(name = 'Remind')
            embed.add_field(name = '='*36 + '\n!remind ["thing to remind"] [time in minutes]\n' + '='*36,
                            value = 'Example: !remind "to do laundry" 30\nSends a DM to you reminding you to do something in the time you give.')

            await ctx.send(embed = embed)
        else:

            embed = discord.Embed(colour = discord.Colour.red())

            embed.set_author(name = 'Reminder set for ' + sec + ' minutes from now.\nIt will arrive in your DMs.')
            await ctx.send(ctx.message.author.mention, embed = embed)

            time = float(sec)*60
            author = ctx.message.author
            user = self.client.get_user(author.id)  

            embed2 = discord.Embed(colour = discord.Colour.red())

            embed2.set_author(name = 'You asked me to remind you.')

            await asyncio.sleep(time)
            await user.send(embed = embed2)




    @commands.command(pass_context = True)
    async def time(self, ctx, arg, unit = 'min'):

        if unit.lower() == 'min' or 'm' or 'mins':
            mins = float(arg)*60
            await ctx.send(arg + ' minutes is ' + str(mins) + ' seconds.')

        elif unit.lower() == 'hour' or 'h' or 'hours':
            hours = float(arg)*3600
            await ctx.send(arg + ' hours is ' + str(hours) + 'seconds.')




    @commands.command(pass_context = True)
    async def reaction(self, ctx):

        def check(msg):                         #To check whether the person who called the function is the one being counted
            return msg.author == ctx.author and msg.channel == ctx.channel

        embed1 = discord.Embed(colour = discord.Colour.red())
        embed1.add_field(name = 'Reaction Test', value = 'When this turns green enter any message :red_circle:')

        embed2 = discord.Embed(colour = discord.Colour.red())
        embed2.add_field(name = 'Reaction Test', value = 'Enter any message NOW :green_circle:')

        message = await ctx.send(embed = embed1)
        await asyncio.sleep(random.randint(2,5))
        await message.edit(embed = embed2)
        
        try:
            reactionStart = datetime.now()
            await self.client.wait_for("message", check=check,  timeout=5.0)
            reactionEnd = datetime.now()
            reactionTime = reactionEnd - reactionStart

            embed3 = discord.Embed(colour = discord.Colour.red())
            embed3.add_field(name = 'Reaction Test', value = 'Your reaction time was ' + str(reactionTime)[6] + 's ' + str(reactionTime)[8:11] + 'ms')
            embed3.set_footer(text = "PS. This is inaccurate af cuz of the latency")
            await message.edit(embed = embed3)
        except asyncio.TimeoutError:
            await ctx.send("You took too long...")

def setup(client):
    client.add_cog(commands(client))