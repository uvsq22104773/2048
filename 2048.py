import tkinter as tk
import random
from PIL import Image, ImageTk

# Constants

matrice = [[0, 0, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0]]

square = [[None, None, None, None],
          [None, None, None, None],
          [None, None, None, None],
          [None, None, None, None]]

numbers = [[None, None, None, None],
           [None, None, None, None],
           [None, None, None, None],
           [None, None, None, None]]

images = []

# Placing the square and setting the colors for the numbers

game_over = []

place_square = True
status = ""
mix = [False, False, False, False]
score = 0
highscore = 0
i = "y"
color = {2: "#F6B698", 4: "#F0A07A", 8: "#F38D5D", 16: "#EB7C48", 32: "#EA7138", 64: "#EF7B0E", 128: "#F9A150",
         256: "#D6B554", 512: "#DDE84C", 1024: "#D4A61D", 2048: "F86925"}


# Functions

def save_highscore():
    global highscore
    num1 = -1
    save_matrice = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    file = open("save.txt", "r")
    for ligne in file:
        liste = ligne.split()
        if num1 != -1:
            for j in range(len(liste)):
                save_matrice[num1][j] = int(liste[j])
        num1 += 1
    file = open("save.txt", "w")
    file.write(str(highscore) + "\n")
    for num1 in range(len(save_matrice)):
        for j in range(len(save_matrice[num1])):
            file.write(str(save_matrice[num1][j]) + " ")
        file.write("\n")


def save(event):
    global highscore
    file = open("save.txt", "w")
    file.write(str(highscore) + "\n")
    for num1 in range(len(matrice)):
        for j in range(len(matrice[num1])):
            file.write(str(matrice[num1][j]) + " ")
        file.write("\n")


def load(event):
    global matrice, highscore, i, status
    rematch()
    file = open("save.txt", "r")
    for ligne in file:
        liste = ligne.split()
        if type(i) == str:
            if i == "y":
                highscore = int(liste[0])
                i = "n"
            else:
                pass
        elif type(i) == int:
            if i == -1:
                highscore = int(liste[0])
            else:
                for j in range(len(liste)):
                    matrice[i][j] = int(liste[j])
            i += 1
    if type(i) == int:
        for i in range(4):
            for j in range(4):
                if matrice[i][j] != 0:
                    square[i][j] = create_square(j * 98, i * 98, i, j)
                    numbers[i][j] = create_number(j * 98, i * 98, i, j)

        canvas.itemconfigure(button_exit, fill="#565555")
        canvas.itemconfigure(button_save, fill="#565555")
        status = "play"
    bind(False)
    i = -1


def rematch():
    global place_square, matrice, square, numbers, game_over, status
    for num in range(4):
        for j in range(4):
            if square[num][j] is not None:
                canvas.delete(square[num][j])
            if numbers[num][j] is not None:
                canvas.delete(numbers[num][j])
            square[num][j], numbers[num][j], matrice[num][j] = None, None, 0
    for num in range(len(game_over)):
        canvas.delete(game_over[num])
    game_over = []


def play(event):
    global place_square, matrice, square, numbers, game_over, status
    rematch()
    place_square = True
    matrice_game()
    place_square = True
    bind(True)
    canvas.itemconfigure(button_exit, fill="#565555")
    canvas.itemconfigure(button_save, fill="#565555")
    status = "play"


def exit(event):
    global game_over, matrice, status
    place_square, score = False, 0
    unbind()
    opacity_rectangle(101, 111, 499, 509, fill="black", alpha=0.7)
    game_over.append(canvas.create_text((300, 310), text="Game Over", font=("helvetica", "40"), fill="white"))
    for num in range(4):
        for j in range(4):
            score += matrice[num][j]
    game_over.append(canvas.create_text((300, 340), text=str(score), font=("helvetica", "15"), fill="white"))
    canvas.itemconfigure(button_exit, fill="#C6c5c5")
    canvas.itemconfigure(button_save, fill="#C6c5c5")
    status = ""


