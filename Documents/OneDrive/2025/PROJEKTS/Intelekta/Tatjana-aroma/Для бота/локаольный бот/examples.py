"""
📚 ПРИМЕРЫ И РЕЦЕПТЫ для Telegram бота

Используй эти примеры для расширения функциональности своего бота!
"""

# ═══════════════════════════════════════════════════════════════════════════════
# 1. ИНЛАЙН КНОПКИ (кнопки в сообщении, а не клавиатура)
# ═══════════════════════════════════════════════════════════════════════════════

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_inline_keyboard():
    """Пример инлайн кнопок"""
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="🌐 Посетить сайт", url="https://example.com"))
    builder.add(InlineKeyboardButton(text="📞 Написать", url="https://t.me/your_username"))
    builder.add(InlineKeyboardButton(text="❌ Закрыть", callback_data="close"))
    builder.adjust(1)  # Одна кнопка в ряд
    return builder.as_markup()

# Использование:
# await message.answer("Выбери действие:", reply_markup=get_inline_keyboard())


# ═══════════════════════════════════════════════════════════════════════════════
# 2. ОБРАБОТКА CALLBACK КНОПОК
# ═══════════════════════════════════════════════════════════════════════════════

from aiogram import types
from aiogram.types import CallbackQuery

# @router.callback_query(F.data == "close")
# async def close_button(query: CallbackQuery):
#     await query.message.delete()
#     await query.answer("Закрыто! ✓")

# @router.callback_query(F.data.startswith("like_"))
# async def like_button(query: CallbackQuery):
#     item_id = query.data.split("_")[1]
#     await query.answer(f"Ты лайкнул '{item_id}'! 👍")
#     await query.message.edit_text(f"Спасибо за оценку! (ID: {item_id})")


# ═══════════════════════════════════════════════════════════════════════════════
# 3. ОТПРАВКА РАЗЛИЧНЫХ ТИПОВ КОНТЕНТА
# ═══════════════════════════════════════════════════════════════════════════════

# 📸 Фото
# await message.answer_photo(
#     photo="https://example.com/photo.jpg",
#     caption="Подпись под фото",
#     parse_mode="HTML"
# )

# 🎬 Видео
# await message.answer_video(
#     video="https://example.com/video.mp4",
#     caption="Видео описание",
#     duration=60
# )

# 📄 Документ
# await message.answer_document(
#     document="https://example.com/file.pdf",
#     caption="PDF файл"
# )

# 🎵 Аудио
# await message.answer_audio(
#     audio="https://example.com/song.mp3",
#     title="Название трека",
#     performer="Исполнитель"
# )

# 📍 Локация
# await message.answer_location(
#     latitude=55.7558,
#     longitude=37.6173
# )


# ═══════════════════════════════════════════════════════════════════════════════
# 4. ФОРМАТИРОВАНИЕ ТЕКСТА
# ═══════════════════════════════════════════════════════════════════════════════

# HTML форматирование (parse_mode="HTML")
formatted_text = """
<b>Жирный текст</b>
<i>Курсив</i>
<u>Подчеркивание</u>
<s>Зачеркивание</s>
<code>Моноширинный шрифт</code>
<pre>Блок кода</pre>
<a href="https://example.com">Ссылка</a>

emoji: 😀 🎉 🌟 ✨ 💎 🔥
"""

# await message.answer(formatted_text, parse_mode="HTML")

# Markdown форматирование (parse_mode="Markdown")
markdown_text = """
*Жирный* или __жирный__
_Курсив_ или *курсив*
`Код`
```
Блок кода
```
[Ссылка](https://example.com)
"""

# await message.answer(markdown_text, parse_mode="Markdown")


# ═══════════════════════════════════════════════════════════════════════════════
# 5. ФИЛЬТРЫ И УСЛОВИЯ
# ═══════════════════════════════════════════════════════════════════════════════

from aiogram import F

# Обработка только текста
# @router.message(F.text)
# async def text_handler(message: Message):
#     pass

# Обработка только фото
# @router.message(F.photo)
# async def photo_handler(message: Message):
#     pass

# Обработка по регулярному выражению
# @router.message(F.text.regexp(r"^привет"))
# async def hello_handler(message: Message):
#     pass

# Обработка если текст содержит слово
# @router.message(F.text.contains("спасибо"))
# async def thanks_handler(message: Message):
#     pass

# Множественные условия (И)
# @router.message(F.text.startswith("кто") & F.from_user.is_bot == False)
# async def question_handler(message: Message):
#     pass

# Множественные условия (ИЛИ)
# @router.message(F.text.in_(["hello", "hi", "привет"]))
# async def greeting_handler(message: Message):
#     pass


# ═══════════════════════════════════════════════════════════════════════════════
# 6. РАБОТА С ПОЛЬЗОВАТЕЛЕМ
# ═══════════════════════════════════════════════════════════════════════════════

