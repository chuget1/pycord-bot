import discord
from discord.commands import slash_command
from discord.ext import commands
import requests

class background(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @slash_command(
    name='background',
    description='remove background from an image',
    integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        }
    )
    async def background(self, ctx, url: discord.Option(discord.SlashCommandOptionType.string)):

        

        
        
        def remove_background(image_url):
            try:
                api_key = "FrV8nfqT6KSJSLmXjeBn5tRr"
                api_url = "https://api.remove.bg/v1.0/removebg"
                response = requests.post(api_url, data={'image_url': image_url}, headers={'X-Api-Key': api_key})
                if response.status_code == 200:
                    with open("output.png", "wb") as f:
                        f.write(response.content)
                    return "output.png", None
                else:
                    return None, f"Failed to remove background. Status code: {response.status_code}"
            except requests.exceptions.RequestException as e:
                return None, f"Error removing background: {e}"
        response = url
        output_image, error_message = remove_background(response)

        if output_image:
            await ctx.respond(file=discord.File(output_image))
        else:
            await ctx.respond(error_message)

def setup(bot):
    bot.add_cog(background(bot))
