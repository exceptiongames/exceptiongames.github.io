#!/usr/bin/env python3
"""Builds every page of the exception games site from the texts below.

Run `python3 build.py` from this folder after changing any text, then commit the
generated HTML together with this file. Standard library only.

Languages: English is the main one (the App Store links point to it), Ukrainian
is the second, Russian the third. Each page lives at <page>/ (English),
<page>/uk/ and <page>/ru/.
"""
import html
import os

LANGS = [("en", "English"), ("uk", "Українська"), ("ru", "Русский")]
EMAIL = "exceptiongames@icloud.com"
MAIL = f'<a href="mailto:{EMAIL}">{EMAIL}</a>'
UPDATED = {"en": "October 11, 2026", "uk": "11 жовтня 2026 р.", "ru": "11 октября 2026 г."}

# Page paths, relative to the site root, without the language folder.
HOME, GAME, PRIVACY, SUPPORT = "", "living-factory/", "living-factory/privacy-policy/", "living-factory/support/"

UI = {
    "en": dict(game="Living Factory", privacy="Privacy Policy", nav_privacy="Privacy", support="Support", nav="Main",
               lang="Language", footer="exception games"),
    "uk": dict(game="Жива фабрика", privacy="Політика конфіденційності", nav_privacy="Конфіденційність", support="Підтримка", nav="Головне меню",
               lang="Мова", footer="exception games"),
    "ru": dict(game="Живая фабрика", privacy="Политика конфиденциальности", nav_privacy="Конфиденциальность", support="Поддержка", nav="Главное меню",
               lang="Язык", footer="exception games"),
}

# ---------------------------------------------------------------- texts

HOME_TEXT = {
    "en": dict(title="exception games",
               desc="exception games is an independent developer of small, calm games for iPhone.",
               lead="An independent developer of small, calm games for iPhone.",
               card="An ant-colony logic puzzle for iPhone."),
    "uk": dict(title="exception games",
               desc="exception games — незалежний розробник невеликих спокійних ігор для iPhone.",
               lead="Незалежний розробник невеликих спокійних ігор для iPhone.",
               card="Логічна головоломка про мурашину колонію для iPhone."),
    "ru": dict(title="exception games",
               desc="exception games — независимый разработчик небольших спокойных игр для iPhone.",
               lead="Независимый разработчик небольших спокойных игр для iPhone.",
               card="Логическая головоломка про муравьиную колонию для iPhone."),
}

GAME_TEXT = {
    "en": dict(
        lead="An ant-colony logic puzzle for iPhone by exception games.",
        body=[
            "Send signals along rows and columns, move across soil and leaves, and lead every ant to its nest. "
            "Fifty handcrafted workshops in four chapters, a new workshop of the day every day, and a secret hidden in every workshop.",
            "Made for the whole family: a hint for when you are stuck, a step-by-step introduction to every new tile, "
            "instructions read aloud for children who cannot read yet, and several players on one iPhone.",
            "No ads, no purchases for real money, no accounts, no timer. No internet needed.",
        ],
        facts="iPhone · iOS 18 or later · 43 languages"),
    "uk": dict(
        lead="Логічна головоломка про мурашину колонію для iPhone від exception games.",
        body=[
            "Надсилайте сигнали вздовж рядів і стовпців, пересувайтеся по землі й листках і приведіть кожну мурашку до нірки. "
            "П’ятдесят цехів у чотирьох розділах, щодня новий цех дня і секрет у кожному цеху.",
            "Для всієї родини: підказка, коли щось не виходить, покрокове знайомство з кожною новою клітинкою, "
            "озвучення завдань для дітей, які ще не вміють читати, і кілька гравців на одному iPhone.",
            "Без реклами, без покупок за справжні гроші, без облікових записів і без таймера. Інтернет не потрібен.",
        ],
        facts="iPhone · iOS 18 або новіша · 43 мови"),
    "ru": dict(
        lead="Логическая головоломка про муравьиную колонию для iPhone от exception games.",
        body=[
            "Отправляйте сигналы по рядам и столбцам, шагайте по земле и листьям и приведите каждого муравья в норку. "
            "Пятьдесят цехов в четырёх главах, каждый день новый цех дня и секрет в каждом цехе.",
            "Для всей семьи: подсказка, когда что-то не получается, пошаговое знакомство с каждой новой клеткой, "
            "озвучка заданий для детей, которые ещё не умеют читать, и несколько игроков на одном iPhone.",
            "Без рекламы, без покупок за реальные деньги, без аккаунтов и без таймера. Интернет не нужен.",
        ],
        facts="iPhone · iOS 18 или новее · 43 языка"),
}