# Получение информации о пользователе
# user_id = message.from_user.id
# username = message.from_user.username
# first_name = message.from_user.first_name
# last_name = message.from_user.last_name
# language = message.from_user.language_code
# is_bot = message.from_user.is_bot

# Сохранение истории
# users_history = {}
# if user_id not in users_history:
#     users_history[user_id] = []
# users_history[user_id].append(message.text)


# ═══════════════════════════════════════════════════════════════════════════════
# 7. ЗАДЕРЖКИ И АСИНХРОННОСТЬ
# ═══════════════════════════════════════════════════════════════════════════════

import asyncio

# Отправить сообщение, подождать, отправить еще одно
# await message.answer("Думаю...")
# await asyncio.sleep(2)
# await message.answer("Вот ответ!")

# Отправить несколько сообщений в быстрой последовательности
# for i in range(1, 6):
#     await message.answer(f"Сообщение #{i}")
#     await asyncio.sleep(0.5)


# ═══════════════════════════════════════════════════════════════════════════════
# 8. РЕДАКТИРОВАНИЕ СООБЩЕНИЙ
# ═══════════════════════════════════════════════════════════════════════════════

# Изменить текст уже отправленного сообщения
# sent_message = await message.answer("Загрузка...")
# await asyncio.sleep(2)
# await sent_message.edit_text("Загрузка завершена! ✓")

# Удалить сообщение
# await message.delete()

# Ответить на сообщение (reply)
# await message.reply("Отличный вопрос! 😊")


# ═══════════════════════════════════════════════════════════════════════════════
# 9. КАСТОМНЫЕ ФИЛЬТРЫ
# ═══════════════════════════════════════════════════════════════════════════════

from aiogram.filters import BaseFilter

# class IsAdmin(BaseFilter):
#     async def __call__(self, message: Message) -> bool:
#         admin_ids = [123456789, 987654321]
#         return message.from_user.id in admin_ids

# @router.message(IsAdmin())
# async def admin_command(message: Message):
#     await message.answer("Привет, админ! 👑")


# ═══════════════════════════════════════════════════════════════════════════════
# 10. ОБРАБОТКА ОШИБОК
# ═══════════════════════════════════════════════════════════════════════════════

from aiogram.types import TelegramAPIError

# try:
#     await message.answer("Отправляю сообщение...")
# except TelegramAPIError as e:
#     print(f"Ошибка Telegram: {e}")
# except Exception as e:
#     print(f"Неожиданная ошибка: {e}")


# ═══════════════════════════════════════════════════════════════════════════════
# 11. СОСТОЯНИЯ И КОНТЕКСТ (для многошаговых сценариев)
# ═══════════════════════════════════════════════════════════════════════════════

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

# class RegistrationStates(StatesGroup):
#     waiting_for_name = State()
#     waiting_for_age = State()
#     waiting_for_email = State()

# @router.message(CommandStart())
# async def start_registration(message: Message, state: FSMContext):
#     await state.set_state(RegistrationStates.waiting_for_name)
#     await message.answer("Как тебя зовут?")

# @router.message(RegistrationStates.waiting_for_name)
# async def process_name(message: Message, state: FSMContext):
#     await state.update_data(name=message.text)
#     await state.set_state(RegistrationStates.waiting_for_age)
#     await message.answer("Сколько тебе лет?")

# @router.message(RegistrationStates.waiting_for_age)
# async def process_age(message: Message, state: FSMContext):
#     await state.update_data(age=message.text)
#     await state.set_state(RegistrationStates.waiting_for_email)
#     await message.answer("Твой email?")

# @router.message(RegistrationStates.waiting_for_email)
# async def process_email(message: Message, state: FSMContext):
#     data = await state.get_data()
#     await message.answer(
#         f"Спасибо! Твои данные:\n"
#         f"Имя: {data['name']}\n"
#         f"Возраст: {data['age']}\n"
#         f"Email: {message.text}"
#     )
#     await state.clear()


# ═══════════════════════════════════════════════════════════════════════════════
# 12. ПЛАНИРОВЩИК ЗАДАЧ (APScheduler)
# ═══════════════════════════════════════════════════════════════════════════════

# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from datetime import datetime

# scheduler = AsyncIOScheduler()

# async def scheduled_message(bot: Bot):
#     await bot.send_message(chat_id=YOUR_CHAT_ID, text="Привет! Это автоматическое сообщение 👋")

# # Каждый день в 9:00
# scheduler.add_job(scheduled_message, "cron", hour=9, minute=0, args=(bot,))
# scheduler.start()


print("""
🎉 Примеры успешно загружены!

Используй эти шаблоны для расширения своего бота.
Раскомментируй нужные части кода и адаптируй под свои нужды.

Документация: https://docs.aiogram.dev/
""")
