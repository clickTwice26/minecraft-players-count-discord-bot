import responses
import discord
import constants
import asyncio
from discord.ext import tasks, commands
from discord.ext.commands import Bot
from discord.ext.commands import Context
from dotenv import load_dotenv

import func
async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        func.debug("Error: {e}", "True")
def run_discord_bot():
    TOKEN = constants.token
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)


    @client.event
    async def on_ready():
        print(f"{client.user} is running")
        status_task.start()
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        func.debug(f"Message log: {username},{channel},{user_message}", "true")
        # print(f"{username} said {user_message} {channel}")
        try:
            if user_message[0] == constants.command_prefix:
                user_message = user_message[1:]
                await send_message(message, user_message, is_private=False)
            else:
                pass
                # await send_message(message, user_message, is_private=False)
        except IndexError:
            func.debug(f"Error: INDEXERROR", "true")
            pass
        except Exception as error:
            func.debug(f"Error: {error}", "true")
    @tasks.loop()
    async def status_task() -> None:
        await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=str(func.playerOnlineCounter())+" Players"))
        await client.change_presence(status=discord.Status.online, activity=discord.Game(f"on {constants.site}"))

        await asyncio.sleep(1)
    client.run(TOKEN)
