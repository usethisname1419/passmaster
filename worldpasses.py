import random
import string
import requests
import argparse

def get_random_words(lang='en', count=1000):
    """Get random words based on language (using latin characters)"""
    
    # API endpoints and fallback words for different languages
    lang_data = {
        'en': {
            'api': "https://random-word-api.herokuapp.com/word?number=1000",
            'fallback': ['password', 'secret', 'secure', 'admin', 'login', 'welcome']
        },
        'es': {
            'api': "https://api.dictionaryapi.dev/api/v2/entries/es/",
            'fallback': ['contrasena', 'secreto', 'seguro', 'administrador', 'bienvenido', 'entrada', 'clave', 'usuario']
        },
        'da': {
            'api': "https://api.dictionaryapi.dev/api/v2/entries/da/",
            'fallback': ['adgangskode', 'sikkerhed', 'administrator', 'velkommen', 'hemmelighed', 'bruger', 'kodeord']
        },
        'fi': {
            'api': "https://api.dictionaryapi.dev/api/v2/entries/fi/",
            'fallback': ['salasana', 'turvallisuus', 'yllapitaja', 'tervetuloa', 'kayttaja', 'hallinta', 'kirjaudu']
        },
        'no': {
            'api': "https://api.dictionaryapi.dev/api/v2/entries/no/",
            'fallback': ['passord', 'sikkerhet', 'administrator', 'velkommen', 'bruker', 'innlogging', 'hemmelighet']
        },
        'fr': {
            'api': "https://api.dictionaryapi.dev/api/v2/entries/fr/",
            'fallback': ['motdepasse', 'bonjour', 'securite', 'administrateur', 'bienvenue', 'secret']
        },
        'ru': {
            'api': "https://api.dictionaryapi.dev/api/v2/entries/ru/",
            'fallback': ['parol', 'sekretniy', 'bezopasnost', 'admin', 'vhod', 'privet']
        },
        'cn': {
            'api': None,
            'fallback': [
        'mima', 'anquan', 'guanliyuan', 'denglu', 'nihao', 'huanying',
        'yonghu', 'zhanghu', 'shouji', 'youxiang', 'wenben', 'shujuku',
        'wangluo', 'ruanjian', 'yingjian', 'xitong', 'zhuce', 'tuichu',
        'kaishi', 'jieshu', 'bangzhu', 'shezhi', 'geren', 'gongsi',
        'xuexiao', 'laoshi', 'xuesheng', 'pengyou', 'jiating', 'gonggong',
        'beijing', 'shanghai', 'xianggang', 'taiwan', 'zhongguo', 'meiguo',
        'yingyu', 'hanyu', 'riyu', 'xiandai', 'gudai', 'weilai'
    ]
        },
        'ng': {
            'api': None,
            'fallback': [
        'asina', 'asiri', 'alaase', 'wole', 'ekabo', 'aabo',
        'oluko', 'akeko', 'ile', 'omo', 'baba', 'iya', 
        'olorun', 'eniyan', 'alafia', 'owuro', 'ale', 'osan',
        'ojo', 'osu', 'odun', 'opolopo', 'kere', 'tobi',
        'dara', 'buru', 'gbogbo', 'okan', 'meji', 'meta',
        'iwe', 'ise', 'owo', 'ile', 'oko', 'oja',
        'lagos', 'ibadan', 'ife', 'abeokuta', 'osun', 'oyo',
        'yoruba', 'hausa', 'igbo', 'nigeria', 'afrika', 'duniya'
    ]
        }
    }
    if lang not in lang_data:
        print(f"Unsupported language {lang}, using English")
        lang = 'en'
    
    word_list = []
    
    # Try API if available
    if lang_data[lang]['api']:
        try:
            response = requests.get(lang_data[lang]['api'])
            if response.status_code == 200:
                word_list = response.json()
        except:
            print(f"API failed for {lang}, using fallback words")
    
    # Use fallback if no words or no API
    if not word_list:
        word_list = lang_data[lang]['fallback']
    
    return word_list