def detect_lose():
    global place_square, game_over, status
    lose, score = True, 0
    for num in range(4):
        for j in range(4):
            if matrice[num][j] == 0:
                lose = False
            if num != 3 and matrice[num][j] == matrice[num + 1][j]:
                lose = False
            if j != 3 and matrice[num][j] == matrice[num][j + 1]:
                lose = False
    if lose:
        place_square = False
        unbind()
        opacity_rectangle(101, 111, 499, 509, fill="black", alpha=0.7)
        game_over.append(canvas.create_text((300, 310), text="Game Over", font=("helvetica", "40"), fill="white"))
        for num in range(4):
            for j in range(4):
                score += matrice[num][j]
        game_over.append(canvas.create_text((300, 340), text=str(score), font=("helvetica", "15"), fill="white"))
        canvas.itemconfigure(rectangle_exit, fill="#E0e0e0", outline="#E0e0e0")
        canvas.itemconfigure(button_exit, fill="#C6c5c5")
        canvas.itemconfigure(rectangle_save, fill="#E0e0e0", outline="#E0e0e0")
        canvas.itemconfigure(button_save, fill="#C6c5c5")
        status = ""


def matrice_game():
    global square, numbers, place_square, matrice
    if place_square:
        ligne, colonne = random.randint(0, 3), random.randint(0, 3)
        while matrice[ligne][colonne] != 0:
            ligne, colonne = random.randint(0, 3), random.randint(0, 3)

        if square[ligne][colonne] is None:
            random_2_4 = random.randint(0, 9)
            if random_2_4 == 0:
                matrice[ligne][colonne] = 4
            else:
                matrice[ligne][colonne] = 2

            square[ligne][colonne] = create_square(colonne * 98, ligne * 98, ligne, colonne)
            numbers[ligne][colonne] = create_number(colonne * 98, ligne * 98, ligne, colonne)
        place_square = False
    print(matrice[0], "|", square[0], "|", numbers[0]), print(matrice[1], "|", square[1], "|", numbers[1]), print(
        matrice[2], "|", square[2], "|", numbers[2]), print(matrice[3], "|", square[3], "|", numbers[3]), print(
        "-----------")


def create_square(x, y, i, j):
    global color
    square = canvas.create_rectangle((x + 108, y + 118), (198 + x, 208 + y), fill=color[matrice[i][j]],
                                     outline=color[matrice[i][j]])
    return square


def create_number(x, y, ligne, colonne):
    global matrice
    number = canvas.create_text((x + 152, y + 162), text=matrice[ligne][colonne], font=("helvetica", "30"),
                                fill="black")
    return number


def movement_up():
    global square, numbers, matrice, place_square, color, mix
    move = False
    for i in range(4):
        for j in range(4):
            d = 118
            if i != 0 and square[i][j] is not None and square[i - 1][j] is None:
                place_square = True
            if square[i][j] is not None:
                x0, y0, x1, y1 = canvas.coords(square[i][j])
                if i > 0 and square[i - 1][j] is not None:
                    a, b, c, d = canvas.coords(square[i - 1][j])
                    d += 8
                if y0 > d:
                    move = True
                    canvas.move(square[i][j], 0, -2)
                    canvas.move(numbers[i][j], 0, -2)
                    y0 -= 2
                    if y0 == 118: square[i][j], square[i - 1][j], numbers[i][j], numbers[i - 1][j], matrice[i][j], \
                                  matrice[i - 1][j] = None, square[i][j], None, numbers[i][j], 0, matrice[i][j]
                    if y0 == 216: square[i][j], square[i - 1][j], numbers[i][j], numbers[i - 1][j], matrice[i][j], \
                                  matrice[i - 1][j] = None, square[i][j], None, numbers[i][j], 0, matrice[i][j]
                    if y0 == 314: square[i][j], square[i - 1][j], numbers[i][j], numbers[i - 1][j], matrice[i][j], \
                                  matrice[i - 1][j] = None, square[i][j], None, numbers[i][j], 0, matrice[i][j]
                elif i > 0 and matrice[i][j] != 0 and matrice[i - 1][j] != 0 and matrice[i][j] == matrice[i - 1][
                    j] and y0 > b and mix[j] == False:
                    canvas.move(square[i][j], 0, -2)
                    canvas.move(numbers[i][j], 0, -2)
                    move = True
                    if y0 - 2 == b:
                        mix[j] = True
                        if y0 - 2 == 118:
                            mix[j] = "remix"
                        canvas.delete(square[i][j])
                        matrice[i - 1][j] *= 2
                        matrice[i][j] = 0
                        canvas.itemconfigure(square[i - 1][j], fill=color[matrice[i - 1][j]],
                                             outline=color[matrice[i - 1][j]])
                        square[i][j] = None
                        canvas.delete(numbers[i][j])
                        canvas.itemconfigure(numbers[i - 1][j], text=str(matrice[i - 1][j]))
                        numbers[i][j] = None
                        place_square = True
                elif i > 1 and matrice[i][j] != 0 and matrice[i - 1][j] != 0 and matrice[i][j] == matrice[i - 1][
                    j] and y0 > b and mix[j] == "remix":
                    canvas.move(square[i][j], 0, -2)
                    canvas.move(numbers[i][j], 0, -2)
                    move = True
                    if y0 - 2 == b:
                        canvas.delete(square[i][j])
                        matrice[i - 1][j] *= 2
                        matrice[i][j] = 0
                        canvas.itemconfigure(square[i - 1][j], fill=color[matrice[i - 1][j]],
                                             outline=color[matrice[i - 1][j]])
                        square[i][j] = None
                        canvas.delete(numbers[i][j])
                        canvas.itemconfigure(numbers[i - 1][j], text=str(matrice[i - 1][j]))
                        numbers[i][j] = None
                        place_square = True
    if move:
        canvas.after(1, movement_up)
    else:
        bind(True), detect_lose()