# Each section is (heading, [paragraphs]). Paragraph strings may contain HTML.
# Owner decisions of October 11, 2026: support mail is kept up to 12 months after the question is
# resolved; the responsible party is the developer shown as the seller on the App Store page.
PRIVACY_TEXT = {
    "en": dict(
        effective="Effective date",
        intro="Living Factory (“the app”) is an ant-colony logic puzzle game for iPhone. exception games is the trade name "
              "of its developer, the person or company shown as the seller on the app’s App Store page, who is responsible "
              "for this policy (“we”). This policy explains what happens to information in the app, on this website and "
              "in messages to support.",
        summary="In short: the app collects no data. Everything it saves stays on your iPhone, unless a grown-up saves a backup copy somewhere else.",
        sections=[
            ("Data the app collects", ["None. The app does not collect, transmit, sell or share any personal data. It contains no "
                                       "advertising, analytics, accounts, tracking or third-party SDKs, and it does not connect "
                                       "to the internet."]),
            ("Data stored on your device", [
                "Game progress (current workshop, unfinished games with undo history, completed workshops, best results and stars, "
                "results of the Workshop of the day, which workshops were solved with a hint, ants bought with stars, found secrets "
                "and how far their hints have opened, tutorial status), the names of players added on this device, and the sound, "
                "haptics and read-aloud settings are stored locally on your device using Apple’s standard app storage.",
                "Player names are optional; you can keep the default “Player 2” and so on. The app never sends this data anywhere. "
                "It may be included in your own device backups under Apple’s terms, and in a backup copy that a grown-up saves "
                "(see “Backup copy”)."]),
            ("Reading aloud", ["When reading aloud is on, the app speaks the puzzle instructions with the speech synthesizer built "
                               "into iOS on the device. No text or audio leaves the device, and the app never uses the microphone."]),
            ("Motion sensor", ["Only while the result of a solved workshop is on the screen, the app reads the iPhone’s motion "
                               "sensor on the device to notice playful moves that reveal hidden secrets, such as a gentle shake or "
                               "turning the phone over. The readings are never stored or sent. The app does not use location, "
                               "the camera, contacts or photos."]),
            ("Third parties", [
                "The app shares no data with anyone: it contains no third-party code and talks to no servers. Apple handles "
                "downloads, updates and device backups under Apple’s own privacy policy.",
                "If you chose in iOS settings to share analytics with app developers, Apple may give us anonymous crash reports "
                "and aggregated statistics that do not identify you."]),
            ("Keeping and deleting data", [
                "Data stays on your iPhone until you delete it. To remove one player’s progress, open Settings → Players, switch "
                "to another player and delete that one (a grown-up confirms it). The player who is playing now cannot be "
                "deleted. Deleting the app removes all players and all data from your device.",
                "The app never sends us your data, so there is nothing from the app for us to keep, look up or delete."]),
            ("Backup copy", [
                "In Settings → Backup copy, after passing the parental gate, a grown-up can save every player’s progress, the "
                "players’ names and the sound, haptics and read-aloud settings as one file. The file goes wherever the grown-up "
                "chooses in the Files window, for example on this iPhone or in iCloud Drive under Apple’s terms. The app never "
                "sends the file anywhere and keeps no copy of its own, and we never receive it.",
                "Restoring a copy, also behind the parental gate, replaces all players and their progress on the device with the "
                "ones in the file. Deleting the app does not delete a saved copy: delete the file in Files when you no longer "
                "need it."]),
            ("Messages to support", [
                "If you write to us, we receive your e-mail address and anything you include (for example, a screenshot). "
                "We use it only to answer you, share it with no one, and delete the correspondence within 12 months after the "
                "question is resolved, or sooner on request. E-mail is delivered by Apple’s iCloud Mail. Please ask a grown-up "
                "to write to us, not a child."]),
            ("This website", ["This website uses no cookies or analytics. It is hosted on GitHub Pages, which may log visitors’ "
                              "IP addresses for security under GitHub’s privacy statement."]),
            ("Children", [
                "The game is made for children and families. It does not knowingly collect any information from anyone, "
                "including children under 13. There are no ads, no purchases for real money, no accounts, no chat and no "
                "social media links. The ant shop uses only stars earned in the game.",
                "Pages outside the game, such as this policy and the support page, open only after a grown-up passes a "
                "parental gate, and so do saving and restoring a backup copy. Because the app collects no personal information, there is no data collection for a parent "
                "to consent to."]),
            ("Your rights", [f"Privacy laws such as the EU General Data Protection Regulation (GDPR) give you the right to ask what "
                             f"personal data we hold about you, and to have it corrected or deleted. The app gives us none; the "
                             f"only data we may hold is your messages to support. To ask about it or to have it deleted, write to "
                             f"{MAIL}. You may also complain to your local data protection authority."]),
            ("Changes", ["If a future version changes how data is handled, this page will be updated before that version is "
                         "released, and the effective date above will change."]),
            ("Contact", [f"exception games · {MAIL}"]),
        ]),
    "uk": dict(
        effective="Дата набрання чинності",
        intro="«Жива фабрика» (далі — «застосунок») — логічна головоломка про мурашину колонію для iPhone. exception games — "
              "торгова назва її розробника, тобто особи чи компанії, зазначеної як продавець на сторінці застосунку в App Store, "
              "яка відповідає за цю політику («ми»). Ця політика пояснює, що відбувається з інформацією в застосунку, на цьому "
              "сайті та в листах до підтримки.",
        summary="Коротко: застосунок не збирає жодних даних. Усе, що він зберігає, залишається на вашому iPhone, якщо тільки дорослий не збереже резервну копію деінде.",
        sections=[
            ("Які дані збирає застосунок", ["Жодних. Застосунок не збирає, не передає, не продає й не розкриває жодних персональних "
                                            "даних. У ньому немає реклами, аналітики, облікових записів, відстеження та сторонніх "
                                            "SDK, і він не підключається до інтернету."]),
            ("Що зберігається на пристрої", [
                "Прогрес гри (поточний цех, незавершені партії з історією скасування, пройдені цехи, найкращі результати та зірки, "
                "результати цеху дня, позначки про цехи, розв’язані з підказкою, куплені за зірки мурашки, знайдені секрети й "
                "відкриті до них підказки, стан навчання), імена гравців, доданих на цьому пристрої, а також налаштування звуку, "
                "вібрації та читання вголос зберігаються локально стандартними засобами iOS.",
                "Імена вказувати не обов’язково: можна залишити «Гравець 2» тощо. Застосунок нікуди не надсилає ці дані. "
                "Вони можуть потрапити до ваших резервних копій пристрою відповідно до умов Apple, а також до резервної копії, "
                "яку збереже дорослий (див. «Резервна копія»)."]),
            ("Читання вголос", ["Коли читання вголос увімкнено, застосунок озвучує завдання вбудованим синтезатором мовлення iOS на "
                                "самому пристрої. Текст і звук не виходять за межі пристрою; мікрофон застосунок не використовує."]),
            ("Датчик руху", ["Лише поки на екрані результат розв’язаного цеху, застосунок зчитує дані датчика руху iPhone на самому "
                             "пристрої, щоб помітити ігрові рухи, які відкривають сховані секрети, наприклад легке струшування "
                             "або перевертання телефона. Показання ніде не зберігаються й нікуди не передаються. Застосунок не "
                             "використовує геолокацію, камеру, контакти чи фото."]),
            ("Треті сторони", [
                "Застосунок ні з ким не ділиться даними: у ньому немає стороннього коду, і він не звертається до жодних серверів. "
                "Завантаження, оновлення та резервні копії пристрою обробляє Apple відповідно до власної політики конфіденційності.",
                "Якщо в налаштуваннях iOS ви дозволили ділитися аналітикою з розробниками, Apple може надавати нам анонімні звіти "
                "про збої та узагальнену статистику, які не дають змоги вас ідентифікувати."]),
            ("Зберігання та видалення даних", [
                "Дані залишаються на вашому iPhone, доки ви їх не видалите. Щоб видалити прогрес одного гравця, відкрийте "
                "«Налаштування» → «Гравці», перейдіть на іншого гравця й видаліть потрібного (дорослий підтверджує дію). Гравця, "
                "який зараз грає, видалити не можна. Видалення застосунку стирає всіх гравців і всі дані з пристрою.",
                "Застосунок ніколи не надсилає нам ваших даних, тому з застосунку на нашому боці немає чого зберігати, шукати чи "
                "видаляти."]),
            ("Резервна копія", [
                "У розділі «Налаштування» → «Резервна копія», після батьківської перевірки, дорослий може зберегти прогрес усіх "
                "гравців, їхні імена та налаштування звуку, вібрації й читання вголос в одному файлі. Файл потрапляє туди, куди "
                "дорослий вибере у вікні «Файли», наприклад на цей iPhone або в iCloud Drive відповідно до умов Apple. Застосунок "
                "нікуди не надсилає файл і не зберігає власної копії, а ми ніколи його не отримуємо.",
                "Відновлення копії, теж після батьківської перевірки, замінює всіх гравців і їхній прогрес на пристрої тими, що є "
                "у файлі. Видалення застосунку не видаляє збережену копію: видаліть файл у «Файлах», коли він більше не потрібен."]),
            ("Листи до підтримки", [
                "Якщо ви нам напишете, ми отримаємо вашу адресу електронної пошти та все, що ви додасте до листа (наприклад, знімок "
                "екрана). Ми використовуємо ці дані лише для відповіді, нікому їх не передаємо й видаляємо листування протягом "
                "12 місяців після розв’язання питання або раніше на ваш запит. Пошту доставляє iCloud Mail від Apple. Просимо, "
                "щоб нам писав дорослий, а не дитина."]),
            ("Цей сайт", ["Цей сайт не використовує файли cookie й аналітику. Його розміщено на GitHub Pages, який може записувати "
                          "IP-адреси відвідувачів з міркувань безпеки відповідно до положення GitHub про конфіденційність."]),
            ("Діти", [
                "Гра створена для дітей і родин. Вона свідомо не збирає жодної інформації ні про кого, зокрема про дітей до 13 "
                "років. У ній немає реклами, покупок за справжні гроші, облікових записів, чату та посилань на соціальні мережі. "
                "У крамниці мурашок можна платити лише зірками, заробленими в грі.",
                "Сторінки поза грою, як-от ця політика та сторінка підтримки, відкриваються лише після того, як дорослий пройде "
                "батьківську перевірку; так само захищені збереження й відновлення резервної копії. Застосунок не збирає персональної інформації, тож немає збору даних, на який батьки мали б "
                "давати згоду."]),
            ("Ваші права", [f"Законодавство про захист персональних даних, зокрема Загальний регламент ЄС про захист даних (GDPR), "
                            f"дає вам право дізнатися, які ваші персональні дані ми маємо, і вимагати їх виправлення чи видалення. "
                            f"Застосунок не передає нам жодних даних; єдине, що ми можемо мати, — ваші листи до підтримки. Щоб "
                            f"запитати про них або попросити їх видалити, напишіть на {MAIL}. Ви також можете звернутися зі скаргою "
                            f"до органу із захисту персональних даних у вашій країні."]),
            ("Зміни", ["Якщо майбутня версія змінить роботу з даними, цю сторінку буде оновлено до виходу такої версії, а дату "
                       "набрання чинності вгорі буде змінено."]),
            ("Контакти", [f"exception games · {MAIL}"]),
        ]),
    "ru": dict(
        effective="Дата вступления в силу",
        intro="«Живая фабрика» (далее — «приложение») — логическая головоломка про муравьиную колонию для iPhone. exception games — "
              "торговое имя её разработчика, то есть человека или компании, указанных продавцом на странице приложения в App Store, "
              "которые отвечают за эту политику («мы»). Эта политика объясняет, что происходит с информацией в приложении, на этом "
              "сайте и в письмах в поддержку.",
        summary="Коротко: приложение не собирает никаких данных. Всё, что оно сохраняет, остаётся на вашем iPhone, если только взрослый не сохранит резервную копию в другом месте.",
        sections=[
            ("Какие данные собирает приложение", ["Никаких. Приложение не собирает, не передаёт, не продаёт и не раскрывает "
                                                  "персональные данные. В нём нет рекламы, аналитики, аккаунтов, отслеживания и "
                                                  "сторонних SDK; приложение не подключается к интернету."]),
            ("Что хранится на устройстве", [
                "Прогресс игры (текущий цех, незавершённые партии с историей отмены, пройденные цеха, лучшие результаты и звёзды, "
                "результаты цеха дня, отметки о цехах, решённых с подсказкой, купленные за звёзды муравьи, найденные секреты и "
                "открытые к ним подсказки, состояние обучения), имена игроков, добавленных на этом устройстве, и настройки звука, "
                "вибрации и чтения вслух хранятся локально стандартными средствами iOS.",
                "Имена указывать не обязательно: можно оставить «Игрок 2» и т. д. Приложение никуда не отправляет эти данные. "
                "Они могут попасть в ваши резервные копии устройства в соответствии с условиями Apple, а также в резервную копию, "
                "которую сохранит взрослый (см. «Резервная копия»)."]),
            ("Чтение вслух", ["Когда чтение вслух включено, приложение озвучивает задания встроенным синтезатором речи iOS на самом "
                              "устройстве. Текст и звук не покидают устройство; микрофон приложение не использует."]),
            ("Датчик движения", ["Только пока на экране результат решённого цеха, приложение считывает данные датчика движения iPhone "
                                 "на самом устройстве, чтобы заметить игровые движения, которые открывают спрятанные секреты, "
                                 "например лёгкое встряхивание или переворот телефона. Показания нигде не сохраняются и никуда не "
                                 "передаются. Приложение не использует геолокацию, камеру, контакты и фото."]),
            ("Третьи стороны", [
                "Приложение ни с кем не делится данными: в нём нет стороннего кода, и оно не обращается ни к каким серверам. "
                "Загрузки, обновления и резервные копии устройства обрабатывает Apple в соответствии с собственной политикой "
                "конфиденциальности.",
                "Если в настройках iOS вы разрешили делиться аналитикой с разработчиками, Apple может передавать нам анонимные "
                "отчёты о сбоях и обобщённую статистику, которые не позволяют вас идентифицировать."]),
            ("Хранение и удаление данных", [
                "Данные остаются на вашем iPhone, пока вы их не удалите. Чтобы удалить прогресс одного игрока, откройте "
                "«Настройки» → «Игроки», переключитесь на другого игрока и удалите нужного (взрослый подтверждает действие). "
                "Игрока, который сейчас играет, удалить нельзя. Удаление приложения стирает всех игроков и все данные с устройства.",
                "Приложение никогда не отправляет нам ваши данные, поэтому из приложения на нашей стороне нечего хранить, искать "
                "или удалять."]),
            ("Резервная копия", [
                "В разделе «Настройки» → «Резервная копия», после родительской проверки, взрослый может сохранить прогресс всех "
                "игроков, их имена и настройки звука, вибрации и чтения вслух в одном файле. Файл попадает туда, куда взрослый "
                "выберет в окне «Файлы», например на этот iPhone или в iCloud Drive в соответствии с условиями Apple. Приложение "
                "никуда не отправляет файл и не хранит собственной копии, а мы никогда его не получаем.",
                "Восстановление копии, тоже после родительской проверки, заменяет всех игроков и их прогресс на устройстве теми, "
                "что есть в файле. Удаление приложения не удаляет сохранённую копию: удалите файл в «Файлах», когда он больше не "
                "нужен."]),
            ("Письма в поддержку", [
                "Если вы нам напишете, мы получим ваш адрес электронной почты и всё, что вы приложите к письму (например, снимок "
                "экрана). Мы используем эти данные только для ответа, никому их не передаём и удаляем переписку в течение "
                "12 месяцев после решения вопроса или раньше по вашей просьбе. Почту доставляет iCloud Mail от Apple. Просим, "
                "чтобы нам писал взрослый, а не ребёнок."]),
            ("Этот сайт", ["Этот сайт не использует файлы cookie и аналитику. Он размещён на GitHub Pages, который может записывать "
                           "IP-адреса посетителей в целях безопасности согласно положению GitHub о конфиденциальности."]),
            ("Дети", [
                "Игра создана для детей и семей. Она сознательно не собирает никакой информации ни о ком, включая детей младше 13 "
                "лет. В ней нет рекламы, покупок за реальные деньги, аккаунтов, чата и ссылок на соцсети. В магазине муравьёв "
                "платят только звёздами, заработанными в игре.",
                "Страницы вне игры, например эта политика и страница поддержки, открываются только после того, как взрослый "
                "пройдёт родительскую проверку; так же защищены сохранение и восстановление резервной копии. Приложение не собирает персональную информацию, поэтому нет сбора данных, на "
                "который родители должны были бы давать согласие."]),
            ("Ваши права", [f"Законодательство о защите персональных данных, например Общий регламент ЕС по защите данных (GDPR), "
                            f"даёт вам право узнать, какие ваши персональные данные у нас есть, и потребовать их исправления или "
                            f"удаления. Приложение не передаёт нам никаких данных; единственное, что у нас может быть, — ваши "
                            f"письма в поддержку. Чтобы спросить о них или попросить их удалить, напишите на {MAIL}. Вы также "
                            f"можете подать жалобу в орган по защите персональных данных в вашей стране."]),
            ("Изменения", ["Если будущая версия изменит обработку данных, эта страница будет обновлена до выхода такой версии, а "
                           "дата вступления в силу вверху изменится."]),
            ("Контакты", [f"exception games · {MAIL}"]),
        ]),
}

