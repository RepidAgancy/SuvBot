def translate(text, lang):
    translation = {
        'You are already on the page':{
            'en':"You are already on the page",
            "uz":"Siz allaqachon asosiy menu dasiz",
            'ru':"VI uje na asnovnoy menu"
        }
    }

    return translation.get(text, {}).get(lang, text)