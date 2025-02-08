import random
import string
import requests
import datetime
import itertools
from concurrent.futures import ThreadPoolExecutor
import sys
import time

class PasswordGenerator:
    def __init__(self):
        self.words = set()
        self.batch_size = 10000
        self.progress = 0
        self.min_length = 8
        self.max_length = 12
       
        # Common patterns and components
        self.patterns = {
            'numbers': [
                '123', '1234', '12345', '111', '000', '2023', '2024',
                '666', '777', '888', '999', '321', '456', '654', '789'
            ],
            'special_chars': ['!', '@', '#', '$', '%', '&', '*', '?', '.'],
            'years': [str(year) for year in range(2020, 2025)],
            'months': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'],
            'common_suffixes': ['123', '1234', '12345', '!', '@', '#', '$'],
            'common_prefixes': ['The', 'My', 'A', 'Super', 'Ultra', 'Mega'],
            'leet_replacements': {
                'a': ['4', '@'],
                'e': ['3'],
                'i': ['1', '!'],
                'o': ['0'],
                's': ['5', '$'],
                't': ['7'],
                'b': ['8'],
                'g': ['9'],
                'z': ['2']
            }
        }

    def fetch_words(self):
        """Fetch base words for password generation"""
        print("Fetching base words...")
       
        # Common base words
        base_words = [
            "pass", "admin", "root", "user", "login",
            "secure", "dragon", "master", "hello", "ninja",
            "super", "tiger", "trust", "power", "magic",
            "cyber", "hack", "system", "network", "cloud",
            "data", "crypto", "secret", "shadow", "dark",
            "light", "fire", "ice", "storm", "thunder",
            "winter", "summer", "spring", "autumn", "star"
        ]
       
        try:
            # Try to fetch additional words from API
            response = requests.get("https://random-word-api.herokuapp.com/word?number=100")
            if response.status_code == 200:
                api_words = [word.lower() for word in response.json()
                           if self.min_length <= len(word) <= self.max_length]
                base_words.extend(api_words)
        except:
            pass
       
        self.words = set(base_words)
        print(f"Loaded {len(self.words)} base words")

    def apply_leet(self, word):
        """Apply leet speak transformations"""
        variations = {word}
       
        for char, replacements in self.patterns['leet_replacements'].items():
            new_variations = set()
            for current in variations:
                if char in current.lower():
                    for replacement in replacements:
                        new_variations.add(current.lower().replace(char, replacement))
            variations.update(new_variations)
       
        return variations

    def generate_word_variations(self, word):
        """Generate variations of a single word"""
        variations = set()
       
        # Base variations
        base_variations = [
            word.lower(),
            word.capitalize(),
            word.upper(),
            word.title()
        ]
       
        # Apply patterns to each base variation
        for base in base_variations:
            # Add numbers
            for num in self.patterns['numbers']:
                variations.add(f"{base}{num}")
                variations.add(f"{num}{base}")
           
            # Add special characters
            for char in self.patterns['special_chars']:
                variations.add(f"{base}{char}")
                variations.add(f"{char}{base}")
                variations.add(f"{base}{char}{char}")
           
            # Add year combinations
            for year in self.patterns['years']:
                variations.add(f"{base}{year}")
           
            # Add month combinations
            for month in self.patterns['months']:
                variations.add(f"{base}{month}")
               
            # Add prefix-suffix combinations
            for prefix in self.patterns['common_prefixes']:
                for suffix in self.patterns['common_suffixes']:
                    variations.add(f"{prefix}{base}{suffix}")
           
            # Add leet speak variations
            variations.update(self.apply_leet(base))
           
            # Add special combinations
            for num in self.patterns['numbers']:
                for char in self.patterns['special_chars']:
                    variations.add(f"{base}{num}{char}")
                    variations.add(f"{base}{char}{num}")
                    variations.add(f"{num}{base}{char}")

        return {v for v in variations
                if self.min_length <= len(v) <= self.max_length}

    def password_generator(self, num_passwords):
        """Generate passwords within length constraints"""
        used_passwords = set()
       
        for word in self.words:
            variations = self.generate_word_variations(word)
           
            for password in variations:
                if len(used_passwords) >= num_passwords:
                    return
               
                if (password not in used_passwords and
                    self.min_length <= len(password) <= self.max_length):
                    used_passwords.add(password)
                    yield password
                   
                    self.progress += 1
                    if self.progress % 1000 == 0:
                        self.print_progress(self.progress, num_passwords)

    def print_progress(self, current, total):
        """Display progress bar"""
        progress = (current / total) * 100
        sys.stdout.write(f'\rProgress: [{current}/{total}] {progress:.1f}%')
        sys.stdout.flush()

    def generate_passwords(self, output_file, num_passwords=250000):
        """Main password generation function"""
        print(f"Starting password generation (length {self.min_length}-{self.max_length})...")
       
        self.fetch_words()
       
        with open(output_file, 'w', encoding='utf-8') as f:
            for password in self.password_generator(num_passwords):
                f.write(f"{password}\n")
               
        print(f"\nCompleted! Generated {self.progress} passwords")

def main():
    try:
        generator = PasswordGenerator()
        generator.generate_passwords("passwords_8_12.txt", 50000)
    except KeyboardInterrupt:
        print("\nGeneration interrupted by user")
    except Exception as e:
        print(f"\nError during generation: {e}")

if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings()
    main()
