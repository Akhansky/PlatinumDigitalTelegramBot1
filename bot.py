from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8386635045:AAGFvD3elLsT3AIWAWPlCnuWsoKo2ZJ6TUA"

user_state = {}

WELCOME = {
    "en": "*Welcome to Platinum Digital!*\nPlease select the service you are interested in.",
    "ru": "*Добро пожаловать в компанию Platinum Digital!*\nПожалуйста, выберите интересующую вас услугу.",
    "km": "*ស្វាគមន៍មកកាន់ក្រុមហ៊ុន Platinum Digital!*\nសូមជ្រើសរើសសេវាកម្មដែលអ្នកចាប់អារម្មណ៍។"
}

SERVICES = {
    "en": [
        ("🌐 Website Design", "service_website"),
        ("📅 Booking and OTA Set-up", "service_booking"),
        ("🎨 Logo Design", "service_logo"),
        ("📦 Company Branding Kit", "service_branding"),
        ("📣 Social Media Promotion (Monthly)", "service_social"),
        ("🔍 SEO", "service_seo"),
        ("📍 Google Business & Maps Set-Up", "service_maps")
    ],
    "ru": [
        ("🌐 Создание сайта", "service_website"),
        ("📅 Настройка Booking и OTA", "service_booking"),
        ("🎨 Дизайн логотипа", "service_logo"),
        ("📦 Фирменный стиль", "service_branding"),
        ("📣 Продвижение в соцсетях (ежемесячно)", "service_social"),
        ("🔍 SEO", "service_seo"),
        ("📍 Google Бизнес и Карты", "service_maps")
    ],
    "km": [
        ("🌐 ការរចនាគេហទំព័រ", "service_website"),
        ("📅 ការកំណត់ Booking និង OTA", "service_booking"),
        ("🎨 ការរចនាឡូហ្គោ", "service_logo"),
        ("📦 កញ្ចប់ស្លាកសញ្ញា", "service_branding"),
        ("📣 ផ្សព្វផ្សាយបណ្តាញសង្គម (សេវាប្រចាំខែ)", "service_social"),
        ("🔍 SEO", "service_seo"),
        ("📍 Google Business & Maps Set-Up", "service_maps")
    ]
}