def movement_down():
    global square, numbers, matrice, place_square, mix
    move = False
    for i in range(3, -1, -1):
        for j in range(4):
            b = 502
            if i != 3 and square[i][j] is not None and square[i + 1][j] is None:
                place_square = True
            if square[i][j] is not None:
                x0, y0, x1, y1 = canvas.coords(square[i][j])
                if i < 3 and square[i + 1][j] is not None:
                    a, b, c, d = canvas.coords(square[i + 1][j])
                    b -= 8
                if y1 < b:
                    move = True
                    canvas.move(square[i][j], 0, 2)
                    canvas.move(numbers[i][j], 0, 2)
                    y1 += 2
                    if y1 == 502: square[i][j], square[i + 1][j], numbers[i][j], numbers[i + 1][j], matrice[i][j], \
                                  matrice[i + 1][j] = None, square[i][j], None, numbers[i][j], 0, matrice[i][j]
                    if y1 == 404: square[i][j], square[i + 1][j], numbers[i][j], numbers[i + 1][j], matrice[i][j], \
                                  matrice[i + 1][j] = None, square[i][j], None, numbers[i][j], 0, matrice[i][j]
                    if y1 == 306: square[i][j], square[i + 1][j], numbers[i][j], numbers[i + 1][j], matrice[i][j], \
                                  matrice[i + 1][j] = None, square[i][j], None, numbers[i][j], 0, matrice[i][j]
                elif i < 3 and matrice[i][j] != 0 and matrice[i + 1][j] != 0 and matrice[i][j] == matrice[i + 1][
                    j] and y1 < d and mix[j] == False:
                    canvas.move(square[i][j], 0, 2)
                    canvas.move(numbers[i][j], 0, 2)
                    move = True
                    if y1 + 2 == d:
                        mix[j] = True
                        if y1 + 2 == 502:
                            mix[j] = "remix"
                        canvas.delete(square[i][j])
                        matrice[i + 1][j] *= 2
                        matrice[i][j] = 0
                        canvas.itemconfigure(square[i + 1][j], fill=color[matrice[i + 1][j]],
                                             outline=color[matrice[i + 1][j]])
                        square[i][j] = None
                        canvas.delete(numbers[i][j])
                        canvas.itemconfigure(numbers[i + 1][j], text=str(matrice[i + 1][j]))
                        numbers[i][j] = None
                        place_square = True
                elif i < 2 and matrice[i][j] != 0 and matrice[i + 1][j] != 0 and matrice[i][j] == matrice[i + 1][
                    j] and y1 < d and mix[j] == "remix":
                    canvas.move(square[i][j], 0, 2)
                    canvas.move(numbers[i][j], 0, 2)
                    move = True
                    if y1 + 2 == d:
                        canvas.delete(square[i][j])
                        matrice[i + 1][j] *= 2
                        matrice[i][j] = 0
                        canvas.itemconfigure(square[i + 1][j], fill=color[matrice[i + 1][j]],
                                             outline=color[matrice[i + 1][j]])
                        square[i][j] = None
                        canvas.delete(numbers[i][j])
                        canvas.itemconfigure(numbers[i + 1][j], text=str(matrice[i + 1][j]))
                        numbers[i][j] = None
                        place_square = True
    if move:
        canvas.after(1, movement_down)
    else:
        bind(True), detect_lose()


