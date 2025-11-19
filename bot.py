import asyncio
import logging
import gspread
from aiogram import Bot, Dispatcher, Router, F, types
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# --- 1. Настройки ---

# Вставь сюда токен, который ты получил у @BotFather в Telegram
# Или используй переменную окружения BOT_TOKEN из .env файла
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN") 

# Это JSON-файл, который ты скачаешь из Google Cloud (об этом ниже)
# Положи его рядом с 'bot.py'
try:
    GC = gspread.service_account(filename='service_account.json')
    # Открываем таблицу по ее ПОЛНОМУ имени
    SHEET = GC.open("BotContent") 
    WORKSHEET = SHEET.worksheet("Cards") # Открываем лист "Cards"
    logging.info("Успешно подключились к Google Sheets!")
except Exception as e:
    logging.error(f"Ошибка подключения к Google Sheets: {e}")
    exit()

# --- 2. "Кэш" данных из таблицы ---
# Мы не будем дергать таблицу на каждого юзера, 
# а загрузим данные один раз при старте
card_data = {}

# --- 3. Наш Роутер (обработчик сообщений) ---
router = Router()

# --- 4. Функции ---

async def load_data_from_sheet():
    """Загружает (или обновляет) данные из таблицы в наш 'кэш'."""
    global card_data
    try:
        # get_all_records() удобно превращает строки в словари
        data = WORKSHEET.get_all_records() 
        temp_data = {}
        for row in data:
            if row['state']: # Убедимся, что ячейка 'state' не пустая
                temp_data[row['state']] = row['interpretation']
        
        card_data = temp_data
        logging.info(f"Данные из таблицы загружены: {list(card_data.keys())}")
        return True
    except Exception as e:
        logging.error(f"Ошибка загрузки данных из таблицы: {e}")
        return False

def get_states_keyboard():
    """Создает динамическую клавиатуру на основе данных из таблицы."""
    builder = ReplyKeyboardBuilder()
    # Идем по всем ключам (названиям состояний)
    for state_name in card_data.keys():
        builder.add(KeyboardButton(text=state_name))
    # Ставим по 2 кнопки в ряд, чтобы было красиво
    builder.adjust(2) 
    return builder.as_markup(resize_keyboard=True)

# --- 5. Хэндлеры (Реакции бота) ---

@router.message(CommandStart())
async def cmd_start(message: Message):
    """Реакция на команду /start"""
    if not card_data:
        # Если кэш пуст (например, при первом запуске), грузим
        if not await load_data_from_sheet():
            await message.answer("Ой, база знаний (таблица) сейчас спит. Попробуй /start позже.")
            return

    keyboard = get_states_keyboard()
    await message.answer(
        "Привет! Я твой личный бот-диагност. 🔮\n\nВыбери свое состояние, и я вытяну для тебя карту...",
        reply_markup=keyboard
    )

@router.message(F.text.in_(card_data.keys()))
async def send_interpretation(message: Message):
    """
    Эта 'магия' (F.text.in_) ловит только те сообщения,
    текст которых ТОЧНО совпадает с одним из наших 'state' в таблице.
    То есть, ловит нажатия на наши кнопки.
    """
    # Получаем интерпретацию по тексту сообщения (названию кнопки)
    interpretation = card_data.get(message.text)
    
    # 1. Отправляем основную интерпретацию
    await message.answer(interpretation, reply_markup=types.ReplyKeyboardRemove()) # Прячем кнопки

    # 2. Делаем твой CTA (Call to Action)
    # (Тут можно сделать Inline-кнопки для перехода)
    await asyncio.sleep(1) # Маленькая пауза для "драматургии"
    await message.answer(
        "Хочешь глубже разобраться в себе и получить полный расклад?\n\n"
        "Записывайся на платную диагностику или переходи на наш канал!",
        # reply_markup= (тут могут быть твои кнопки на сайт/канал)
    )
    
    # Сразу предлагаем начать заново
    await asyncio.sleep(2)
    await message.answer(
        "Нажми /start, если захочешь вытянуть еще одну карту."
    )


@router.message()
async def unknown_text(message: Message):
    """Реакция на любой другой текст, который не /start и не кнопка."""
    await message.answer("Я не понял... Пожалуйста, выбери одно из состояний на клавиатуре или нажми /start.")


# --- 6. Запуск бота ---

async def main():
    # Настройка логирования (чтобы видеть в консоли, что делает бот)
    logging.basicConfig(level=logging.INFO)
    
    # Загружаем данные из таблицы ПЕРЕД запуском
    if not await load_data_from_sheet():
        logging.critical("Не удалось загрузить данные из таблицы. Бот не может стартовать.")
        return

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    
    # Начинаем опрашивать Telegram
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())