#!/usr/bin/env python3
"""Builds every page of the exception games site from the texts below.

Run `python3 build.py` from this folder after changing any text, then commit the
generated HTML together with this file. Standard library only.

Languages: English is the main one (the App Store links point to it), Ukrainian
is the second, Russian the third, then German, Japanese, Korean and Chinese
(Simplified and Traditional; owner decision of October 12, 2026). Each page lives
at <page>/ (English) and <page>/<folder>/ for the others (uk, ru, de, ja, ko,
zh-hans, zh-hant). Every non-English page says that the English version applies
if a translation differs (owner decision A of October 14, 2026).
"""
import html
import os

# (code for lang and hreflang, name in the switcher). The folder is the code in lower case.
LANGS = [("en", "English"), ("uk", "Українська"), ("ru", "Русский"), ("de", "Deutsch"), ("ja", "日本語"),
         ("ko", "한국어"), ("zh-Hans", "简体中文"), ("zh-Hant", "繁體中文")]
EMAIL = "exceptiongames@icloud.com"
MAIL = f'<a href="mailto:{EMAIL}">{EMAIL}</a>'
UPDATED = {"en": "October 16, 2026", "uk": "16 жовтня 2026 р.", "ru": "16 октября 2026 г.", "de": "16. Oktober 2026",
           "ja": "2026年10月16日", "ko": "2026년 10월 16일", "zh-Hans": "2026年10月16日", "zh-Hant": "2026 年 10 月 16 日"}

# "Skip to content" and the translation note at the foot of every non-English page; {en} is the link to the
# English version of the same page.
SKIP = {"en": "Skip to content", "uk": "До основного вмісту", "ru": "К основному содержанию", "de": "Zum Inhalt springen", "ja": "本文へ移動",
        "ko": "본문으로 건너뛰기", "zh-Hans": "跳到正文", "zh-Hant": "跳至主要內容"}
TRANSLATION_NOTE = {
    "uk": "Це переклад. У разі розбіжностей між ним і {en} переважну силу має англійська версія.",
    "ru": "Это перевод. В случае расхождений между ним и {en} преимущественную силу имеет английская версия.",
    "de": "Dies ist eine Übersetzung. Weicht sie von der {en} ab, gilt die englische Fassung.",
    "ja": "このページは翻訳です。{en}と内容が異なる場合は、英語版が優先されます。",
    "ko": "이 페이지는 번역본입니다. {en}과 내용이 다를 경우 영문판이 우선합니다.",
    "zh-Hans": "本页为译文。如与{en}不一致，以英文版为准。",
    "zh-Hant": "本頁為譯文。如與{en}不一致，以英文版為準。",
}
ENGLISH_VERSION = {"uk": "англійською версією", "ru": "английской версией", "de": "englischen Fassung",
                   "ja": "英語版", "ko": "영문판", "zh-Hans": "英文版", "zh-Hant": "英文版"}

# Page paths, relative to the site root, without the language folder.
HOME, GAME, PRIVACY, SUPPORT = "", "ant-foragers/", "ant-foragers/privacy-policy/", "ant-foragers/support/"
# The game was called Living Factory until October 16, 2026. Its old addresses are compiled into early builds and may
# be saved anywhere, so each one keeps a page that sends the visitor to the new address.
OLD_PAGES = {"living-factory/": GAME, "living-factory/privacy-policy/": PRIVACY, "living-factory/support/": SUPPORT}

UI = {
    "en": dict(game="Ant Foragers", privacy="Privacy Policy", nav_privacy="Privacy", support="Support", nav="Main",
               lang="Language", footer="exception games"),
    "uk": dict(game="Фуражири", privacy="Політика конфіденційності", nav_privacy="Конфіденційність", support="Підтримка", nav="Головне меню",
               lang="Мова", footer="exception games"),
    "ru": dict(game="Фуражиры", privacy="Политика конфиденциальности", nav_privacy="Конфиденциальность", support="Поддержка", nav="Главное меню",
               lang="Язык", footer="exception games"),
    "de": dict(game="Futtersucher", privacy="Datenschutzerklärung", nav_privacy="Datenschutz", support="Support", nav="Hauptnavigation",
               lang="Sprache", footer="exception games"),
    "ja": dict(game="エサ運びアリ", privacy="プライバシーポリシー", nav_privacy="プライバシー", support="サポート", nav="メインメニュー",
               lang="言語", footer="exception games"),
    "ko": dict(game="먹이 찾는 개미", privacy="개인정보 처리방침", nav_privacy="개인정보 보호", support="지원", nav="주 메뉴",
               lang="언어", footer="exception games"),
    "zh-Hans": dict(game="搬食物的蚂蚁", privacy="隐私政策", nav_privacy="隐私", support="支持", nav="主菜单",
                    lang="语言", footer="exception games"),
    "zh-Hant": dict(game="搬食物的螞蟻", privacy="隱私權政策", nav_privacy="隱私權", support="支援", nav="主選單",
                    lang="語言", footer="exception games"),
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
    "de": dict(title="exception games",
               desc="exception games ist ein unabhängiger Entwickler kleiner, ruhiger Spiele für das iPhone.",
               lead="Ein unabhängiger Entwickler kleiner, ruhiger Spiele für das iPhone.",
               card="Ein Logikrätsel rund um eine Ameisenkolonie für das iPhone."),
    "ja": dict(title="exception games",
               desc="exception games は、iPhone 向けに落ち着いて遊べる小さなゲームを作っているインディー開発者です。",
               lead="iPhone 向けに落ち着いて遊べる小さなゲームを作っているインディー開発者です。",
               card="アリのコロニーを舞台にした iPhone 向けロジックパズル。"),
    "ko": dict(title="exception games",
               desc="exception games는 iPhone용 작고 차분한 게임을 만드는 독립 개발자입니다.",
               lead="iPhone용 작고 차분한 게임을 만드는 독립 개발자입니다.",
               card="iPhone용 개미 마을 논리 퍼즐입니다."),
    "zh-Hans": dict(title="exception games",
                    desc="exception games 是一个独立开发者，为 iPhone 制作小巧、舒缓的游戏。",
                    lead="独立开发者，为 iPhone 制作小巧、舒缓的游戏。",
                    card="一款以蚁群为主题的 iPhone 逻辑解谜游戏。"),
    "zh-Hant": dict(title="exception games",
                    desc="exception games 是獨立開發者，專為 iPhone 製作小巧、悠閒的遊戲。",
                    lead="獨立開發者，專為 iPhone 製作小巧、悠閒的遊戲。",
                    card="一款以蟻群為主題的 iPhone 邏輯解謎遊戲。"),
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
    "de": dict(
        lead="Ein Logikrätsel rund um eine Ameisenkolonie für das iPhone, entwickelt von exception games.",
        body=[
            "Senden Sie Signale entlang der Zeilen und Spalten, schicken Sie die Ameisen über Erde und Blätter und "
            "führen Sie jede zu ihrem Nest. Fünfzig von Hand gestaltete Werkhallen in vier Kapiteln, jeden Tag eine "
            "neue Werkhalle des Tages "
            "und in jeder Werkhalle ein verstecktes Geheimnis.",
            "Für die ganze Familie gemacht: ein Tipp, wenn es nicht weitergeht, eine Schritt-für-Schritt-Einführung "
            "in jede neue Art von Feld, vorgelesene Aufgaben für Kinder, die noch nicht lesen können, und mehrere "
            "Spieler auf einem iPhone.",
            "Keine Werbung, keine Käufe mit echtem Geld, keine Konten, kein Zeitlimit. Kein Internet nötig.",
        ],
        facts="iPhone · iOS 18 oder neuer · 43 Sprachen"),
    "ja": dict(
        lead="exception games による、アリのコロニーを舞台にした iPhone 向けロジックパズル。",
        body=[
            "行や列に沿って合図を送り、土や葉っぱの上を進むアリたちを、1匹残らず巣穴へ導きましょう。4つの章に、ひと"
            "つずつ手作りした50の作業場。毎日新しい「今日の作業場」が登場し、どの作業場にもひみつがひとつ隠れていま"
            "す。",
            "家族みんなのために作りました。行き詰まったときはヒントを使えます。新しい種類のマスが出てくると、一歩ず"
            "つ紹介します。まだ字が読めない子どものために説明を読み上げる機能もあり、1台の iPhone で何人ものプレイヤ"
            "ーが遊べます。",
            "広告なし、課金なし、アカウントなし、タイマーなし。インターネットは必要ありません。",
        ],
        facts="iPhone · iOS 18 以降 · 43言語"),
    "ko": dict(
        lead="exception games가 만든 iPhone용 개미 마을 논리 퍼즐입니다.",
        body=[
            "행과 열을 따라 신호를 보내고, 흙과 나뭇잎 위를 지나 모든 개미를 개미굴로 이끄세요. "
            "손수 만든 작업장 50개가 4개의 장에 담겨 있고, 매일 새로운 오늘의 작업장이 열리며, 작업장마다 비밀이 "
            "하나씩 숨어 있습니다.",
            "온 가족을 위해 만들었습니다. 막혔을 때 쓸 수 있는 힌트, 새로운 타일이 나올 때마다 차근차근 알려 주는 "
            "안내, 아직 글을 읽지 못하는 아이를 위한 설명 읽어 주기 기능이 있고, iPhone 한 대로 여러 플레이어가 "
            "함께 플레이할 수 있습니다.",
            "광고, 유료 결제, 계정, 타이머가 없습니다. 인터넷도 필요 없습니다.",
        ],
        facts="iPhone · iOS 18 이상 · 43개 언어"),
    "zh-Hans": dict(
        lead="exception games 出品的一款以蚁群为主题的 iPhone 逻辑解谜游戏。",
        body=[
            "沿着行和列发出信号，让蚂蚁走过泥土和叶子，把每只蚂蚁带回蚁窝。"
            "四章共五十个精心设计的车间，每天都有新的今日车间，每个车间里还藏着一个秘密。",
            "为全家人设计：卡关时有提示，每种新格子都有循序渐进的介绍，为还不识字的孩子朗读说明，"
            "一台 iPhone 可供多位玩家使用。",
            "没有广告，没有真钱内购，没有账户，没有计时器。无需联网。",
        ],
        facts="iPhone · iOS 18 或更高版本 · 43 种语言"),
    "zh-Hant": dict(
        lead="exception games 推出的一款以蟻群為主題的 iPhone 邏輯解謎遊戲。",
        body=[
            "沿著橫列和直行發出訊號，讓螞蟻走過泥土和葉子，把每隻螞蟻帶回蟻窩。"
            "四章共五十個精心設計的工坊，每天都有新的今日工坊，每個工坊裡還藏著一個秘密。",
            "為全家人設計：卡關時有提示，每種新格子都有循序漸進的介紹，為還不識字的孩子朗讀說明，"
            "一台 iPhone 可供多位玩家使用。",
            "沒有廣告，沒有用真錢購買的項目，沒有帳號，沒有計時器。不需要連網。",
        ],
        facts="iPhone · iOS 18 或以上版本 · 43 種語言"),
}

