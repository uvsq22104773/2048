import itertools
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
color = {2: "#b0e3f6", 4: "#b1cae9", 8: "#c0bbdc", 16: "#cfb1d5",
         32: "#e1b0d0", 64: "#f6accd", 128: "#fac0b5", 256: "#fdd6ab",
         512: "#fce8b3", 1024: "#ebefb2", 2048: "#d7e8b2", 4096: "#d9e8b1",
         8192: "#cee7c7", 16384: "#c7e6d7", 32768: "#a7d8bb", 65536: "#8dcca6",
         131072: "#52d085"}


# Functions

def save_highscore():
    # enregistre le meilleur score dans un fichier save.txt
    global highscore
    save_matrice = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    file = open("save.txt", "r")
    for num1, ligne in enumerate(file, start=-1):
        liste = ligne.split()
        if num1 != -1:
            for j in range(len(liste)):
                save_matrice[num1][j] = int(liste[j])
    file = open("save.txt", "w")
    file.write(str(highscore) + "\n")
    for item in save_matrice:
        for j in range(len(item)):
            file.write(f"{str(item[j])} ")
        file.write("\n")


def save(event):
    # ouvre le fichier save.txt puis écris le score de la matrice du jeux
    global highscore
    file = open("save.txt", "w")
    file.write(str(highscore) + "\n")
    for num1 in range(len(matrice)):
        for j in range(len(matrice[num1])):
            file.write(f"{str(matrice[num1][j])} ")
        file.write("\n")


def load(event):
    # charge le fichier save.txt et redémare la fonction rematche (netoie la grille de la partie en cour)
    global matrice, highscore, i, status
    rematch()
    file = open("save.txt", "r")
    for ligne in file:
        liste = ligne.split()
        if type(i) == str:
            if i == "y":
                highscore = int(liste[0])
                i = "n"
        elif type(i) == int:
            if i == -1:
                highscore = int(liste[0])
            else:
                for j in range(len(liste)):
                    matrice[i][j] = int(liste[j])
            i += 1
    if type(i) == int:
        for i, j in itertools.product(range(4), range(4)):
            if matrice[i][j] != 0:
                square[i][j] = create_square(j * 98, i * 98, i, j)
                numbers[i][j] = create_number(j * 98, i * 98, i, j)

        canvas.itemconfigure(button_exit, fill="#565555")
        canvas.itemconfigure(button_save, fill="#565555")
        status = "play"
    bind(False)
    i = -1


def rematch():
    # suprimme tous les canvas presents
    global place_square, matrice, square, numbers, game_over, status
    for num, j in itertools.product(range(4), range(4)):
        if square[num][j] is not None:
            canvas.delete(square[num][j])
        if numbers[num][j] is not None:
            canvas.delete(numbers[num][j])
        square[num][j], numbers[num][j], matrice[num][j] = None, None, 0
    for num in range(len(game_over)):
        canvas.delete(game_over[num])
    game_over = []


def play(event):
    # demare le jeux en nettoyant la grille et fait apparaitre 2 carrés
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
    # crée un canvas transparent qui marque que la partie est terminee
    global game_over, matrice, status
    square_placement, score1 = False, 0
    unbind()
    opacity_rectangle(101, 111, 499, 509, fill="black", alpha=0.7)
    game_over.append(canvas.create_text(
        (300, 310), text="Game Over", font=("helvetica", "40"), fill="white"))
    for num, j in itertools.product(range(4), range(4)):
        score1 += matrice[num][j]
    game_over.append(canvas.create_text((300, 340), text=str(
        score1), font=("helvetica", "15"), fill="white"))
    canvas.itemconfigure(button_exit, fill="#C6c5c5")
    canvas.itemconfigure(button_save, fill="#C6c5c5")
    status = ""


def detect_lose():
    # verifie quand la grille est pleine si oui elle verifie si 2 chiffres identiques sont places cote a cote sinon game over
    global place_square, game_over, status
    lose, score1 = True, 0
    for num, j in itertools.product(range(4), range(4)):
        if matrice[num][j] == 0:
            lose = False
        if num != 3 and matrice[num][j] == matrice[num + 1][j]:
            lose = False
        if j != 3 and matrice[num][j] == matrice[num][j + 1]:
            lose = False
    if lose:
        _extracted_from_detect_lose_12(score1)


