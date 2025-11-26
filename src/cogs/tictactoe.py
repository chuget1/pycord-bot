import discord
from discord.ext import commands
zero_width_space = "\u200b"

turn = "x"

spaces = [
    '0', '1', '2',
    '3', '4', '5',
    '6', '7', '8',
]

def show_board():
    print(spaces[0:3])
    print(spaces[3:6])
    print(spaces[6:9])

row_one = str(spaces[0:3])
row_two = str(spaces[3:6])
row_three = str(spaces[6:9])



class MyView(discord.ui.View): # Create a class called MyView that subclasses discord.ui.View
    @discord.ui.button(label="Click me!", style=discord.ButtonStyle.primary, emoji="😎") # Create a button with the label "😎 Click me!" with color Blurple
    async def button_callback(self, button, interaction):
        await self.disable



class tictactoe(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='tictactoe',
        description='Play tic tac toe with a member'
    )
    async def tictactoe(self, ctx, member: discord.Member):
        
        await ctx.respond(self, row_one + "\n" + row_two + "\n" + row_three, view=MyView)

        # Buttons with zero-width space as initial label
         # This is the zero-width space
        

def setup(bot):
    bot.add_cog(tictactoe(bot))