import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

API_TOKEN = os.getenv("BOT_TOKEN")  # Вставь свой токен сюда или через .env

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Вопросы (заполни до 14 штук по своему сценарию)
questions = [
    {
        "text": "Ты скорее...",
        "options": [
            {"emoji": "🔧", "text": "Люблю изобретать и чинить", "value": "технарь"},
            {"emoji": "💬", "text": "Общаюсь с людьми и руковожу", "value": "руководитель"},
            {"emoji": "🎭", "text": "Мечтаю и создаю искусство", "value": "творец"},
            {"emoji": "💪", "text": "Работаю руками, мне не страшен труд", "value": "рабочий"}
        ]
    },
    # Добавь тут остальные 13 вопросов по тому же шаблону!
    # ...
]

# Для хранения ответов пользователя
user_progress = {}

def get_keyboard(options):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for opt in options:
        kb.add(KeyboardButton(f"{opt['emoji']} {opt['text']}"))
    return kb

# Функция отправки вопроса
async def ask_question(message, q_num):
    if q_num >= len(questions):
        await message.answer("Тест завершён! Скоро появится твой результат 🏆", reply_markup=types.ReplyKeyboardRemove())
        return

    q = questions[q_num]
    text = f"Вопрос {q_num+1} из {len(questions)}:\n{q['text']}"
    kb = get_keyboard(q["options"])
    await message.answer(text, reply_markup=kb)
    user_progress[message.from_user.id] = q_num

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer("Привет! Это «Плёнка судьбы»\nТест из 14 вопросов покажет, кем бы ты был(а) в XX веке.")
    await asyncio.sleep(1.5)
    await ask_question(message, 0)

@dp.message_handler(lambda message: message.text and message.from_user.id in user_progress)
async def handle_answer(message: types.Message):
    q_num = user_progress[message.from_user.id]
    # Здесь можно сохранить ответ пользователя
    await ask_question(message, q_num + 1)

if __name__ == "__main__":
    executor.start_polling(dp)