# TODO Rename this here and in `detect_lose`
def _extracted_from_detect_lose_12(score1):
    # declanche le canvas transparent et le score
    place_square = False
    unbind()
    opacity_rectangle(101, 111, 499, 509, fill="black", alpha=0.7)
    game_over.append(canvas.create_text(
        (300, 310), text="Game Over", font=("helvetica", "40"), fill="white"))
    for num, j in itertools.product(range(4), range(4)):
        score1 += matrice[num][j]
    game_over.append(canvas.create_text((300, 340), text=str(
        score1), font=("helvetica", "15"), fill="white"))
    canvas.itemconfigure(rectangle_exit, fill="#E0e0e0", outline="#E0e0e0")
    canvas.itemconfigure(button_exit, fill="#C6c5c5")
    canvas.itemconfigure(rectangle_save, fill="#E0e0e0", outline="#E0e0e0")
    canvas.itemconfigure(button_save, fill="#C6c5c5")
    status = ""


def matrice_game():
    # la fonction tire au sort un chiffre entre 0 et 3 pour la ligne et la colonne, indique si la case est pleine ou pas si elle l'est elle retire au sort
    global square, numbers, place_square, matrice
    if place_square:
        ligne, colonne = random.randint(0, 3), random.randint(0, 3)
        while matrice[ligne][colonne] != 0:
            ligne, colonne = random.randint(0, 3), random.randint(0, 3)

        if square[ligne][colonne] is None:
            random_2_4 = random.randint(0, 9)
            matrice[ligne][colonne] = 4 if random_2_4 == 0 else 2
            square[ligne][colonne] = create_square(
                colonne * 98, ligne * 98, ligne, colonne)
            numbers[ligne][colonne] = create_number(
                colonne * 98, ligne * 98, ligne, colonne)
        place_square = False


def create_square(x, y, number, j):
    # crée un carré en fonction des coordonees de la grille de matrice_game et le place au bon endroit
    global color
    return canvas.create_rectangle((x + 108, y + 118), (198 + x, 208 + y), fill=color[matrice[number][j]],
                                   outline=color[matrice[number][j]])


def create_number(x, y, ligne, colonne):
    # crée le nombre sur le carré crée juste avant
    global matrice
    return canvas.create_text((x + 152, y + 162), text=matrice[ligne][colonne], font=("helvetica", "30"), fill="black")


def movement_up():
    # quand la touche du haut est activee il déclanche la fonction et récupère les coordonees de y0 (haut du carré) et lui enlève 1 jusqu'a ce qu'il rencontre un obstacle
    # elle détecte un obstacle ou pas (valeur d'un autre carré ou pas) et elle s'arrete au coordonees de l'autre carré
    # si les 2 carrés ont la même valeur alors ils ce superposent, l'un des 2 ce suprimme et l'autre modifie sa valeur
    global square, numbers, matrice, place_square, color, mix, b
    move = False
    for number, j in itertools.product(range(4), range(4)):
        d = 118
        if number != 0 and square[number][j] is not None and square[number - 1][j] is None:
            place_square = True
        if square[number][j] is not None:
            x0, y0, x1, y1 = canvas.coords(square[number][j])
            if number > 0 and square[number - 1][j] is not None:
                a, b, c, d = canvas.coords(square[number - 1][j])
                d += 8
            if y0 > d:
                move = True
                canvas.move(square[number][j], 0, -2)
                canvas.move(numbers[number][j], 0, -2)
                y0 -= 2
                if y0 in {118, 216, 314}:
                    square[number][j], square[number - 1][j], numbers[number][j], numbers[number - 1][j], \
                    matrice[number][j], \
                    matrice[number - 1][j] = None, square[number][j], None, numbers[number][j], 0, \
                                             matrice[number][j]
            elif number > 0 and matrice[number][j] != 0 and matrice[number - 1][j] != 0 and matrice[number][j] == \
                    matrice[number - 1][
                        j] and y0 > b and mix[j] == False:
                canvas.move(square[number][j], 0, -2)
                canvas.move(numbers[number][j], 0, -2)
                move = True
                if y0 - 2 == b:
                    mix[j] = True
                    if y0 == 120:
                        mix[j] = "remix"
                    canvas.delete(square[number][j])
                    matrice[number - 1][j] *= 2
                    matrice[number][j] = 0
                    canvas.itemconfigure(square[number - 1][j], fill=color[matrice[number - 1][j]],
                                         outline=color[matrice[number - 1][j]])
                    square[number][j] = None
                    canvas.delete(numbers[number][j])
                    canvas.itemconfigure(
                        numbers[number - 1][j], text=str(matrice[number - 1][j]))
                    numbers[number][j] = None
                    place_square = True
            elif number > 1 and matrice[number][j] != 0 and matrice[number - 1][j] != 0 and matrice[number][j] == \
                    matrice[number - 1][
                        j] and y0 > b and mix[j] == "remix":
                canvas.move(square[number][j], 0, -2)
                canvas.move(numbers[number][j], 0, -2)
                move = True
                if y0 - 2 == b:
                    canvas.delete(square[number][j])
                    matrice[number - 1][j] *= 2
                    matrice[number][j] = 0
                    canvas.itemconfigure(square[number - 1][j], fill=color[matrice[number - 1][j]],
                                         outline=color[matrice[number - 1][j]])
                    square[number][j] = None
                    canvas.delete(numbers[number][j])
                    canvas.itemconfigure(
                        numbers[number - 1][j], text=str(matrice[number - 1][j]))
                    numbers[number][j] = None
                    place_square = True
    if move:
        canvas.after(1, movement_up)
    else:
        bind(True), detect_lose()