# Each section is (heading, [paragraphs]). Paragraph strings may contain HTML.
# Owner decisions of October 11, 2026: support mail is kept up to 12 months after the question is
# resolved; the responsible party is the developer shown as the seller on the App Store page.
PRIVACY_TEXT = {
    "en": dict(
        effective="Effective date",
        intro="Ant Foragers (“the app”) is an ant-colony logic puzzle game for iPhone. exception games is the trade name "
              "of its developer, the person or company shown as the Seller (in some countries, the Provider) on the "
              "app’s App Store page, who is responsible for this policy (“we”). This policy explains what happens to "
              "information in the app, on this website and in messages to support.",
        summary="In short: the app collects no data. Everything it saves stays on your iPhone, unless a grown-up saves a backup copy somewhere else.",
        sections=[
            ("Data the app collects", ["None. The app does not collect, transmit, sell or share any personal data. It contains no "
                                       "advertising, analytics, accounts, tracking or third-party SDKs, and it does not connect "
                                       "to the internet."]),
            ("Data stored on your device", [
                "Game progress (current workshop, unfinished games with undo history, completed workshops, best results and stars, "
                "results of the Workshop of the day, which workshops were solved with a hint, ants bought with stars or won for a perfect chapter, found secrets "
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
                "Data stays on your iPhone until you delete it. To remove one player’s progress, open Settings → "
                "Players, switch to another player, then delete the player you want to remove (a grown-up confirms "
                "it). The player who is playing now cannot be "
                "deleted. If a backup copy was restored earlier, the progress kept from before it may still include that "
                "player (see “Backup copy”). Deleting the app removes all players and all data from your device.",
                "The app never sends us your data, so there is nothing from the app for us to keep, look up or delete."]),
            ("Backup copy", [
                "In Settings → Backup copy, after passing the parental gate, a grown-up can save every player’s progress, the "
                "players’ names and the sound, haptics and read-aloud settings as one file. The file goes wherever the grown-up "
                "chooses in the Files window, for example on this iPhone or in iCloud Drive under Apple’s terms. The app never "
                "sends the file anywhere and keeps no copy of its own, and we never receive it.",
                "Restoring a copy, also behind the parental gate, replaces all players and their progress on the device with the "
                "ones in the file. Deleting the app does not delete a saved copy: delete the file in Files when you no longer "
                "need it.",
                "Before a restore replaces anything, the app keeps the progress that was on the device (all players, their "
                "names and the settings) in its own storage on this iPhone. A grown-up can then return it with Settings → "
                "Backup copy → Bring back the previous progress, behind the parental gate. Only one such state is kept, and a "
                "later restore can replace it. To tell whether anyone has played since a restore, the app also remembers what "
                "the restored file wrote. Both stay on the device and are never sent anywhere; deleting the app removes them. "
                "The kept progress does not change later: if a player is deleted, they stay in it, and bringing it back "
                "returns every player it holds."]),
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
        intro="«Фуражири» (далі — «застосунок») — логічна головоломка про мурашину колонію для iPhone. exception games — "
              "торгова назва її розробника, тобто особи чи компанії, зазначеної на сторінці застосунку в App Store "
              "як «Постачальник» (продавець), "
              "яка відповідає за цю політику («ми»). Ця політика пояснює, що відбувається з інформацією в застосунку, на цьому "
              "сайті та в листах до підтримки.",
        summary="Коротко: застосунок не збирає жодних даних. Усе, що він зберігає, залишається на вашому iPhone, якщо тільки дорослий не збереже резервну копію деінде.",
        sections=[
            ("Які дані збирає застосунок", ["Жодних. Застосунок не збирає, не передає, не продає й не розкриває жодних персональних "
                                            "даних. У ньому немає реклами, аналітики, облікових записів, відстеження та сторонніх "
                                            "SDK, і він не підключається до інтернету."]),
            ("Що зберігається на пристрої", [
                "Прогрес гри (поточний цех, незавершені партії з історією скасування, пройдені цехи, найкращі результати та зірки, "
                "результати цеху дня, позначки про цехи, розв’язані з підказкою, мурашки, куплені за зірки або здобуті за ідеально пройдений розділ, знайдені секрети й "
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
                "який зараз грає, видалити не можна. Якщо раніше відновлювали резервну копію, прогрес, збережений перед "
                "відновленням, може й далі містити цього гравця (див. «Резервна копія»). Видалення застосунку стирає всіх гравців і всі дані з пристрою.",
                "Застосунок ніколи не надсилає нам ваших даних, тому з застосунку на нашому боці немає чого зберігати, шукати чи "
                "видаляти."]),
            ("Резервна копія", [
                "У розділі «Налаштування» → «Резервна копія», після батьківської перевірки, дорослий може зберегти прогрес усіх "
                "гравців, їхні імена та налаштування звуку, вібрації й читання вголос в одному файлі. Файл потрапляє туди, куди "
                "дорослий вибере у вікні «Файли», наприклад на цей iPhone або в iCloud Drive відповідно до умов Apple. Застосунок "
                "нікуди не надсилає файл і не зберігає власної копії, а ми ніколи його не отримуємо.",
                "Відновлення копії, теж після батьківської перевірки, замінює всіх гравців і їхній прогрес на пристрої тими, що є "
                "у файлі. Видалення застосунку не видаляє збережену копію: видаліть файл у «Файлах», коли він більше не потрібен.",
                "Перш ніж відновлення щось замінить, застосунок зберігає прогрес, що був на пристрої (усіх гравців, їхні імена "
                "та налаштування), у власному сховищі на цьому iPhone. Так дорослий зможе повернути його: «Налаштування» → "
                "«Резервна копія» → «Повернути попередній прогрес», після батьківської перевірки. Зберігається лише один такий "
                "стан, і наступне відновлення може його замінити. Щоб знати, чи хтось грав після відновлення, застосунок також "
                "пам’ятає, що саме записав відновлений файл. Ці дані залишаються на пристрої й нікуди не надсилаються; видалення "
                "застосунку стирає їх. Збережений прогрес потім не змінюється: якщо видалити гравця, у ньому він залишиться, а "
                "повернення прогресу поверне всіх гравців, які в ньому є."]),
            ("Листи до підтримки", [
                "Якщо ви нам напишете, ми отримаємо вашу адресу електронної пошти та все, що ви напишете в листі або додасте до нього (наприклад, знімок екрана). Ми використовуємо ці дані лише для відповіді, нікому "
                "їх не передаємо й видаляємо листування протягом "
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
        intro="«Фуражиры» (далее — «приложение») — логическая головоломка про муравьиную колонию для iPhone. exception games — "
              "торговое имя её разработчика, то есть человека или компании, указанных на странице приложения в App "
              "Store как «Провайдер» (продавец), "
              "которые отвечают за эту политику («мы»). Эта политика объясняет, что происходит с информацией в приложении, на этом "
              "сайте и в письмах в поддержку.",
        summary="Коротко: приложение не собирает никаких данных. Всё, что оно сохраняет, остаётся на вашем iPhone, если только взрослый не сохранит резервную копию в другом месте.",
        sections=[
            ("Какие данные собирает приложение", ["Никаких. Приложение не собирает, не передаёт, не продаёт и не раскрывает "
                                                  "персональные данные. В нём нет рекламы, аналитики, аккаунтов, отслеживания и "
                                                  "сторонних SDK; приложение не подключается к интернету."]),
            ("Что хранится на устройстве", [
                "Прогресс игры (текущий цех, незавершённые партии с историей отмены, пройденные цеха, лучшие результаты и звёзды, "
                "результаты цеха дня, отметки о цехах, решённых с подсказкой, муравьи, купленные за звёзды или полученные за идеально пройденную главу, найденные секреты и "
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
                "Игрока, который сейчас играет, удалить нельзя. Если раньше восстанавливали резервную копию, прогресс, "
                "сохранённый перед восстановлением, может по-прежнему содержать этого игрока (см. «Резервная копия»). "
                "Удаление приложения стирает всех игроков и все данные с устройства.",
                "Приложение никогда не отправляет нам ваши данные, поэтому из приложения на нашей стороне нечего хранить, искать "
                "или удалять."]),
            ("Резервная копия", [
                "В разделе «Настройки» → «Резервная копия», после родительской проверки, взрослый может сохранить прогресс всех "
                "игроков, их имена и настройки звука, вибрации и чтения вслух в одном файле. Файл попадает туда, куда взрослый "
                "выберет в окне «Файлы», например на этот iPhone или в iCloud Drive в соответствии с условиями Apple. Приложение "
                "никуда не отправляет файл и не хранит собственной копии, а мы никогда его не получаем.",
                "Восстановление копии, тоже после родительской проверки, заменяет всех игроков и их прогресс на устройстве теми, "
                "что есть в файле. Удаление приложения не удаляет сохранённую копию: удалите файл в «Файлах», когда он больше не "
                "нужен.",
                "Прежде чем восстановление что-то заменит, приложение сохраняет прогресс, который был на устройстве (всех "
                "игроков, их имена и настройки), в собственном хранилище на этом iPhone. Так взрослый сможет вернуть его: "
                "«Настройки» → «Резервная копия» → «Вернуть прежний прогресс», после родительской проверки. Хранится только одно "
                "такое состояние, и следующее восстановление может его заменить. Чтобы знать, играл ли кто-нибудь после "
                "восстановления, приложение также запоминает, что именно записал восстановленный файл. Эти данные остаются на "
                "устройстве и никуда не отправляются; удаление приложения стирает их. Сохранённый прогресс потом не меняется: "
                "если удалить игрока, в нём он останется, а возврат прогресса вернёт всех игроков, которые в нём есть."]),
            ("Письма в поддержку", [
                "Если вы нам напишете, мы получим ваш адрес электронной почты и всё, что вы напишете в письме или приложите к нему (например, снимок экрана). Мы используем эти данные только для ответа, никому их не "
                "передаём и удаляем переписку в течение "
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
    "de": dict(
        effective="Gültig ab",
        intro="Futtersucher („die App“) ist ein Logikrätsel rund um eine Ameisenkolonie für das iPhone. "
              "exception games ist "
              "der Handelsname ihres Entwicklers, also der Person oder des Unternehmens, die bzw. das auf der "
              "App-Store-Seite der App als „Anbieter“ angegeben ist. Dieser Entwickler ist für diese Erklärung "
              "verantwortlich („wir“). Diese Erklärung beschreibt, was "
              "mit Informationen in der App, auf dieser Website und in Nachrichten an den Support geschieht.",
        summary="Kurz gesagt: Die App erfasst keine Daten. Alles, was sie speichert, bleibt auf Ihrem iPhone, es sei denn, ein Erwachsener speichert eine Sicherungskopie an einem anderen Ort.",
        sections=[
            ("Welche Daten die App erfasst", ["Keine. Die App erfasst, überträgt, verkauft oder teilt keine personenbezogenen "
                                              "Daten. Sie enthält keine Werbung, keine Analysedienste, keine "
                                              "Konten, kein Tracking und keine SDKs von Drittanbietern, und sie "
                                              "verbindet sich nicht mit dem Internet."]),
            ("Auf dem Gerät gespeicherte Daten", [
                "Der Spielfortschritt (aktuelle Werkhalle, angefangene Spiele mit ihrem Rückgängig-Verlauf, gelöste "
                "Werkhallen, "
                "Bestwerte und Sterne, Ergebnisse der Werkhalle des Tages, welche Werkhallen mit einem Tipp gelöst wurden, "
                "Ameisen, die mit Sternen gekauft oder für ein perfektes Kapitel gewonnen wurden, gefundene "
                "Geheimnisse und wie weit die Tipps dazu schon aufgedeckt sind, Stand der Einführung), die Namen "
                "der auf diesem Gerät hinzugefügten Spieler "
                "sowie die Einstellungen für Ton, Haptik und Vorlesen werden lokal auf Ihrem Gerät gespeichert, im üblichen "
                "App-Speicher von Apple.",
                "Spielernamen sind freiwillig; Sie können die Vorgabe „Spieler 2“ usw. beibehalten. Die App sendet diese Daten "
                "nirgendwohin. Diese Daten können nach den Bedingungen von Apple in Ihren eigenen Gerätebackups "
                "enthalten sein, außerdem in einer Sicherungskopie, die ein Erwachsener speichert (siehe "
                "„Sicherungskopie“)."]),
            ("Vorlesen", ["Wenn das Vorlesen eingeschaltet ist, liest die App die Aufgaben mit der in iOS "
                          "integrierten Sprachausgabe direkt auf dem Gerät vor. Weder Texte noch Audiodaten "
                          "verlassen das Gerät, und die App verwendet nie das Mikrofon."]),
            ("Bewegungssensor", ["Nur solange das Ergebnis einer gelösten Werkhalle angezeigt wird, liest die App "
                                 "den Bewegungssensor des iPhone direkt auf dem Gerät aus, um spielerische "
                                 "Bewegungen zu erkennen, die versteckte "
                                 "Geheimnisse aufdecken, etwa ein sanftes Schütteln oder das Umdrehen des Telefons. Die Messwerte "
                                 "werden weder gespeichert noch gesendet. Die App greift nicht auf Standort, "
                                 "Kamera, Kontakte oder Fotos zu."]),
            ("Dritte", [
                "Die App teilt mit niemandem Daten: Sie enthält keinen Code von Drittanbietern und verbindet sich "
                "mit keinem Server. "
                "Downloads, Updates und Gerätebackups wickelt Apple nach seiner eigenen Datenschutzrichtlinie ab.",
                "Wenn Sie in den iOS-Einstellungen das Teilen von Analysedaten mit App-Entwicklern aktiviert haben, "
                "kann Apple uns anonyme Absturzberichte und zusammengefasste Statistiken bereitstellen, anhand "
                "derer Sie nicht identifiziert werden können."]),
            ("Aufbewahren und Löschen von Daten", [
                "Die Daten bleiben auf Ihrem iPhone, bis Sie sie löschen. Um den Fortschritt eines Spielers zu entfernen, öffnen "
                "Sie Einstellungen → Spieler, wechseln zu einem anderen Spieler und löschen dann den Spieler, "
                "dessen Fortschritt Sie entfernen möchten (ein Erwachsener bestätigt das). "
                "Der Spieler, der gerade spielt, kann nicht gelöscht werden. Wurde zuvor eine Sicherungskopie "
                "wiederhergestellt, kann der Fortschritt, den die App vor dieser Wiederherstellung aufbewahrt hat, "
                "diesen Spieler noch enthalten (siehe „Sicherungskopie“). Wenn Sie die App "
                "löschen, werden alle Spieler und alle Daten von Ihrem Gerät entfernt.",
                "Die App sendet uns nie Ihre Daten, daher gibt es bei uns aus der App nichts, was wir aufbewahren, "
                "einsehen oder löschen könnten."]),
            ("Sicherungskopie", [
                "Unter Einstellungen → Sicherungskopie kann ein Erwachsener nach der Elternabfrage den Fortschritt aller Spieler, "
                "ihre Namen und die Einstellungen für Ton, Haptik und Vorlesen in einer Datei speichern. Die Datei "
                "wird an dem Ort gespeichert, den der Erwachsene im Fenster „Dateien“ auswählt, zum Beispiel auf "
                "diesem iPhone oder nach den Bedingungen von Apple in iCloud Drive. Die App sendet die Datei "
                "nirgendwohin und behält keine eigene Kopie, und wir erhalten sie nie.",
                "Das Wiederherstellen einer Kopie, ebenfalls nach der Elternabfrage, ersetzt alle Spieler und ihren Fortschritt "
                "auf dem Gerät durch die Spieler und den Fortschritt aus der Datei. Wenn Sie die App löschen, "
                "bleibt eine gespeicherte Kopie erhalten: Löschen Sie die Datei "
                "in „Dateien“, wenn Sie sie nicht mehr brauchen.",
                "Bevor eine Wiederherstellung etwas ersetzt, bewahrt die App den Fortschritt, der auf dem Gerät war (alle Spieler, "
                "ihre Namen und die Einstellungen), in ihrem eigenen Speicher auf diesem iPhone auf. Ein "
                "Erwachsener kann ihn danach zurückholen, ebenfalls nach der Elternabfrage: unter Einstellungen → "
                "Sicherungskopie → Früheren Fortschritt zurückholen. Es "
                "wird nur ein solcher Stand aufbewahrt, und eine spätere Wiederherstellung kann ihn ersetzen. Um zu erkennen, ob "
                "seit einer Wiederherstellung jemand gespielt hat, merkt sich die App außerdem den Stand, den die "
                "Wiederherstellung aus der Datei geschrieben hat. Beides bleibt auf dem Gerät und wird nie "
                "gesendet; das Löschen der App entfernt beides. Der "
                "aufbewahrte Fortschritt ändert sich später nicht: Wird ein Spieler gelöscht, bleibt er darin, und das Zurückholen "
                "bringt alle Spieler zurück, die er enthält."]),
            ("Nachrichten an den Support", [
                "Wenn Sie uns schreiben, erhalten wir Ihre E-Mail-Adresse und alles, was Ihre Nachricht enthält "
                "(zum Beispiel einen Screenshot). Wir verwenden diese Angaben nur, um Ihnen zu antworten, geben sie "
                "an niemanden weiter und löschen den "
                "Schriftverkehr innerhalb von 12 Monaten, nachdem die Frage geklärt ist, oder auf Wunsch früher. E-Mails werden "
                "über iCloud Mail von Apple zugestellt. Bitte lassen Sie einen Erwachsenen schreiben, kein Kind."]),
            ("Diese Website", ["Diese Website verwendet keine Cookies und keine Analysedienste. Sie wird bei GitHub "
                               "Pages gehostet; "
                               "GitHub kann die IP-Adressen der Besucher aus Sicherheitsgründen nach der GitHub-Datenschutzerklärung "
                               "protokollieren."]),
            ("Kinder", [
                "Das Spiel ist für Kinder und Familien gemacht. Es erfasst wissentlich keine Informationen von irgendjemandem, auch "
                "nicht von Kindern unter 13 Jahren. Es gibt keine Werbung, keine Käufe mit echtem Geld, keine Konten, keinen Chat "
                "und keine Links zu sozialen Netzwerken. Im Ameisenladen bezahlt man nur mit Sternen, die im Spiel "
                "verdient wurden.",
                "Seiten außerhalb des Spiels, wie diese Erklärung und die Support-Seite, öffnen sich erst, nachdem ein Erwachsener "
                "die Elternabfrage gelöst hat; dasselbe gilt für das Speichern und Wiederherstellen einer Sicherungskopie. Da die "
                "App keine personenbezogenen Daten erfasst, gibt es keine Datenerhebung, in die Eltern einwilligen müssten."]),
            ("Ihre Rechte", [f"Datenschutzgesetze wie die Datenschutz-Grundverordnung der EU (DSGVO) geben Ihnen "
                             f"das Recht, Auskunft darüber zu verlangen, welche personenbezogenen Daten wir über "
                             f"Sie gespeichert haben, und diese berichtigen oder löschen zu lassen. Über die App "
                             f"erhalten wir keine solchen Daten; die einzigen Daten, die wir möglicherweise "
                             f"gespeichert haben, sind Ihre Nachrichten an den Support. Für eine Auskunft oder "
                             f"Löschung schreiben Sie an {MAIL}. Sie können sich außerdem bei der für Sie "
                             f"zuständigen Datenschutzaufsichtsbehörde beschweren."]),
            ("Änderungen", ["Wenn eine künftige Version der App den Umgang mit Daten ändert, wird diese Seite vor "
                            "dem Erscheinen dieser Version aktualisiert und das oben angegebene Datum „Gültig ab“ "
                            "angepasst."]),
            ("Kontakt", [f"exception games · {MAIL}"]),
        ]),
    "ja": dict(
        effective="発効日",
        intro="エサ運びアリ（以下「本アプリ」といいます）は、アリのコロニーを舞台にした iPhone 向けのロジックパズル"
              "ゲームです。exception games は、本アプリの開発者（以下「当方」といいます）の屋号です。当方とは、App "
              "Store の本アプリのページに「販売元」として表示されている個人または法人であり、本ポリシーについて責任"
              "を負います。本ポリシーでは、本アプリ、このウェブサイト、および"
              "サポートへのメッセージで、情報がどのように扱われるかを説明します。",
        summary="簡単にまとめると、本アプリはデータを一切収集しません。本アプリが保存するものはすべてお使いの "
                "iPhone に残ります。ただし、大人がバックアップを別の場所に保存した場合を除きます。",
        sections=[
            ("本アプリが収集するデータ", ["ありません。本アプリは個人データを収集、送信、販売、共有しません。広告、解析、"
                                          "アカウント、トラッキング、サードパーティの SDK は含まれておらず、インターネットにも接続しません。"]),
            ("デバイスに保存されるデータ", [
                "ゲームの進行状況（現在の作業場、「元に戻す」の履歴を含む途中のゲーム、クリアした作業場、ベスト記録"
                "と星、今日の作業場の結果、ヒントを使って解いた作業場、星で買ったアリ、章をパーフェクトでクリアして"
                "もらったアリ、見つけたひみつ、ひみつのヒントがどこまで表示されたか、チュートリアルの状態）、このデ"
                "バイスで追加したプレイヤーの名前、サウンド・"
                "振動・読み上げの設定は、Apple 標準のアプリ用ストレージを使ってお使いのデバイスにローカルに保存されます。",
                "プレイヤー名の入力は任意で、「プレイヤー2」などの初期名のままでもかまいません。本アプリがこれらのデータを"
                "どこかに送ることはありません。お使いのデバイス自体のバックアップ（Apple の規約が適用されます）や、"
                "大人が保存したバックアップファイル（「バックアップ」を参照）に含まれる場合があります。"]),
            ("読み上げ", ["「説明を読み上げる」がオンのとき、本アプリはデバイス上の iOS 内蔵の音声合成でパズルの説明"
                      "を読み上げます。"
                          "テキストや音声がデバイスの外に出ることはなく、マイクを使うこともありません。"]),
            ("モーションセンサー", ["クリアした作業場の結果が画面に表示されている間だけ、本アプリはデバイス上で iPhone の"
                                    "モーションセンサーを読み取り、そっと振る、ひっくり返すといった、隠れたひみつを"
                                    "見つける遊びの"
                                    "動きを検出します。読み取った値が保存・送信されることはありません。本アプリは位置情報、カメラ、"
                                    "連絡先、写真を使いません。"]),
            ("第三者", [
                "本アプリは誰ともデータを共有しません。サードパーティのコードを含まず、どのサーバーとも通信しません。"
                "ダウンロード、アップデート、デバイスのバックアップは、Apple が自社のプライバシーポリシーに基づいて取り扱います。",
                "iOS の設定で App デベロッパとの解析データの共有を選んだ場合、Apple が当方に、匿名のクラッシュレポートと、"
                "お客様を特定しない集計統計を提供することがあります。"]),
            ("データの保管と削除", [
                "データは削除するまでお使いの iPhone に残ります。あるプレイヤーの進行状況を消すには、「設定」→「プレ"
                "イヤー」を開き、別のプレイヤーに切り替えてから、消したいプレイヤーを削除します（大人が確認しま"
                "す）。いまプレイ中のプレイヤーは"
                "削除できません。以前にバックアップを復元したことがある場合、復元の前に保管された進行状況に、そのプレイヤーが"
                "まだ含まれていることがあります（「バックアップ」を参照）。本アプリを削除すると、すべてのプレイヤーとすべての"
                "データがデバイスから消去されます。",
                "本アプリがお客様のデータを当方に送ることはないため、当方には、本アプリに由来する保管・照会・削除の対象となる"
                "ものはありません。"]),
            ("バックアップ", [
                "「設定」→「バックアップ」では、保護者確認を通過した大人が、全プレイヤーの進行状況、プレイヤーの名"
                "前、サウンド・"
                "振動・読み上げの設定をひとつのファイルとして保存できます。ファイルは、大人が「ファイル」の画面で選"
                "んだ場所、たとえばこの iPhone や iCloud Drive（Apple の規約が適用されます）に保存されます。本アプリ"
                "がファイルをどこかに送ることは"
                "なく、独自のコピーも保持せず、当方がそれを受け取ることもありません。",
                "バックアップの復元も保護者確認の後で行い、デバイス上のすべてのプレイヤーとその進行状況を、ファイルの内容に"
                "置き換えます。本アプリを削除しても、保存したバックアップは削除されません。不要になったら「ファイル」で"
                "ファイルを削除してください。",
                "復元によって何かが置き換わる前に、本アプリはデバイスにあった進行状況（すべてのプレイヤー、その名前、設定）を、"
                "この iPhone 上の本アプリ専用の保存領域に保管します。大人は保護者確認の後、「設定」→「バックアッ"
                "プ」→「以前の進行状況に戻す」で、保管された進行状況に戻せます。保管されるのはひとつの状態だけで、後"
                "の復元で置き換わることがあります。復元後に誰かが"
                "遊んだかどうかを判断するため、本アプリは復元したファイルが書き込んだ内容も記憶します。どちらもデバイス上に"
                "とどまり、送信されることはありません。本アプリを削除すると両方とも消えます。保管された進行状況は後から変わり"
                "ません。プレイヤーを削除してもその中には残り、保管された進行状況に戻すと、そこに含まれるすべてのプ"
                "レイヤーが戻ります。"]),
            ("サポートへのメッセージ", [
                "当方にご連絡いただくと、お客様のメールアドレスと、お送りいただいた内容すべて（スクリーンショットな"
                "ど）を受け取ります。"
                "これらは返信のためだけに使い、誰とも共有せず、お問い合わせが解決してから12か月以内に、またはご依頼があれば"
                "それより早く、やり取りを削除します。メールは Apple の iCloud メールで配信されます。ご連絡は、お子さまではなく"
                "大人の方からお願いします。"]),
            ("このウェブサイト", ["このウェブサイトは Cookie も解析も使用しません。GitHub Pages でホストされてお"
                          "り、GitHub は同社のプライバシーステートメントに基づき、セキュリティのために訪問者"
                          "の IP アドレスを記録する"
                                  "ことがあります。"]),
            ("子ども", [
                "このゲームは子どもと家族のために作られています。13歳未満の子どもを含め、誰からも意図して情報を収集することは"
                "ありません。広告、課金、アカウント、チャット、ソーシャルメディアへのリンクはありません。アリの"
                "お店で使えるのは、ゲーム内で獲得した星だけです。",
                "本ポリシーやサポートページなど、ゲームの外のページは、大人が保護者確認を通過した後にだけ開きます。"
                "バックアップの保存と復元も同様です。本アプリは個人データを収集しないため、保護者の同意が必要となるデータ収集は"
                "ありません。"]),
            ("お客様の権利", [f"EU 一般データ保護規則（GDPR）などのプライバシー法では、当方が保有するお客様の個人デ"
                        f"ータの開示、訂正、削除を求める権利が認められています。本アプリは当方にデータを一切"
                              f"渡しません。当方が保有し得るのは、サポートへのメッセージだけです。その確認や削除をご希望の場合は、"
                              f"{MAIL} までご連絡ください。お住まいの地域のデータ保護機関に苦情を申し立てることもできます。"]),
            ("変更", ["将来のバージョンでデータの取り扱いが変わる場合、そのバージョンの公開前にこのページを更新し、上記の発効日を"
                      "変更します。"]),
            ("お問い合わせ", [f"exception games · {MAIL}"]),
        ]),
    "ko": dict(
        effective="시행일",
        intro="먹이 찾는 개미(이하 ‘앱’)는 개미 마을을 무대로 한 iPhone용 논리 퍼즐 게임입니다. exception games는 "
              "앱 개발자(App Store의 앱 페이지에 ‘제공자’로 표시되는 개인 또는 회사, 이하 ‘당사’)의 상호이며, "
              "당사가 이 방침에 대한 책임을 집니다. 이 방침은 앱, 이 웹사이트, 지원 문의 메시지에서 정보가 어떻게 "
              "처리되는지 설명합니다.",
        summary="요약하면, 앱은 어떤 데이터도 수집하지 않습니다. 앱이 저장하는 모든 것은 사용자의 iPhone에 남습니다. 단, 어른이 백업을 다른 곳에 저장하는 경우는 예외입니다.",
        sections=[
            ("앱이 수집하는 데이터", ["없습니다. 앱은 어떠한 개인정보도 수집, 전송, 판매 또는 공유하지 않습니다. "
                             "광고, 분석, 계정, "
                                      "추적, 타사 SDK가 없으며 인터넷에 연결하지 않습니다."]),
            ("기기에 저장되는 데이터", [
                "게임 진행 상황(현재 작업장, 되돌리기 기록이 남아 있는 진행 중인 게임, 완료한 작업장, 최고 기록과 별, 오늘의 "
                "작업장 결과, 힌트로 푼 작업장, 별을 써서 산 개미나 한 장을 완벽하게 끝내고 받은 개미, 찾은 비밀과 "
                "그 힌트가 열린 정도, "
                "튜토리얼 상태), 이 기기에서 추가한 플레이어 이름, 소리·진동·설명 읽어 주기 설정은 Apple의 표준 앱 "
                "저장 공간을 사용해 "
                "사용자의 기기에 로컬로 저장됩니다.",
                "플레이어 이름은 선택 사항이며 ‘플레이어 2’ 같은 기본 이름을 그대로 써도 됩니다. 앱은 이 데이터를 어디에도 "
                "보내지 않습니다. 다만 이 데이터는 Apple 약관에 따라 사용자 자신의 기기 백업에 포함될 수 있으며, "
                "어른이 저장한 백업 파일(‘백업’ 참조)에도 포함될 수 있습니다."]),
            ("설명 읽어 주기", ["‘설명 읽어 주기’가 켜져 있으면 앱은 기기에 내장된 iOS 음성 합성 기능으로 퍼즐 "
                          "설명을 읽어 줍니다. 텍스트나 음성은 기기 밖으로 나가지 않으며, 앱은 마이크를 "
                          "사용하지 않습니다."]),
            ("동작 센서", ["푼 작업장의 결과가 화면에 표시되어 있는 동안에만 앱은 기기 안에서 iPhone의 동작 센서 "
                       "값을 읽어, 살짝 "
                           "흔들기나 휴대폰 뒤집기처럼 숨은 비밀을 여는 놀이 동작을 감지합니다. 측정값은 저장되거나 전송되지 "
                           "않습니다. 앱은 위치, 카메라, 연락처, 사진을 사용하지 않습니다."]),
            ("제3자", [
                "앱은 누구와도 데이터를 공유하지 않습니다. 타사 코드가 없으며 어떤 서버와도 통신하지 않습니다. 다운로드, "
                "업데이트, 기기 백업은 Apple이 자체 개인정보 처리방침에 따라 처리합니다.",
                "iOS 설정에서 앱 개발자와 분석 정보를 공유하기로 선택한 경우, Apple은 당사에 익명의 충돌 보고서와 사용자를 "
                "식별할 수 없는 집계 통계를 제공할 수 있습니다."]),
            ("데이터 보관 및 삭제", [
                "데이터는 사용자가 삭제할 때까지 iPhone에 남아 있습니다. 한 플레이어의 진행 상황을 지우려면 설정 → "
                "플레이어를 열고, 다른 플레이어로 바꾼 뒤 지우려는 플레이어를 삭제하세요(어른의 확인이 필요합니다). "
                "지금 플레이 중인 플레이어는 삭제할 수 없습니다. 이전에 백업을 복원한 적이 있다면, 복원 전에 보관해 "
                "둔 진행 상황에는 삭제한 플레이어가 아직 남아 있을 수 있습니다(‘백업’ 참조). 앱을 삭제하면 모든 "
                "플레이어와 모든 데이터가 기기에서 지워집니다.",
                "앱은 사용자의 데이터를 당사에 보내지 않으므로, 당사가 보관·조회·삭제할 수 있는 앱 데이터는 없습니다."]),
            ("백업", [
                "어른은 설정 → 백업에서 보호자 확인을 통과한 뒤 모든 플레이어의 진행 상황, 플레이어 이름, "
                "소리·진동·설명 읽어 주기 설정을 하나의 파일로 저장할 수 있습니다. 파일은 어른이 ‘파일’ 창에서 고른 "
                "곳, 예를 들어 이 iPhone이나 Apple "
                "약관에 따른 iCloud Drive에 저장됩니다. 앱은 파일을 어디에도 보내지 않고 자체 사본도 보관하지 않으며, 당사도 "
                "파일을 받지 않습니다.",
                "백업 복원도 보호자 확인을 거친 뒤에 할 수 있으며, 기기의 모든 플레이어와 그 진행 상황을 파일에 있는 것으로 "
                "바꿉니다. 앱을 삭제해도 저장한 백업은 삭제되지 않습니다. 더 이상 필요 없으면 ‘파일’에서 파일을 삭제하세요.",
                "복원으로 무언가가 바뀌기 전에, 앱은 기기에 있던 진행 상황(모든 플레이어, 플레이어 이름, 설정)을 이 "
                "iPhone 안의 앱 자체 저장 공간에 보관합니다. 어른은 보호자 확인을 거친 뒤 설정 → 백업 → 이전 진행 "
                "상황으로 되돌리기를 눌러 이 진행 상황을 되찾을 수 있습니다. 이렇게 보관되는 상태는 하나뿐이며, "
                "이후에 다시 복원하면 새로운 상태로 대체될 수 있습니다. 복원 후 누군가 플레이했는지 알 수 있도록, "
                "앱은 복원한 파일이 기록한 내용도 기억합니다. 두 가지 모두 기기에만 남고 어디에도 전송되지 않으며, "
                "앱을 삭제하면 함께 지워집니다. 보관된 진행 상황은 나중에 바뀌지 않습니다. 플레이어를 삭제해도 그 "
                "플레이어는 보관된 진행 상황에 남아 있고, 되돌리면 그 안의 모든 플레이어가 돌아옵니다."]),
            ("지원 문의 메시지", [
                "당사에 연락하시면 이메일 주소와, 메일에 담아 보내신 모든 내용(예: 스크린샷)을 당사가 받게 됩니다. "
                "이 정보는 답변에만 사용하고 누구와도 공유하지 않으며, 주고받은 이메일은 문의가 해결된 후 12개월 "
                "이내에, 또는 요청하시면 그보다 일찍 삭제합니다. 이메일은 Apple의 iCloud Mail을 통해 전달됩니다. "
                "아이가 아닌 어른이 연락해 주세요."]),
            ("이 웹사이트", ["이 웹사이트는 쿠키나 분석 도구를 사용하지 않습니다. GitHub Pages에서 호스팅되며, GitHub는 GitHub "
                             "개인정보 보호정책에 따라 보안을 위해 방문자의 IP 주소를 기록할 수 있습니다."]),
            ("어린이", [
                "이 게임은 어린이와 가족을 위해 만들어졌습니다. 만 13세 미만 어린이를 포함해 누구로부터도 고의로 "
                "정보를 수집하지 않습니다. 광고, 유료 결제, 계정, 채팅, 소셜 미디어 링크가 없습니다. 개미 "
                "상점에서는 게임에서 얻은 "
                "별만 사용합니다.",
                "이 방침과 지원 페이지처럼 게임 밖의 페이지는 어른이 보호자 확인을 통과한 뒤에만 열리며, 백업 저장과 복원도 "
                "마찬가지입니다. 앱은 개인정보를 수집하지 않으므로 부모가 동의해야 할 데이터 수집이 없습니다."]),
            ("사용자의 권리", [f"EU 일반 개인정보 보호법(GDPR) 같은 개인정보 보호법은 당사가 보유한 사용자의 "
                         f"개인정보가 무엇인지 문의하고, 이를 정정하거나 삭제하도록 요청할 권리를 보장합니다. "
                         f"앱은 당사에 어떠한 데이터도 제공하지 않으며, 당사가 보유할 수 있는 데이터는 지원 "
                         f"문의로 보낸 메시지뿐입니다. 이에 대해 문의하거나 "
                               f"삭제를 원하시면 {MAIL}으로 연락해 주세요. 거주 지역의 개인정보 보호 감독기관에 "
                               f"민원을 제기할 수도 "
                               f"있습니다."]),
            ("변경", ["향후 버전에서 데이터 처리 방식이 바뀌면, 해당 버전이 출시되기 전에 이 페이지를 업데이트하고 위의 시행일을 "
                      "변경합니다."]),
            ("연락처", [f"exception games · {MAIL}"]),
        ]),
    "zh-Hans": dict(
        effective="生效日期",
        intro="《搬食物的蚂蚁》（以下简称“本应用”）是一款以蚁群为主题的 iPhone 逻辑解谜游戏。exception games 是本应用开"
              "发者（以下简称“我们”）的商号。该开发者即在本应用 App Store 页面上列为“提供者”的个人或公司，并对本政策"
              "负责。本政策说明本应用、本网站以及发至支持邮箱的消息中的信息会如何处理。",
        summary="简而言之：本应用不收集任何数据。它保存的一切都留在您的 iPhone 上，除非有成年人把备份保存到别处。",
        sections=[
            ("本应用收集的数据", ["无。本应用不收集、传输、出售或分享任何个人信息。它没有广告、分析工具、账户或跟踪"
                          "功能，不含第三方 SDK，也不连接互联网。"]),
            ("保存在设备上的数据", [
                "游戏进度（当前车间、带撤销记录的未完成游戏、已完成的车间、最佳成绩和星星、今日车间的结果、哪些车间是借助提示"
                "解开的、用星星买的蚂蚁或因完美通关一章而获得的蚂蚁、找到的秘密及其提示已揭示到哪一步、教程状态）、在此设备上"
                "添加的玩家名字，以及声音、振动和朗读设置，都通过 Apple 标准的应用存储保存在您的设备本地。",
                "玩家名字可以不填，保留“玩家 2”之类的默认名字即可。本应用绝不会把这些数据发送到任何地方。它们可能会依照 Apple "
                "的条款包含在您自己的设备备份中，也可能包含在成年人保存的备份里（见“备份”）。"]),
            ("朗读", ["开启“朗读说明”后，本应用会在设备上使用 iOS 内置的语音合成功能朗读谜题说明。任何文字或音频都不"
                    "会离开设备，本应用也从不"
                      "使用麦克风。"]),
            ("运动传感器", ["只有在已解开车间的结果显示在屏幕上时，本应用才会在设备上读取 iPhone 的运动传感器，以识"
                       "别能揭开隐藏秘密的趣味动作，例如轻轻摇晃或把手机翻过来。传感器读数既不会被保存，也不会"
                       "被发送。本应用不使用位置、相机、通讯录"
                            "或照片。"]),
            ("第三方", [
                "本应用不与任何人分享数据：它不含第三方代码，也不与任何服务器通信。下载、更新和设备备份由 Apple 依照其自身的"
                "隐私政策处理。",
                "如果您在 iOS 设置中开启了“与 App 开发者共享”（共享分析数据），Apple 可能会向我们提供匿名的崩溃报告"
                "和无法识别您身份的汇总统计数据。"]),
            ("数据的保留与删除", [
                "数据会一直保留在您的 iPhone 上，直到您删除它。要删除某位玩家的进度，请打开“设置”→“玩家”，先切换到其"
                "他玩家，再删除要移除的那位玩家（需由成年人确认）。当前正在玩的玩家无法删除。如果以前恢复过备份，恢"
                "复前保留的进度中可能仍包含被删除的玩家（见“备份”）。删除本应用会从您的设备上移除所有玩家和所有数"
                "据。",
                "本应用从不向我们发送您的数据，因此我们没有任何来自本应用的数据可供保留、查询或删除。"]),
            ("备份", [
                "在“设置”→“备份”中，成年人通过家长验证后，可以把所有玩家的进度、玩家名字以及声音、振动和朗读设置保存"
                "为一个文件。文件会保存到成年人在“文件”窗口中选择的位置，例如这台 iPhone 上，或依照 Apple 的条款保存"
                "在 iCloud 云盘中。本应用不会把文件发送到任何地方，自身也不保留副本；我们也绝不会收到该文件。",
                "恢复备份同样需要通过家长验证，它会用文件中的内容替换设备上的所有玩家及其进度。删除本应用不会删除已保存的备份："
                "不再需要时，请在“文件” App 中删除该文件。",
                "在恢复备份、替换任何内容之前，本应用会把设备上原有的进度（所有玩家、玩家名字和设置）保存在此 "
                "iPhone 上本应用自己的存储空间中。之后，成年人可以在“设置”→“备份”→“恢复之前的进度”中通过家长验证，把"
                "这些进度找回来。这样的进度只保留一份，之后的恢复可能会替换它。为了判断恢复后是否有人玩过，本应用还"
                "会记住所恢复文件写入的内容。两者都只留在设备上，绝不发送到任何地方；删除本应用会将它们一并移除。保"
                "留的进度之后不会改变：即使删除某位玩家，该玩家仍保留在其中；找回进度时，会恢复其中的所有玩家。"]),
            ("发至支持邮箱的消息", [
                "如果您给我们写信，我们会收到您的电子邮件地址以及您在邮件中提供的任何内容（例如截图）。我们仅将这些"
                "信息用于回复您，不与任何人分享，并在问题解决后 12 个月内删除往来邮件；如您要求，也可更早删除。邮件"
                "通过 Apple 的 iCloud 邮件投递。请由成年人而不是孩子给我们写信。"]),
            ("本网站", ["本网站不使用 Cookie 或分析工具。它托管在 GitHub Pages 上，GitHub 可能会依照其隐私声明，为安全"
                        "起见记录访问者的 IP 地址。"]),
            ("儿童", [
                "本游戏为儿童和家庭而设计。它不会有意收集任何人（包括 13 岁以下儿童）的任何信息。游戏中没有广告、没"
                "有需用真钱支付的 App 内购买项目、没有账户、没有聊天，也没有社交媒体链接。蚂蚁商店只接受在游戏中获得"
                "的星星。",
                "游戏以外的页面，例如本政策和支持页面，只有在成年人通过家长验证后才会打开；保存和恢复备份也是如此。由于本应用"
                "不收集个人信息，因此不存在需要家长同意的数据收集。"]),
            ("您的权利", [f"欧盟《通用数据保护条例》（GDPR）等隐私保护法律赋予您以下权利：查询我们持有哪些关于您的个"
                      f"人信息，并要求更正或删除这些信息。本应用不向我们提供任何数据；我们可能持有的唯一数据是您"
                      f"发至支持邮箱的消息。如需查询或删除，请写信至 {MAIL}。您也可以向当地的数据保护监管机构投"
                      f"诉。"]),
            ("变更", ["如果未来的版本改变了数据的处理方式，本页面会在该版本发布之前更新，上方的生效日期也会随之更改。"]),
            ("联系方式", [f"exception games · {MAIL}"]),
        ]),
    "zh-Hant": dict(
        effective="生效日期",
        intro="《搬食物的螞蟻》（以下稱「本 App」）是一款以蟻群為主題的 iPhone 邏輯解謎遊戲。exception games 是本 App 開發者"
              "的商號；該開發者即在本 App 的 App Store 頁面上標示為「供應商」的個人或公司，並對本政策負責（以下稱「"
              "我們」）。本政策說明在本 App 中、本網站上，以及您寄給支援團隊的訊息中，資訊會如何處理。",
        summary="簡單來說：本 App 不收集任何資料。它儲存的一切都留在您的 iPhone 上，除非有大人把備份儲存到其他地方。",
        sections=[
            ("本 App 收集的資料", ["沒有。本 App 不收集、傳輸、販售或分享任何個人資料。它不含廣告、分析、帳號、追蹤或第三方 "
                                   "SDK，也不連線到網際網路。"]),
            ("儲存在裝置上的資料", [
                "遊戲進度（目前的工坊、含復原紀錄的未完成遊戲、已完成的工坊、最佳成績與星星、今日工坊的結果、哪些工坊是靠提示"
                "解開的、用星星買的螞蟻或因完美完成一章而獲得的螞蟻、找到的秘密與其提示已開啟的程度、教學狀態）、在此裝置上"
                "新增的玩家名稱，以及音效、震動與朗讀設定，都透過 Apple 標準的 App 儲存空間儲存在您的裝置上。",
                "玩家名稱可以不填，保留「玩家 2」之類的預設名稱即可。本 App 絕不會把這些資料傳送到任何地方。它們可能會依照 "
                "Apple 的條款包含在您自己的裝置備份中，也可能包含在大人儲存的備份裡（見「備份」）。"]),
            ("朗讀", ["開啟「朗讀說明」時，本 App 會在裝置上使用 iOS 內建的語音合成朗讀謎題說明。文字與聲音不會離開"
                    "裝置，本 App 也從不"
                      "使用麥克風。"]),
            ("動作感測器", ["只有在已解開工坊的結果顯示於螢幕上時，本 App 才會在裝置上讀取 iPhone 的動作感測器，以察覺能揭開"
                            "隱藏秘密的有趣動作，例如輕輕搖晃或把手機翻過來。這些讀數絕不會被儲存或傳送。本 App 不使"
                            "用定位、相機、"
                            "聯絡人或照片。"]),
            ("第三方", [
                "本 App 不與任何人分享資料：它不含第三方程式碼，也不與任何伺服器通訊。下載、更新與裝置備份由 Apple 依照其自身的"
                "隱私權政策處理。",
                "如果您在 iOS 設定中選擇與 App 開發者分享分析資料，Apple 可能會向我們提供匿名的當機報告，以及無法識別您身分的"
                "彙總統計。"]),
            ("資料的保留與刪除", [
                "資料會一直保留在您的 iPhone 上，直到您刪除為止。若要刪除某位玩家的進度，請打開「設定」→「玩家」，先"
                "切換到另一位玩家，再刪除要移除的那位玩家（需由大人確認）。正在遊玩的玩家無法刪除。如果先前曾回復備"
                "份，回復前保留的進度中可能仍包含被刪除的玩家"
                "（見「備份」）。刪除本 App 會從您的裝置移除所有玩家與所有資料。",
                "本 App 從不把您的資料傳送給我們，因此我們這裡沒有任何來自本 App 的資料需要保留、查詢或刪除。"]),
            ("備份", [
                "在「設定」→「備份」中，通過家長驗證後，大人可以把所有玩家的進度、玩家名稱以及音效、震動與朗讀設定儲"
                "存成一個檔案。"
                "檔案會存放在大人於「檔案」視窗中選擇的位置，例如此 iPhone 上，或依照 Apple 條款存放在 iCloud 雲碟中。本 App "
                "不會把檔案傳送到任何地方，也不保留自己的副本，我們也從不會收到它。",
                "回復備份同樣需要通過家長驗證，它會用檔案中的內容取代裝置上的所有玩家及其進度。刪除本 App 不會刪除已儲存的"
                "備份：不再需要時，請在「檔案」App 中刪除該檔案。",
                "在回復取代任何內容之前，本 App 會把裝置上原有的進度（所有玩家、他們的名稱與設定）保存在此 iPhone 上本 App "
                "自己的儲存空間中。之後，大人可以在通過家長驗證後，透過「設定」→「備份」→「回復之前的進度」把它找回"
                "來。只會保留一份"
                "這樣的狀態，之後的回復可能會取代它。為了判斷回復後是否有人玩過，本 App 也會記下回復時由該檔案寫入的"
                "內容。兩者都"
                "只留在裝置上，絕不傳送到任何地方；刪除本 App 會將它們一併移除。保留的進度之後不會改變：刪除某位玩家"
                "後，該玩家仍會保留在其中，找回進度時會回復其中的所有玩家。"]),
            ("寄給支援團隊的訊息", [
                "如果您寫信給我們，我們會收到您的電子郵件地址，以及您在信中提供的任何內容（例如螢幕截圖）。我們只會"
                "用這些資料回覆您，不會與任何人分享，並在問題解決後 12 個月內刪除往來信件；如您提出要求，我們會提前"
                "刪除。郵件透過 Apple 的 iCloud 郵件遞送。"
                "請由大人而不是孩子寫信給我們。"]),
            ("本網站", ["本網站不使用 Cookie 或分析工具。它託管於 GitHub Pages，GitHub 可能會依照 GitHub 隱私權聲明，基於安全"
                        "考量記錄訪客的 IP 位址。"]),
            ("兒童", [
                "本遊戲為兒童與家庭而設計。它不會在知情的情況下收集任何人的資訊，包括未滿 13 歲的兒童。遊戲中沒有廣"
                "告、沒有用真錢購買的項目、沒有帳號、沒有聊天功能，也沒有社群媒體連結。螞蟻商店只使用在遊戲中贏得的"
                "星星。",
                "遊戲以外的頁面，例如本政策與支援頁面，只有在大人通過家長驗證後才會開啟；儲存與回復備份也是如此。由"
                "於本 App 不收集個人資料，因此沒有需要家長同意的資料收集。"]),
            ("您的權利", [f"歐盟《一般資料保護規則》（GDPR）等個人資料保護法規賦予您權利，可詢問我們持有哪些關於您的"
                      f"個人資料，並要求更正或刪除這些資料。本 App 不會向我們提供任何資料；我們可能持有的唯一資"
                      f"料是您寄給支援團隊的訊息。如需查詢或"
                          f"刪除，請寫信至 {MAIL}。您也可以向當地的資料保護主管機關提出申訴。"]),
            ("變更", ["如果未來的版本改變了資料的處理方式，本頁面會在該版本發布前更新，上方的生效日期也會隨之變更。"]),
            ("聯絡方式", [f"exception games · {MAIL}"]),
        ]),
}

SUPPORT_TEXT = {
    "en": dict(
        intro="Ant Foragers is an ant-colony logic puzzle game for iPhone by exception games.",
        contact_h="Contact", contact=f"Write to {MAIL}. We read every message and answer in English, Ukrainian or Russian.",
        bug="Reporting a bug? Please include your iPhone model, iOS version, the workshop number and what happened. A screenshot helps.",
        faq_h="Questions and answers",
        faq=[
            ("Where is my progress saved?", "Only on your iPhone. The game has no accounts and no cloud sync. Deleting the app erases all progress, so update the app without deleting it."),
            ("How do I start a workshop over?", "Tap Restart. To replay the tutorial, open Settings → Replay tutorial."),
            ("I’m stuck. What can I do?", "Tap Undo to take back the last signal, or tap Hint to see the next signal. A workshop solved with a hint earns one star; tap Restart and solve it on your own for more. The workshop of the day has no hint."),
            ("Can several people play on one iPhone?", "Yes. Add players in Settings → Players. Each player has their own stars, records and ants."),
            ("How do I keep progress safe or move it to another iPhone?", "Ask a grown-up to open Settings → Backup copy → Save a copy and keep the file in Files, for example in iCloud Drive. On the other iPhone, or if the game ever starts from scratch, use Restore from a copy. Restoring replaces the progress on that iPhone. If a grown-up picked the wrong file, Bring back the previous progress in the same place returns what was there before."),
            ("Are there ads or in-app purchases?", "No. There are no ads and no purchases for real money. Ants in the shop are bought with stars earned in the game."),
            ("Does the game collect data?", "No. There are no analytics, accounts or tracking. See the <a href=\"{privacy}\">Privacy Policy</a>."),
            ("Which devices are supported?", "iPhone with iOS 18 or later. The game works without the internet."),
        ]),
    "uk": dict(
        intro="«Фуражири» — логічна головоломка про мурашину колонію для iPhone від exception games.",
        contact_h="Зв’язок", contact=f"Пишіть на {MAIL}. Ми читаємо кожен лист і відповідаємо українською, англійською або російською.",
        bug="Знайшли помилку? Вкажіть модель iPhone, версію iOS, номер цеху й опишіть, що сталося. Знімок екрана дуже допоможе.",
        faq_h="Запитання та відповіді",
        faq=[
            ("Де зберігається прогрес?", "Лише на вашому iPhone: облікових записів і хмарної синхронізації немає. Видалення застосунку стирає весь прогрес, тому оновлюйте застосунок, не видаляючи його."),
            ("Як почати цех заново?", "Натисніть «Заново». Щоб повторити навчання, відкрийте «Налаштування» → «Повторити навчання»."),
            ("Не виходить розв’язати. Що робити?", "Натисніть «Скасувати», щоб скасувати останній сигнал, або «Підказка», щоб побачити наступний сигнал. За цех, розв’язаний із підказкою, нараховується лише одна зірка; натисніть «Заново» й розв’яжіть його самостійно, щоб отримати більше. У цеху дня підказки немає."),
            ("Чи можуть грати кілька людей на одному iPhone?", "Так. Додайте гравців у «Налаштування» → «Гравці». У кожного свої зірки, рекорди й мурашки."),
            ("Як зберегти прогрес або перенести його на інший iPhone?", "Попросіть дорослого відкрити «Налаштування» → «Резервна копія» → «Зберегти копію» й покласти файл у «Файли», наприклад в iCloud Drive. На іншому iPhone або якщо гра колись почнеться з нуля, натисніть «Відновити з копії». Відновлення замінює прогрес на тому iPhone. Якщо дорослий вибрав не той файл, «Повернути попередній прогрес» там само поверне те, що було раніше."),
            ("Чи є реклама або покупки в застосунку?", "Ні. Реклами й покупок за справжні гроші немає. Мурашок у крамниці купують за зірки, зароблені в грі."),
            ("Чи збирає гра дані?", "Ні: ні аналітики, ні облікових записів, ні відстеження. Докладніше — у <a href=\"{privacy}\">політиці конфіденційності</a>."),
            ("Які пристрої підтримуються?", "iPhone з iOS 18 або новішою. Гра працює без інтернету."),
        ]),
    "ru": dict(
        intro="«Фуражиры» — логическая головоломка про муравьиную колонию для iPhone от exception games.",
        contact_h="Связь", contact=f"Пишите на {MAIL}. Мы читаем каждое письмо и отвечаем на русском, украинском или английском.",
        bug="Нашли ошибку? Укажите модель iPhone, версию iOS, номер цеха и опишите, что произошло. Снимок экрана очень поможет.",
        faq_h="Вопросы и ответы",
        faq=[
            ("Где хранится прогресс?", "Только на вашем iPhone: аккаунтов и облачной синхронизации нет. Удаление приложения стирает весь прогресс, поэтому обновляйте приложение, не удаляя его."),
            ("Как начать цех заново?", "Нажмите «Заново». Чтобы повторить обучение, откройте «Настройки» → «Повторить обучение»."),
            ("Не получается решить. Что делать?", "Нажмите «Отменить», чтобы отменить последний сигнал, или «Подсказка», чтобы увидеть следующий сигнал. За цех, решённый с подсказкой, даётся одна звезда; нажмите «Заново» и решите его сами, чтобы получить больше. В цехе дня подсказки нет."),
            ("Могут ли играть несколько человек на одном iPhone?", "Да. Добавьте игроков в «Настройки» → «Игроки». У каждого свои звёзды, рекорды и муравьи."),
            ("Как сберечь прогресс или перенести его на другой iPhone?", "Попросите взрослого открыть «Настройки» → «Резервная копия» → «Сохранить копию» и положить файл в «Файлы», например в iCloud Drive. На другом iPhone или если игра когда-нибудь начнётся с нуля, нажмите «Восстановить из копии». Восстановление заменяет прогресс на том iPhone. Если взрослый выбрал не тот файл, «Вернуть прежний прогресс» там же вернёт то, что было раньше."),
            ("Есть ли реклама или покупки в приложении?", "Нет. Рекламы и покупок за реальные деньги нет. Муравьёв в магазине покупают за звёзды, заработанные в игре."),
            ("Собирает ли игра данные?", "Нет: ни аналитики, ни аккаунтов, ни отслеживания. Подробнее — в <a href=\"{privacy}\">политике конфиденциальности</a>."),
            ("Какие устройства поддерживаются?", "iPhone с iOS 18 или новее. Игра работает без интернета."),
        ]),
    "de": dict(
        intro="Futtersucher ist ein Logikrätsel rund um eine Ameisenkolonie für das iPhone, entwickelt von "
              "exception games.",
        contact_h="Kontakt", contact=f"Schreiben Sie an {MAIL}. Wir lesen jede Nachricht und antworten auf Englisch.",
        bug="Möchten Sie einen Fehler melden? Nennen Sie bitte Ihr iPhone-Modell, die iOS-Version und die Nummer "
            "der Werkhalle, und beschreiben Sie, was passiert ist. Ein Screenshot hilft.",
        faq_h="Fragen und Antworten",
        faq=[
            ("Wo wird mein Fortschritt gespeichert?", "Nur auf Ihrem iPhone. Das Spiel hat keine Konten und keine Cloud-Synchronisierung. Wenn Sie die App löschen, geht der gesamte Fortschritt verloren; aktualisieren Sie die App deshalb, ohne sie zu löschen."),
            ("Wie beginne ich eine Werkhalle von vorn?", "Tippen Sie auf „Neustart“. Um die Einführung zu wiederholen, öffnen Sie Einstellungen → Einführung wiederholen."),
            ("Ich komme nicht weiter. Was kann ich tun?", "Tippen Sie auf „Rückgängig“, um das letzte Signal zurückzunehmen, oder auf „Tipp“, um das nächste Signal zu sehen. Eine mit einem Tipp gelöste Werkhalle bringt einen Stern; tippen Sie auf „Neustart“ und lösen Sie sie selbst, um mehr Sterne zu bekommen. Die Werkhalle des Tages hat keinen Tipp."),
            ("Können mehrere Personen auf einem iPhone spielen?", "Ja. Fügen Sie Spieler unter Einstellungen → Spieler hinzu. Jeder Spieler hat eigene Sterne, Rekorde und Ameisen."),
            ("Wie sichere ich den Fortschritt oder bringe ihn auf ein anderes iPhone?", "Bitten Sie einen Erwachsenen, Einstellungen → Sicherungskopie → Kopie sichern zu öffnen und die Datei in „Dateien“ abzulegen, zum Beispiel in iCloud Drive. Auf dem anderen iPhone, oder falls das Spiel einmal von vorn beginnt, verwenden Sie „Aus Kopie wiederherstellen“. Das Wiederherstellen ersetzt den Fortschritt auf diesem iPhone. Hat ein Erwachsener die falsche Datei gewählt, bringt „Früheren Fortschritt zurückholen“ an derselben Stelle zurück, was vorher da war."),
            ("Gibt es Werbung oder In-App-Käufe?", "Nein. Es gibt keine Werbung und keine Käufe mit echtem Geld. Im Ameisenladen werden Ameisen mit Sternen gekauft, die im Spiel verdient wurden."),
            ("Erfasst das Spiel Daten?", "Nein. Es gibt keine Analysedienste, keine Konten und kein Tracking. Mehr dazu in der <a href=\"{privacy}\">Datenschutzerklärung</a>."),
            ("Welche Geräte werden unterstützt?", "iPhone mit iOS 18 oder neuer. Das Spiel funktioniert ohne Internet."),
        ]),
    "ja": dict(
        intro="エサ運びアリは、exception games による、アリのコロニーを舞台にした iPhone 向けロジックパズルゲームです。",
        contact_h="お問い合わせ", contact=f"{MAIL} までご連絡ください。すべてのメッセージに目を通し、英語でお返事します。",
        bug="不具合をご報告いただく際は、iPhone の機種、iOS のバージョン、作業場の番号、何が起きたかをお書きくださ"
            "い。スクリーンショットがあると助かります。",
        faq_h="よくある質問",
        faq=[
            ("進行状況はどこに保存されますか？", "お使いの iPhone の中だけです。アカウントやクラウド同期はありません。App を削除するとすべての進行状況が消えるので、削除せずにアップデートしてください。"),
            ("作業場を最初からやり直すには？", "「やり直す」をタップします。チュートリアルをもう一度遊ぶには、「設定」→「チュートリアルを再プレイ」をタップします。"),
            ("行き詰まりました。どうすればいいですか？", "「元に戻す」をタップすると直前の合図を元に戻せます。「ヒント」をタップすると次の合図がわかります。ヒントを使って解いた作業場は星1つです。「やり直す」をタップして自分で解けば、もっと星がもらえます。今日の作業場にはヒントがありません。"),
            ("1台の iPhone で何人も遊べますか？", "はい。「設定」→「プレイヤー」でプレイヤーを追加してください。プレイヤーごとに星、記録、アリが別々になります。"),
            ("進行状況を守ったり、別の iPhone に移したりするには？", "大人の人に「設定」→「バックアップ」→「バックアップを保存」をタップしてもらい、ファイルを「ファイル」（たとえば iCloud Drive）に保存してください。別の iPhone で、またはゲームが最初からになってしまったときは、「バックアップから復元」を使います。復元すると、その iPhone の進行状況は置き換わります。違うファイルを選んでしまった場合は、同じ場所の「以前の進行状況に戻す」で前の状態に戻せます。"),
            ("広告や App 内課金はありますか？", "いいえ。広告も App 内課金もありません。「アリのお店」のアリは、ゲーム内で獲得した星で買います。"),
            ("ゲームはデータを収集しますか？", "いいえ。解析、アカウント、トラッキングはありません。詳しくは<a href=\"{privacy}\">プライバシーポリシー</a>をご覧ください。"),
            ("対応機種は？", "iOS 18 以降を搭載した iPhone です。インターネットに接続しなくても遊べます。"),
        ]),
    "ko": dict(
        intro="먹이 찾는 개미는 exception games가 만든 iPhone용 개미 마을 논리 퍼즐 게임입니다.",
        contact_h="문의", contact=f"{MAIL}으로 연락해 주세요. 모든 메시지를 읽고 영어로 답변드립니다.",
        bug="버그를 발견하셨나요? iPhone 모델, iOS 버전, 작업장 번호와 어떤 문제가 있었는지 적어 주세요. 스크린샷이 "
            "있으면 도움이 됩니다.",
        faq_h="자주 묻는 질문",
        faq=[
            ("진행 상황은 어디에 저장되나요?", "사용자의 iPhone에만 저장됩니다. 계정이나 클라우드 동기화는 없습니다. 앱을 삭제하면 모든 진행 상황이 지워지므로, 삭제하지 말고 업데이트하세요."),
            ("작업장을 처음부터 다시 하려면 어떻게 하나요?", "‘다시 시작’을 누르세요. 튜토리얼을 다시 하려면 설정 → 튜토리얼 다시 하기를 누르세요."),
            ("막혔어요. 어떻게 해야 하나요?", "‘되돌리기’를 누르면 마지막 신호를 되돌릴 수 있고, ‘힌트’를 누르면 다음 신호를 볼 수 있습니다. 힌트를 써서 풀면 별은 1개입니다. ‘다시 시작’을 누르고 혼자 풀면 별을 더 받을 수 있습니다. 오늘의 작업장에는 힌트가 없습니다."),
            ("iPhone 한 대로 여러 명이 플레이할 수 있나요?", "네. 설정 → 플레이어에서 플레이어를 추가하세요. 플레이어마다 별, 기록, 개미가 따로 있습니다."),
            ("진행 상황을 안전하게 지키거나 다른 iPhone으로 옮기려면 어떻게 하나요?", "어른에게 설정 → 백업 → 백업 저장을 눌러 파일을 ‘파일’(예: iCloud Drive)에 보관해 달라고 하세요. 다른 iPhone에서, 또는 게임이 처음부터 다시 시작되었다면 ‘백업에서 복원’을 사용하세요. 복원하면 그 iPhone의 진행 상황이 바뀝니다. 어른이 잘못된 파일을 골랐다면, 같은 곳의 ‘이전 진행 상황으로 되돌리기’를 누르면 복원 전 상태로 돌아갑니다."),
            ("광고나 인앱 구매가 있나요?", "아니요. 광고도, 유료 결제도 없습니다. 개미 상점의 개미는 게임에서 모은 별로 삽니다."),
            ("게임이 데이터를 수집하나요?", "아니요. 분석, 계정, 추적이 없습니다. <a href=\"{privacy}\">개인정보 처리방침</a>을 참고하세요."),
            ("어떤 기기를 지원하나요?", "iOS 18 이상이 설치된 iPhone입니다. 인터넷 없이도 플레이할 수 있습니다."),
        ]),
    "zh-Hans": dict(
        intro="《搬食物的蚂蚁》是 exception games 推出的一款以蚁群为主题的 iPhone 逻辑解谜游戏。",
        contact_h="联系我们", contact=f"请写信至 {MAIL}。我们会阅读每一封邮件，并用英语回复。",
        bug="要报告问题吗？请写明您的 iPhone 型号、iOS 版本、车间编号以及发生了什么。附上截图会很有帮助。",
        faq_h="常见问题",
        faq=[
            ("我的进度保存在哪里？", "只保存在您的 iPhone 上。游戏没有账户，也没有云同步。删除本应用会清除所有进度，所以请直接更新，不要删除。"),
            ("如何重新开始一个车间？", "点击“重新开始”。要重玩教程，请打开“设置”→“重玩教程”。"),
            ("我卡住了，怎么办？", "点击“撤销”可以撤回上一次信号，点击“提示”可以看到下一次信号。借助提示解开的车间只得一颗星；点击“重新开始”自己解开，就能得到更多星星。今日车间没有提示。"),
            ("一台 iPhone 能多人玩吗？", "可以。在“设置”→“玩家”中添加玩家。每位玩家都有自己的星星、纪录和蚂蚁。"),
            ("如何备份进度，或把它转移到另一台 iPhone？", "请大人打开“设置”→“备份”→“保存备份”，并把文件存放到“文件” App 中，例如 iCloud 云盘。在另一台 iPhone 上，或者游戏哪天从头开始时，请使用“从备份恢复”。恢复会替换那台 iPhone 上的进度。如果大人选错了文件，可以在同一位置点击“恢复之前的进度”，找回原来的内容。"),
            ("有广告或 App 内购买吗？", "没有。没有广告，也没有需用真钱支付的购买项目。商店里的蚂蚁要用游戏中获得的星星购买。"),
            ("游戏会收集数据吗？", "不会。没有分析、账户或跟踪。详见<a href=\"{privacy}\">隐私政策</a>。"),
            ("支持哪些设备？", "搭载 iOS 18 或更高版本的 iPhone。游戏无需联网即可运行。"),
        ]),
    "zh-Hant": dict(
        intro="《搬食物的螞蟻》是 exception games 推出的一款以蟻群為主題的 iPhone 邏輯解謎遊戲。",
        contact_h="聯絡我們", contact=f"請寫信至 {MAIL}。我們會閱讀每一則訊息，並以英文回覆。",
        bug="要回報問題嗎？請寫明您的 iPhone 機型、iOS 版本、工坊編號以及發生了什麼事。附上螢幕截圖會很有幫助。",
        faq_h="常見問題",
        faq=[
            ("我的進度儲存在哪裡？", "只儲存在您的 iPhone 上。遊戲沒有帳號，也沒有雲端同步。刪除本 App 會清除所有進度，所以請直接更新，不要刪除。"),
            ("如何重新開始一個工坊？", "點一下「重新開始」。若要重玩教學，請打開「設定」→「重玩教學」。"),
            ("我卡住了，怎麼辦？", "點一下「復原」可以收回上一次訊號，點一下「提示」可以看到下一次訊號。靠提示解開的工坊只得一顆星；點一下「重新開始」自己解開，就能得到更多星星。今日工坊沒有提示。"),
            ("一台 iPhone 可以多人玩嗎？", "可以。在「設定」→「玩家」中新增玩家。每位玩家都有自己的星星、紀錄與螞蟻。"),
            ("如何備份進度，或把它轉移到另一台 iPhone？", "請大人打開「設定」→「備份」→「儲存備份」，並把檔案存放在「檔案」App 中，例如 iCloud 雲碟。在另一台 iPhone 上，或遊戲哪天從頭開始時，請使用「從備份回復」。回復會取代那台 iPhone 上的進度。如果大人選錯了檔案，可以在同一處點一下「回復之前的進度」，找回原本的內容。"),
            ("有廣告或 App 內購買嗎？", "沒有。沒有廣告，也沒有用真錢購買的項目。「螞蟻商店」裡的螞蟻是用遊戲中贏得的星星購買。"),
            ("遊戲會收集資料嗎？", "不會。沒有分析、帳號或追蹤。詳見<a href=\"{privacy}\">隱私權政策</a>。"),
            ("支援哪些裝置？", "搭載 iOS 18 或以上版本的 iPhone。遊戲不需連網即可執行。"),
        ]),
}

# ---------------------------------------------------------------- rendering

def url(page, lang):
    """Site-root-relative path of a page in a language; the folder is the language code in lower case."""
    return page + ("" if lang == "en" else lang.lower() + "/")


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
    note = "" if lang == "en" else '\n    <p class="translation">' + TRANSLATION_NOTE[lang].format(
        en=f'<a href="{rel(here, url(page, "en"))}" hreflang="en">{ENGLISH_VERSION[lang]}</a>') + "</p>"
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
<a class="skip" href="#main">{SKIP[lang]}</a>
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
  <div class="wrap">© 2026 {ui["footer"]}<span aria-hidden="true"> · </span><span class="nowrap">{MAIL}</span>{note}</div>
</footer>
</body>
</html>
'''


def write(page, lang, title, desc, body):
    path = url(page, lang) + "index.html"
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(render(page, lang, title, desc, body))


def write_redirect(old, new, lang):
    path, target = url(old, lang), url(new, lang)
    os.makedirs(path, exist_ok=True)
    link = rel(path, target)
    with open(path + "index.html", "w", encoding="utf-8") as f:
        f.write(f'''<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex">
  <title>{html.escape(UI[lang]["game"])}</title>
  <link rel="canonical" href="https://exceptiongames.github.io/{target}">
  <meta http-equiv="refresh" content="0; url={link}">
</head>
<body>
<p><a href="{link}">{html.escape(UI[lang]["game"])}</a></p>
</body>
</html>
''')


def build():
    for old, new in OLD_PAGES.items():
        for lang, _ in LANGS:
            write_redirect(old, new, lang)
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
<p class="meta">{p["effective"]}{"：" if lang in ("ja", "zh-Hans", "zh-Hant") else ": "}{UPDATED[lang]}</p>
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
    print("built", len(LANGS) * 4, "pages and", len(LANGS) * len(OLD_PAGES), "redirects")
