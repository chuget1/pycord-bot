import discord
import asyncio
import os
from dotenv import load_env


bot = discord.Bot(
    intents=discord.Intents.all(),
    integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install},
    allowed_contexts={discord.InteractionContextType.guild, discord.InteractionContextType.bot_dm, discord.InteractionContextType.private_channel},
)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    while True:
        await bot.change_presence(activity=discord.Game(name="with petibors toes"))
        await asyncio.sleep(60)


extensions = [# load cogs
    'cogs.ping',
    'cogs.avatar',
    'cogs.background',
    'cogs.caleb',
    'cogs.hello',
    'cogs.bs',
    'cogs.riodejaneiro',
    'cogs.tictactoe',
]

if __name__ == '__main__': # import cogs from cogs folder
    for extension in extensions:
        bot.load_extension(extension)
        print(extension)

bot.run("secret")  # bot token