def movement_down():
    # quand la touche du haut est activee il déclanche la fonction et récupère les coordonees de y1 (bas du carré) et lui ajoute 1 jusqu'a ce qu'il rencontre un obstacle
    # elle détecte un obstacle ou pas (valeur d'un autre carré ou pas) et elle s'arrete au coordonees de l'autre carré
    # si les 2 carrés ont la même valeur alors ils ce superposent, l'un des 2 se suprime et l'autre modifie sa valeur
    global square, numbers, matrice, place_square, mix, d
    move = False
    for number, j in itertools.product(range(3, -1, -1), range(4)):
        b = 502
        if number != 3 and square[number][j] is not None and square[number + 1][j] is None:
            place_square = True
        if square[number][j] is not None:
            x0, y0, x1, y1 = canvas.coords(square[number][j])
            if number < 3 and square[number + 1][j] is not None:
                a, b, c, d = canvas.coords(square[number + 1][j])
                b -= 8
            if y1 < b:
                move = True
                canvas.move(square[number][j], 0, 2)
                canvas.move(numbers[number][j], 0, 2)
                y1 += 2
                if y1 in {502, 404, 306}:
                    square[number][j], square[number + 1][j], numbers[number][j], numbers[number + 1][j], \
                    matrice[number][j], \
                    matrice[number + 1][j] = None, square[number][j], None, numbers[number][j], 0, \
                                             matrice[number][j]
            elif number < 3 and matrice[number][j] != 0 and matrice[number + 1][j] != 0 and matrice[number][j] == \
                    matrice[number + 1][
                        j] and y1 < d and mix[j] == False:
                canvas.move(square[number][j], 0, 2)
                canvas.move(numbers[number][j], 0, 2)
                move = True
                if y1 + 2 == d:
                    mix[j] = True
                    if y1 == 500:
                        mix[j] = "remix"
                    canvas.delete(square[number][j])
                    matrice[number + 1][j] *= 2
                    matrice[number][j] = 0
                    canvas.itemconfigure(square[number + 1][j], fill=color[matrice[number + 1][j]],
                                         outline=color[matrice[number + 1][j]])
                    square[number][j] = None
                    canvas.delete(numbers[number][j])
                    canvas.itemconfigure(
                        numbers[number + 1][j], text=str(matrice[number + 1][j]))
                    numbers[number][j] = None
                    place_square = True
            elif number < 2 and matrice[number][j] != 0 and matrice[number + 1][j] != 0 and matrice[number][j] == \
                    matrice[number + 1][
                        j] and y1 < d and mix[j] == "remix":
                canvas.move(square[number][j], 0, 2)
                canvas.move(numbers[number][j], 0, 2)
                move = True
                if y1 + 2 == d:
                    canvas.delete(square[number][j])
                    matrice[number + 1][j] *= 2
                    matrice[number][j] = 0
                    canvas.itemconfigure(square[number + 1][j], fill=color[matrice[number + 1][j]],
                                         outline=color[matrice[number + 1][j]])
                    square[number][j] = None
                    canvas.delete(numbers[number][j])
                    canvas.itemconfigure(
                        numbers[number + 1][j], text=str(matrice[number + 1][j]))
                    numbers[number][j] = None
                    place_square = True
    if move:
        canvas.after(1, movement_down)
    else:
        bind(True), detect_lose()


