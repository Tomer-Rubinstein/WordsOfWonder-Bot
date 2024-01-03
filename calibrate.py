import subprocess
import pickle

GETEVENT_MAX_VALUE = 4040
# adb shell wm size
screen_width = 1080
screen_height = 2340

process = subprocess.Popen(["adb", "shell", "getevent", "-l"], stdout=subprocess.PIPE)

curr_x = 0
curr_y = 0

taps = []
while True:
    output = process.stdout.readline().decode().strip()
    if output is None and process.poll() is not None:
        break
    if output:
        # first comes ABS_MT_POSITION_X and then immediately ABS_MT_POSITION_Y
        if "ABS_MT_POSITION_X" in output:
            curr_x = int(output.split(' ')[-1], 16)
            curr_x = curr_x * screen_width // GETEVENT_MAX_VALUE

        if "ABS_MT_POSITION_Y" in output:
            curr_y = int(output.split(' ')[-1], 16)
            curr_y = curr_y * screen_height // GETEVENT_MAX_VALUE

            if curr_y < screen_height/3:
                # user signals to stop listening for further taps
                break

            print(f"[+] found: ({curr_x}, {curr_y})")
            taps.append(tuple([curr_x, curr_y]))

            curr_x = 0
            curr_y = 0

rc = process.poll()

print("saving taps:", taps)
pickle.dump(taps, open(f"{len(taps)}_taps.p", "wb"))
