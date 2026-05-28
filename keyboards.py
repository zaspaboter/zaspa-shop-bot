from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🛒 Магазин"),
            KeyboardButton(text="👤 Профиль")
        ],
        [
            KeyboardButton(text="🏆 Топ"),
            KeyboardButton(text="👥 Пригласить")
        ]
    ],
    resize_keyboard=True
)

shop_kb = InlineKeyboardMarkup(
    inline_keyboard=[

        [
            InlineKeyboardButton(
                text="TikTok подписка — 1 монета",
                callback_data="buy_tiktok"
            )
        ],

        [
            InlineKeyboardButton(
                text="Аватарка — 1 монета",
                callback_data="buy_avatar"
            )
        ],

        [
            InlineKeyboardButton(
                text="Лайк + репост — 1 монета",
                callback_data="buy_like"
            )
        ],

        [
            InlineKeyboardButton(
                text="ZIP файл — 2 монеты",
                callback_data="buy_zip"
            )
        ],

        [
            InlineKeyboardButton(
                text="Тутор на ВД — 2 монеты",
                callback_data="buy_tutor"
            )
        ],

        [
            InlineKeyboardButton(
                text="Приписка в чате — 2 монеты",
                callback_data="buy_prefix"
            )
        ],

        [
            InlineKeyboardButton(
                text="ВД от zaspa — 3 монеты",
                callback_data="buy_vd"
            )
        ],

        [
            InlineKeyboardButton(
                text="Голосовое приветствие — 5 монет",
                callback_data="buy_voice"
            )
        ],

        [
            InlineKeyboardButton(
                text="NodeVideo Pro Android — 6 монет",
                callback_data="buy_node"
            )
        ],

        [
            InlineKeyboardButton(
                text="Приват от zaspa — 12 монет",
                callback_data="buy_private"
            )
        ]
    ]
)