def movement_right():
    # quand la touche du haut est activee elle déclanche la fonction et récupère les coordonees de x1 (le cote droit du carré) et lui ajoute 1 jusqu'a ce qu'il rencontre un obstacle
    # elle détecte un obstacle ou pas (valeur d'un autre carré ou pas) et elle s'arrete au coordonees de l'autre carré
    # si les 2 carrés on la même valeur alors ils se superposent, l'un des 2 ce suprimme et l'autre modifie ça valeur
    global square, numbers, matrice, place_square, mix, c
    move = False
    for number1, j in itertools.product(range(4), range(3, -1, -1)):
        a = 492
        if j != 3 and square[number1][j] is not None and square[number1][j + 1] is None:
            place_square = True
        if square[number1][j] is not None:
            x0, y0, x1, y1 = canvas.coords(square[number1][j])
            if j < 3 and square[number1][j + 1] is not None:
                a, b, c, d = canvas.coords(square[number1][j + 1])
                a -= 8
            if x1 < a:
                move = True
                canvas.move(square[number1][j], 2, 0)
                canvas.move(numbers[number1][j], 2, 0)
                x1 += 2
                if x1 in {492, 394, 296}:
                    square[number1][j], square[number1][j + 1], numbers[number1][j], numbers[number1][j + 1], \
                    matrice[number1][j], \
                    matrice[number1][j + 1] = None, square[number1][j], None, numbers[number1][j], 0, matrice[number1][
                        j]
            elif j < 3 and matrice[number1][j] != 0 and matrice[number1][j + 1] != 0 and matrice[number1][j] == \
                    matrice[number1][
                        j + 1] and x1 < c and mix[number1] == False:
                canvas.move(square[number1][j], 2, 0)
                canvas.move(numbers[number1][j], 2, 0)
                move = True
                if x1 + 2 == c:
                    mix[number1] = True
                    if x1 == 490:
                        mix[number1] = "remix"
                    canvas.delete(square[number1][j])
                    matrice[number1][j + 1] *= 2
                    matrice[number1][j] = 0
                    canvas.itemconfigure(square[number1][j + 1], fill=color[matrice[number1][j + 1]],
                                         outline=color[matrice[number1][j + 1]])
                    square[number1][j] = None
                    canvas.delete(numbers[number1][j])
                    canvas.itemconfigure(
                        numbers[number1][j + 1], text=str(matrice[number1][j + 1]))
                    numbers[number1][j] = None
                    place_square = True
            elif j < 2 and matrice[number1][j] != 0 and matrice[number1][j + 1] != 0 and matrice[number1][j] == \
                    matrice[number1][
                        j + 1] and x1 < c and mix[number1] == "remix":
                canvas.move(square[number1][j], 2, 0)
                canvas.move(numbers[number1][j], 2, 0)
                move = True
                if x1 + 2 == c:
                    canvas.delete(square[number1][j])
                    matrice[number1][j + 1] *= 2
                    matrice[number1][j] = 0
                    canvas.itemconfigure(square[number1][j + 1], fill=color[matrice[number1][j + 1]],
                                         outline=color[matrice[number1][j + 1]])
                    square[number1][j] = None
                    canvas.delete(numbers[number1][j])
                    canvas.itemconfigure(
                        numbers[number1][j + 1], text=str(matrice[number1][j + 1]))
                    numbers[number1][j] = None
                    place_square = True
    if move:
        canvas.after(1, movement_right)
    else:
        bind(True), detect_lose()


