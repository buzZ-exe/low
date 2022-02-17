import discord, praw, cogs.config as config
from discord.ext import commands
from random import randint


reddit = praw.Reddit(client_id = config.client_id,
                    client_secret = config.client_secret,
                    user_agent = config.client_agent)


class redditCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(aliases = ['pun'],
                        description = 'Sends a cheesy old pun back',
                        brief = 'Dad joke galore')
    async def Pun(self, ctx):
        joke = reddit.subreddit('dadjokes').hot()
        joke_post = randint(1, 50)
        for i in range(0, joke_post):
            submission = next(x for x in joke if x.stickied == False)

        embed = discord.Embed(colour = discord.Colour.red())
        embed.add_field(name = submission.title, value = submission.selftext)
        embed.set_footer(text = 'Thank you, r/dadjokes')

        await ctx.send(embed = embed)




    @commands.command(aliases = ['darkjoke', 'djoke', 'dj'])
    async def Darkjoke(self, ctx):
        joke = reddit.subreddit('darkjokes').hot()
        joke_post = randint(1, 50)
        for i in range(0, joke_post):
            submission = next(x for x in joke if x.stickied == False)
        embed = discord.Embed(colour = discord.Colour.red())
        embed.add_field(name = submission.title, value = submission.selftext)
        embed.set_footer(text = 'Thank you, r/darkjokes')

        await ctx.send(embed = embed)




    @commands.command(pass_context = True)
    async def meme(self, ctx):
        meme = reddit.subreddit('memes').hot()
        meme_post = randint(1, 50)
        for i in range(0, meme_post):
            submission = next(x for x in meme if x.stickied == False)

        embed = discord.Embed(colour = discord.Colour.red())
        embed.set_image(url = submission.url)
        embed.set_footer(text = "Thank you, r/memes")

        await ctx.send(embed = embed)




    @commands.command(aliases = ['dm'],
                    pass_context = True)
    async def dankmeme(self, ctx):
        meme = reddit.subreddit('dankmemes').hot()
        meme_post = randint(1, 50)
        for i in range(0, meme_post):
            submission = next(x for x in meme if not x.stickied)

        embed = discord.Embed(colour = discord.Colour.red())
        embed.set_image(url = submission.url)
        embed.set_footer(text = "Thank you, r/dankmemes")

        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(redditCommands(bot))