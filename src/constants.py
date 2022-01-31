from types import SimpleNamespace

import emoji

from src.utils.keyboard import create_keyboard


keys = SimpleNamespace(
    setting=emoji.emojize(":gear: Settings"),
    exit=emoji.emojize(":cross_mark: Exit")
    )

keyboards = SimpleNamespace(
    main=create_keyboard(keys.setting, keys.exit)
)