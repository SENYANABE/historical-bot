import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

API_TOKEN = os.getenv("BOT_TOKEN") or "YOUR_TOKEN_HERE"  # Вставьте ваш токен

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Полный список из 14 вопросов
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

# Хранение состояния: q_index и answers
user_state = {}

def get_keyboard(options):
    kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for opt in options:
        kb.add(KeyboardButton(f"{opt['emoji']} {opt['text']}"))
    return kb

@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    # Инициализируем
    user_state[message.chat.id] = {'q': 0, 'answers': []}
    await message.answer("Привет! Это «Плёнка судьбы»
Тест из 14 вопросов покажет, кем бы ты был(а) в XX веке.")
    await asyncio.sleep(1.5)
    q0 = questions[0]
    await message.answer(f"Вопрос 1 из {len(questions)}:
{q0['text']}", reply_markup=get_keyboard(q0['options']))

@dp.message_handler(lambda message: message.chat.id in user_state)
async def process_answer(message: types.Message):
    state = user_state[message.chat.id]
    idx = state['q']
    # Найдём выбранный opt.value
    selected = None
    for opt in questions[idx]['options']:
        if message.text.startswith(opt['emoji']):
            selected = opt['value']
            break
    if selected:
        state['answers'].append(selected)
    idx += 1
    if idx < len(questions):
        state['q'] = idx
        q = questions[idx]
        await message.answer(f"Вопрос {idx+1} из {len(questions)}:
{q['text']}", reply_markup=get_keyboard(q['options']))
    else:
        # Подсчёт результатов
        counts = {}
        for v in state['answers']:
            counts[v] = counts.get(v, 0) + 1
        result_key = max(counts, key=counts.get)
        titles = {
            "технарь": "Технарь",
            "руководитель": "Руководитель",
            "творец": "Творец",
            "рабочий": "Рабочий"
        }
        await message.answer(f"📝 Ваш результат: {titles.get(result_key, result_key)}", reply_markup=types.ReplyKeyboardRemove())
        user_state.pop(message.chat.id)

if __name__ == "__main__":
    executor.start_polling(dp)
