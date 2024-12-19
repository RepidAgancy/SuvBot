from aiogram.utils.i18n import I18n


def translate(text, lang):
    translation = {
        'You are already on the page':{
            'en':"You are already on the page",
            "uz":"Siz allaqachon asosiy menu dasiz",
            'ru':"Вы уже на странице"
        },
        'Kompaniyani locatsiyasini kiriting:':{
            'ru':'Введите местоположение компании:',
            'uz':'Kompaniyani locatsiyasini kiriting:',
            'en':'Enter location of your place:'

        },
        'Order successfully added, after 2 days later you will get':{
            'en':'Order successfully added, after 2 days later you will get',
            'uz':'Buyurtma muvvafaqiyatli qoshildi va 2 kundan song yetib boradi',
            'ru':'Заказ успешно добавлен, через 2 дня вы получите',
        },
        'Please select your language':{
            'en':'Please select your language:',
            'uz':'Iltimos kerakli tilni tanglang:',
            'ru':"Пожалуйста, выберите язык:"
        },
        'Please select a valid language from the options.':{
            'en':'Please select a valid language from the options.',
            'uz':'Iltimos togri tilni tanlang',
            'ru':'Пожалуйста, выберите действительный язык из вариантов.'
        },
        'Enter your phone number or send number':{
            'en':'Enter your phone number or send number',
            'uz':'Telefon raqamni tanglang yoki telefon raqam jonating',
            'ru':'Введите свой номер телефона или отправьте номер'
        },
        'Select valid language':{
            'en':'Select valid language',
            'ru':'Выберите действительный язык',
            'uz':'Kerakli tilni tanglang'
        },
        "Language successfully changed":{
            'en':'Language successfully changed',
            'uz':'Til muvafaqiyatli o\'zgartirildi',
            'ru':'Язык успешно изменен'
        },
        'You come to the main home again':{
            'en':'You come to the main home again',
            'uz':'Asosiy sahifaga keldingiz',
            'ru':'Вы снова приходите в главный дом',
        },
        'Foydalanuvchi turini kiritng':{
            'en':'Foydalanuvchi turini kiritng',
            'uz':'Foydalanuvchi turini kiritng',
            'ru':'Введите тип пользователя',
        },
        'Yuridik shaxs':{
            'en':'Legel entity',
            'ru':'Юридическое лицо',
            'uz':'Yuridik shaxs'
        },
        'Jismoniy shaxs':{
            'en':'Physical person',
            'uz':'Jismoniy shaxs',
            'ru':'Физическое лицо'
        },
        'Kompany nomini kiriting':{
            'en':"Enter company name",
            'uz':'Kompany nomini kiriting',
            'ru':'Введите название компании'
        },
        'Telefon raqamingizni kiriting':{
            'en':'Enter phone number',
            'uz':'Telefon raqamingizni kiriting',
            "ru":'Введите свой номер телефона',
        },
        'Kompaniya nomi 100 sozdan oshmasin': {
            'en': "Company name must not exceed 100 characters.",
            'uz': "Kompaniya nomi 100 sozdan oshmasin.",
            'ru': "Название компании не должно превышать 100 символов."
        },
        'Telefon raqam kiriting':{
            'uz':'Telefon raqam kiriting',
            'en':"Enter phone number",
            'ru':'Введите номер телефона'
        },
        'Botimizga xush kelibsiz':{
            'en':"Welcome to our water bot",
            'uz':'Botimizga xush kelibsiz',
            'ru':'Добро пожаловать в наш бот'
        },
        '🇺🇿 Til':{
            'en':'🇺🇿 Language',
            'uz':'🇺🇿 Til',
            'ru':'🇺🇿 Язык'
        },
        "📱 Phone number": {
        "uz": "📱 Telefon raqami",
        "ru": "📱 Номер телефона",
        "en": "📱 Phone number"
    },
    "Tasdiqlayman": {
        "uz": "Tasdiqlayman",
        "ru": "Подтверждаю",
        "en": "Confirm"
    },
    "Qo'lda kiritaman": {
        "uz": "Qo'lda kiritaman",
        "ru": "Ввод вручную",
        "en": "Enter manually"
    },
    "Location": {
        "uz": "Manzil",
        "ru": "Локация",
        "en": "Location"
    },
    "💧 Mahsulotlar": {
        "uz": "💧 Mahsulotlar",
        "ru": "💧 Продукты",
        "en": "💧 Products"
    },
    "🛒 Korzinka": {
        "uz": "🛒 Korzinka",
        "ru": "🛒 Корзина",
        "en": "🛒 Basket"
    },
    "Buyurtmani qayta takrorlash": {
        "uz": "Buyurtmani qayta takrorlash",
        "ru": "Повторить заказ",
        "en": "Repeat the order"
    },
    "💴 Suv harid qlish": {
        "uz": "💴 Suv harid qilish",
        "ru": "💴 Купить воду",
        "en": "💴 Buy water"
    },
    "🛠 Sozlamalar": {
        "uz": "🛠 Sozlamalar",
        "ru": "🛠 Настройки",
        "en": "🛠 Settings"
    },
    "🇺🇿 Til": {
        "uz": "🇺🇿 Til",
        "ru": "🇺🇿 Язык",
        "en": "🇺🇿 Language"
    },
    "Back": {
        "uz": "Ortga",
        "ru": "Назад",
        "en": "Back"
    },
    "Basket products": {
        "uz": "Korzinkadagi mahsulotlar",
        "ru": "Товары в корзине",
        "en": "Basket products"
    },
    "Choose products": {
        "uz": "Mahsulotlarni tanlang",
        "ru": "Выберите продукты",
        "en": "Choose products"
    },
    "I choose your option": {
        "uz": "Men sizning variantingizni tanlayman",
        "ru": "Я выбираю ваш вариант",
        "en": "I choose your option"
    },
    "Barcha mahsulotlar": {
        "uz": "Barcha mahsulotlar",
        "ru": "Все продукты",
        "en": "All products"
    },
    "Mahsulot qo'shish": {
        "uz": "Mahsulot qo'shish",
        "ru": "Добавить продукт",
        "en": "Add product"
    },
    "Barcha buyurtmalar": {
        "uz": "Barcha buyurtmalar",
        "ru": "Все заказы",
        "en": "All orders"
    },
    "Buyurtmalar tarixi": {
        "uz": "Buyurtmalar tarixi",
        "ru": "История заказов",
        "en": "Order history"
    },
    "Qayta takrorlash": {
        "uz": "Qayta takrorlash",
        "ru": "Повторить",
        "en": "Repeat"
    },
    "Jismoniy shaxs": {
        "uz": "Jismoniy shaxs",
        "ru": "Физическое лицо",
        "en": "Individual"
    },
    "Yuridik shaxs": {
        "uz": "Yuridik shaxs",
        "ru": "Юридическое лицо",
        "en": "Legal entity"
    },
    "Barcha mahsulotlar": {
        "uz": "Barcha mahsulotlar",
        "ru": "Все продукты",
        "en": "All products"
    },
    "Mahsulot qo'shish": {
        "uz": "Mahsulot qo'shish",
        "ru": "Добавить продукт",
        "en": "Add product"
    },
    "Barcha buyurtmalar": {
        "uz": "Barcha buyurtmalar",
        "ru": "Все заказы",
        "en": "All orders"
    },
    "Buyurtmalar tarixi": {
        "uz": "Buyurtmalar tarixi",
        "ru": "История заказов",
        "en": "Order history"
    },
    "Qayta takrorlash": {
        "uz": "Qayta takrorlash",
        "ru": "Повторить",
        "en": "Repeat"
    },
    "Uzr jigar korzinkada hech nima yo'q":{
        'uz':'Buyurtmalar topilmadi',
        'ru':'Заказы не найдены',
        'en':"Basket items not found"
    },
    'Tilni tanlang':{
        'en':'Choose language',
        'uz':'Tilni tanlang',
        'ru':'Выберите язык'
    },
    "According to your input:\n"
        "— Number of employees: {number_employee}\n"
        "— Number of days: {time_drink_water}\n"
        "— Location: {location}\n\n"
        "Based on the provided information, you need to purchase {water_needed} units of 18.9 liters of water.":{
        "en": (
        "According to your input:\n"
        "— Number of employees: {number_employee}\n"
        "— Number of days: {time_drink_water}\n"
        "— Location: {location}\n\n"
        "Based on the provided information, you need to purchase {water_needed} units of 18.9 liters of water."
    ),
    "uz": (
        "Sizning ma'lumotlaringiz asosida:\n"
        "— Xodimlar soni: {number_employee}\n"
        "— Kunlar soni: {time_drink_water}\n"
        "— Joylashuv: {location}\n\n"
        "Berilgan ma'lumotlarga asoslanib, sizga {water_needed} dona 18.9 litr suv xarid qilish kerak."
    ),
    "ru": (
        "Согласно вашим данным:\n"
        "— Количество сотрудников: {number_employee}\n"
        "— Количество дней: {time_drink_water}\n"
        "— Местоположение: {location}\n\n"
        "На основании предоставленной информации вам нужно приобрести {water_needed} единиц воды объемом 18.9 литра."
    )
        },
    'Bu mazilni tasdiqlaysizmi **{location_}**':{
        'uz':'Bu mazilni tasdiqlaysizmi **{location_}**',
        'en':'Did you verify location **{location_}',
        'ru':'Можете ли вы подтвердить это местоположение **{location_}**'
    },
    "How many emplyee have":{
        'en':"How many emplyee have",
        'ru':'Сколько сотрудников',
        'uz':'Nechta hodim ishlaydi'
    },
    'Qolda kirit':{
        'en':'Enter your location',
        'uz':'Hozirgi turgan joyizni kiriting',
        'ru':'Введите свое текущее местоположение'
    },
    'Input location !!!!!:':{
        'en':'Input location !!!!!',
        'uz':'Locatsiyani kiriting',
        'ru':'Место ввода !!!!!',
    },
    'How may days needed water:':{
        'en':'How may days needed water:',
        'uz':'Nechi kunga suv yetishi kerak',
        'ru':'Сколько дней понадобится вода:'
    },
    'Please input digits only':{
        'en':'Please input digits only',
        'uz':'Faqat raqamlar kiriting',
        'ru':'Пожалуйста, вводите только цифры'
    },
    "order_added": {
        "en": "Order successfully added! Delivery will take place in 2 days.",
        "uz": "Buyurtma muvaffaqiyatli qo'shildi! Yetkazib berish 2 kun ichida amalga oshiriladi.",
        "ru": "Заказ успешно добавлен! Доставка состоится через 2 дня."
    },
    "order_added_final": {
        "en": "Order successfully added, after 2 days later you will get.",
        "uz": "Buyurtma muvaffaqiyatli qo'shildi, 2 kun ichida olasiz.",
        "ru": "Заказ успешно добавлен, через 2 дня вы получите."
    },
    "error_occurred": {
        "en": "An error occurred. Please try again.",
        "uz": "Xatolik yuz berdi. Iltimos, qayta urinib ko'ring.",
        "ru": "Произошла ошибка. Пожалуйста, попробуйте снова."
    },
    "choose_product": {
        "en": "Choose product and continue.",
        "uz": "Mahsulotni tanlang va davom eting.",
        "ru": "Выберите продукт и продолжите."
    },
    "How many do you need product?": {
        "en": "How many do you need product?",
        "uz": "Mahsulotdan nechta kerak?",
        "ru": "Сколько вам нужно продукта?"
    },
    "Please enter a valid quantity (digits only).": {
        "en": "Please enter a valid quantity (digits only).",
        "uz": "Iltimos, to'g'ri miqdorni kiriting (faqat raqamlar).",
        "ru": "Пожалуйста, введите правильное количество (только цифры)."
    },
    "Error: Product not found.": {
        "en": "Error: Product not found.",
        "uz": "Xatolik: Mahsulot topilmadi.",
        "ru": "Ошибка: Продукт не найден."
    },
    "Error: Basket not found.": {
        "en": "Error: Basket not found.",
        "uz": "Xatolik: Korzina topilmadi.",
        "ru": "Ошибка: Корзина не найдена."
    },
    'How may litrs needed:':{
        'en':'How may litrs needed:',
        'ru':'Сколько литров понадобится:',
        'uz':'Qancha kerak suv'
    },
    'Recommandation products':{
        'en':'Recommandation products',
        'uz':'Tafsiyani olish',
        'ru':'Получить предложение'
    },
    'Choose product and continue':{
        'en':'Choose product and continue',
        'ru':'Выберите продукт и продолжайте',
        'uz':'Mahsulot tanlang va davom ettiring'
    },
    "🛍 Product: {name}\n"
            "📦 Quantity: {quantity}\n"
            "💰 Price per item: {price} UZS\n"
            "🔢 Total: {total} UZS\n":{
                'en':"🛍 Product: {name}\n"
                    "📦 Quantity: {quantity}\n"
                    "💰 Price per item: {price} UZS\n"
                    "🔢 Total: {total} UZS\n",
                'ru':"🛍Продукт: {name}\n"
                    "📦 Количество: {quantity}\n"
                    "💰 Цена за единицу товара: {price} UZS\n"
                    "🔢 Всего: {total} сум\n",
               'uz':"🛍Mahsulot: {name}\n"
                    "📦 Miqdor: {miqdor}\n"
                    "💰 Birlik narxi: {narx} so'm\n"
                    "🔢 Jami: {jami} summa\n"
            },
        'Item is deleted successfully':{
            'en':'Item is deleted successfully',
            'ru':'Объект успешно удален',
            'uz':"Mahsulot muvaffaqiyatli o'chirildi"
        },
    'All products':{
        'en':'All products',
        'uz':'Barcha mahsulotlar',
        'ru':'Все продукты'
    },
    '''
📋 Company Details:
- 🏢 Company Name: {company_name}
- 📞 Contact: {company_contact}
- 👷 Number of Employees: {number_employee} ta
- 📍 Address: {location}
- 🚚 Delivery Time: {time_drink} kun
- 🕒 Order Date: {created_at}

📦 Products:
        ''':{
        'uz':'''
📋 Kompaniya haqida ma'lumot:
- 🏢 Kompaniya nomi: {company_name}
- 📞 Aloqa: {company_contact}
- 👷 Xodimlar soni: {son_xodim}
- 📍Manzil: {joy}
- 🚚 Yetkazib berish muddati: {time_drink} kun.
- 🕒 Buyurtma sanasi: {created_at}

📦Mahsulotlar:''',
        'ru':'''
📋 Подробности о компании:
- 🏢 Название компании: {company_name}
- 📞 Контакт: {company_contact}
- 👷 Количество сотрудников: {number_employee}
- 📍Адрес: {location}
- 🚚 Срок доставки: {time_drink} дней.
- 🕒 Дата заказа: {created_at}

📦Продукция:''',
        'en':''' 
📋 Company Details:
- 🏢 Company Name: {company_name}
- 📞 Contact: {company_contact}
- 👷 Number of Employees: {number_employee} ta
- 📍 Address: {location}
- 🚚 Delivery Time: {time_drink} kun
- 🕒 Order Date: {created_at}

📦 Products'''
    },
    'Qayta takrorlash':{
        'en':'Repeat once',
        'uz':'Qayta takrorlash',
        'ru':'Повторите еще раз'
    },
    'Nomi: {name} Narxi: {price}':{
        'en':"Name: {name}"

            "Price: {price}",
        'uz':"Nomi: {name}"

            "Narxi: {price}",
        'ru':"Имя: {name}"

            "Цена: {price}",
    },
    ''' 
    - 🛍 Product Name: {product_name}
    - 🔢 Quantity: {quantity}
    - 💰 Price: {price} UZS''':{
            'en':'''
    - 🛍 Product Name: {product_name}
    - 🔢 Quantity: {quantity}
    - 💰 Price: {price} UZS''',
                'ru':'''
    - 🛍 Название продукта: {product_name}
    - 🔢 Количество: {quity}
    - 💰 Цена: {price} сум.''',
                'uz':'''
    - 🛍 Mahsulot nomi: {mahsulot_nomi}
    - 🔢 Miqdori: {quity}
    - 💰 Narxi: {narxi} so'm.'''

        },
        'Buyurtma rasmilashtirildi':{
            'en':'Order completed successfully',
            'ru':'Заказ выполнен',
            'uz':'Buyurtma rasmilashtirildi'
        },
     '''
Nomi: {name}

Narxi: {price}
            ''':{
        'en': '''
Name: {name}

Price: {price}
            ''',
    'ru':'''
Имя: {name}

Цена: {price}''',
    'uz':'''
Nome: {name}

Narxi: {price}
''',
    },
    'Nechta kerak':{
        'en':'How many needed',
        'uz':'Nechta kerak',
        'ru':'Сколько вам нужно?'
    },
    ''' 🛍 Product: {name}
            📦 Quantity: {quantity}
            💰 Price per item: {price} UZS
            🔢 Total: {total} UZS''':{
                'en':''' 
            🛍 Product: {name}
            📦 Quantity: {quantity}
            💰 Price per item: {price} UZS
            🔢 Total: {total} UZS''',

            'uz':''' 
            🛍 Mahsulot: {name}
            📦 Soni: {quantity}
            💰 Mahsulot narxi: {price} UZS
            🔢 Jamo: {total} UZS''',
            
            'ru':'''
            🛍 Товар: {name}
            📦 Количество: {quantity}
            💰 Цена за единицу: {price} сум.
            🔢 Итого: {total} UZS'''
   },
        '❌ Delete':{
            'en':'❌ Delete',
            'uz':"❌ 'Ochirish",
            'ru':'❌ Удалить'
        },
        'Product add basket successfully':{
            'en':'Product add basket successfully',
            'ru':'Товар успешно добавлен в корзину',
            'uz':"Mahsulot korzinkaga qo'shildi"
        },
        'Sizda hali buyurtmalar yoq':
        {
            'en':'You do not have orders',
            'uz':'Sizda hali buyurtmalar yoq',
            'ru':'У вас еще есть заказы'
        }
    }

    return translation.get(text, {}).get(lang, text)



