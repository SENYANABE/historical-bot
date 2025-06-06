 (cd "$(git rev-parse --show-toplevel)" && git apply --3way <<'EOF' 
diff --git a/bot.py b/bot.py
index 2d246effe485deb24382ee24766ea69fc3e3bf0c..b69f43e89668194bf7bb2bcbf780516ea2827aad 100644
--- a/bot.py
+++ b/bot.py
@@ -102,68 +102,118 @@ questions = [
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
 
 # Состояние пользователя: какой вопрос и список ответов
 user_state = {}
 
+# Итоговая историческая справка
+info_text = """\
+🎞️ Плёнка судьбы: твоя профессия в XX веке
+
+Поздравляем, ты прошёл Телеграм-бот «Плёнка судьбы» и мы готовы заглянуть к тебе в душу и показать, кем бы ты жил(а) в прошлом веке. 👇👇👇
+
+🏭 Фабричный рабочий
+📜 Историческая справка:
+"Пятилетку — в четыре года!" Рабочий класс был "гегемоном" — ковал победы у станка. А ещё — бил рекорды, как стахановцы.
+🌟 Знаменитые представители:
+Алексей Гастев (поэт труда), Иван Овчинников (ударник производства).
+
+🔩 Технарь
+📽️ Кадр из прошлого:
+Если XX век — гигантский механизм, то технари были его главными часовщиками! Они собирали танки на конвейере, писали первые программы на перфокартах и запускали ракеты в космос. В СССР их называли "интеллектуальным пролетариатом" — без них не было бы ни спутника, ни атомной бомбы.
+🌟 Звёзды эпохи:
+• Сергей Королёв — сделал из ракет искусство, а из Гагарина — легенду
+• Лев Термен — изобрёл терменвокс (музыкальный инструмент, на котором играют… без прикосновений!)
+• Алексей Гастев — поэт труда, превративший рабочий процесс в науку
+
+💡 Интересно: Первые советские компьютеры занимали целые комнаты, а программисты вручную переключали лампы.
+
+🎨 Творец
+📽️ Кадр из прошлого:
+Время цензуры, подпольных выставок и песен, которые знала вся страна — даже если их не передавали по радио. Творцы были голосом эпохи: они писали "в стол", рисовали авангард в подвалах, а их фильмы становились культовыми, несмотря на запреты.
+🌟 Звёзды эпохи:
+• Владимир Высоцкий — пел так, что его голос записывали на рентгеновские снимки ("музыка на костях")
+• Михаил Булгаков — написал "Мастера и Маргариту" и спрятал рукопись на 30 лет
+• Людмила Гурченко — стала символом оттепели с одной лишь фразой: "Ах, как кружится голова!"
+
+💡 Интересно: Некоторые художники-нонконформисты выставлялись в квартирах — это называлось "квартирными выставками".
+
+🎬 Ну что же, ты узнал, какой будет твоя роль в истории?
+
+Доволен своим выбором? Если хочешь удостовериться, то проходи наш чат-бот ещё раз и убедись точно в своей профессии! 🔮"""
+
 def make_keyboard(opts):
     kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
     for o in opts:
         kb.add(KeyboardButton(f"{o['emoji']} {o['text']}"))
     return kb
 
 @dp.message_handler(commands=['start'])
 async def start_quiz(msg: types.Message):
     user_state[msg.chat.id] = {'idx': 0, 'answers': []}
-    await msg.answer("Привет! Это «Плёнка судьбы»\nТест из 14 вопросов покажет, кем бы ты был(а) в XX веке.")
+    # Отправляем приветственную картинку и описание теста
+    try:
+        with open("images/start.png", "rb") as photo:
+            await msg.answer_photo(photo, caption="Добро пожаловать в тест \u00ab\u041f\u043b\u0451\u043d\u043a\u0430 \u0441\u0443\u0434\u044c\u0431\u044b\u00bb!")
+    except Exception:
+        await msg.answer("Добро пожаловать в тест \u00ab\u041f\u043b\u0451\u043d\u043a\u0430 \u0441\u0443\u0434\u044c\u0431\u044b\u00bb!")
     await asyncio.sleep(1.5)
+    await msg.answer("Тест из 14 вопросов покажет, кем бы ты был(а) в XX веке.")
+    await asyncio.sleep(1.0)
     q = questions[0]
-    await msg.answer(f"Вопрос 1 из {len(questions)}:\n{q['text']}", reply_markup=make_keyboard(q['options']))
+    await msg.answer(
+        f"Вопрос 1 из {len(questions)}:\n{q['text']}",
+        reply_markup=make_keyboard(q['options'])
+    )
 
 @dp.message_handler(lambda m: m.chat.id in user_state)
 async def process_answer(m: types.Message):
     state = user_state[m.chat.id]
     idx = state['idx']
     # определяем выбор
     choice = None
     for o in questions[idx]['options']:
         if m.text.startswith(o['emoji']):
             choice = o['value']
             break
     if choice:
         state['answers'].append(choice)
     idx += 1
     if idx < len(questions):
         state['idx'] = idx
         q = questions[idx]
         await m.answer(f"Вопрос {idx+1} из {len(questions)}:\n{q['text']}", reply_markup=make_keyboard(q['options']))
     else:
         # подсчёт и вывод результата
         counts = {}
         for v in state['answers']:
             counts[v] = counts.get(v, 0) + 1
         res = max(counts, key=counts.get)
         names = {"технарь":"Технарь","руководитель":"Руководитель","творец":"Творец","рабочий":"Рабочий"}
-        await m.answer(f"📝 Ваш результат: {names.get(res, res)}", reply_markup=types.ReplyKeyboardRemove())
+        await m.answer(
+            f"📝 Ваш результат: {names.get(res, res)}",
+            reply_markup=types.ReplyKeyboardRemove(),
+        )
+        await m.answer(info_text)
         del user_state[m.chat.id]
 
 if __name__ == "__main__":
-    executor.start_polling(dp)
+    executor.start_polling(dp)
 
EOF
)