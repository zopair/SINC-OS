"""Optional Telegram entry point for the SINC-OS OrbitX bot."""

from __future__ import annotations

import argparse
import os


def build_bot(token: str):
    """Create the Telegram bot, rejecting missing credentials explicitly."""
    if not token or not token.strip():
        raise ValueError("TELEGRAM_BOT_TOKEN is required to start OrbitX.")

    try:
        import telebot
    except ImportError as exc:
        raise RuntimeError("Install project dependencies with: pip install -r requirements.txt") from exc

    bot = telebot.TeleBot(token.strip())

    @bot.message_handler(commands=["start"])
    def start(message):
        bot.reply_to(message, "OrbitX is online.")

    return bot


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the optional SINC-OS Telegram bot.")
    parser.add_argument("--check", action="store_true", help="Validate imports without starting polling.")
    args = parser.parse_args()

    if args.check:
        import telebot  # noqa: F401
        print("OrbitX dependencies are available.")
        return 0

    bot = build_bot(os.getenv("TELEGRAM_BOT_TOKEN", ""))
    print("OrbitX Telegram bot is starting.")
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
