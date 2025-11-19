import asyncio
import logging
import pandas as pd
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
# Добавили импорты для кнопок-ссылок
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# --- 1. НАСТРОЙКИ ---
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

import os

print("DEBUG ENV KEYS:", list(os.environ.keys()))
print("DEBUG BOT_TOKEN EXISTS:", "BOT_TOKEN" in os.environ)
print("DEBUG BOT_TOKEN VALUE:", BOT_TOKEN)


# --- 2. ФУНКЦИЯ ЧТЕНИЯ БАЗЫ ДАННЫХ ---
def load_data():
    print("🔄 Пытаюсь открыть файл data.csv...")
    try:
        # Если будут кракозябры, поменяй encoding='utf-8' на encoding='cp1251'
        df = pd.read_csv('data.csv', encoding='utf-8', sep=None, engine='python')
        
        data_dict = {}
        for index, row in df.iterrows():
            trigger = str(row[0]).strip() 
            data_dict[trigger] = {
                "text": str(row[1]),
                "image": str(row[2]) if pd.notna(row[2]) else None
            }
        print(f"✅ Успех! Загружено {len(data_dict)} карт.")
        return data_dict
    except Exception as e:
        print(f"❌ ОШИБКА чтения файла: {e}")
        return {}

responses = load_data()

# --- 3. ИНИЦИАЛИЗАЦИЯ БОТА ---
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- 4. КЛАВИАТУРА (МЕНЮ) ---
def get_keyboard():
    builder = []
    row = []
    for key in responses.keys():
        if not key.startswith("/"): 
            row.append(KeyboardButton(text=key))
            if len(row) == 2:
                builder.append(row)
                row = []
    if row:
        builder.append(row)
    return ReplyKeyboardMarkup(keyboard=builder, resize_keyboard=True)

# --- 5. ХЭНДЛЕРЫ ---

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    start_text = responses.get("/start", {"text": "Привет! Выбери карту 👇"})
    # Если start_text словарь (из базы), берем поле text, если строка - оставляем как есть
    if isinstance(start_text, dict):
        text_to_send = start_text["text"]
    else:
        text_to_send = start_text
        
    await message.answer(text_to_send, reply_markup=get_keyboard())

@dp.message()
async def bot_message(message: types.Message):
    user_text = message.text
    
    # Проверяем, есть ли такая карта в базе
    if user_text in responses:
        data = responses[user_text]
        
        # 1. Отправляем Карту (Фото + Описание)
        if data['image'] and data['image'].startswith('http'):
            await message.answer_photo(photo=data['image'], caption=data['text'])
        else:
            await message.answer(data['text'])
            
        # 2. Пауза для эффекта
        await asyncio.sleep(1)
        
        # 3. Кнопки с ссылками (CTA)
        keyboard_links = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✨ Записаться на разбор", url="https://aromaterapija.store/ru/")], 
            [InlineKeyboardButton(text="📷 Мой Инстаграм", url="https://www.instagram.com/aroma_riga?igsh=MW5leDBocmdkd2ZteQ==")]
        ])
        
        await message.answer(
            "Хочешь разобрать ситуацию глубоко? Жми кнопку ниже! 👇", 
            reply_markup=keyboard_links
        )

    else:
        # Если юзер написал бред
        await message.answer("Я не знаю такой команды. Нажми на кнопку в меню! 🔮")

# --- 6. ЗАПУСК ---
async def main():
    print("🚀 Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":

    asyncio.run(main())
