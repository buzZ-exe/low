#bot.py

#For ZenQuotes
import json, requests

#For main bot functionality
import discord, praw
from discord.ext.commands import Bot

#For bot functions
import random, asyncio, config

global status_state                 #Unused variable for future commands - Don't delete       
status_state = 'with Humans'        #Probably never gonna use

BOT_PREFIX = "!"

client = Bot(command_prefix = BOT_PREFIX)

client.remove_command('help')

reddit = praw.Reddit(client_id = config.client_id,
                    client_secret = config.client_secret,
                    user_agent = config.client_agent)

@client.event
async def on_ready():
    global status_state
    print("Logged in as " + client.user.name)
    game = discord.Game(status_state)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="with my battery."))


@client.event
async def on_member_join(member):
    channel = await member.create_dm()
    await channel.send('Hello,' + member.mention + '. Welcome to the server!')
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello, {0.author.mention}'.format(message)
        await message.channel.send(msg)

    elif message.content.startswith('!code'):
            await message.delete()

    elif message.content.startswith('!say'):
        await message.delete()

    elif message.content.startswith('!guess'):
        await message.channel.send('Alright. I have a number between 1 and 10 in mind. Guess it')

        def guess_check(m):
            return m.content.isdigit() and m.author == message.author and m.channel == message.channel

        try:
            guess = await client.wait_for('message', timeout=5.0, check=guess_check)
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

    await client.process_commands(message)

@client.command(pass_context = True,
                aliases = ['random', 'roll'],
                description = 'Generates a random number between one and the number you input',
                brief = 'Random number generator')
async def Random(ctx, number = 100):
    response = random.randint(1,int(number))
    await ctx.send(str(response))

@client.command(aliases = ['flip', 'toss'],
                description = 'Flips a coin',
                brief = 'Flips a coin')
async def Flip(ctx):
    num = random.randint(0,1)
    response = 'Tails'
    if num == 0:
        response = 'Tails'
    elif num == 1:
        response = 'Heads'
    await ctx.send('>>> ' + response)

@client.command(aliases = ['quote'],
                description = "Displays a random quote")
async def Quote(ctx):
    response = requests.get('https://zenquotes.io/api/random')
    jRes = json.loads(response.text)

    embed = discord.Embed(colour = discord.Colour.red())

    embed.set_author(name = 'Quote')
    embed.add_field(name = jRes[0]['q'], value = 'By ' + jRes[0]['a'])
    
    await ctx.send(embed = embed)

@client.command(aliases = ['face', 'emoticon'],
                description = "Returns a random face emoticon from the internet",
                brief = "Sends a face ( ͡° ͜ʖ ͡°)")
async def Face(ctx):
    import response_lists
    
    num = random.randint(1,len(response_lists.face_responses)-1)
    await ctx.send(response_lists.face_responses[num])

@client.command(aliases = ['add', 'advertise', 'addme', 'plugme'],
                description = "Sends the link you need to add this bot to your server.",
                breif = "Sends the link you need to add this bot.")
async def Add(ctx):
    response = 'https://discordapp.com/oauth2/authorize?client_id=730435329420689428&scope=bot'
    await ctx.send(response)

@client.command(aliases = ['me'],
                description = 'Presenst yourself in the third person',
                brief = 'Refers to you in the third person')
async def Me(ctx, *,  arg):
    response = ">>> " + ctx.message.author.mention + " " + arg
    await ctx.send(response)

@client.command(aliases = ['poll', 'vote'],
                description = 'Creates a poll on the spot',
                brief = 'Creates a poll on the spot')
async def Poll(ctx, ques, *args:str):

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
    

@client.command(aliases = ['guess'],
                description = 'Play a guess game with the bot',
                brief = 'Play a simple guess game with the bot.')
async def Guess():
    pass

@client.command(aliases = ['pun'],
                description = 'Sends a cheesy old pun back',
                brief = 'Dad joke galore')
async def Pun(ctx):
    joke = reddit.subreddit('dadjokes').hot()
    joke_post = random.randint(1, 50)
    for i in range(0, joke_post):
        submission = next(x for x in joke if x.stickied == False)

    embed = discord.Embed(colour = discord.Colour.red())
    embed.add_field(name = submission.title, value = submission.selftext)
    embed.set_footer(text = 'Thank you, r/dadjokes')

    await ctx.send(embed = embed)