def movement_left():
    # quand la touche du haut est activee elle déclanche la fonction et récupère les coordonees de x0 (le cote gauche du carré) et lui retire 1 jusqu'a ce qu'il rencontre un obstacle
    # elle détecte un obstacle ou pas (valeur d'un autre carré ou pas) et elle s'arrete au coordonees de l'autre carré
    # si les 2 carrés ont la même valeur alors ils se superposent, l'un des 2 ce suprime et l'autre modifie sa valeur
    global square, numbers, matrice, place_square, mix, a
    move = False
    for num, j in itertools.product(range(4), range(4)):
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
                if x0 in {108, 206, 304}:
                    square[num][j], square[num][j - 1], numbers[num][j], numbers[num][j - 1], \
                    matrice[num][j], \
                    matrice[num][j - 1] = None, square[num][j], None, numbers[num][j], 0, matrice[num][j]
            elif j > 0 and matrice[num][j] != 0 and matrice[num][j - 1] != 0 and matrice[num][j] == matrice[num][
                j - 1] and x1 > a and mix[num] == False:
                canvas.move(square[num][j], -2, 0)
                canvas.move(numbers[num][j], -2, 0)
                move = True
                if x0 - 2 == a:
                    mix[num] = True
                    if x0 == 110:
                        mix[num] = "remix"
                    canvas.delete(square[num][j])
                    matrice[num][j - 1] *= 2
                    matrice[num][j] = 0
                    canvas.itemconfigure(square[num][j - 1], fill=color[matrice[num][j - 1]],
                                         outline=color[matrice[num][j - 1]])
                    square[num][j] = None
                    canvas.delete(numbers[num][j])
                    canvas.itemconfigure(
                        numbers[num][j - 1], text=str(matrice[num][j - 1]))
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
                    canvas.itemconfigure(
                        numbers[num][j - 1], text=str(matrice[num][j - 1]))
                    numbers[num][j] = None
                    place_square = True
    if move:
        canvas.after(1, movement_left)
    else:
        bind(True), detect_lose()


def movement(direction):
    # désactive les bouttons pendant qu'un carré bouge et déclanche un mouvement
    unbind()
    if direction == "up":
        movement_up()
    if direction == "down":
        movement_down()
    if direction == "right":
        movement_right()
    if direction == "left":
        movement_left()


def unbind():
    # désactive les bouttons assignes
    global root
    root.unbind("z"), root.unbind("s"), root.unbind("d"), root.unbind("q")
    root.unbind("<Up>"), root.unbind("<Down>"), root.unbind("<Right>"), root.unbind("<Left>")


def bind(new_game):
    # active les touches et marque le score en haut du canvas et si le score est plus haut que le high score alors il le ramplace
    global root, mix, text_score, highscore
    mix = [False, False, False, False]
    root.bind("z", lambda e: movement("up"))
    root.bind("s", lambda e: movement("down"))
    root.bind("d", lambda e: movement("right"))
    root.bind("q", lambda e: movement("left"))
    root.bind("<Up>", lambda e: movement("up"))
    root.bind("<Down>", lambda e: movement("down"))
    root.bind("<Right>", lambda e: movement("right"))
    root.bind("<Left>", lambda e: movement("left"))
    if new_game:
        matrice_game()
    score1 = sum(matrice[num][j] for num, j in itertools.product(range(4), range(4)))

    if score1 > highscore:
        highscore = score1
        save_highscore()
    canvas.itemconfigure(text_score, text=str(score1))
    canvas.itemconfigure(text_highscore, text=str(highscore))


# Widgets Creation

root = tk.Tk()
root.title("2048 Game")
canvas = tk.Canvas(root, width=598, height=621, bg="#ececec")
# canvas d'esthétique
canvas.create_rectangle(108, 118, 198, 208, fill="#E0e0e0", outline="#E0e0e0")
canvas.create_rectangle(206, 118, 296, 208, fill="#E0e0e0", outline="#E0e0e0")
canvas.create_rectangle(304, 118, 394, 208, fill="#E0e0e0", outline="#E0e0e0")
canvas.create_rectangle(402, 118, 492, 208, fill="#E0e0e0", outline="#E0e0e0")
canvas.create_rectangle(108, 216, 198, 306, fill="#E0e0e0", outline="#E0e0e0")
canvas.create_rectangle(206, 216, 296, 306, fill="#E0e0e0", outline="#E0e0e0")
canvas.create_rectangle(304, 216, 394, 306, fill="#E0e0e0", outline="#E0e0e0")
canvas.create_rectangle(402, 216, 492, 306, fill="#E0e0e0", outline="#E0e0e0")
canvas.create_rectangle(108, 314, 198, 404, fill="#E0e0e0", outline="#E0e0e0")
canvas.create_rectangle(206, 314, 296, 404, fill="#E0e0e0", outline="#E0e0e0")
canvas.create_rectangle(304, 314, 394, 404, fill="#E0e0e0", outline="#E0e0e0")
canvas.create_rectangle(402, 314, 492, 404, fill="#E0e0e0", outline="#E0e0e0")
canvas.create_rectangle(108, 412, 198, 502, fill="#E0e0e0", outline="#E0e0e0")
canvas.create_rectangle(206, 412, 296, 502, fill="#E0e0e0", outline="#E0e0e0")
canvas.create_rectangle(304, 412, 394, 502, fill="#E0e0e0", outline="#E0e0e0")
canvas.create_rectangle(402, 412, 492, 502, fill="#E0e0e0", outline="#E0e0e0")

