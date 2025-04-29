from telebot import *
from googletrans import Translator  # pip install googletrans==4.0.0-rc1
from langdetect import detect
import wikipedia

bot = TeleBot('YOUR_BOT_TOKEN')  # Замените на ваш токен от @BotFather
translator = Translator()

user_states = {}
search_condit = {}
victorina_states = {}

# Вопросы викторины по программированию
questions = [
    {
        'question': 'Какой язык программирования самый популярный в 2023 году?',
        'options': ['Python', 'JavaScript', 'Java', 'C++'],
        'answer': 'Python'
    },
    {
        'question': 'Что означает HTML?',
        'options': ['HyperText Markup Language', 'High-Level Text Language',
                    'Home Tool Markup Language', 'Hyperlinks and Text Markup Language'],
        'answer': 'HyperText Markup Language'
    },
    {
        'question': 'Какой оператор используется для проверки равенства по значению и типу в JavaScript?',
        'options': ['==', '=', '===', '!=', '!=='],
        'answer': '==='
    },
    {
        'question': 'Что такое рекурсия в программировании?',
        'options': ['Вызов функции самой себя', 'Быстрая сортировка',
                    'Цикл с условием', 'Объектно-ориентированное программирование'],
        'answer': 'Вызов функции самой себя'
    },
    {
        'question': 'Какой язык не является объектно-ориентированным?',
        'options': ['Java', 'C++', 'Python', 'C', 'Ruby'],
        'answer': 'C'
    },
    {
        'question': 'Что такое API?',
        'options': ['Application Programming Interface', 'Advanced Programming Interface',
                    'Automated Programming Interface', 'Application Process Integration'],
        'answer': 'Application Programming Interface'
    },
    {
        'question': 'Какой символ используется для однострочных комментариев в Python?',
        'options': ['//', '#', '--', '/*', '*/'],
        'answer': '#'
    },
    {
        'question': 'Что выведет этот код: print(2 + 2 * 2) в Python?',
        'options': ['6', '8', '4', 'Ошибка'],
        'answer': '6'
    },
    {
        'question': 'Какой из этих типов данных является изменяемым в Python?',
        'options': ['int', 'str', 'tuple', 'list', 'float'],
        'answer': 'list'
    },
    {
        'question': 'Как называется парадигма программирования, основанная на понятиях "объектов"?',
        'options': ['Функциональное программирование', 'Логическое программирование',
                    'Объектно-ориентированное программирование', 'Императивное программирование'],
        'answer': 'Объектно-ориентированное программирование'
    },
    {
        'question': 'Какой язык создал Брендан Эйх за 10 дней?',
        'options': ['Python', 'Java', 'JavaScript', 'PHP', 'Ruby'],
        'answer': 'JavaScript'
    },
    {
        'question': 'Что такое Git?',
        'options': ['Язык программирования', 'Система контроля версий',
                    'Фреймворк для веб-разработки', 'Реляционная база данных'],
        'answer': 'Система контроля версий'
    },
    {
        'question': 'Какой метод используется для добавления элемента в конец списка в Python?',
        'options': ['append()', 'add()', 'insert()', 'push()', 'extend()'],
        'answer': 'append()'
    },
    {
        'question': 'Что такое SQL?',
        'options': ['Simple Query Language', 'Structured Query Language',
                    'Standard Query Language', 'System Query Language'],
        'answer': 'Structured Query Language'
    },
    {
        'question': 'Какой из этих языков является компилируемым?',
        'options': ['Python', 'JavaScript', 'Ruby', 'C++', 'PHP'],
        'answer': 'C++'
    }
]

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, '''Приветствую тебя! 
    Используй /translate для активации перевода и /stoptranslate для его деактивации.
    Используй /search для активации поиска в Интернете и /desearch для завершения
    Используй /victorina для запуска викторины по программированию''')

@bot.message_handler(commands=['translate'])
def start_translate(message):
    user_states[message.chat.id] = True
    bot.send_message(message.chat.id, 'Перевод активирован. Отправляйте сообщения для перевода.')

@bot.message_handler(commands=['stoptranslate'])
def stop_translate(message):
    user_states[message.chat.id] = False
    bot.send_message(message.chat.id, 'Перевод деактивирован.')

@bot.message_handler(commands=['search'])
def search(message):
    search_condit[message.chat.id] = True
    bot.send_message(message.chat.id, 'Поиск активирован. Введите запрос!')

@bot.message_handler(commands=['desearch'])
def desearch(message):
    search_condit[message.chat.id] = False
    bot.send_message(message.chat.id, 'Поиск деактивирован.')

@bot.message_handler(commands=['victorina'])
def victorina(message):
    global question_index
    victorina_states[message.chat.id] = True
    question_index = 0
    bot.send_message(message.chat.id, 'Викторина по программированию запущена!')
    ask_question(message.chat.id, question_index)


def ask_question(chat_id, question_index):
    question = questions[question_index]
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for option in question['options']:
        markup.add(option)
    bot.send_message(chat_id, f'Вопрос {question_index + 1}/{len(questions)}: {question["question"]}',
                     reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    global question_index

    # Обработка викторины
    if victorina_states.get(message.chat.id, False):
        user_answer = message.text
        correct_answer = questions[question_index]['answer']

        if user_answer == correct_answer:
            bot.send_message(message.chat.id, '✅ Правильно!')
        else:
            bot.send_message(message.chat.id, f'❌ Неправильно! Правильный ответ: {correct_answer}')

        if question_index < len(questions) - 1:
            question_index += 1
            ask_question(message.chat.id, question_index)
        else:
            victorina_states[message.chat.id] = False
            bot.send_message(message.chat.id, '🎉 Викторина завершена! Спасибо за участие!',
                             reply_markup=types.ReplyKeyboardRemove())

    # Обработка перевода
    elif user_states.get(message.chat.id, False):
        try:
            translate_text = translator.translate(message.text, src=detect(message.text), dest='en').text
            bot.send_message(message.chat.id, translate_text)
        except Exception as e:
            bot.send_message(message.chat.id, f'Ошибка перевода: {str(e)}')

    # Обработка поиска
    elif search_condit.get(message.chat.id, False):
        wikipedia.set_lang('ru')
        try:
            result = wikipedia.search(message.text)
            if not result:
                bot.send_message(message.chat.id, 'По вашему запросу ничего не найдено')
            else:
                page = wikipedia.page(result[0])
                bot.send_message(message.chat.id, page.url)
        except wikipedia.exceptions.DisambiguationError as e:
            bot.send_message(message.chat.id, f'Уточните запрос. Возможные варианты: {", ".join(e.options[:5])}')
        except Exception as e:
            bot.send_message(message.chat.id, f'Ошибка поиска: {str(e)}')

bot.polling()
