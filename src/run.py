import emoji
from loguru import logger

from src.bot import bot
from src.constants import keyboards


class Bot:

    def __init__(self, telegram_bot):

        self.bot = telegram_bot

        # register handlers
        self.handler()

        # run bot
        logger.info("bot is running...")
        self.bot.infinity_polling()

    def handler(self):

        @self.bot.message_handler(commands=["start"])
        def send_welcome(message):
            self.send_message(
                message.chat.id,
                "welcome to my new bot",
                reply_to_message_id=message.message_id,
                reply_markup=keyboards.main
                )

        @self.bot.message_handler(func=lambda msg: "Settings" in msg.text)
        def setting(message):
            self.send_message(message.chat.id, "you choose settings")

        @self.bot.message_handler(content_types="text")
        def echo(message):
            self.send_message(message.chat.id, message.text)

        @self.bot.message_handler(content_types="photo")
        def image(message):
            self.send_message(message.chat.id, "you send photo")

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


if __name__ == "__main__":
    logger.info("start")
    bot = Bot(bot)
    logger.info("done!")
