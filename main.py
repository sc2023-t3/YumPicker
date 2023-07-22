import logging
import os
from importlib import import_module

from colorlog import ColoredFormatter
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application


def list_modules(directory: str) -> list[str]:
    """
    List all modules in a directory
    :param directory: The directory to list modules in
    :return: A list of modules
    """
    file_list = []

    for root, _, files in os.walk(directory):
        for file in files:
            relative_path = os.path.relpath(os.path.join(root, file), directory)
            dotted_path = os.path.splitext(relative_path)[0].replace(os.path.sep, '.')
            file_list.append(dotted_path)

    return file_list


def load_extension(application: Application, name: str) -> None:
    """
    Load an extension
    :param application: The application to load the extension in
    :param name: The name of the extension
    :return: None
    """
    module = import_module(name)

    module.setup(application)


def load_extensions_in(application: Application, package: str):
    """
    Load all extensions in a directory
    :param application: The application to load extensions in
    :param package: The package to load extensions from
    :return: None
    """
    for file in list_modules(package):
        load_extension(application, f"{package}.{file}")


def setup_logging() -> None:
    """
    Set up the loggings for the bot
    :return: None
    """
    formatter = ColoredFormatter(
        '%(asctime)s %(log_color)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'white',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(filename="concept.log", encoding="utf-8", mode="w")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logging.basicConfig(
        handlers=[stream_handler, file_handler], level=logging.INFO
    )


def main() -> None:
    load_dotenv()

    setup_logging()

    application = Application.builder().token(os.getenv("TELEGRAM_TOKEN")).build()

    load_extensions_in(application, "extensions")

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
