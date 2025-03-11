import argparse
import sys
import random
from typing import List
from rich.progress import Progress
from rich.console import Console
from itertools import combinations

class WordlistManipulator:
    def __init__(self):
        self.console = Console()
        # Previous prefixes and suffixes lists remain (from last script)
        # Adding new transformation patterns
        self.prefixes = [
            # Years
            "2024", "2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015",
            
            # Common Numbers
            "123", "1234", "12345", "111", "000", "999", "666", "777", "888", "555",
            "11", "22", "33", "44", "55", "66", "77", "88", "99", "00",
            "01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
            
            # Special Characters
            "!", "@", "#", "$", "%", "^", "&", "*", "(", ")",
            "_", "-", "+", "=", "~", "`", "<", ">", "?", "/",
            "!@", "@#", "#$", "$%", "%^", "^&", "&*", "*(", "()", "_+",
            "!@#", "@#$", "#$%", "$%^", "%^&", "^&*", "&*(", "*()", "_+_",
            
            # Number Patterns
            "123", "234", "345", "456", "567", "678", "789", "890",
            "321", "432", "543", "654", "765", "876", "987", "098",
            "111", "222", "333", "444", "555", "666", "777", "888", "999", "000",
            "1122", "2233", "3344", "4455", "5566", "6677", "7788", "8899", "9900",
            
            # Mixed Special Characters and Numbers
            "1!", "2@", "3#", "4$", "5%", "6^", "7&", "8*", "9(", "0)",
            "!1", "@2", "#3", "$4", "%5", "^6", "&7", "*8", "(9", ")0",
            "1@", "2#", "3$", "4%", "5^", "6&", "7*", "8(", "9)", "0_",
            
            # Repeating Patterns
            "11", "111", "1111", "22", "222", "2222", "33", "333", "3333",
            "44", "444", "4444", "55", "555", "5555", "66", "666", "6666",
            "77", "777", "7777", "88", "888", "8888", "99", "999", "9999",
            
            # Special Sequences
            "0x", "0X", "0z", "0Z", "1x", "1X", "1z", "1Z", "2x", "2X",
            "__", "--", "++", "**", "@@", "##", "$$", "%%", "&&", "||",
            
            # More Complex Patterns
            "1a", "2b", "3c", "4d", "5e", "6f", "7g", "8h", "9i", "0j",
            "a1", "b2", "c3", "d4", "e5", "f6", "g7", "h8", "i9", "j0",
            
            # Binary-style
            "0b", "1b", "10", "01", "001", "010", "011", "100", "101", "110",
            
            # Hex-style
            "0x", "1x", "2x", "3x", "4x", "5x", "6x", "7x", "8x", "9x",
            
            # More Special Characters Combinations
            ".-", "._", ".~", ".-_", "._~", ".~-", "-.", "_.", "~.",
            "+=", "-=", "*=", "/=", "!=", "@=", "#=", "$=", "%=", "^="
        ]

        # Expanded list of suffixes
        self.suffixes = [
            # Years
            "2024", "2023", "2022", "2021", "2020", "2019", "2018", "2017", "2016", "2015", "1990", "1985", "1999", "2000",
            
            # Common Numbers
            "123", "1234", "12345", "111", "000", "999", "666", "777", "888", "555",
            "11", "22", "33", "44", "55", "66", "77", "88", "99", "00",
            "01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
            
            # Special Characters
            "!", "@", "#", "$", "%", "^", "&", "*", "(", ")",
            "_", "-", "+", "=", "~", "`", "<", ">", "?", "/",
            "!@", "@#", "#$", "$%", "%^", "^&", "&*", "*(", "()", "_+",
            "!@#", "@#$", "#$%", "$%^", "%^&", "^&*", "&*(", "*()", "_+_",
            
            # Number Patterns
            "123", "234", "345", "456", "567", "678", "789", "890",
            "321", "432", "543", "654", "765", "876", "987", "098",
            "111", "222", "333", "444", "555", "666", "777", "888", "999", "000",
            
            # Mixed Special Characters and Numbers
            "1!", "2@", "3#", "4$", "5%", "6^", "7&", "8*", "9(", "0)",
            "!1", "@2", "#3", "$4", "%5", "^6", "&7", "*8", "(9", ")0",
            
            # Common Number Endings
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
            "00", "01", "02", "03", "04", "05", "06", "07", "08", "09",
            
            # Special Character Endings
            "_1", "_2", "_3", "_4", "_5", "_6", "_7", "_8", "_9", "_0",
            "-1", "-2", "-3", "-4", "-5", "-6", "-7", "-8", "-9", "-0",
            
            # More Complex Endings
            "!!", "@@", "##", "$$", "%%", "^^", "&&", "**", "((", "))",
            "!@#", "#@!", "$#@", "@#$", "#$%", "%$#", "&^%", "%^&",
            
            # Binary and Hex
            "0x0", "0x1", "0x2", "0x3", "0x4", "0x5", "0x6", "0x7", "0x8", "0x9",
            "0b0", "0b1", "0b00", "0b01", "0b10", "0b11",
            
            # Special Sequences
            ".0", ".1", ".2", ".3", ".4", ".5", ".6", ".7", ".8", ".9",
            "_0", "_1", "_2", "_3", "_4", "_5", "_6", "_7", "_8", "_9",
            
            # More Special Characters
            "+=", "-=", "*=", "/=", "!=", "@=", "#=", "$=", "%=", "^=",
            "++", "--", "**", "//", "!!", "@@", "##", "$$", "%%", "^^",
            
            # Complex Number Patterns
            "001", "002", "003", "004", "005", "006", "007", "008", "009",
            "101", "202", "303", "404", "505", "606", "707", "808", "909",
            
            # Special Character Combinations
            "._", ".-", ".~", "._-", ".-~", ".~_", "-.", "_.", "~.",
            "+=", "-=", "*=", "/=", "!=", "@=", "#=", "$=", "%=", "^="
        ]
        
        self.leet_map = {
            'a': ['4', '@', 'A', 'α', '∆'],
            'b': ['8', 'B', '13', 'ß'],
            'e': ['3', 'E', '€', 'ε'],
            'g': ['6', '9', 'G'],
            'i': ['1', '!', '|', 'I', 'ï'],
            'l': ['1', '|', 'L', '£'],
            'o': ['0', 'O', 'ø', 'θ'],
            's': ['5', '$', 'S', '§'],
            't': ['7', '+', 'T'],
            'z': ['2', 'Z', 'ζ']
        }

        self.number_patterns = [
            "0123", "1234", "2345", "3456", "4567", "5678", "6789",
            "9876", "8765", "7654", "6543", "5432", "4321", "3210",
            "0000", "1111", "2222", "3333", "4444", "5555", "6666", "7777", "8888", "9999",
            "0101", "1010", "2020", "3030", "4040", "5050", "6060", "7070", "8080", "9090",
            "1212", "2323", "3434", "4545", "5656", "6767", "7878", "8989", "9090",
            "0123456789", "9876543210",
            "112233", "445566", "778899", "998877", "665544", "332211",
            "121212", "232323", "343434", "454545", "565656", "676767", "787878", "898989",
            "11235813", # Fibonacci
            "31415926", # Pi
            "27182818", # e
            "13579", "24680", # Odd/Even
            "19283746", "64728391" # Keyboard patterns
        ]

        self.special_sequences = [
            "!@#$",
            "!@#",
            "@#$",
            "#$%",
            "!@",
            "@#",
            "#$",
            "$%",
            "_%",
            "_@",
            "-_",
            "._",
            "_.",
            "-.",
            ".-",
            "!_",
            "@_",
            "#_",
            "$_",
            "%_",
            "_!",
            "_@",
            "_#",
            "_$",
            "_%",
            "!-",
            "@-",
            "#-",
            "$-",
            "%-",
            "-!",
            "-@",
            "-#",
            "-$",
            "-%",
            ".",
            "_",
            "-",
            "!",
            "@",
            "#",
            "$",
            "%",
            "&",
            "*"
        ]

        self.keyboard_patterns = [
            "qwerty", "asdfgh", "zxcvbn",
            "qwertyuiop", "asdfghjkl", "zxcvbnm",
            "1qaz", "2wsx", "3edc", "4rfv", "5tgb", "6yhn",
            "7ujm", "8ik,", "9ol.", "0p;/",
            "1qaz2wsx", "3edc4rfv", "5tgb6yhn", "7ujm8ik,",
            "zxcvasdfqwer", "poiulkjhmnbv"
        ]

    def generate_complex_patterns(self, word: str) -> List[str]:
        """Generate complex patterns from the word."""
        patterns = set()
        
        # Reverse patterns
        patterns.add(word[::-1])
        patterns.add(word + word[::-1])
        patterns.add(word[::-1] + word)
        
        # Duplicate patterns
        patterns.add(word * 2)
        patterns.add(word + word.upper())
        patterns.add(word.upper() + word)
        
        # Alternating case
        patterns.add(''.join(c.upper() if i % 2 else c.lower() for i, c in enumerate(word)))
        patterns.add(''.join(c.lower() if i % 2 else c.upper() for i, c in enumerate(word)))
        
        # Mirror patterns
        patterns.add(word + ''.join(reversed(word)))
        
        # Incremental patterns
        for i in range(1, min(5, len(word))):
            patterns.add(word + word[:i])
            patterns.add(word[:i] + word)
        
        return list(patterns)

    def apply_leet_speak(self, word: str) -> List[str]:
        """Apply leet speak transformations."""
        leet_words = set()
        leet_words.add(word)
        
        # Generate combinations of leet replacements
        for char in word.lower():
            if char in self.leet_map:
                new_words = set()
                replacements = self.leet_map[char]
                for current_word in leet_words:
                    for replacement in replacements:
                        new_words.add(current_word.replace(char, replacement))
                leet_words.update(new_words)
        
        return list(leet_words)

    def apply_random_transformations(self, word: str) -> List[str]:
        """Apply random transformations to the word."""
        transformed = set()
        
        # Random case transformations
        transformed.add(word.upper())
        transformed.add(word.lower())
        transformed.add(word.capitalize())
        transformed.add(word.title())
        
        # Random number appendages
        for _ in range(3):
            transformed.add(f"{word}{random.randint(0, 999):03d}")
            transformed.add(f"{random.randint(0, 999):03d}{word}")
        
        # Random special character insertions
        special_chars = "!@#$%^&*"
        for _ in range(2):
            char = random.choice(special_chars)
            pos = random.randint(0, len(word))
            transformed.add(word[:pos] + char + word[pos:])
        
        # Random pattern combinations
        if random.random() < 0.3:  # 30% chance
            pattern = random.choice(self.number_patterns)
            transformed.add(f"{word}{pattern}")
        
        if random.random() < 0.3:  # 30% chance
            sequence = random.choice(self.special_sequences)
            transformed.add(f"{sequence}{word}")
        
        return list(transformed)

    def manipulate_word(self, word: str) -> List[str]:
        """Generate variations of a word using various transformations."""
        variations = set()
        
        # Base word
        variations.add(word)
        
        # Apply complex patterns
        variations.update(self.generate_complex_patterns(word))
        
        # Apply leet speak transformations
        variations.update(self.apply_leet_speak(word))
        
        # Apply random transformations
        variations.update(self.apply_random_transformations(word))
        
        # Random prefix/suffix application
        if random.random() < 0.4:  # 40% chance for prefix
            prefix = random.choice(self.prefixes)
            variations.add(f"{prefix}{word}")
        
        if random.random() < 0.4:  # 40% chance for suffix
            suffix = random.choice(self.suffixes)
            variations.add(f"{word}{suffix}")
        
        # Special combinations (less frequent)
        if random.random() < 0.2:  # 20% chance for both
            prefix = random.choice(self.prefixes)
            suffix = random.choice(self.suffixes)
            variations.add(f"{prefix}{word}{suffix}")
        
        # Add some keyboard patterns
        if random.random() < 0.3:  # 30% chance
            pattern = random.choice(self.keyboard_patterns)
            variations.add(f"{word}{pattern}")
            variations.add(f"{pattern}{word}")
        
        return list(variations)

    def process_wordlist(self, input_file: str, output_file: str):
        """Process the input wordlist and write variations to output file."""
        try:
            # Read input file
            with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
                words = [line.strip() for line in f if line.strip()]

            total_words = len(words)
            all_variations = set()

            # Process each word with progress bar
            with Progress() as progress:
                task = progress.add_task("[cyan]Processing wordlist...", total=total_words)

                for word in words:
                    variations = self.manipulate_word(word)
                    all_variations.update(variations)
                    progress.advance(task)

            # Write output file
            with open(output_file, 'w', encoding='utf-8') as f:
                for variation in sorted(all_variations):
                    f.write(f"{variation}\n")

            self.console.print(f"\n[green]Success![/green]")
            self.console.print(f"Original words: {total_words}")
            self.console.print(f"Generated variations: {len(all_variations)}")
            self.console.print(f"Output saved to: {output_file}")

        except Exception as e:
            self.console.print(f"[red]Error: {str(e)}[/red]")
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Advanced Wordlist Manipulator")
    parser.add_argument("-i", "--input", required=True, help="Input wordlist file")
    parser.add_argument("-o", "--output", required=True, help="Output file for modified wordlist")
    args = parser.parse_args()

    manipulator = WordlistManipulator()
    manipulator.process_wordlist(args.input, args.output)

if __name__ == "__main__":
    main()