@client.command(aliases = ['darkjoke', 'djoke', 'dj'])
async def Darkjoke(ctx):
    joke = reddit.subreddit('darkjokes').hot()
    joke_post = random.randint(1, 50)
    for i in range(0, joke_post):
        submission = next(x for x in joke if x.stickied == False)

    embed = discord.Embed(colour = discord.Colour.red())
    embed.add_field(name = submission.title, value = submission.selftext)
    embed.set_footer(text = 'Thank you, r/darkjokes')

    await ctx.send(embed = embed)

@client.command(pass_context = True)
async def meme(ctx):
    meme = reddit.subreddit('memes').hot()
    meme_post = random.randint(1, 50)
    for i in range(0, meme_post):
        submission = next(x for x in meme if x.stickied == False)

    embed = discord.Embed(colour = discord.Colour.red())
    embed.set_image(url = submission.url)
    embed.set_footer(text = "Thank you, r/memes")

    await ctx.send(embed = embed)

@client.command(aliases = ['dm'],
                pass_context = True)
async def dankmeme(ctx):
    meme = reddit.subreddit('dankmemes').hot()
    meme_post = random.randint(1, 50)
    for i in range(0, meme_post):
        submission = next(x for x in meme if not x.stickied)

    embed = discord.Embed(colour = discord.Colour.red())
    embed.set_image(url = submission.url)
    embed.set_footer(text = "Thank you, r/dankmemes")

    await ctx.send(embed = embed)

@client.command(aliases = ['remind', 'remindme'],
                pass_context = True)
async def Remind(ctx, sec = None):

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
        user = client.get_user(author.id)  

        embed2 = discord.Embed(colour = discord.Colour.red())

        embed2.set_author(name = 'You asked me to remind you.')

        await asyncio.sleep(time)
        await user.send(embed = embed2)

@client.command(pass_context = True)
async def time(ctx, arg, unit = 'min'):

    if unit.lower() == 'min' or 'm' or 'mins':
        mins = float(arg)*60
        await ctx.send(arg + ' minutes is ' + str(mins) + ' seconds.')

    elif unit.lower() == 'hour' or 'h' or 'hours':
        hours = float(arg)*3600
        await ctx.send(arg + ' hours is ' + str(hours) + 'seconds.')


