import discord
from discord.ext import commands
import requests
import datetime

api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjgyMzI2NmRkLTViMGEtNDc3NS1hNzdkLTA2YjI0ZGIwNmFjMSIsImlhdCI6MTc0MzA5MDY4Mywic3ViIjoiZGV2ZWxvcGVyLzIzOGI1ODVlLWNiOWItZWYwMS0zMjIzLTJkNDNlZjU0YzlhOCIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiNDQuMTkyLjY5Ljg4Il0sInR5cGUiOiJjbGllbnQifV19._ZINh7fuLRUIZqdsHiJ0-ijpEj7j7A2wKtIETF2kSAx5gEJEX0bagr6_Gy62z-rY4eBhJX5XpMB4T-zgsTdINQ"

headers = {
    "Authorization": f"Bearer {api_key}"
}

class bs(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='bs',
        description='Get brawl stars profile by ID',
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        }
    )
    async def bs(self, ctx, player_tag: discord.Option(discord.SlashCommandOptionType.string)):
        
        def get_info(user):
            url = f"https://api.brawlstars.com/v1/players/{user}"
            response = requests.get(url, headers=headers)
            data = response.json()
            name = data["name"]
            icon = data["icon"]["id"]
            trophies = str(data["trophies"])
            vict_3v3 = str(data["3vs3Victories"])
            vict_solo = str(data["soloVictories"])
            vict_duo = str(data["duoVictories"])
            num_brawlers = str(len(data["brawlers"]))
            brawlers = data["brawlers"]
            first_brawler = brawlers[0]["name"]
            latest_brawler = brawlers[-1]["name"]
            highest_trophies = str(data["highestTrophies"])
            favorite_brawler = "None"
            favorite_image = "None" #Sets a default image value

            def find_favorite():
                nonlocal favorite_brawler
                most_trophies = 0
                for brawler in brawlers:
                    trophies = brawler["trophies"]
                    if trophies > int(most_trophies):
                        most_trophies = trophies
                        favorite_brawler = brawler["name"]
                return favorite_brawler
            
            def find_image():
                nonlocal favorite_image
                for brawler in brawlers:
                    if brawler["name"].lower() == favorite_brawler.lower():
                        brawler_id = brawler["id"]
                        favorite_image = f"https://cdn.brawlstats.com/character-models/{brawler_id}.png"
                        break
                return favorite_image
            
            favorite_brawler = find_favorite()
            favorite_image = find_image()
            print(favorite_image)
            return name, icon, trophies, str(highest_trophies), vict_3v3, vict_solo, vict_duo, num_brawlers, first_brawler, latest_brawler, favorite_brawler, favorite_image

        useable_player_tag = player_tag.replace("#", "%23")
        name, icon, trophies, highest_trophies, vict_3v3, vict_solo, vict_duo, num_brawlers, first_brawler, latest_brawler, favorite_brawler, favorite_image = get_info(useable_player_tag)

        embed = discord.Embed(
            title=name,
            url="https://example.com",
            colour=0x11ff00,
            timestamp=datetime.datetime.now()
        )

        embed.set_author(name=player_tag,
                            icon_url=f"https://cdn.brawlstats.com/player-thumbnails/{icon}.png")
        
        embed.add_field(name="Trophies",
                            value="----------------------------------------------------------------",
                            inline=False)
        embed.add_field(name="Current",
                            value="<:bs_trophy:1354857336245846266> " + str(trophies),
                            inline=True)
        embed.add_field(name="Highest",
                            value="<:bs_trophy:1354857336245846266> " + highest_trophies,
                            inline=True)
        embed.add_field(name="Ranked",
                            value="-----------------------------------------------------------------",
                            inline=False)
        embed.add_field(name="Current",
                            value="N/A",
                            inline=True)
        embed.add_field(name="Highest",
                            value="N/A",
                            inline=True)
        embed.add_field(name="Wins",
                            value="-----------------------------------------------------------------",
                            inline=False)
        embed.add_field(name="Solo",
                            value="<:showdown:1354865837974094134> " + vict_solo,
                            inline=True)
        embed.add_field(name="Duo",
                            value="<:duo_showdown:1354865820609806408> " + vict_duo,
                            inline=True)
        embed.add_field(name="3v3",
                            value="<:3v3:1354865804369334292> " + vict_3v3,
                            inline=True)
        embed.add_field(name="Brawlers",
                            value="-----------------------------------------------------------------",
                            inline=False)
        embed.add_field(name="First Brawler",
                            value="<:tier1:1354885763208188095> " + first_brawler,
                            inline=True)
        embed.add_field(name="Latest Brawler",
                            value="<:tiermax:1354886311571361813> " + latest_brawler,
                            inline=True)
        embed.add_field(name="Favorite Brawler",
                            value="<:bs_heart:1354884859755237527> " + favorite_brawler,
                            inline=True)

        embed.set_thumbnail(url=favorite_image)
        
        embed.set_footer(text="Brawl Stars")
        
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(bs(bot))