# definition des widgets crées sur le canvas
load_rectangle = canvas.create_rectangle(
    108, 515, 198, 551, fill="#E0e0e0", outline="#E0e0e0")
rectangle_save = canvas.create_rectangle(
    206, 515, 296, 551, fill="#E0e0e0", outline="#E0e0e0")
play_rectangle = canvas.create_rectangle(
    304, 515, 394, 551, fill="#E0e0e0", outline="#E0e0e0")
rectangle_exit = canvas.create_rectangle(
    402, 515, 492, 551, fill="#E0e0e0", outline="#E0e0e0")
button_load = canvas.create_text(
    (153, 533), text="Load", font=("helvetica", "18"), fill="#565555")
button_save = canvas.create_text(
    (251, 533), text="Save", font=("helvetica", "18"), fill="#C6c5c5")
button_play = canvas.create_text(
    (349, 533), text="Play", font=("helvetica", "18"), fill="#565555")
button_exit = canvas.create_text(
    (447, 533), text="Exit", font=("helvetica", "18"), fill="#C6c5c5")

canvas.create_rectangle(304, 56, 394, 96, fill="#E0e0e0", outline="#E0e0e0")
canvas.create_text((349, 68), text="SCORE", font=(
    "Arial Bold", "10"), fill="#565555")
text_score = canvas.create_text(
    (349, 83), text="0", font=("Helvetica", "13"), fill="#565555")

canvas.create_rectangle(402, 56, 492, 96, fill="#E0e0e0", outline="#E0e0e0")
canvas.create_text((449, 68), text="HIGHSCORE",
                   font=("Arial Bold", "10"), fill="#565555")
text_highscore = canvas.create_text((449, 83), text=str(
    highscore), font=("Helvetica", "13"), fill="#565555")

canvas.create_text((204, 76), text="2048", font=(
    "Arial", "50", "bold"), fill="black")

canvas.grid()
load(1)


# Détection de la position de la souris inspiré de la source: https://codertw.com/程式語言/114662/

def motion(event):
    # détecte la position de la sourie et détecte si elle est sur un boutton ou pas pour activation désactivation
    global status
    x, y = event.x, event.y
    if 100 < x < 200 and 515 < y < 551:
        root.bind('<Button-1>', load)
    elif 200 < x < 300 and 515 < y < 551 and status == "play":
        root.bind('<Button-1>', save)
    elif 300 < x < 400 and 515 < y < 551:
        root.bind('<Button-1>', play)
    elif 400 < x < 500 and 515 < y < 551 and status == "play":
        root.bind('<Button-1>', exit)
    else:
        root.unbind('<Button-1>')
    # print("Mouse position:", (event.x, event.y))


canvas.bind('<Motion>', motion)


# Sert uniquement pour l'esthétique, source: https://www.tutorialspoint.com/how-to-make-a-tkinter-canvas-rectangle-transparent
def opacity_rectangle(x, y, a, b, **options):
    # sert a crée un widgets transparent
    global game_over
    if 'alpha' in options:
        alpha = int(options.pop('alpha') * 255)
        fill = options.pop('fill')
        fill = root.winfo_rgb(fill) + (alpha,)
        image = Image.new('RGBA', (a - x, b - y), fill)
        images.append(ImageTk.PhotoImage(image))
        game_over.append(canvas.create_image(
            x, y, image=images[-1], anchor='nw'))
        game_over.append(canvas.create_rectangle(x, y, a, b, **options))


root.mainloop()
