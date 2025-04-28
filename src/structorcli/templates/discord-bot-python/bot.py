import discord
from discord.ext import commands

# Replace '!' with your desired bot prefix
bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

# Replace 'YOUR_TOKEN_HERE' with your bot's token
bot.run("YOUR_TOKEN_HERE")
