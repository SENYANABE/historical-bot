import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from collections import Counter

API_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

questions = [{'options': [{'emoji': '🔧', 'text': 'Люблю изобретать и чинить', 'value': 'технарь'},
              {'emoji': '💬', 'text': 'Общаюсь с людьми и руковожу', 'value': 'руководитель'},
              {'emoji': '🎭', 'text': 'Мечтаю и создаю искусство', 'value': 'творец'},
              {'emoji': '💪', 'text': 'Работаю руками, мне не страшен труд', 'value': 'рабочий'}],
  'text': 'Ты скорее...'},
 {'options': [{'emoji': '😌', 'text': 'Предпочитаю стабильность и порядок', 'value': 'руководитель'},
              {'emoji': '💥', 'text': 'Люблю, когда адреналин кипит', 'value': 'рабочий'},
              {'emoji': '🧠', 'text': 'Главное — интерес, риск пусть будет', 'value': 'технарь'},
              {'emoji': '🚜', 'text': 'Мне всё равно, работа — это дело', 'value': 'рабочий'}],
  'text': 'Как ты относишься к риску?'},
 {'options': [{'emoji': '🎤', 'text': 'Выступление перед публикой', 'value': 'творец'},
              {'emoji': '🧪', 'text': 'Демонстрация нового эксперимента', 'value': 'технарь'},
              {'emoji': '👮', 'text': "Заявление в духе 'порядок будет!'", 'value': 'руководитель'},
              {'emoji': '👷', 'text': 'Работа в цеху у станка', 'value': 'рабочий'}],
  'text': 'Какая сцена тебе ближе?'},
 {'options': [{'emoji': '📕', 'text': 'Записную книжку и перо', 'value': 'руководитель'},
              {'emoji': '📷', 'text': 'Плёнку, чтобы снимать хронику', 'value': 'творец'},
              {'emoji': '🔬', 'text': 'Мини-микроскоп — мало ли', 'value': 'технарь'},
              {'emoji': '🥾', 'text': 'Кирзовые сапоги, вдруг стройка', 'value': 'рабочий'}],
  'text': 'Что бы ты взял(а) с собой в командировку в 1965?'},
 {'options': [{'emoji': '🏭', 'text': 'Завод с гулом станков', 'value': 'рабочий'},
              {'emoji': '📚', 'text': 'Кабинет с книгами и бумагами', 'value': 'руководитель'},
              {'emoji': '🎬', 'text': 'Съёмочная площадка или сцена', 'value': 'творец'},
              {'emoji': '✈️', 'text': 'Кабина пилота или командный пункт', 'value': 'технарь'}],
  'text': 'Выбери идеальное рабочее место:'},
 {'options': [{'emoji': '📬',
               'text': 'Немедленно докладываю начальству — это важно',
               'value': 'руководитель'},
              {'emoji': '🧪',
               'text': 'Анализирую данные, вдруг это эксперимент',
               'value': 'технарь'},
              {'emoji': '✍️',
               'text': 'Превращаю в сценарий — звучит кинематографично',
               'value': 'творец'},
              {'emoji': '🤷\u200d♂️',
               'text': 'Сначала доделаю смену, потом всё остальное',
               'value': 'рабочий'}],
  'text': 'Ты получил(а) срочную телеграмму из ЦК. Твоя реакция?'},
 {'options': [{'emoji': '🔧', 'text': 'Починю! Это настоящая находка', 'value': 'технарь'},
              {'emoji': '🎤', 'text': 'Использую как реквизит в пьесе', 'value': 'творец'},
              {'emoji': '📻',
               'text': 'Отдам на завод, пусть пускают в производство',
               'value': 'рабочий'},
              {'emoji': '📚',
               'text': 'Поищу информацию о нём — может, он шпионский',
               'value': 'руководитель'}],
  'text': 'На улицу выбросили редкий трофейный магнитофон 1950-х. Что ты сделаешь?'},
 {'options': [{'emoji': '🔍',
               'text': 'Отличный прибор — можно изучать кристаллы',
               'value': 'технарь'},
              {'emoji': '📸', 'text': 'Использую для домашней лекции', 'value': 'руководитель'},
              {'emoji': '🖼', 'text': 'Превращу в часть сценографии', 'value': 'творец'},
              {'emoji': '❓', 'text': 'Не знаю, что это, но кручу и верчу', 'value': 'рабочий'}],
  'text': 'Тебе дали предмет: слайдоскоп. Что ты думаешь?'},
 {'options': [{'emoji': '🚂', 'text': 'На Байкало-Амурскую магистраль', 'value': 'рабочий'},
              {'emoji': '🎭', 'text': 'В Дом творчества в Переделкино', 'value': 'творец'},
              {'emoji': '🧪', 'text': 'В закрытую лабораторию', 'value': 'технарь'},
              {'emoji': '🧱',
               'text': 'На восстановление села после войны',
               'value': 'руководитель'}],
  'text': 'Тебе дают выбор командировки. Куда поедешь?'},
 {'options': [{'emoji': '⚔️', 'text': 'Иду на фронт добровольцем', 'value': 'рабочий'},
              {'emoji': '🔬', 'text': 'Присоединяюсь к разработке техники', 'value': 'технарь'},
              {'emoji': '📣', 'text': 'Поднимаю мораль духа народа', 'value': 'творец'},
              {'emoji': '🚑', 'text': 'Работаю в медсанбате', 'value': 'руководитель'}],
  'text': 'Ты оказался(лась) в 1943. Что делаешь?'},
 {'options': [{'emoji': '🐌', 'text': 'Медленные процессы и бюрократия', 'value': 'рабочий'},
              {'emoji': '📢', 'text': 'Когда никто не слушает', 'value': 'творец'},
              {'emoji': '📉',
               'text': 'Когда нет смысла в том, что делаешь',
               'value': 'руководитель'},
              {'emoji': '🚫', 'text': 'Когда не дают ничего делать руками', 'value': 'технарь'}],
  'text': 'Что тебя больше всего раздражает на работе?'},
 {'options': [{'emoji': '✏️', 'text': 'Карандаш и блокнот', 'value': 'руководитель'},
              {'emoji': '🔧', 'text': 'Гаечный ключ', 'value': 'технарь'},
              {'emoji': '📢', 'text': 'Микрофон', 'value': 'творец'},
              {'emoji': '👩\u200d🔬', 'text': 'Пробирка', 'value': 'рабочий'}],
  'text': 'Твой главный рабочий инструмент?'},
 {'options': [{'emoji': '🏅', 'text': 'Плакат с героями труда', 'value': 'рабочий'},
              {'emoji': '🎭', 'text': 'Афишу спектакля', 'value': 'творец'},
              {'emoji': '🧬', 'text': 'Схему строения молекулы', 'value': 'технарь'},
              {'emoji': '📜', 'text': 'Цитату Ленина или Гагарина', 'value': 'руководитель'}],
  'text': 'Что бы ты повесил(а) у себя на стене?'},
 {'options': [{'emoji': '🚀', 'text': 'Технологии и космос', 'value': 'технарь'},
              {'emoji': '📖', 'text': 'Образованных людей', 'value': 'руководитель'},
              {'emoji': '🎼', 'text': 'Искусство и свободу', 'value': 'творец'},
              {'emoji': '🔨', 'text': 'Много труда и больших строек', 'value': 'рабочий'}],
  'text': 'Когда ты слышишь слово «будущее», ты представляешь...'}]

