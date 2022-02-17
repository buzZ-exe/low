import discord
from discord.ext import commands

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def help(self, ctx, cmd = None):

        if cmd == None:           #This is where i wish python had a switch statement 

            embed = discord.Embed(colour = discord.Colour.red())

            embed.set_author(name = 'HELP HAS ARRIVED')
            embed.add_field(name = ':+1: Add', value = 'Sends the link you need to add this bot.', inline = True)
            embed.add_field(name = ':face_with_raised_eyebrow: Face', value = 'Sends a face ( ͡° ͜ʖ ͡°)', inline = True)
            embed.add_field(name = ':arrows_counterclockwise: Flip', value = 'Flips a coin.', inline = True)
            embed.add_field(name = ':point_right: Reaction', value = 'Measures your reaction time', inline = True)
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

        elif cmd.lower() == 'reaction':

            embed = discord.Embed(colour = discord.Colour.red())
            embed.set_author(name = 'Reaction')
            embed.add_field(name = '='*36 + '\n!reaction\n' + '='*36,
                            value = "Measures your reaction time(highly inaccurate)")

        elif cmd.lower() == 'quote':

            embed = discord.Embed(colour = discord.Colour.red())
            embed.set_author(name = 'Quote')
            embed.add_field(name = '='*36 + '\n!quote [text]\n' + '='*36,
                            value = 'Gives a random quote from the internet.')

        elif cmd.lower() == 'random':

            embed = discord.Embed(colour = discord.Colour.red())
            embed.set_author(name = 'Random / Roll')   
            embed.add_field(name = '='*36 + '\n!random [number]\n' + '='*36,
                            value = 'Sends a random number from between 1 and the number that you give.')

        elif cmd.lower() == 'help':

            embed = discord.Embed(colour = discord.Colour.red())            
            embed.set_author(name = "I see you're the sigma male of the group")
            embed.add_field(name = 'Congrats.', value = '*claps*')

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

def setup(bot):
    bot.add_cog(HelpCommand(bot))