SERVICE_TEXTS = {
    "en": {
        "service_website": "🌐 Website Design by Platinum Digital\n\nWe create modern, responsive, and user-friendly websites tailored to your business needs.\n\n🔹 Custom design\n🔹 Mobile optimized\n🔹 Fast performance\n🔹 SEO-friendly\n\n💰 Starts at $50\n\nLet’s build your online presence today!",
        "service_booking": "📅 Booking and OTA Set-up\n\nWe help you set up and manage your online booking systems and OTA channels efficiently.\n\n🔹 Channel management\n🔹 Integration with PMS\n🔹 Calendar sync\n🔹 Reporting and analytics\n\n💰 Prices start at just $25\n\nBoost your bookings and streamline operations!",
        "service_logo": "🎨 Logo Design by Platinum Digital\n\nNeed a logo that stands out and truly represents your brand?\n\nWe create modern, custom logos that are memorable, scalable, and tailored to your business identity.\n\n🔹 Unique concept\n🔹 High-quality formats\n🔹 Fast delivery\n🔹 100% original design\n\n💰 Flat price: $10\n\nLet’s create your brand’s signature look!",
        "service_branding": "📦 Company Branding Kit\n\nWant a professional, consistent look for your business?\n\nOur Branding Kit includes everything you need to establish a strong visual identity.\n\n🔹 Custom logo design\n🔹 Social media visuals\n🔹 Color palette & typography\n🔹 Brand style guide\n\n💰 Starts at $70\n\nBuild trust and recognition today!",
        "service_social": "📣 Social Media Promotion (Monthly)\n\nWant to grow your audience and stay visible online — every day?\n\nWe offer monthly marketing services for Facebook, Instagram, Google Ads, and TikTok.\n\n🔹 Content creation & posting\n🔹 Ad setup & optimization\n🔹 Platform management\n🔹 Reports & insights\n\n💰 Starts at $150/month\n\nLet’s grow your brand — one post at a time.",
        "service_seo": "🔍 Search Engine Optimization (SEO)\n\nWant more traffic and better Google rankings?\n\nOur SEO service helps your site rank higher and attract the right audience.\n\n🔹 Keyword research\n🔹 On-page optimization\n🔹 Technical SEO fixes\n🔹 Backlink strategies\n\n💰 Starts at $50\n\nBoost visibility and results now!",
        "service_maps": "📍 Google Business & Maps Set-Up\n\nMake sure customers can find you instantly on Google.\n\nWe’ll set up and optimize your Google Business profile and Maps listing.\n\n🔹 Google Business profile setup\n🔹 Map pin placement\n🔹 Info, hours & photos upload\n🔹 SEO-friendly optimization\n\n💰 Flat price: $20\n\nBe seen by locals and tourists alike!"
    },
    "ru": {
        "service_website": "🌐 Создание сайта от Platinum Digital\n\nСоздаём современные, адаптивные и удобные сайты под нужды вашего бизнеса.\n\n🔹 Индивидуальный дизайн\n🔹 Оптимизация для мобильных\n🔹 Быстрая загрузка\n🔹 SEO-оптимизация\n\n💰 От $50\n\nСоздайте ваше онлайн-присутствие уже сегодня!",
        "service_booking": "📅 Настройка Booking и OTA\n\nМы поможем вам наладить систему онлайн-бронирования и интеграции с OTA.\n\n🔹 Управление каналами\n🔹 Интеграция с PMS\n🔹 Синхронизация календаря\n🔹 Аналитика и отчёты\n\n💰 От $25\n\nУвеличьте бронирования и упростите процессы!",
        "service_logo": "🎨 Дизайн логотипа от Platinum Digital\n\nНужен логотип, который выделяется и отражает суть бренда?\n\n🔹 Уникальная концепция\n🔹 Высокое качество\n🔹 Быстрая доставка\n🔹 100% оригинальный дизайн\n\n💰 Фиксированная цена: $10\n\nСоздадим лицо вашего бренда!",
        "service_branding": "📦 Фирменный стиль\n\nХотите профессиональный и цельный имидж для бизнеса?\n\n🔹 Дизайн логотипа\n🔹 Оформление соцсетей\n🔹 Цвета и шрифты\n🔹 Гайд по стилю\n\n💰 От $70\n\nПовышайте доверие к бренду!",
        "service_social": "📣 Продвижение в соцсетях (ежемесячно)\n\nХотите быть видимыми каждый день?\n\n🔹 Создание контента\n🔹 Настройка рекламы\n🔹 Ведение страниц\n🔹 Отчёты и аналитика\n\n💰 От $150 в месяц\n\nРазвивайте бренд — шаг за шагом.",
        "service_seo": "🔍 SEO (поисковая оптимизация)\n\nХотите больше трафика и позиций в Google?\n\n🔹 Ключевые слова\n🔹 SEO-оптимизация страниц\n🔹 Технические исправления\n🔹 Построение ссылок\n\n💰 От $50\n\nУлучшите видимость уже сегодня!",
        "service_maps": "📍 Настройка Google Business и Карт\n\nЧтобы вас находили быстро и легко.\n\n🔹 Создание профиля Google\n🔹 Точка на карте\n🔹 Загрузка фото, графика, инфо\n🔹 SEO-настройки\n\n💰 $20\n\nСтаньте видимы в онлайне!"
    },
    "km": {
        "service_website": "🌐 ការរចនាគេហទំព័រ\n\nយើងបង្កើតគេហទំព័រដែលទាន់សម័យ ងាយប្រើ និងសមស្របនឹងអាជីវកម្មរបស់អ្នក។\n\n🔹 រចនាផ្ទាល់ខ្លួន\n🔹 ជាប្រភេទ Mobile-Friendly\n🔹 ល្បឿនលឿន\n🔹 SEO Friendly\n\n💰 ចាប់ពី $50\n\nចាប់ផ្តើមស្ថាបនា៖ អត្តសញ្ញាអនឡាញរបស់អ្នកថ្ងៃនេះ!",
        "service_booking": "📅 ការកំណត់ Booking និង OTA\n\nយើងជួយអ្នកដំឡើងនិងគ្រប់គ្រងប្រព័ន្ធការកក់តាមអនឡាញ។\n\n🔹 គ្រប់គ្រងប៉ុស្តិ៍\n🔹 ភ្ជាប់ទៅ PMS\n🔹 Sync ប្រតិទិន\n🔹 របាយការណ៍\n\n💰 ចាប់ពី $25\n\nបង្កើនការកក់របស់អ្នក!",
        "service_logo": "🎨 ការរចនាឡូហ្គោ\n\nតើអ្នកត្រូវការ Logo ដែលទាក់ទាញ និងទាក់ទងនឹងម៉ាករបស់អ្នក?\n\n🔹 គំនិតដើម\n🔹 គុណភាពខ្ពស់\n🔹 ផ្ដល់ជូនលឿន\n🔹 រចនាដើមសុទ្ធ\n\n💰 $10\n\nបង្កើតអត្តសញ្ញាផ្លូវការរបស់អ្នក!",
        "service_branding": "📦 កញ្ចប់ស្លាកសញ្ញា\n\nសម្លេងដ៏វិជ្ជាជីវៈសម្រាប់អាជីវកម្មរបស់អ្នក។\n\n🔹 Logo ផ្ទាល់ខ្លួន\n🔹 ប្លង់បណ្តាញសង្គម\n🔹 ពណ៌និងអក្សរ\n🔹 សៀវភៅរចនាម៉ាក\n\n💰 ចាប់ពី $70\n\nបង្កើតភាពជឿជាក់ និង ការទទួលស្គាល់។",
        "service_social": "📣 ផ្សព្វផ្សាយបណ្តាញសង្គម (ប្រចាំខែ)\n\nស្ថាបនាជំនឿជាក់បណ្តាញអនឡាញ។\n\n🔹 បង្កើតមាតិកា\n🔹 ផ្សាយពាណិជ្ជកម្ម\n🔹 គ្រប់គ្រងគណនី\n🔹 របាយការណ៍\n\n💰 ចាប់ពី $150/ខែ\n\nពង្រីកសញ្ញាអាជីវកម្មរបស់អ្នក។",
        "service_seo": "🔍 SEO (បង្កើនលទ្ធភាពក្នុងការ​ស្វែងរក)\n\nចង់ឲ្យគេឃើញគេហទំព័ររបស់អ្នក?\n\n🔹 ស្រាវជ្រាវពាក្យគន្លឹះ\n🔹 អុបទិម៉ាយទំព័រ\n🔹 ជួសជុលបច្ចេកទេស\n🔹 Strategy Backlink\n\n💰 ចាប់ពី $50\n\nកើនលទ្ធភាព និងលទ្ធផល។",
        "service_maps": "📍 Google Business & Maps\n\nដើម្បីអតិថិជនរកឃើញអ្នកបានភ្លាមៗ។\n\n🔹 បង្កើតគណនី Google\n🔹 បង្ហាញទីតាំង\n🔹 ផ្ទុកព័ត៌មាន\n🔹 បង្កើនSEO\n\n💰 តម្លៃ $20\n\nឲ្យមនុស្សនៅជិតអ្នកឃើញអ្នក។"
    }
}