# Здесь можно продолжить с добавлением всех вопросов

user_answers = {}

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_answers[user_id] = {"step": 0, "answers": []}
    await send_question(message.chat.id, user_id)

async def send_question(chat_id, user_id):
    step = user_answers[user_id]["step"]
    if step >= len(questions):
        await send_result(chat_id, user_id)
        return

    question = questions[step]
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    for option in question["options"]:
        keyboard.add(KeyboardButton(f"{option['emoji']} {option['text']}"))

    await bot.send_message(chat_id, f"*Вопрос {step+1}:*\n{question['text']}", parse_mode="Markdown", reply_markup=keyboard)

@dp.message_handler()
async def answer_handler(message: types.Message):
    user_id = message.from_user.id
    if user_id not in user_answers:
        return

    step = user_answers[user_id]["step"]
    if step >= len(questions):
        return

    options = questions[step]["options"]
    selected = None
    for option in options:
        if option["text"] in message.text:
            selected = option["value"]
            break

    if selected:
        user_answers[user_id]["answers"].append(selected)
        user_answers[user_id]["step"] += 1
        await send_question(message.chat.id, user_id)

async def send_result(chat_id, user_id):
    counts = Counter(user_answers[user_id]["answers"])
    top_prof = counts.most_common(1)[0][0]

    history = {
        "технарь": "Инженер: ключевая фигура индустриализации. Строил будущее страны.",
        "руководитель": "Партийный деятель: управлял процессами и вдохновлял массы.",
        "творец": "Художник или актёр: создавал смыслы, которые переживают эпоху.",
        "рабочий": "Рабочий: героическая профессия, двигал стройки века и заводы."
    }

    famous = {
        "технарь": "Сергей Королёв, Андрей Туполев",
        "руководитель": "Юрий Андропов, Лаврентий Берия",
        "творец": "Андрей Тарковский, Майя Плисецкая",
        "рабочий": "Алексей Стаханов, Пётр Кривоногов"
    }

    text = f"🔎 Ты — {top_prof.title()}!\n\n"            f"📜 {history.get(top_prof, 'Интересная профессия XX века!')}\n"            f"🎖 Знаменитые представители: {famous.get(top_prof, '—')}"

    await bot.send_message(chat_id, text, reply_markup=types.ReplyKeyboardRemove())
    user_answers.pop(user_id, None)

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp)


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer("Привет! Это «Плёнка судьбы»\nТест из 14 вопросов покажет, кем бы ты был(а) в XX веке.")
    await asyncio.sleep(1.5)
    await ask_question(message, 0)