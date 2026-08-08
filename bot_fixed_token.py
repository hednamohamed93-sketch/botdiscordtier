"""AllTiers Discord bot entrypoint.

Registers slash commands per-guild (instant availability, no global command
propagation delay) on ready and whenever the bot joins a new guild.
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

import discord
from discord.ext import commands
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent))

from database.db import close_pool, init_pool  # noqa: E402

load_dotenv()

LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_DIR / "bot.log"),
    ],
)
logger = logging.getLogger("alltiers.bot")

intents = discord.Intents.default()
# Only the default (unprivileged) intents are needed -- no message content or
# member intents required for slash commands, buttons, and embeds.

bot = commands.Bot(command_prefix="!", intents=intents)


async def _sync_commands_for_guild(guild: discord.Guild) -> None:
    """Copy the globally-declared commands into this guild's command tree and
    sync just that guild, so slash commands appear instantly (seconds) instead
    of waiting for global propagation (up to ~1 hour)."""
    try:
        bot.tree.copy_global_to(guild=guild)
        synced = await bot.tree.sync(guild=guild)
        logger.info("Synced %d commands for guild %s", len(synced), guild.id)
    except Exception:
        logger.exception("Failed to sync commands for guild %s", guild.id)


@bot.event
async def on_ready() -> None:
    logger.info("Logged in as %s", bot.user)

    for guild in bot.guilds:
        await _sync_commands_for_guild(guild)


@bot.event
async def on_guild_join(guild: discord.Guild) -> None:
    await _sync_commands_for_guild(guild)


async def main() -> None:
    token = os.environ.get("MTUzNTc1MTM3OTU0NzU5NDg2NA.G6fLd9.qKFtA1PE1ZtB45FA7WNbT16XAW9PV62DHvhmhY")
    if not token:
        logger.error(
            "DISCORD_BOT_TOKEN is not set -- the bot cannot start. "
            "Add it via Replit Secrets."
        )
        return

    try:
        await init_pool()
    except Exception:
        logger.exception(
            "Failed to initialize the database pool -- the bot cannot start."
        )
        return

    try:
        async with bot:
            await bot.load_extension("cogs.queue_cog")
            await bot.load_extension("cogs.testing_cog")
            await bot.start(token)
    finally:
        await close_pool()


if __name__ == "__main__":
    asyncio.run(main())
