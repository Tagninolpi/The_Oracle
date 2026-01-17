import asyncio
import os
import discord
from discord.ext import commands
from aiohttp import web
from dotenv import load_dotenv

# ----------------- CONFIG -----------------
load_dotenv()  # Load .env file if it exists (for local testing)
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")  # Will use Render env if deployed
USE_WEB = os.environ.get("USE_WEB", "False").lower() == "true"  # Manual toggle
PORT = int(os.environ.get("PORT", 5000))  # Render provides PORT env variable
# -----------------------------------------

# ---------- Discord Bot ----------
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=None, intents=discord.Intents.default())

    async def setup_hook(self):
        # Load all cogs
        if os.path.isdir("cogs"):
            for file in os.listdir("cogs"):
                if file.endswith(".py") and not file.startswith("_"):
                    await self.load_extension(f"cogs.{file[:-3]}")
        # Sync slash commands
        await self.tree.sync()
        print("✅ Slash commands synced")

    async def on_ready(self):
        print(f"✅ Logged in as {self.user} ({self.user.id})")

# ---------- Web Server ----------
async def handle(request):
    return web.Response(text="Bot is alive!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    print(f"🌐 Web server running on port {PORT}")

# ---------- Main ----------
async def main():
    bot = Bot()

    if USE_WEB:
        # Start web server in background (needed for Render Web Service)
        await start_web_server()

    async with bot:
        await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