def movement_right():
    global square, numbers, matrice, place_square, mix
    move = False
    for i in range(4):
        for j in range(3, -1, -1):
            a = 492
            if j != 3 and square[i][j] is not None and square[i][j + 1] is None:
                place_square = True
            if square[i][j] is not None:
                x0, y0, x1, y1 = canvas.coords(square[i][j])
                if j < 3 and square[i][j + 1] is not None:
                    a, b, c, d = canvas.coords(square[i][j + 1])
                    a -= 8
                if x1 < a:
                    move = True
                    canvas.move(square[i][j], 2, 0)
                    canvas.move(numbers[i][j], 2, 0)
                    x1 += 2
                    if x1 == 492: square[i][j], square[i][j + 1], numbers[i][j], numbers[i][j + 1], matrice[i][j], \
                                  matrice[i][j + 1] = None, square[i][j], None, numbers[i][j], 0, matrice[i][j]
                    if x1 == 394: square[i][j], square[i][j + 1], numbers[i][j], numbers[i][j + 1], matrice[i][j], \
                                  matrice[i][j + 1] = None, square[i][j], None, numbers[i][j], 0, matrice[i][j]
                    if x1 == 296: square[i][j], square[i][j + 1], numbers[i][j], numbers[i][j + 1], matrice[i][j], \
                                  matrice[i][j + 1] = None, square[i][j], None, numbers[i][j], 0, matrice[i][j]
                elif j < 3 and matrice[i][j] != 0 and matrice[i][j + 1] != 0 and matrice[i][j] == matrice[i][
                    j + 1] and x1 < c and mix[i] == False:
                    canvas.move(square[i][j], 2, 0)
                    canvas.move(numbers[i][j], 2, 0)
                    move = True
                    if x1 + 2 == c:
                        mix[i] = True
                        if x1 + 2 == 492:
                            mix[i] = "remix"
                        canvas.delete(square[i][j])
                        matrice[i][j + 1] *= 2
                        matrice[i][j] = 0
                        canvas.itemconfigure(square[i][j + 1], fill=color[matrice[i][j + 1]],
                                             outline=color[matrice[i][j + 1]])
                        square[i][j] = None
                        canvas.delete(numbers[i][j])
                        canvas.itemconfigure(numbers[i][j + 1], text=str(matrice[i][j + 1]))
                        numbers[i][j] = None
                        place_square = True
                elif j < 2 and matrice[i][j] != 0 and matrice[i][j + 1] != 0 and matrice[i][j] == matrice[i][
                    j + 1] and x1 < c and mix[i] == "remix":
                    canvas.move(square[i][j], 2, 0)
                    canvas.move(numbers[i][j], 2, 0)
                    move = True
                    if x1 + 2 == c:
                        canvas.delete(square[i][j])
                        matrice[i][j + 1] *= 2
                        matrice[i][j] = 0
                        canvas.itemconfigure(square[i][j + 1], fill=color[matrice[i][j + 1]],
                                             outline=color[matrice[i][j + 1]])
                        square[i][j] = None
                        canvas.delete(numbers[i][j])
                        canvas.itemconfigure(numbers[i][j + 1], text=str(matrice[i][j + 1]))
                        numbers[i][j] = None
                        place_square = True
    if move:
        canvas.after(1, movement_right)
    else:
        bind(True), detect_lose()


