from ppadb.client import Client as AdbClient
import movement
from letter_detection import find_transformed_letters_cords
from PIL import Image

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
print(letters_cords)

movement.guess_word(letters_cords, "RIPEC", device)
