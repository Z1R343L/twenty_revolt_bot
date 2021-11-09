import logging
from os import getenv
from urllib.parse import urlencode
from base64 import urlsafe_b64encode, urlsafe_b64decode

import uvloop
from aiohttp import ClientSession
import defectio
from defectio.ext import commands
import dill as pickle

uvloop.install()
logging.basicConfig(level=logging.DEBUG)

baseurl = "http://twenty_api:8000/twenty/"

bot = commands.Bot(command_prefix="_")


async def fetch_endpoint(url: str, param: dict = None) -> dict:
    param['agent'] = 'revolt'
    async with ClientSession() as session:
        async with session.get(url + urlencode(param)) as response:
            return await response.json()

async def message_hook(message, ID: str, bot) -> None:
    new_data = pickle.dumps({"channel_id": message.channel.id, "message_id": message.id})
    data = await fetch_endpoint(url=f"{baseurl}set?", param={"id": ID, "prefix": "message", "data": urlsafe_b64encode(new_data)})
    old_data = pickle.loads(urlsafe_b64decode(s=data['old_data']))
    await bot.http.delete_message(channel_id=old_data['channel_id'], message_id=old_data['message_id'])



@bot.command()
async def play(ctx):
    await ctx.message.delete()
    data = await fetch_endpoint(url=f"{baseurl}new_game?", param={"id": ctx.author.id, "name": ctx.author.name})
    message = await ctx.send(f"score: {data['score']}", file=defectio.File(data['image_path']))
    await message_hook(message=message, ID=ctx.author.id, bot=bot)

@bot.command(aliases=["l"])
async def left(ctx):
    await ctx.message.delete()
    data = await fetch_endpoint(url=f"{baseurl}move?", param={"id": ctx.author.id, "action": "left"})
    message = await ctx.send(f"score: {data['score']}", file=defectio.File(data['image_path']))
    await message_hook(message=message, ID=ctx.author.id, bot=bot)



@bot.command(aliases=["r"])
async def right(ctx):
    await ctx.message.delete()
    data = await fetch_endpoint(url=f"{baseurl}move?", param={"id": ctx.author.id, "action": "right"})
    message = await ctx.send(f"score: {data['score']}", file=defectio.File(data['image_path']))
    await message_hook(message=message, id=ctx.author.id, bot=bot)



@bot.command(aliases=["u"])
async def up(ctx):
    await ctx.message.delete()
    data = await fetch_endpoint(url=f"{baseurl}move?", param={"id": ctx.author.id, "action": "up"})
    message = await ctx.send(f"score: {data['score']}", file=defectio.File(data['image_path']))
    await message_hook(message=message, id=ctx.author.id, bot=bot)




@bot.command(aliases=["d"])
async def down(ctx):
    await ctx.message.delete()
    data = await fetch_endpoint(url=f"{baseurl}move?", param={"id": ctx.author.id, "action": "down"})
    message = await ctx.send(f"score: {data['score']}", file=defectio.File(data['image_path']))
    await message_hook(message=message, id=ctx.author.id, bot=bot)



bot.run(getenv("TOKEN"))