SUPPORT_TEXT = {
    "en": dict(
        intro="Living Factory is an ant-colony logic puzzle game for iPhone by exception games.",
        contact_h="Contact", contact=f"Write to {MAIL}. We read every message and answer in English, Ukrainian or Russian.",
        bug="Reporting a bug? Please include your iPhone model, iOS version, the workshop number and what happened. A screenshot helps.",
        faq_h="Questions and answers",
        faq=[
            ("Where is my progress saved?", "Only on your iPhone. The game has no accounts and no cloud sync. Deleting the app erases all progress, so update the app without deleting it."),
            ("How do I start a workshop over?", "Tap Restart. To replay the tutorial, open Settings → Replay tutorial."),
            ("I’m stuck. What can I do?", "Tap Undo to take back the last signal, or tap Hint to see the next signal. A workshop solved with a hint earns one star; tap Restart and solve it on your own for more. The workshop of the day has no hint."),
            ("Can several people play on one iPhone?", "Yes. Add players in Settings → Players. Each player has their own stars, records and ants."),
            ("How do I keep progress safe or move it to another iPhone?", "Ask a grown-up to open Settings → Backup copy → Save a copy and keep the file in Files, for example in iCloud Drive. On the other iPhone, or if the game ever starts from scratch, use Restore from a copy. Restoring replaces the progress on that iPhone."),
            ("Are there ads or in-app purchases?", "No. There are no ads and no purchases for real money. Ants in the shop are bought with stars earned in the game."),
            ("Does the game collect data?", "No. There are no analytics, accounts or tracking. See the <a href=\"{privacy}\">Privacy Policy</a>."),
            ("Which devices are supported?", "iPhone with iOS 18 or later. The game works without the internet."),
        ]),
    "uk": dict(
        intro="«Жива фабрика» — логічна головоломка про мурашину колонію для iPhone від exception games.",
        contact_h="Зв’язок", contact=f"Пишіть на {MAIL}. Ми читаємо кожен лист і відповідаємо українською, англійською або російською.",
        bug="Знайшли помилку? Вкажіть модель iPhone, версію iOS, номер цеху й опишіть, що сталося. Знімок екрана дуже допоможе.",
        faq_h="Запитання та відповіді",
        faq=[
            ("Де зберігається прогрес?", "Лише на вашому iPhone: облікових записів і хмарної синхронізації немає. Видалення застосунку стирає весь прогрес, тому оновлюйте застосунок, не видаляючи його."),
            ("Як почати цех заново?", "Натисніть «Заново». Щоб повторити навчання, відкрийте «Налаштування» → «Повторити навчання»."),
            ("Не виходить розв’язати. Що робити?", "Натисніть «Скасувати», щоб скасувати останній сигнал, або «Підказка», щоб побачити наступний сигнал. За цех, розв’язаний із підказкою, нараховується лише одна зірка; натисніть «Заново» й розв’яжіть його самостійно, щоб отримати більше. У цеху дня підказки немає."),
            ("Чи можуть грати кілька людей на одному iPhone?", "Так. Додайте гравців у «Налаштування» → «Гравці». У кожного свої зірки, рекорди й мурашки."),
            ("Як зберегти прогрес або перенести його на інший iPhone?", "Попросіть дорослого відкрити «Налаштування» → «Резервна копія» → «Зберегти копію» й покласти файл у «Файли», наприклад в iCloud Drive. На іншому iPhone або якщо гра колись почнеться з нуля, натисніть «Відновити з копії». Відновлення замінює прогрес на тому iPhone."),
            ("Чи є реклама або покупки в застосунку?", "Ні. Реклами й покупок за справжні гроші немає. Мурашок у крамниці купують за зірки, зароблені в грі."),
            ("Чи збирає гра дані?", "Ні: ні аналітики, ні облікових записів, ні відстеження. Докладніше — у <a href=\"{privacy}\">політиці конфіденційності</a>."),
            ("Які пристрої підтримуються?", "iPhone з iOS 18 або новішою. Гра працює без інтернету."),
        ]),
    "ru": dict(
        intro="«Живая фабрика» — логическая головоломка про муравьиную колонию для iPhone от exception games.",
        contact_h="Связь", contact=f"Пишите на {MAIL}. Мы читаем каждое письмо и отвечаем на русском, украинском или английском.",
        bug="Нашли ошибку? Укажите модель iPhone, версию iOS, номер цеха и опишите, что произошло. Снимок экрана очень поможет.",
        faq_h="Вопросы и ответы",
        faq=[
            ("Где хранится прогресс?", "Только на вашем iPhone: аккаунтов и облачной синхронизации нет. Удаление приложения стирает весь прогресс, поэтому обновляйте приложение, не удаляя его."),
            ("Как начать цех заново?", "Нажмите «Заново». Чтобы повторить обучение, откройте «Настройки» → «Повторить обучение»."),
            ("Не получается решить. Что делать?", "Нажмите «Отменить», чтобы отменить последний сигнал, или «Подсказка», чтобы увидеть следующий сигнал. За цех, решённый с подсказкой, даётся одна звезда; нажмите «Заново» и решите его сами, чтобы получить больше. В цехе дня подсказки нет."),
            ("Могут ли играть несколько человек на одном iPhone?", "Да. Добавьте игроков в «Настройки» → «Игроки». У каждого свои звёзды, рекорды и муравьи."),
            ("Как сберечь прогресс или перенести его на другой iPhone?", "Попросите взрослого открыть «Настройки» → «Резервная копия» → «Сохранить копию» и положить файл в «Файлы», например в iCloud Drive. На другом iPhone или если игра когда-нибудь начнётся с нуля, нажмите «Восстановить из копии». Восстановление заменяет прогресс на том iPhone."),
            ("Есть ли реклама или покупки в приложении?", "Нет. Рекламы и покупок за реальные деньги нет. Муравьёв в магазине покупают за звёзды, заработанные в игре."),
            ("Собирает ли игра данные?", "Нет: ни аналитики, ни аккаунтов, ни отслеживания. Подробнее — в <a href=\"{privacy}\">политике конфиденциальности</a>."),
            ("Какие устройства поддерживаются?", "iPhone с iOS 18 или новее. Игра работает без интернета."),
        ]),
}

