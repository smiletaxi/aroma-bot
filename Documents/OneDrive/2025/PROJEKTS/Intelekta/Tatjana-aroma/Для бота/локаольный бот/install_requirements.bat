@echo off
REM Скрипт для быстрой установки всех зависимостей на Windows

echo.
echo ====================================================
echo   Telegram Bot - Установка зависимостей (Windows)
echo ====================================================
echo.

REM Проверяем, установлен ли Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python не найден! 
    echo Скачай Python с https://www.python.org/
    echo При установке отметь "Add Python to PATH"
    pause
    exit /b 1
)

echo ✓ Python найден

REM Обновляем pip
echo.
echo Обновляю pip...
python -m pip install --upgrade pip

REM Устанавливаем зависимости из requirements.txt
echo.
echo Устанавливаю зависимости...
pip install -r requirements.txt

REM Проверяем установку
echo.
echo Проверяю установку...
python -c "import aiogram; print('✓ aiogram установлен')"
python -c "import dotenv; print('✓ python-dotenv установлен')"
python -c "import gspread; print('✓ gspread установлен')"

echo.
echo ✅ Все зависимости установлены!
echo.
echo Следующие шаги:
echo 1. Открой файл .env и добавь свой BOT_TOKEN
echo 2. Запусти бот: python simple_bot.py
echo.
pause
