@echo off
REM Скрипт для быстрого запуска бота на Windows

echo.
echo ================================================
echo   🤖 Telegram Bot - Запуск
echo ================================================
echo.

REM Проверяем, установлены ли зависимости
python -c "import aiogram" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Зависимости не установлены!
    echo Запусти: install_requirements.bat
    pause
    exit /b 1
)

echo ✓ Все готово к запуску!
echo.

REM Выбираем вариант бота
echo Выбери, какой бот запустить:
echo 1 - Простой бот (рекомендуется)
echo 2 - Полный бот с Google Sheets
echo.

set /p choice="Введи номер (1 или 2): "

if "%choice%"=="1" (
    echo.
    echo 🚀 Запускаю simple_bot.py...
    echo.
    python simple_bot.py
) else if "%choice%"=="2" (
    echo.
    echo 🚀 Запускаю bot.py...
    echo.
    python bot.py
) else (
    echo ❌ Неверный выбор!
    pause
    exit /b 1
)

pause
