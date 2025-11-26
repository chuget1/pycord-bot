import discord
from discord.commands import slash_command, SlashCommandGroup
from discord.ext import commands
import requests
import re

class Roblox(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    roblox = SlashCommandGroup(
        "roblox",
        "Roblox related commands",
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        }
        )

    def fetch_user_id(self, name):
        response = requests.get(f'https://www.roblox.com/users/profile?username={name}')
        if not response.ok:
            return 7207597985
        user_id = re.search(r'\d+', response.url).group(0)
        return user_id

    def fetch_avatar_url(self, user_id):
        try:
            url = f"https://thumbnails.roblox.com/v1/users/avatar?userIds={user_id}&size=720x720&format=Png&isCircular=false"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return data['data'][0]['imageUrl']
            else:
                return None
        except requests.exceptions.RequestException as e:
            print("Error fetching avatar URL:", e)
            return None

    def fetch_username(self, user_id):
        try:
            response = requests.get(f"https://users.roblox.com/v1/users/{user_id}")
            if response.status_code == 200:
                user_data = response.json()
                return user_data.get('displayName')
            else:
                return None
        except requests.exceptions.RequestException as e:
            print("Error fetching username:", e)
            return None

    def fetch_description(self, user_id):
        try:
            response = requests.get(f"https://users.roblox.com/v1/users/{user_id}")
            if response.status_code == 200:
                user_data = response.json()
                return user_data.get('description')
            else:
                return None
        except requests.exceptions.RequestException as e:
            print("Error fetching username:", e)
            return None

    def construct_item_url(self, asset_id):
        base_url = "https://www.roblox.com/catalog/"
        return f"{base_url}{asset_id}/"

    def fetch_item_name(self, asset_id):
        try:
            response = requests.get(f"https://catalog.roblox.com/v1/catalog/items/{asset_id}/details")
            if response.status_code == 200:
                item_data = response.json()
                return item_data.get('name')
            else:
                return f"Item {asset_id}"
        except requests.exceptions.RequestException as e:
            print(f"Error fetching item name for {asset_id}:", e)
            return f"Item {asset_id}"

    @roblox.command(
        name='avatar',
        description='Get avatar items of a user',
    )
    async def avatar(self, ctx, username: discord.Option(discord.SlashCommandOptionType.string)):
        user_id = self.fetch_user_id(username)
        avatar_url = self.fetch_avatar_url(user_id)
        username_display = self.fetch_username(user_id)
        desc = self.fetch_description(user_id)

        r = requests.get(f"https://avatar.roblox.com/v1/users/{user_id}/currently-wearing")
        if r.status_code == 200:
            json_data = r.json()
            asset_ids = json_data['assetIds']
            item_links = []
            for asset_id in asset_ids:
                item_url = self.construct_item_url(asset_id)
                item_name = self.fetch_item_name(asset_id)
                item_links.append(f"[{item_name}]({item_url})")

            embed = discord.Embed(
                title=username_display,
                description=desc,
                color=discord.Colour.nitro_pink(),
            )
            embed.add_field(name="Equipped avatar items:", value="\n".join(item_links))
            embed.set_thumbnail(url=avatar_url)
            await ctx.respond(embed=embed)
        else:
            await ctx.respond("Could not find the user's avatar items.")

    @roblox.command(
        name='portrait',
        description='Display a large avatar picture of a user',
    )
    async def portrait(self, ctx, username: discord.Option(discord.SlashCommandOptionType.string)):
        user_id = self.fetch_user_id(username)
        avatar_url = self.fetch_avatar_url(user_id)
        username_display = self.fetch_username(user_id)

        if avatar_url:
            embed = discord.Embed(
                title=f"{username_display}'s Avatar",
                color=discord.Colour.blue()
            )
            embed.set_image(url=avatar_url)
            await ctx.respond(embed=embed)
        else:
            await ctx.respond("Could not fetch the user's avatar.")

def setup(bot):
    bot.add_cog(Roblox(bot))