def language_keyboard():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
        InlineKeyboardButton("🇰🇭 ខ្មែរ", callback_data="lang_km"),
        InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")
    ]])

def main_keyboard(lang):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(name, callback_data=code)] for name, code in SERVICES[lang]
    ] + [[InlineKeyboardButton("🔙 Back", callback_data="back_to_lang")]])

def service_keyboard(lang):
    contact_button = {
        "en": "📞 Contact Us",
        "ru": "📞 Свяжитесь с нами",
        "km": "📞 ទំនាក់ទំនង​ពួក​យើង"
    }.get(lang, "📞 Contact Us")

    return InlineKeyboardMarkup([
        [InlineKeyboardButton(contact_button, callback_data="contact")],
        [InlineKeyboardButton("🔙 Back", callback_data="back_to_services")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Choose your language / ជ្រើសរើសភាសា / Выберите язык",
        reply_markup=language_keyboard()
    )

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id

    if data.startswith("lang_"):
        lang = data[5:]
        context.user_data["lang"] = lang
        user_state[user_id] = "services"
        await query.edit_message_text(WELCOME[lang], reply_markup=main_keyboard(lang), parse_mode="Markdown")

    elif data.startswith("service_"):
        lang = context.user_data.get("lang", "en")
        context.user_data["last_menu"] = "services"
        context.user_data["last_lang"] = lang
        text = SERVICE_TEXTS[lang][data]
        await query.edit_message_text(text, reply_markup=service_keyboard(lang))

    elif data == "back_to_services":
        lang = context.user_data.get("last_lang", "en")
        await query.edit_message_text(WELCOME[lang], reply_markup=main_keyboard(lang), parse_mode="Markdown")

    elif data == "back_to_lang":
        await query.edit_message_text(
            "Choose your language / Выберите язык / ជ្រើសរើសភាសា",
            reply_markup=language_keyboard()
        )

    elif data == "contact":
        # Отправляем ссылку на Telegram профиль
        await query.edit_message_text(
            "📬 Click the link to contact us:\nhttps://t.me/PlatinumDigital202"
        )

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    print("Бот запущен")
    app.run_polling()
