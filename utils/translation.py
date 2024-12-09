def translate(text, lang):
    translation = {
        'You are already on the page':{
            'en':"You are already on the page",
            "uz":"Siz allaqachon asosiy menu dasiz",
            'ru':"Вы уже на странице"
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
        }
    }

    return translation.get(text, {}).get(lang, text)