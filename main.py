import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.client.default import DefaultBotProperties

from config import (
    TOKEN,
    ADMIN_ID,
    CHANNEL_ID,
    CHANNEL_LINK,
    BOT_USERNAME
)

from database import (
    add_user,
    get_user,
    get_top_users,
    create_order,
    get_order,
    update_order_status,
    add_coins,
    remove_coins
)

from keyboards import menu, shop_kb


bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()


SHOP_ITEMS = {
    "buy_tiktok": ("Подписка TikTok от zaspa", 1),
    "buy_avatar": ("Аватарка от zaspa", 1),
    "buy_like": ("Лайк + репост видео от zaspa", 1),
    "buy_zip": ("ZIP файл от zaspa", 2),
    "buy_tutor": ("Тутор на ВД от zaspa", 2),
    "buy_prefix": ("Приписка в чате от zaspa", 2),
    "buy_vd": ("ВД от zaspa", 3),
    "buy_voice": ("Голосовое приветствие от zaspa", 5),
    "buy_node": ("NodeVideo Pro Android", 6),
    "buy_private": ("Приват от zaspa", 12)
}


async def check_user_subscription(user_id: int) -> bool:

    try:

        chat_member = await bot.get_chat_member(
            chat_id=CHANNEL_ID,
            user_id=user_id
        )

        if chat_member.status == "member":
            return True

        if chat_member.status == "administrator":
            return True

        if chat_member.status == "creator":
            return True

        return False

    except Exception as error:
        print("Ошибка проверки подписки:", error)
        return False


@dp.message(F.text.startswith("/start"))
async def start_handler(message: Message):

    user_id = message.from_user.id
    username = message.from_user.username

    arguments = message.text.split()

    invited_by = None

    if len(arguments) > 1:
        try:
            invited_by = int(arguments[1])
        except Exception:
            invited_by = None

    if invited_by == user_id:
        invited_by = None

    is_subscribed = await check_user_subscription(user_id)

    if is_subscribed is False:

        subscribe_button = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📢 Подписаться на канал",
                        url=CHANNEL_LINK
                    )
                ]
            ]
        )

        await message.answer(
            "❌ Вы не подписаны на канал.\n"
            "Подпишитесь, чтобы использовать бота.",
            reply_markup=subscribe_button
        )

        return

    add_user(user_id, username, invited_by)

    await message.answer(
        "🔥 Добро пожаловать в магазин zaspa!\n\n"
        "👥 Приглашай друзей и получай 1 монету\n"
        "🛒 Покупай товары в магазине\n"
        "💰 Используй монеты внутри бота",
        reply_markup=menu
    )


@dp.message(F.text == "👤 Профиль")
async def profile_handler(message: Message):

    user = get_user(message.from_user.id)

    if user is None:
        await message.answer("❌ Пользователь не найден в базе данных.")
        return

    top_users = get_top_users()

    user_position = "Нет в топе"

    position_counter = 1

    for top_user in top_users:

        username = top_user[0]

        if username == user[1]:
            user_position = position_counter

        position_counter = position_counter + 1

    profile_text = (
        "👤 Профиль пользователя\n\n"
        f"🆔 ID: {user[0]}\n"
        f"👤 Username: @{user[1]}\n"
        f"💰 Баланс монет: {user[2]}\n"
        f"👥 Приглашено друзей: {user[4]}\n"
        f"🏆 Позиция в топе: {user_position}"
    )

    await message.answer(profile_text)


@dp.message(F.text == "🏆 Топ")
async def top_handler(message: Message):

    top_users = get_top_users()

    text = "🏆 ТОП 10 пользователей по приглашениям\n\n"

    position = 1

    for user in top_users:

        username = user[0]
        invited_count = user[1]

        text = text + str(position) + ". @" + str(username) + " — " + str(invited_count) + " друзей\n"

        position = position + 1

    await message.answer(text)


@dp.message(F.text == "👥 Пригласить")
async def invite_handler(message: Message):

    referral_link = "https://t.me/" + BOT_USERNAME + "?start=" + str(message.from_user.id)

    text = (
        "👥 Ваша реферальная ссылка:\n\n"
        + referral_link +
        "\n\n💰 За каждого друга вы получаете 1 монету"
    )

    await message.answer(text)


@dp.message(F.text == "🛒 Магазин")
async def shop_handler(message: Message):

    await message.answer(
        "🛒 Магазин товаров от zaspa\n"
        "Выберите товар ниже:",
        reply_markup=shop_kb
    )


@dp.callback_query(F.data.startswith("buy_"))
async def buy_handler(callback: CallbackQuery):

    user = get_user(callback.from_user.id)

    if user is None:
        await callback.answer("Ошибка пользователя", show_alert=True)
        return

    item_key = callback.data

    if item_key not in SHOP_ITEMS:
        await callback.answer("Товар не найден", show_alert=True)
        return

    item_name = SHOP_ITEMS[item_key][0]
    item_price = SHOP_ITEMS[item_key][1]

    if user[2] < item_price:
        await callback.answer("❌ Недостаточно монет", show_alert=True)
        return

    remove_coins(callback.from_user.id, item_price)

    order_id = create_order(
        callback.from_user.id,
        item_name,
        item_price
    )

    admin_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Выполнить заказ",
                    callback_data="done_" + str(order_id)
                )
            ],
            [
                InlineKeyboardButton(
                    text="❌ Отказать в заказе",
                    callback_data="cancel_" + str(order_id)
                )
            ]
        ]
    )

    await bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            "🛒 Новый заказ\n\n"
            "🆔 ID заказа: " + str(order_id) + "\n"
            "👤 Пользователь: @" + str(callback.from_user.username) + "\n"
            "📦 Товар: " + item_name + "\n"
            "💰 Цена: " + str(item_price) + " монет"
        ),
        reply_markup=admin_keyboard
    )

    await callback.message.answer(
        "✅ Ваш заказ создан!\n"
        "Ожидайте подтверждения администратора."
    )

    await callback.answer()


@dp.callback_query(F.data.startswith("done_"))
async def order_done_handler(callback: CallbackQuery):

    if callback.from_user.id != ADMIN_ID:
        return

    order_id = int(callback.data.split("_")[1])

    order = get_order(order_id)

    if order is None:
        return

    update_order_status(order_id, "done")

    user_id = order[1]
    item_name = order[2]

    await bot.send_message(
        chat_id=user_id,
        text=(
            "✅ Ваш заказ выполнен!\n\n"
            "📦 Товар: " + item_name
        )
    )

    await callback.message.edit_text(
        callback.message.text + "\n\n✅ ВЫПОЛНЕНО"
    )


@dp.callback_query(F.data.startswith("cancel_"))
async def order_cancel_handler(callback: CallbackQuery):

    if callback.from_user.id != ADMIN_ID:
        return

    order_id = int(callback.data.split("_")[1])

    order = get_order(order_id)

    if order is None:
        return

    update_order_status(order_id, "cancel")

    user_id = order[1]
    item_name = order[2]
    price = order[3]

    add_coins(user_id, price)

    await bot.send_message(
        chat_id=user_id,
        text=(
            "❌ Ваш заказ отменён\n\n"
            "💰 Монеты возвращены\n"
            "📦 Товар: " + item_name
        )
    )

    await callback.message.edit_text(
        callback.message.text + "\n\n❌ ОТМЕНЕНО"
    )


async def main():

    print("БОТ ЗАПУЩЕН")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
