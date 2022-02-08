from types import SimpleNamespace

import emoji

from src.utils.keyboard import create_keyboard


keys = SimpleNamespace(
    random_connect=emoji.emojize(":bust_in_silhouette: Random Connect"),
    setting=emoji.emojize(":gear: Settings"),
    exit=emoji.emojize(":cross_mark: Exit")
    )

keyboards = SimpleNamespace(
    main=create_keyboard(keys.random_connect),
    exit=create_keyboard(keys.exit)
)

states = SimpleNamespace(
    random_connect="RANDOM_CONNECT",
    main="MAIN",
    connected="CONNECTED",
)
