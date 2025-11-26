import discord
#from discord.commands import slash_command
from discord.ext import commands


class ping(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
                    name='ping',
                    description='return bot latency',
                    integration_types={
                        discord.IntegrationType.guild_install,
                        discord.IntegrationType.user_install,
                    })
    async def ping(self, ctx: discord.ApplicationContext):
        await ctx.respond(f"pong! ({self.bot.latency*1000:.2f} ms)")


def setup(bot):
    bot.add_cog(ping(bot))
