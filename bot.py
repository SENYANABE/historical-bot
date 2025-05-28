
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from collections import Counter

API_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

questions = [
    {
        "text": "Ты скорее...",
        "options": [
            {"emoji": "🔧", "text": "Люблю изобретать и чинить", "value": "технарь"},
            {"emoji": "💬", "text": "Общаюсь с людьми и руковожу", "value": "руководитель"},
            {"emoji": "🎭", "text": "Мечтаю и создаю искусство", "value": "творец"},
            {"emoji": "💪", "text": "Работаю руками, мне не страшен труд", "value": "рабочий"}
        ,
    {"text": "Что бы ты взял(а) с собой в командировку в 1965?", "options": ['📕 Записную книжку и перо', '📷 Плёнку, чтобы снимать хронику', '🔬 Мини-микроскоп — мало ли', '🥾 Кирзовые сапоги, вдруг стройка']},
    {"text": "Выбери идеальное рабочее место:", "options": ['🏭 Завод с гулом станков', '📚 Кабинет с книгами и бумагами', '🎬 Съёмочная площадка или сцена', '✈️ Кабина пилота или командный пункт']},
    {"text": "Ты получил(а) срочную телеграмму из ЦК. Твоя реакция?", "options": ['📬 Немедленно докладываю начальству — это важно', '🧪 Анализирую данные, вдруг это эксперимент', '✍️ Превращаю в сценарий — звучит кинематографично', '🤷\u200d♂️ Сначала доделаю смену, потом всё остальное']},
    {"text": "На улицу выбросили редкий трофейный магнитофон 1950-х. Что ты сделаешь?", "options": ['🔧 Починю! Это настоящая находка', '🎤 Использую как реквизит в пьесе', '📻 Отдам на завод, пусть пускают в производство', '📚 Поищу информацию о нём — может, он шпионский']},
    {"text": "Тебе дали предмет: слайдоскоп. Что ты думаешь?", "options": ['🔍 Отличный прибор — можно изучать кристаллы', '📸 Использую для домашней лекции', '🖼 Превращу в часть сценографии', '❓ Не знаю, что это, но кручу и верчу']},
    {"text": "Тебе дают выбор командировки. Куда поедешь?", "options": ['🚂 На Байкало-Амурскую магистраль', '🎭 В Дом творчества в Переделкино', '🧪 В закрытую лабораторию', '🧱 На восстановление села после войны']},
    {"text": "Ты оказался(лась) в 1943. Что делаешь?", "options": ['⚔️ Иду на фронт добровольцем', '🔬 Присоединяюсь к разработке техники', '📣 Поднимаю мораль духа народа', '🚑 Работаю в медсанбате']},
    {"text": "Что тебя больше всего раздражает на работе?", "options": ['🐌 Медленные процессы и бюрократия', '📢 Когда никто не слушает', '📉 Когда нет смысла в том, что делаешь', '🚫 Когда не дают ничего делать руками']},
    {"text": "Твой главный рабочий инструмент?", "options": ['✏️ Карандаш и блокнот', '🔧 Гаечный ключ', '📢 Микрофон', '👩\u200d🔬 Пробирка']},
    {"text": "Что бы ты повесил(а) у себя на стене?", "options": ['🏅 Плакат с героями труда', '🎭 Афишу спектакля', '🧬 Схему строения молекулы', '📜 Цитату Ленина или Гагарина']},
    {"text": "Когда ты слышишь слово «будущее», ты представляешь...", "options": ['🚀 Технологии и космос', '📖 Образованных людей', '🎼 Искусство и свободу', '🔨 Много труда и больших строек']}]
    },
    {
        "text": "Как ты относишься к риску?",
        "options": [
            {"emoji": "😌", "text": "Предпочитаю стабильность и порядок", "value": "руководитель"},
            {"emoji": "💥", "text": "Люблю, когда адреналин кипит", "value": "рабочий"},
            {"emoji": "🧠", "text": "Главное — интерес, риск пусть будет", "value": "технарь"},
            {"emoji": "🚜", "text": "Мне всё равно, работа — это дело", "value": "рабочий"}
        ]
    },
    {
        "text": "Какая сцена тебе ближе?",
        "options": [
            {"emoji": "🎤", "text": "Выступление перед публикой", "value": "творец"},
            {"emoji": "🧪", "text": "Демонстрация нового эксперимента", "value": "технарь"},
            {"emoji": "👮", "text": "Заявление в духе 'порядок будет!'", "value": "руководитель"},
            {"emoji": "👷", "text": "Работа в цеху у станка", "value": "рабочий"}
        ]
    }
    # ... Остальные 11 вопросов будут добавлены по аналогии
]

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
