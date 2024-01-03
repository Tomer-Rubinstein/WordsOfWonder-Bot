import requests
import re

def unscramble_letters(letters: str) -> list[str]:
    html = requests.get(f'https://wordunscrambler.me/unscramble/{letters}').text
    regex_exp = r'data-word="(.*?)"'

    anagrams = [
        word
        for word in re.findall(regex_exp, html)
        if len(word) > 2
    ]    

    return anagrams