# ---------------------------------------------------------------- rendering

def url(page, lang):
    """Site-root-relative path of a page in a language."""
    return page + ("" if lang == "en" else lang + "/")


def rel(from_path, to_path):
    """Relative link between two folder-style paths ("" is the root)."""
    depth = from_path.count("/")
    return ("../" * depth) + to_path or "./"


def render(page, lang, title, desc, body):
    here = url(page, lang)
    up = "../" * here.count("/")
    ui = UI[lang]
    nav = [(GAME, ui["game"]), (PRIVACY, ui["nav_privacy"]), (SUPPORT, ui["support"])]
    nav_html = "\n".join(
        f'      <a href="{rel(here, url(p, lang))}"{" aria-current=\"page\"" if p == page else ""}>{html.escape(t)}</a>'
        for p, t in nav)
    switch = '<span class="globe" aria-hidden="true">🌐</span>' + "".join(
        f'<span aria-current="true">{name}</span>' if code == lang
        else f'<a href="{rel(here, url(page, code))}" hreflang="{code}" lang="{code}">{name}</a>'
        for code, name in LANGS)
    alternates = "\n".join(
        f'  <link rel="alternate" hreflang="{code}" href="https://exceptiongames.github.io/{url(page, code)}">'
        for code, _ in LANGS)
    return f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(desc)}">
  <link rel="canonical" href="https://exceptiongames.github.io/{here}">
{alternates}
  <link rel="alternate" hreflang="x-default" href="https://exceptiongames.github.io/{page}">
  <link rel="icon" type="image/png" sizes="32x32" href="{up}assets/exception-games-favicon.png">
  <link rel="apple-touch-icon" href="{up}assets/exception-games-touch-icon.png">
  <meta name="theme-color" content="#FFF9EA" media="(prefers-color-scheme: light)">
  <meta name="theme-color" content="#2A211A" media="(prefers-color-scheme: dark)">
  <link rel="stylesheet" href="{up}assets/style.css">
