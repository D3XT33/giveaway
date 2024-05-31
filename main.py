import os
import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
import datetime

# Ładowanie zmiennych środowiskowych z pliku .env
load_dotenv()
TOKEN = os.getenv("token")

# Inicjalizacja intents
intents = discord.Intents.default()
intents.message_content = True  # Włączenie dostępu do treści wiadomości
intents.members = True  # Włączenie dostępu do członków

# Utworzenie obiektu bot z odpowiednimi intents
bot = commands.Bot(command_prefix=">", case_sensitive=False, intents=intents)
bot.remove_command("help")

@bot.event
async def on_ready():
    print("Bot logged in")
    # Nie zmieniaj statusu tutaj, aby unikać banowania IP przez Discord.

@bot.command()
@commands.has_permissions(administrator=True)
async def giveaway(ctx, winner: discord.Member, duration_hours: float, *, message: str):
    await ctx.message.delete()
    UTC_now = datetime.datetime.utcnow()
    int_dur = int(duration_hours)  # Konwersja na int
    dur_seconds = int_dur * 3600  # Konwersja godzin na sekundy
    giveaway_embed = discord.Embed(title=f"`🎉` Giveaway na {message}")
    giveaway_embed.description = (
        f"**Kliknij w emotke :tada: aby dolaczyc do giveaway, kończy się za {duration_hours} godzin.**"

        f"                                                                                __Ten konkurs rozpoczął się {UTC_now.year}-{UTC_now.month}-{UTC_now.day} "
        f"{UTC_now.hour}:{UTC_now.minute}__"
    )
    gw_msg = await ctx.send(embed=giveaway_embed)
    await gw_msg.add_reaction("🎉")
    await asyncio.sleep(dur_seconds)
    winner_embed = discord.Embed(title="`🎉` Giveaway sie zakonczyl", description=f"<@{winner.id}> **Wygral: {message} Gratulacje!**")
    await ctx.send(f"<@{winner.id}>", embed=winner_embed)

# Uruchomienie bota
bot.run(TOKEN)