def generate_passwords(lang='en'):
    special_chars = "!$@#*^()%&"
    words = get_random_words(lang)
    passwords = set()
    
    print(f"Generating 400,000 passwords using {lang} words...")
    
    # NEW: Pattern 0: Totally Random (50k)
    while len(passwords) < 50000:
        length = random.randint(8, 15)
        all_chars = string.ascii_letters + string.digits + special_chars
        pwd = ''.join(random.choice(all_chars) for _ in range(length))
        passwords.add(pwd)
    
    # Pattern 1: Numbers with special chars (50k)
    while len(passwords) < 100000:
        num = random.randint(100000, 999999999)
        chars = ''.join(random.choices(special_chars, k=random.randint(2,4)))
        pwd = f"{num}{chars}"
        if 8 <= len(pwd) <= 15:
            passwords.add(pwd)
    
    # Pattern 2: 3 letters + 3 numbers + 3 special chars (50k)
    while len(passwords) < 150000:
        letters = ''.join(random.choices(string.ascii_letters, k=3))
        numbers = ''.join(random.choices(string.digits, k=3))
        chars = ''.join(random.choices(special_chars, k=3))
        pwd = f"{letters}{numbers}{chars}"
        passwords.add(pwd)
    
    # Pattern 3: Semi-structured mix (50k)
    while len(passwords) < 200000:
        length = random.randint(8, 15)
        parts = [
            ''.join(random.choices(string.ascii_letters, k=random.randint(3,5))),
            ''.join(random.choices(string.digits, k=random.randint(2,4))),
            ''.join(random.choices(special_chars, k=random.randint(2,3)))
        ]
        random.shuffle(parts)
        pwd = ''.join(parts)
        passwords.add(pwd)
    
    # Pattern 4: Word-based passwords (50k)
    while len(passwords) < 250000:
        word = random.choice(words)
        pattern = random.choice([
            lambda: word + str(random.randint(1990,2024)) + random.choice(special_chars),
            lambda: word + random.choice(special_chars) + ''.join(random.choices(string.digits, k=3)),
            lambda: word.title() + random.choice(special_chars) + str(random.randint(2020,2024)),
            lambda: word + ''.join(random.choices(string.digits, k=2)) + random.choice(words)
        ])
    # Pattern 5: Mixed case with special chars and numbers (50k)
    while len(passwords) < 300000:
        letters = ''.join(random.choices(string.ascii_letters, k=random.randint(4,6)))
        numbers = ''.join(random.choices(string.digits, k=random.randint(2,4)))
        chars = ''.join(random.choices(special_chars, k=random.randint(2,3)))
        pwd = f"{letters}{numbers}{chars}"
        passwords.add(pwd)
    
    # Pattern 6: Word + Random Special Char + Year (50k)
    while len(passwords) < 350000:
        word = random.choice(words)
        year = random.randint(2010, 2024)
        chars = random.choice(special_chars)
        pwd = f"{word}{chars}{year}"
        if 8 <= len(pwd) <= 15:
            passwords.add(pwd)

  
    # NEW: Pattern 7: 2 words + 3 numbers + special char (50k)
    while len(passwords) < 400000:
        word1 = random.choice(words)
        word2 = random.choice(words)
        numbers = ''.join(random.choices(string.digits, k=3))
        special_char = random.choice(special_chars)
        pwd = f"{word1}{word2}{numbers}{special_char}"
        if 8 <= len(pwd) <= 15:
            passwords.add(pwd)

    
    # Write to file
    filename = f'world-passwords_{lang}.txt'
    with open(filename, 'w') as f:
        for password in passwords:
            f.write(password + '\n')
    
    print(f"\nGenerated {len(passwords)} passwords and saved to {filename}")
    print("\nSample passwords:")
    for pwd in list(passwords)[:5]:
        print(pwd)

def main():
    parser = argparse.ArgumentParser(description='Generate passwords with different language words')
    parser.add_argument('lang', choices=['en', 'es', 'da', 'fi', 'no', 'fr', 'ru', 'cn', 'ng'],
                      help='Language for word-based passwords (en=English, es=Spanish, da=Danish, fi=Finnish, no=Norwegian, fr=French, ru=Russian, cn=Chinese, ng=Nigerian)')
    
    args = parser.parse_args()
    generate_passwords(args.lang)

if __name__ == "__main__":
    main()