</head>
<body>
<a class="skip" href="#main">{ {"en": "Skip to content", "uk": "До змісту", "ru": "К содержанию"}[lang] }</a>
<header class="site">
  <div class="wrap">
    <a class="brand" href="{rel(here, url(HOME, lang))}"><picture>
      <source srcset="{up}assets/exception-games-logo-dark.png" media="(prefers-color-scheme: dark)">
      <img src="{up}assets/exception-games-logo.png" width="1170" height="130" alt="exception games">
    </picture></a>
    <nav class="site" aria-label="{ui["nav"]}">
{nav_html}
    </nav>
  </div>
  <div class="wrap langs">
    <nav class="lang-switch" aria-label="{ui["lang"]}">{switch}</nav>
  </div>
</header>
<main id="main" class="wrap">
{body.strip()}
</main>
<footer class="site">
  <div class="wrap">© 2026 {ui["footer"]}<span aria-hidden="true"> · </span><span class="nowrap">{MAIL}</span></div>
</footer>
</body>
</html>
'''


def write(page, lang, title, desc, body):
    path = url(page, lang) + "index.html"
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(render(page, lang, title, desc, body))


def build():
    for lang, _ in LANGS:
        ui, here = UI[lang], None
        # Home
        t = HOME_TEXT[lang]
        here = url(HOME, lang)
        write(HOME, lang, t["title"], t["desc"], f'''