def movement_left():
    global square, numbers, matrice, place_square, mix
    move = False
    for num in range(4):
        for j in range(4):
            c = 108
            if j != 0 and square[num][j] is not None and square[num][j - 1] is None:
                place_square = True
            if square[num][j] is not None:
                x0, y0, x1, y1 = canvas.coords(square[num][j])
                if j > 0 and square[num][j - 1] is not None:
                    a, b, c, d = canvas.coords(square[num][j - 1])
                    c += 8
                if x0 > c:
                    move = True
                    canvas.move(square[num][j], -2, 0)
                    canvas.move(numbers[num][j], -2, 0)
                    x0 -= 2
                    if x0 == 108: square[num][j], square[num][j - 1], numbers[num][j], numbers[num][j - 1], matrice[num][j], \
                                  matrice[num][j - 1] = None, square[num][j], None, numbers[num][j], 0, matrice[num][j]
                    if x0 == 206: square[num][j], square[num][j - 1], numbers[num][j], numbers[num][j - 1], matrice[num][j], \
                                  matrice[num][j - 1] = None, square[num][j], None, numbers[num][j], 0, matrice[num][j]
                    if x0 == 304: square[num][j], square[num][j - 1], numbers[num][j], numbers[num][j - 1], matrice[num][j], \
                                  matrice[num][j - 1] = None, square[num][j], None, numbers[num][j], 0, matrice[num][j]
                elif j > 0 and matrice[num][j] != 0 and matrice[num][j - 1] != 0 and matrice[num][j] == matrice[num][
                    j - 1] and x1 > a and mix[num] == False:
                    canvas.move(square[num][j], -2, 0)
                    canvas.move(numbers[num][j], -2, 0)
                    move = True
                    if x0 - 2 == a:
                        mix[num] = True
                        if x0 - 2 == 108:
                            mix[num] = "remix"
                        canvas.delete(square[num][j])
                        matrice[num][j - 1] *= 2
                        matrice[num][j] = 0
                        canvas.itemconfigure(square[num][j - 1], fill=color[matrice[num][j - 1]],
                                             outline=color[matrice[num][j - 1]])
                        square[num][j] = None
                        canvas.delete(numbers[num][j])
                        canvas.itemconfigure(numbers[num][j - 1], text=str(matrice[num][j - 1]))
                        numbers[num][j] = None
                        place_square = True
                elif j > 1 and matrice[num][j] != 0 and matrice[num][j - 1] != 0 and matrice[num][j] == matrice[num][
                    j - 1] and x1 > a and mix[num] == "remix":
                    canvas.move(square[num][j], -2, 0)
                    canvas.move(numbers[num][j], -2, 0)
                    move = True
                    if x0 - 2 == a:
                        canvas.delete(square[num][j])
                        matrice[num][j - 1] *= 2
                        matrice[num][j] = 0
                        canvas.itemconfigure(square[num][j - 1], fill=color[matrice[num][j - 1]],
                                             outline=color[matrice[num][j - 1]])
                        square[num][j] = None
                        canvas.delete(numbers[num][j])
                        canvas.itemconfigure(numbers[num][j - 1], text=str(matrice[num][j - 1]))
                        numbers[num][j] = None
                        place_square = True
    if move:
        canvas.after(1, movement_left)
    else:
        bind(True), detect_lose()


def movement(direction):
    unbind()
    if direction == "up": movement_up()
    if direction == "down": movement_down()
    if direction == "right": movement_right()
    if direction == "left": movement_left()


def unbind():
    global root
    root.unbind("w"), root.unbind("s"), root.unbind("d"), root.unbind("a")


def bind(new_game):
    global root, mix, text_score, highscore
    score = 0
    mix = [False, False, False, False]
    root.bind("w", lambda e: movement("up"))
    root.bind("s", lambda e: movement("down"))
    root.bind("d", lambda e: movement("right"))
    root.bind("a", lambda e: movement("left"))
    if new_game:
        matrice_game()
    for num in range(4):
        for j in range(4):
            score += matrice[num][j]
    if score > highscore:
        highscore = score
        save_highscore()
    canvas.itemconfigure(text_score, text=str(score))
    canvas.itemconfigure(text_highscore, text=str(highscore))


# Widgets Creation

root = tk.Tk()
root.title("2048 Game")
canvas = tk.Canvas(root, width=598, height=621, bg="#ececec")

