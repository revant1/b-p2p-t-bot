from telegram import Bot
from dotenv import load_dotenv
import os

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")


async def send_telegram_message(user_id, message, parse_mode="HTML"):
    """
    Sends a Telegram message asynchronously using the python-telegram-bot library.

    :param user_id: Telegram chat ID.
    :param message: Message to send.
    :param parse_mode: Telegram parse mode ('HTML', 'Markdown', etc.).
    """
    try:
        await bot.send_message(
            chat_id=user_id,
            text=message,
            parse_mode=parse_mode,
            disable_web_page_preview=True
        )
    except Exception as e:
        print(f"[send_telegram_message] Error sending message to {user_id}: {e}")


def to_float(s):
    if s is None:
        return None
    else:
        return float(s)


def format_table(data, columns, html=False):
    """
    Formats a 2D list into a string representation of a table.
    Optionally formats the output as HTML with bold column names.

    :param data: A 2D list of data.
    :param columns: A list of column names.
    :param html: Whether to use HTML formatting.
    :return: Formatted table string.
    """
    col_widths = [max(len(str(item)) for item in column_data) for column_data in zip(*data)]
    formatted_rows = []
    for row in data:
        formatted_row = []
        for i, col in enumerate(columns):
            col_name = f"<b>{col}</b>" if html else col
            formatted_item = f"{col_name}: {str(row[i]).ljust(col_widths[i])}"
            formatted_row.append(formatted_item)
        formatted_rows.append(",   ".join(formatted_row))
    return "\n".join(formatted_rows)
