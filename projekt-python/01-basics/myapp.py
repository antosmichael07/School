field = [
    [" ", " ", " "],
    [" ", " ", " "],
    [" ", " ", " "]
]

turn = "O"
win = False

def print_field():
    print("     0   1   2")
    print("   +---+---+---+")
    print(f" 0 | {field[0][0]} | {field[1][0]} | {field[2][0]} |")
    print("   +---+---+---+")
    if not win:
        print(f" 1 | {field[0][1]} | {field[1][1]} | {field[2][1]} |   Player {turn} is playing...")
    else:
        print(f" 1 | {field[0][1]} | {field[1][1]} | {field[2][1]} |   Player {turn} won!")
    print("   +---+---+---+")
    print(f" 2 | {field[0][2]} | {field[1][2]} | {field[2][2]} |")
    print("   +---+---+---+")

def switch_players():
    global turn

    if turn == "X":
        turn = "O"
        return
    if turn == "O":
        turn = "X"
        return
    
def check_win():
    global win

    # Vertical |
    for x in range(3):
        win = True
        for y in range(3):
            if field[x][y] != turn:
                win = False
                break
        if win:
            return

    # Horizontal -
    for y in range(3):
        win = True
        for x in range(3):
            if field[x][y] != turn:
                win = False
                break
        if win:
            return

    # Diagonal \
    win = True
    for i in range(3):
        if field[i][i] != turn:
            win = False
            break
    if win:
        return

    # Diagonal /
    win = True
    for i in range(3):
        if field[i][-i-1] != turn:
            win = False
            break
    if win:
        return

# --------------- Start --------------- #

while not win:
    switch_players()
    print_field()

    while True:
        x = int(input("X coordinate: "))
        y = int(input("Y coordinate: "))

        if x > 2 or y > 2:
            print("Invalid move, keep it in the field")
        elif field[x][y] ==  " ":
            field[x][y] = turn
            break
        else:
            print("Invalid move, don't overwrite someone's symbol")

    check_win()

print_field()
