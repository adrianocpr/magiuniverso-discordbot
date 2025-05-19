
import logging
import os

def setup_logger():
    if not os.path.exists("logs"):
        os.makedirs("logs")

    logger = logging.getLogger("discord_bot")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(filename="logs/bot.log", encoding="utf-8", mode="a")
    formatter = logging.Formatter("[%(asctime)s] [%(levelname)8s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
