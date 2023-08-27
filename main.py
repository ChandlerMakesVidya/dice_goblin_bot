import discord
from discord.ext import commands
import operator
import json
import rolldice

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
config_file = open('config.json')
config = json.load(config_file)

initiative_order = {}


@bot.command(name='helpme')
async def helpme(ctx):
    await ctx.send('NO ONE COMING TO HELP')


@bot.command(name='init')
async def initiative(ctx, *args):
    if args[0] == "order":
        await ctx.send('HERE IS INITIATIVE ORDER')
        sorted_initiative_order = dict(
            sorted(initiative_order.items(), key=operator.itemgetter(1), reverse=True))
        init_order_string = ""
        for i in sorted_initiative_order:
            init_order_string += f'{i}: {sorted_initiative_order[i]}\n'
        await ctx.send(init_order_string)
        return
    if args[0] == 'reset':
        initiative_order.clear()
        await ctx.send('INITIATIVE RESET')
        return

    if len(args) < 1:
        await ctx.send('PUT SOMETHING IN DUMBASS')
        return
    number = args[0]
    if not number.isdigit():
        await ctx.send(f'{number} IS NOT NUMBER DUMBASS')
        return
    number = int(number)
    name = ctx.author if len(args) < 2 else ' '.join(args[1:])
    initiative_order[name] = number
    await ctx.send(f'ADDED {name} at position {number}')


@bot.command(name='roll')
async def roll(ctx, *args):
    if len(args) < 1:
        await ctx.send('ROLL WHAT?')
        return
    result, explanation = rolldice.roll_dice(''.join(args))
    await ctx.send(f'YOU ROLLED {result} FROM {explanation}')

bot.run(config['token'])
