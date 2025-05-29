import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

API_TOKEN = os.getenv("BOT_TOKEN")  # Вставь свой токен сюда или через .env

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Вопросы (14 штук)
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
    {
        "text": "Что бы ты взял(а) с собой в командировку в 1965?",
        "options": [
            {"emoji": "📕", "text": "Записную книжку и перо", "value": "руководитель"},
            {"emoji": "📷", "text": "Плёнку, чтобы снимать хронику", "value": "творец"},
            {"emoji": "🔬", "text": "Мини-микроскоп — мало ли", "value": "технарь"},
            {"emoji": "🥾", "text": "Кирзовые сапоги, вдруг стройка", "value": "рабочий"}
        ]
    },
    {
        "text": "Выбери идеальное рабочее место:",
        "options": [
            {"emoji": "🏭", "text": "Завод с гулом станков", "value": "рабочий"},
            {"emoji": "📚", "text": "Кабинет с книгами и бумагами", "value": "руководитель"},
            {"emoji": "🎬", "text": "Съёмочная площадка или сцена", "value": "творец"},
            {"emoji": "✈️", "text": "Кабина пилота или командный пункт", "value": "технарь"}
        ]
    },
    {
        "text": "Ты получил(а) срочную телеграмму из ЦК. Твоя реакция?",
        "options": [
            {"emoji": "📬", "text": "Немедленно докладываю начальству — это важно", "value": "руководитель"},
            {"emoji": "🧪", "text": "Анализирую данные, вдруг это эксперимент", "value": "технарь"},
            {"emoji": "✍️", "text": "Превращаю в сценарий — звучит кинематографично", "value": "творец"},
            {"emoji": "🤷‍♂️", "text": "Сначала доделаю смену, потом всё остальное", "value": "рабочий"}
        ]
    },
    {
        "text": "На улицу выбросили редкий трофейный магнитофон 1950-х. Что ты сделаешь?",
        "options": [
            {"emoji": "🔧", "text": "Починю! Это настоящая находка", "value": "технарь"},
            {"emoji": "🎤", "text": "Использую как реквизит в пьесе", "value": "творец"},
            {"emoji": "📻", "text": "Отдам на завод, пусть пускают в производство", "value": "рабочий"},
            {"emoji": "📚", "text": "Поищу информацию о нём — может, он шпионский", "value": "руководитель"}
        ]
    },
    {
        "text": "Тебе дали предмет: слайдоскоп. Что ты думаешь?",
        "options": [
            {"emoji": "🔍", "text": "Отличный прибор — можно изучать кристаллы", "value": "технарь"},
            {"emoji": "📸", "text": "Использую для домашней лекции", "value": "руководитель"},
            {"emoji": "🖼", "text": "Превращу в часть сценографии", "value": "творец"},
            {"emoji": "❓", "text": "Не знаю, что это, но кручу и верчу", "value": "рабочий"}
        ]
    },
    {
        "text": "Тебе дают выбор командировки. Куда поедешь?",
        "options": [
            {"emoji": "🚂", "text": "На Байкало-Амурскую магистраль", "value": "рабочий"},
            {"emoji": "🎭", "text": "В Дом творчества в Переделкино", "value": "творец"},
            {"emoji": "🧪", "text": "В закрытую лабораторию", "value": "технарь"},
            {"emoji": "🧱", "text": "На восстановление села после войны", "value": "руководитель"}
        ]
    },
    {
        "text": "Ты оказался(лась) в 1943. Что делаешь?",
        "options": [
            {"emoji": "⚔️", "text": "Иду на фронт добровольцем", "value": "рабочий"},
            {"emoji": "🔬", "text": "Присоединяюсь к разработке техники", "value": "технарь"},
            {"emoji": "📣", "text": "Поднимаю мораль духа народа", "value": "творец"},
            {"emoji": "🚑", "text": "Работаю в медсанбате", "value": "руководитель"}
        ]
    },
    {
        "text": "Что тебя больше всего раздражает на работе?",
        "options": [
            {"emoji": "🐌", "text": "Медленные процессы и бюрократия", "value": "рабочий"},
            {"emoji": "📢", "text": "Когда никто не слушает", "value": "творец"},
            {"emoji": "📉", "text": "Когда нет смысла в том, что делаешь", "value": "руководитель"},
            {"emoji": "🚫", "text": "Когда не дают ничего делать руками", "value": "технарь"}
        ]
    },
    {
        "text": "Твой главный рабочий инструмент?",
        "options": [
            {"emoji": "✏️", "text": "Карандаш и блокнот", "value": "руководитель"},
            {"emoji": "🔧", "text": "Гаечный ключ", "value": "технарь"},
            {"emoji": "📢", "text": "Микрофон", "value": "творец"},
            {"emoji": "👩‍🔬", "text": "Пробирка", "value": "рабочий"}
        ]
    },
    {
        "text": "Что бы ты повесил(а) у себя на стене?",
        "options": [
            {"emoji": "🏅", "text": "Плакат с героями труда", "value": "рабочий"},
            {"emoji": "🎭", "text": "Афишу спектакля", "value": "творец"},
            {"emoji": "🧬", "text": "Схему строения молекулы", "value": "технарь"},
            {"emoji": "📜", "text": "Цитату Ленина или Гагарина", "value": "руководитель"}
        ]
    },
    {
        "text": "Когда ты слышишь слово «будущее», ты представляешь...",
        "options": [
            {"emoji": "🚀", "text": "Технологии и космос", "value": "технарь"},
            {"emoji": "📖", "text": "Образованных людей", "value": "руководитель"},
            {"emoji": "🎼", "text": "Искусство и свободу", "value": "творец"},
            {"emoji": "🔨", "text": "Много труда и больших строек", "value": "рабочий"}
        ]
    }
]

# Для хранения прогресса и ответов
user_progress = {}
user_answers = {}

def get_keyboard(options):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for opt in options:
        kb.add(KeyboardButton(f"{opt['emoji']} {opt['text']}"))
    return kb

async def ask_question(message, q_num):
    if q_num >= len(questions):
        answers = user_answers.get(message.from_user.id, [])
        counts = {}
        for ans in answers:
            counts[ans] = counts.get(ans, 0) + 1
        result = max(counts, key=counts.get) if counts else None
        titles = {
            "технарь": "Технарь",
            "руководитель": "Руководитель",
            "творец": "Творец",
            "рабочий": "Рабочий"
        }
        if result:
            await message.answer(f"📝 Ваш результат: {titles[result]}", reply_markup=types.ReplyKeyboardRemove())
        else:
            await message.answer("Что-то пошло не так...", reply_markup=types.ReplyKeyboardRemove())
        return

    q = questions[q_num]
    text = f"Вопрос {q_num+1} из {len(questions)}:\n{q['text']}"
    kb = get_keyboard(q["options"])
    await message.answer(text, reply_markup=kb)
    user_progress[message.from_user.id] = q_num

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_progress[message.from_user.id] = 0
    user_answers[message.from_user.id] = []
    await message.answer("Привет! Это «Плёнка судьбы»\nТест из 14 вопросов покажет, кем бы ты был(а) в XX веке.")
    await asyncio.sleep(1.5)
    await ask_question(message, 0)

@dp.message_handler(lambda message: message.text and message.from_user.id in user_progress)
async def handle_answer(message: types.Message):
    q_num = user_progress[message.from_user.id]
    text = message.text.split(" ", 1)[1]  # убираем emoji и пробел
    user_answers[message.from_user.id].append(text)
    await ask_question(message, q_num + 1)

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp)
