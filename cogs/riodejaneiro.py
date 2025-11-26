import discord
from discord.commands import slash_command
from discord.ext import commands
import requests
from PIL import Image
import io  # Import the io module

class riodejaneiro(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        name='riodejaneiro',
        description='add Rio de Janeiro filter to an image',
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        }
    )
    async def riodejaneiro(self, ctx, image: discord.Attachment):

        try:
            # Download the image data
            image_bytes = await image.read()

            # Open the image from the downloaded bytes
            img = Image.open(io.BytesIO(image_bytes))

            overlay = Image.open("images/rio.png")

            overlay = overlay.resize(img.size)

            img.paste(overlay, (0, 0), overlay)

            img.save("output.png")

            await ctx.respond(file=discord.File("output.png"))

        except Exception as e:
            await ctx.respond(f"Oops! Something went wrong: {e}")

def setup(bot):
    bot.add_cog(riodejaneiro(bot))