<h1>{t["lead"]}</h1>
<div class="card">
  <img src="{"../" * here.count("/")}assets/exception-games-mark.png" width="256" height="256" alt="">
  <div>
    <h2><a href="{rel(here, url(GAME, lang))}">{ui["game"]}</a></h2>
    <p>{t["card"]}</p>
    <p class="meta"><a href="{rel(here, url(PRIVACY, lang))}">{ui["privacy"]}</a><span aria-hidden="true"> · </span><a href="{rel(here, url(SUPPORT, lang))}">{ui["support"]}</a></p>
  </div>
</div>''')
        # Game
        g = GAME_TEXT[lang]
        here = url(GAME, lang)
        paras = "\n".join(f"<p>{p}</p>" for p in g["body"])
        write(GAME, lang, f'{ui["game"]} — exception games', g["lead"], f'''
<img class="hero-mark" src="{"../" * here.count("/")}assets/exception-games-mark.png" width="256" height="256" alt="">
<h1>{ui["game"]}</h1>
<p class="lead">{g["lead"]}</p>
{paras}
<p class="meta">{g["facts"]}</p>
<div class="buttons">
  <a class="button primary" href="{rel(here, url(SUPPORT, lang))}">{ui["support"]}</a>
  <a class="button" href="{rel(here, url(PRIVACY, lang))}">{ui["privacy"]}</a>
