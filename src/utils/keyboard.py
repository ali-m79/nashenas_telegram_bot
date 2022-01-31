import emoji
from telebot import types


def create_keyboard(*keys, row_width=2, resize_keyboard=True):
    """
    create a keyboard from a list of keys.

    Examples:
        keys = ["a", "b", "c"]
    """
    markup = types.ReplyKeyboardMarkup(
        row_width=row_width,
        resize_keyboard=resize_keyboard,
        )
    keys = map(emoji.emojize, keys)
    buttons = map(types.KeyboardButton, keys)
    markup.add(*buttons)

    return markup