@client.command(pass_context = True)
async def help(ctx, cmd = None):

    if cmd == None:

        embed = discord.Embed(colour = discord.Colour.red())

        embed.set_author(name = 'HELP HAS ARRIVED')
        embed.add_field(name = ':+1: Add', value = 'Sends the link you need to add this bot.', inline = True)
        embed.add_field(name = ':face_with_raised_eyebrow: Face', value = 'Sends a face ( ͡° ͜ʖ ͡°)', inline = True)
        embed.add_field(name = ':arrows_counterclockwise: Flip', value = 'Flips a coin.', inline = True)
        embed.add_field(name = ':point_right: Me', value = 'Refers to you in third person.', inline = True)
        embed.add_field(name = ':speech_balloon: Quote', value = 'Sends a random quote from online', inline = True)
        embed.add_field(name = ':game_die: Random', value = 'Random number generator', inline = True)
        embed.add_field(name = ':upside_down: Guess', value = 'Play a guess the number game.', inline = True)
        embed.add_field(name = ':signal_strength: Poll', value = "Create a poll on the spot.", inline = True)
        embed.add_field(name = ':laughing: Pun', value = 'Dad jokes galore.', inline = True)
        embed.add_field(name = ':exclamation: Remind', value = 'Reminds you to do something.', inline = True)
        embed.add_field(name = ':laughing: Meme', value = 'Posts a random meme from r/memes', inline = True)
        embed.add_field(name = ':rofl: Dank Meme', value = 'Posts a random meme from r/dankmemes', inline = True)
        embed.set_footer(text = 'Type !help [command] for more info')
    elif cmd.lower() == 'add':

        embed = discord.Embed(colour = discord.Colour.red())
        embed.set_author(name = 'Add')
        embed.add_field(name = '='*36 + '\nSyntax:- !add (lmao what did you expect?)\n'+ '='*36,
                        value = 'Gives the link you need to add this bot to a server.')

    elif cmd.lower() == 'code':

        embed = discord.Embed(colour = discord.Colour.red())
        embed.set_author(name = 'Code')
        embed.add_field(name = '='*36 + '\n!code [Programming language] [code]\n' + '='*36,
                        value = 'Formats the code text in a box along with markdown text and keyword highlighting.')

    elif cmd.lower() == 'face':
        
        embed = discord.Embed(colour = discord.Colour.red())
        embed.set_author(name = 'Face')
        embed.add_field(name = '='*36 + '\n!face\n' + '='*36,
                        value = 'Sends a message of a random face from the internet.')

    elif cmd.lower() == 'flip':

        embed = discord.Embed(colour = discord.Colour.red())
        embed.set_author(name = 'Flip')
        embed.add_field(name = '='*36 + '\n!flip\n' + '='*36,
                        value = 'Flips a coin, simple as that')

    elif cmd.lower() == 'me':

        embed = discord.Embed(colour = discord.Colour.red())
        embed.set_author(name = 'Me')
        embed.add_field(name = '='*36 + '\n!me [text]\n' + '='*36,
                        value = "Refers to you in third person, so '!me snaps' will become 'Thanos snaps")

    elif cmd.lower() == 'quote':

        embed = discord.Embed(colour = discord.Colour.red())
        embed.set_author(name = 'Quote')
        embed.add_field(name = '='*36 + '\n!quote [text]\n' + '='*36,
                        value = 'Quotes the given text in a box')

    elif cmd.lower() == 'pre':

        embed = discord.Embed(colour = discord.Colour.red())
        embed.set_author(name = 'Pre')
        embed.add_field(name = '='*36 + '\n!pre [text]\n' + '='*36, 
                        value = 'Preserves whitespace and sends the text with a primitive font.')

    elif cmd.lower() == 'random':

        embed = discord.Embed(colour = discord.Colour.red())
        embed.set_author(name = 'Random / Roll')   
        embed.add_field(name = '='*36 + '\n!random [number]\n' + '='*36,
                        value = 'Sends a random number from between 1 and the number that you give.')

    elif cmd.lower() == 'say':

        embed = discord.Embed(colour = discord.Colour.red())
        embed.set_author(name = 'Say')
        embed.add_field(name = '='*36 + '\n!say [text]\n' + '='*36,
                        value = 'Well...it makes me say what you want me to say.')

    elif cmd.lower() == 'help':

        embed = discord.Embed(colour = discord.Colour.red())            
        embed.set_author(name = "Why you gotta be THAT guy, huh?")
        embed.add_field(name = 'Walk on home boy.', value = '*snaps*')

    elif cmd.lower() == 'guess':

        embed = discord.Embed(colour = discord.Colour.red())
        embed.set_author(name = 'Guess')
        embed.add_field(name = '='*36 + '\n!guess\n' + '='*36,
                        value = 'Play a simple guess the number game with me.')

    elif cmd.lower() == 'poll':

        embed = discord.Embed(colour = discord.Colour.red())
        embed.set_author(name = 'Poll')
        embed.add_field(name = '='*36 + '\n!poll "question" option1 option2 ...\n' + '='*36,
                        value = 'Creates a poll with options you give.')

    elif cmd.lower() == 'pun':

        embed = discord.Embed(colour = discord.Colour.red())
        embed.set_author(name = 'Pun')
        embed.add_field(name = '='*36 + '\n!pun\n' + '='*36,
                        value = "For the love of god please don't type this command, I beg you.")

    elif cmd.lower() == 'remind':

        embed = discord.Embed(colour = discord.Colour.red())

        embed.set_author(name = 'Remind')
        embed.add_field(name = '='*36 + '\n!remind ["thing to remind"] [time in minutes]\n' + '='*36,
                        value = 'Example: !remind "to do laundry" 30\nSends a DM to you reminding you to do something in the time you give.')

    elif cmd.lower() == 'meme':

        embed = discord.Embed(colour = discord.Colour.red())

        embed.set_author(name = 'Meme')
        embed.add_field(name = '='*36 + '\n!meme\n' + '='*36,
                        value = 'Posts a random meme from r/memes')

    elif cmd.lower() == 'dank meme' or 'dankmeme':

        embed = discord.Embed(colour = discord.Colour.red())

        embed.set_author(name = 'Dank Meme')
        embed.add_field(name = '='*36 + '\n!dankmeme\n' + '='*36,
                        value = 'Posts a random meme from r/dankmemes')


    await ctx.send(ctx.message.author.mention, embed = embed)


client.run(config.token)