from ppadb.client import Client as AdbClient
import movement
from letter_detection import find_transformed_letters_cords
from PIL import Image
from gpt import GPT
from unscramble import unscramble_letters
import time

def get_first_device():
    client = AdbClient()
    devices = client.devices()

    if len(devices) == 0:
        print("no device attached")
        quit()

    return devices[0]


def save_screenshot(device, out_filename):
    screencap = device.screencap()
    with open(out_filename, "wb") as f:
        f.write(screencap)

if __name__ == "__main__":
    device = get_first_device()
    save_screenshot(device, "screen.png")

    letters_cords = find_transformed_letters_cords("screen.png")
    print("letters_cords:", letters_cords)

    letters = "".join(list(letters_cords.values()))
    print("found letters:", letters)

    # ---> USE GPT-3.5 WITH OPENAI API KEY
    """
    gpt_api = GPT()
    anagrams = gpt_api.find_anagrams(letters)
    """

    # ---> OR USE ONLINE WORD SCRAMBLER (FASTER, MORE ACCURATE, NO API KEY)
    anagrams = unscramble_letters(letters)

    print("found anagrams:", anagrams)

    for anagram in anagrams:
        print("trying:", anagram)
        movement.guess_word(dict(letters_cords), anagram, device)
        time.sleep(0.1)
