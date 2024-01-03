from ppadb.client import Client as AdbClient
import movement
from letter_detection import find_transformed_letters_cords
from PIL import Image
from gpt import GPT
from unscramble import unscramble_letters
import time

client = AdbClient()
devices = client.devices()

if len(devices) == 0:
    print("no device attached")
    quit()

device = devices[0]

screencap = device.screencap()
with open("screen.png", "wb") as f:
    f.write(screencap)

letters_cords = find_transformed_letters_cords("screen.png")
print("letters_cords:", letters_cords)

letters = "".join(list(letters_cords.values()))

# gpt_api = GPT()
# anagrams = gpt_api.find_anagrams(letters)

anagrams = unscramble_letters(letters.lower())

print("got anagarms:", anagrams)
print("from letters:", letters)

for anagram in anagrams:
    print("trying:", anagram)
    movement.guess_word(dict(letters_cords), anagram, device)
    time.sleep(0.5)
