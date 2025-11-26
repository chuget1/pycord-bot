import discord
from discord.ext import commands

class Caleb(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
                            name='caleb',
                            description='Ping a specific member',
                            integration_types={
                                discord.IntegrationType.guild_install,
                                discord.IntegrationType.user_install,
                            }
                            )
    async def caleb(self, ctx, member: discord.Member, num: int):
        if ctx.author.id != 695659304774139945:
            await ctx.respond("no")
        else:
            for i in range(num):
                await ctx.respond(member.mention)

def setup(bot):
    bot.add_cog(Caleb(bot))
