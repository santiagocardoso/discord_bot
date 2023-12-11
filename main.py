import bot
import asyncio

if __name__ == "__main__":
    bot_instance, token = asyncio.run(bot.run_discord_bot())
    asyncio.run(bot_instance.start(token))
