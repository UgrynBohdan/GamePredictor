from loguru import logger
import os
import sys

def setup_logging():
    logger.remove() # Видаляємо дефолтний обробник

    # Налаштування для консолі
    logger.add(
        sys.stderr,
        level=os.environ.get("LOG_LEVEL_CONSOLE", "INFO"), # Рівень з ENV або INFO
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        backtrace=True,
        diagnose=True
    )

    # Налаштування для файлу
    # logger.add(
    #     os.environ.get("LOG_FILE_PATH", "app.log"), # Шлях до файлу з ENV або app.log
    #     rotation="10 MB",
    #     compression="zip",
    #     level=os.environ.get("LOG_LEVEL_FILE", "DEBUG"), # Рівень з ENV або DEBUG
    #     format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
    #     backtrace=True,
    #     diagnose=True
    # )

setup_logging() # Викликаємо налаштування при імпорті цього модуля