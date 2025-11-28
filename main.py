import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.guild_messages = True
intents.guild_reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Botcito04 conectado como: {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Slash commands sincronizados: {len(synced)}")
    except Exception as e:
        print(f"Error al sincronizar slash commands: {e}")

async def load_cogs():
    await bot.load_extension("cogs.welcome")
    await bot.load_extension("cogs.autoroles")
    await bot.load_extension("cogs.levels")
    await bot.load_extension("cogs.economia")
    await bot.load_extension("cogs.moderacion")
    await bot.load_extension("cogs.anuncios")
    await bot.load_extension("cogs.anuncios_admin_auto")
    await bot.load_extension("cogs.confesar")
    await bot.load_extension("cogs.sugerencias")
    await bot.load_extension("cogs.logs")

asyncio.run(load_cogs())

bot.run(TOKEN)