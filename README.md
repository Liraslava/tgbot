# tgbot
a simple telegram bot for practicing working with the telebot library


# Описание проекта
Это Telegram бот с несколькими функциями:
  Переводчик - переводит текст с любого языка на английский
  Поиск в Wikipedia - ищет информацию по запросу
  Викторина по программированию - 15 вопросов на тему программирования

# Установка и запуск
1) Установите необходимые зависимости:
```bash
pip install pyTelegramBotAPI googletrans==4.0.0-rc1 langdetect wikipedia
```
2) Замените 'YOUR_BOT_TOKEN' на токен вашего бота, полученный от @BotFather
3) Запустите бота: python bot.py

# Команды бота:
/start - начать работу с ботом
/victorina - запустить викторину
/translate - активировать режим перевода
/stoptranslate - деактивировать режим перевода
/search - активировать поиск в Wikipedia
/desearch - деактивировать поиск в Wikipedia
