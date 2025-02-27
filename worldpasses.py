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
        'fr': {
            'api': "https://api.dictionaryapi.dev/api/v2/entries/fr/",
            'fallback': ['motdepasse', 'bonjour', 'securite', 'administrateur', 'bienvenue', 'secret']
        },
        'ru': {
            'api': "https://api.dictionaryapi.dev/api/v2/entries/ru/",
            'fallback': ['parol', 'sekretniy', 'bezopasnost', 'admin', 'vhod', 'privet']
        },
        'cn': {
            'api': None,  # No API needed for fallback only
            'fallback': ['mima', 'anquan', 'guanliyuan', 'denglu', 'nihao', 'huanying']
        },
        'ng': {  # Nigerian (Yoruba transliterated)
            'api': None,
            'fallback': ['asina', 'asiri', 'alaase', 'wole', 'ekabo', 'aabo']
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
    
    print(f"Generating 250,000 passwords using {lang} words...")

    while len(passwords) < 50000:
        length = random.randint(8, 14)
        all_chars = string.ascii_letters + string.digits + special_chars
        pwd = ''.join(random.choice(all_chars) for _ in range(length))
        passwords.add(pwd)
    
    # Pattern 1: Numbers with special chars (50k)
    while len(passwords) < 100000:
        num = random.randint(100000, 999999999)
        chars = ''.join(random.choices(special_chars, k=random.randint(2,4)))
        pwd = f"{num}{chars}"
        if 8 <= len(pwd) <= 14:
            passwords.add(pwd)
    
    # Pattern 2: 3 letters + 3 numbers + 3 special chars (50k)
    while len(passwords) < 150000:
        letters = ''.join(random.choices(string.ascii_letters, k=3))
        numbers = ''.join(random.choices(string.digits, k=3))
        chars = ''.join(random.choices(special_chars, k=3))
        pwd = f"{letters}{numbers}{chars}"
        passwords.add(pwd)
    
    # Pattern 3: Random mix (50k)
    while len(passwords) < 200000:
        length = random.randint(8, 14)
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
        
        pwd = pattern()
        if 8 <= len(pwd) <= 14:
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
    parser.add_argument('lang', choices=['en', 'fr', 'ru', 'cn', 'ng'],
                      help='Language for word-based passwords (en=English, fr=French, ru=Russian, cn=Chinese, ng=Nigerian)')
    
    args = parser.parse_args()
    generate_passwords(args.lang)

if __name__ == "__main__":
    main()