canvas.create_rectangle(108, 118, 198, 208, fill="#DEC164", outline="#818589")
canvas.create_rectangle(206, 118, 296, 208, fill="#DEC164", outline="#818589")
canvas.create_rectangle(304, 118, 394, 208, fill="#DEC164", outline="#818589")
canvas.create_rectangle(402, 118, 492, 208, fill="#DEC164", outline="#818589")
canvas.create_rectangle(108, 216, 198, 306, fill="#DEC164", outline="#818589")
canvas.create_rectangle(206, 216, 296, 306, fill="#DEC164", outline="#818589")
canvas.create_rectangle(304, 216, 394, 306, fill="#DEC164", outline="#818589")
canvas.create_rectangle(402, 216, 492, 306, fill="#DEC164", outline="#818589")
canvas.create_rectangle(108, 314, 198, 404, fill="#DEC164", outline="#818589")
canvas.create_rectangle(206, 314, 296, 404, fill="#DEC164", outline="#818589")
canvas.create_rectangle(304, 314, 394, 404, fill="#DEC164", outline="#818589")
canvas.create_rectangle(402, 314, 492, 404, fill="#DEC164", outline="#818589")
canvas.create_rectangle(108, 412, 198, 502, fill="#DEC164", outline="#818589")
canvas.create_rectangle(206, 412, 296, 502, fill="#DEC164", outline="#818589")
canvas.create_rectangle(304, 412, 394, 502, fill="#DEC164", outline="#818589")
canvas.create_rectangle(402, 412, 492, 502, fill="#DEC164", outline="#818589")

load_rectangle = canvas.create_rectangle(108, 515, 198, 551, fill="#B9B6AB", outline="#E0e0e0")
rectangle_save = canvas.create_rectangle(206, 515, 296, 551, fill="#B9B6AB", outline="#E0e0e0")
play_rectangle = canvas.create_rectangle(304, 515, 394, 551, fill="#B9B6AB", outline="#E0e0e0")
rectangle_exit = canvas.create_rectangle(402, 515, 492, 551, fill="#B9B6AB", outline="#E0e0e0")
button_load = canvas.create_text((153, 533), text="Load", font=("helvetica", "18"), fill="#FFFFFF")
button_save = canvas.create_text((251, 533), text="Save", font=("helvetica", "18"), fill="#FFFFFF")
button_play = canvas.create_text((349, 533), text="Play", font=("helvetica", "18"), fill="#FFFFFF")
button_exit = canvas.create_text((447, 533), text="Exit", font=("helvetica", "18"), fill="#FFFFFF")

canvas.create_rectangle(304, 56, 394, 96, fill="#E0e0e0", outline="#E0e0e0")
canvas.create_text((349, 68), text="SCORE", font=("helvetica", "10"), fill="#565555")
text_score = canvas.create_text((349, 83), text="0", font=("helvetica", "13"), fill="#565555")

canvas.create_rectangle(402, 56, 492, 96, fill="#E0e0e0", outline="#E0e0e0")
canvas.create_text((449, 68), text="HIGHSCORE", font=("helvetica", "10"), fill="#565555")
text_highscore = canvas.create_text((449, 83), text=str(highscore), font=("helvetica", "13"), fill="#565555")

canvas.create_text((204, 76), text="2048", font=("helvetica", "50", "bold"), fill="black")

canvas.grid()
load(1)


# Détection de la position de la souris inspiré de la source: https://codertw.com/程式語言/114662/

def motion(event):
    global status
    x, y = event.x, event.y
    if x > 100 and x < 200 and y > 515 and y < 551:
        root.bind('<Button-1>', load)
    elif x > 200 and x < 300 and y > 515 and y < 551 and status == "play":
        root.bind('<Button-1>', save)
    elif x > 300 and x < 400 and y > 515 and y < 551:
        root.bind('<Button-1>', play)
    elif x > 400 and x < 500 and y > 515 and y < 551 and status == "play":
        root.bind('<Button-1>', exit)
    else:
        root.unbind('<Button-1>')
    # print("Mouse position:", (event.x, event.y))


canvas.bind('<Motion>', motion)


# Sert uniquement pour l'esthétique, source: https://www.tutorialspoint.com/how-to-make-a-tkinter-canvas-rectangle-transparent
def opacity_rectangle(x, y, a, b, **options):
    global game_over
    if 'alpha' in options:
        alpha = int(options.pop('alpha') * 255)
        fill = options.pop('fill')
        fill = root.winfo_rgb(fill) + (alpha,)
        image = Image.new('RGBA', (a - x, b - y), fill)
        images.append(ImageTk.PhotoImage(image))
        game_over.append(canvas.create_image(x, y, image=images[-1], anchor='nw'))
        game_over.append(canvas.create_rectangle(x, y, a, b, **options))


root.mainloop()
