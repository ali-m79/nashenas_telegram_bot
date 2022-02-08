import emoji
from telebot import custom_filters
from loguru import logger

from src.bot import bot
from src.constants import keyboards, keys, states
from src.db import db


class Bot:
    """
    Telegram bot to connect two stranger people randomly.
    """
    def __init__(self, telegram_bot, mongodb):
        """
        Initialize bot, custom filters, handelers
        """
        self.bot = telegram_bot
        self.db = mongodb

        # add custom filters
        self.bot.add_custom_filter(custom_filters.TextMatchFilter())

        # register handlers
        self.handler()

        # run bot
        logger.info("bot is running...")
        self.bot.infinity_polling()

    def handler(self):

        @self.bot.message_handler(commands=["start"])
        def start(message):
            """
            start command handler
            """
            self.send_message(
                message.chat.id,
                f"hey, **{message.chat.first_name}** welcome to Bot",
                reply_to_message_id=message.message_id,
                reply_markup=keyboards.main
                )
            self.db.users.update_one(
                {"chat.id": message.chat.id},
                {"$set": message.json},
                upsert=True
            )
            self.update_state(message.chat.id, states.main)

        @self.bot.message_handler(text=[keys.random_connect])
        def random_connect(message):
            """
            randomly connect to another user
            """

            # update states to random connect
            self.send_message(
                message.chat.id,
                ":busts_in_silhouette: Connecting to a random stranger....",
                reply_markup=keyboards.exit
                )
            self.update_state(message.chat.id, states.random_connect)

            # find other user to connect
            other_user = self.db.users.find_one(
                {
                    "state": states.random_connect,
                    "chat.id": {"$ne": message.chat.id}
                }
            )

            if not other_user:
                return

            # update other user state
            self.update_state(other_user["chat"]["id"], states.connected)
            self.send_message(
                other_user["chat"]["id"],
                f"Connected to {message.chat.id} ....",
            )

            # update current user state
            self.update_state(message.chat.id, states.connected)
            self.send_message(
                message.chat.id,
                f"Connected to {other_user['chat']['id']} ....",
            )

            # store connected users
            self.db.users.update_one(
                {"chat.id": message.chat.id},
                {"$set": {"connected_to": other_user["chat"]["id"]}}
            )

            self.db.users.update_one(
                {"chat.id": other_user["chat"]["id"]},
                {"$set": {"connected_to": message.chat.id}}
            )

        @self.bot.message_handler(text=[keys.exit])
        def exit(message):
            """
            exit from chat or connecting state
            """
            # update current user state
            self.send_message(
                message.chat.id,
                keys.exit,
                reply_markup=keyboards.main,
                )
            self.update_state(message.chat.id, states.main)

            # find other connected user
            user = self.db.users.find_one(
                {"chat.id": message.chat.id}
            )
            if not user.get("connected_to"):
                return
            other_chat_id = user["connected_to"]

            # update other user state and terminate the connection
            self.send_message(
                other_chat_id,
                keys.exit,
                reply_markup=keyboards.main,
                )
            self.update_state(other_chat_id, states.main)

            # remove connected user
            self.db.users.update_one(
                {"chat.id": message.chat.id},
                {"$set": {"connected_to": None}}
                )
            self.db.users.update_one(
                {"chat.id": other_chat_id},
                {"$set": {"connected_to": None}}
                )

        @self.bot.message_handler(content_types="text")
        def echo(message):
            """
            echo messages to other connected user
            """
            # check the connection
            user = self.db.users.find_one({"chat.id": message.chat.id})
            if (not user) or (user["state"] != states.connected) or \
                    (user["connected_to"] is None):
                return

            self.send_message(user["connected_to"], message.text)

    def send_message(
        self,
        chat_id, text,
        reply_markup=None,
        emojize=True,
        reply_to_message_id=None,
    ):
        """
        send message to telegram bot.
        """
        if emojize:
            text = emoji.emojize(text)

        self.bot.send_message(
            chat_id,
            text,
            reply_markup=reply_markup,
            reply_to_message_id=reply_to_message_id,
            )

    def update_state(self, chat_id, state):
        """
        Update user state.
        """
        self.db.users.update_one(
            {"chat.id": chat_id},
            {"$set": {"state": state}},
        )


if __name__ == "__main__":
    logger.info("start")
    nashenas_bot = Bot(telegram_bot=bot, mongodb=db)
    logger.info("done!")
