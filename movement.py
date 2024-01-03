

def guess_word(letter_cords: dict[tuple, str], word: str, device):
    # letter_cords = {<x,y>: letter} since letters can be repeated! but <x,y> cords not.
    coordinate_sequence = []
    for char in word:
        for key in letter_cords.keys():
            if char == letter_cords[key]:
                print(char, "adding", key)
                coordinate_sequence.append(key)
                letter_cords[key] = None # mark coordinate in letter_cords as used
                break

    if len(coordinate_sequence) < 2:
        print("words of length 0 or 1 are not possible!")
        quit()

    initial_x, initial_y = coordinate_sequence[0]
    final_x, final_y = coordinate_sequence[-1]

    device.shell(f"input motionevent DOWN {initial_x} {initial_y} 100")

    for i in range(1, len(coordinate_sequence)):
        curr_x, curr_y = coordinate_sequence[i]
        device.shell(f"input motionevent MOVE {curr_x} {curr_y} 100")

    device.shell(f"input motionevent UP {final_x} {final_y} 100")