</div>''')
        # Privacy
        p = PRIVACY_TEXT[lang]
        secs = "\n".join(
            f"<h2>{h}</h2>\n" + "\n".join(f"<p>{x}</p>" for x in xs) for h, xs in p["sections"])
        write(PRIVACY, lang, f'{ui["privacy"]} — {ui["game"]}', p["summary"], f'''
<h1>{ui["privacy"]}<span class="sub">{ui["game"]}</span></h1>
<p class="meta">{p["effective"]}: {UPDATED[lang]}</p>
<p>{p["intro"]}</p>
<p class="summary">{p["summary"]}</p>
{secs}''')
        # Support
        s = SUPPORT_TEXT[lang]
        here = url(SUPPORT, lang)
        privacy_link = rel(here, url(PRIVACY, lang))
        faq = "\n".join(f"  <dt>{q}</dt>\n  <dd>{a.replace('{privacy}', privacy_link)}</dd>" for q, a in s["faq"])
        write(SUPPORT, lang, f'{ui["support"]} — {ui["game"]}', s["intro"], f'''
<h1>{ui["support"]}<span class="sub">{ui["game"]}</span></h1>
<p>{s["intro"]}</p>
<h2>{s["contact_h"]}</h2>
<p>{s["contact"]}</p>
<p>{s["bug"]}</p>
<h2>{s["faq_h"]}</h2>
<dl class="faq">
{faq}
</dl>''')


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    build()
    print("built", len(LANGS) * 4, "pages")
