import tkinter as tk
import random

# Constantes
matrice = [ [0, 0, 0, 0], 
            [0, 0, 0, 0], 
            [0, 0, 0, 0], 
            [0, 0, 0, 0]]

square = [  [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None]]

# Fonctions
def matrice_game():
    global square
    ligne, colonne = random.randint(0,3), random.randint(0,3)
    while square[ligne][colonne] != None:
        ligne, colonne = random.randint(0,3), random.randint(0,3)
    if square[ligne][colonne] == None: square[ligne][colonne] = create_square(colonne*100, ligne*100)

def create_square(x, y):
    square = canvas.create_rectangle((x, y), (100+x, 100+y), fill="red")
    return square

def movement_up():
    global square
    move=False
    for i in range(4):
        for j in range(4):
            d=0
            if square[i][j] != None:
                x0, y0, x1, y1 = canvas.coords(square[i][j])
                if i>0 and square[i-1][j]!=None: 
                    a, b, c, d = canvas.coords(square[i-1][j])
                if y0>d:
                    move=True
                    canvas.move(square[i][j], 0, -2)
                    y0-=2
                    if y0==0: square[i][j], square[i-1][j]=None, square[i][j]
                    if y0==100: square[i][j], square[i-1][j]=None, square[i][j]
                    if y0==200: square[i][j], square[i-1][j]=None, square[i][j]
    canvas.after(1, movement_up) if move==True else bind() 

def movement_down():
    global square
    move=False
    for i in range(3, -1, -1):
        for j in range(4):
            b=400
            if square[i][j] != None:
                x0, y0, x1, y1 = canvas.coords(square[i][j])
                if i<3 and square[i+1][j]!=None:
                    a, b, c, d = canvas.coords(square[i+1][j])
                if y1<b:
                    move=True
                    canvas.move(square[i][j], 0, 2)
                    y1+=2
                    if y1==400: square[i][j], square[i+1][j]=None, square[i][j]
                    if y1==300: square[i][j], square[i+1][j]=None, square[i][j]
                    if y1==200: square[i][j], square[i+1][j]=None, square[i][j]
    canvas.after(1, movement_down) if move==True else bind()
                
def movement_right():
    global square
    move=False
    for i in range(4):
        for j in range(3, -1, -1):
            a=400
            if square[i][j] != None: 
                x0, y0, x1, y1 = canvas.coords(square[i][j])
                if j<3 and square[i][j+1]!=None:
                    a, b, c, d = canvas.coords(square[i][j+1])
                if x1<a:
                    move=True
                    canvas.move(square[i][j], 2, 0)
                    x1+=2
                    if x1==400: square[i][j], square[i][j+1]=None, square[i][j]
                    if x1==300: square[i][j], square[i][j+1]=None, square[i][j]
                    if x1==200: square[i][j], square[i][j+1]=None, square[i][j]
    canvas.after(1, movement_right) if move==True else bind()
                
def movement_left():
    global square
    move=False
    for i in range(4):
        for j in range(4):
            c=0
            if square[i][j] != None:
                x0, y0, x1, y1 = canvas.coords(square[i][j])
                if j>0 and square[i][j-1]!=None:
                    a, b, c, d = canvas.coords(square[i][j-1])
                if x0>c:
                    move=True
                    canvas.move(square[i][j], -2, 0)
                    x0-=2
                    if x0==0: square[i][j], square[i][j-1]=None, square[i][j]
                    if x0==100: square[i][j], square[i][j-1]=None, square[i][j]
                    if x0==200: square[i][j], square[i][j-1]=None, square[i][j]
    canvas.after(1, movement_left) if move==True else bind()

#addition
def addition(c1, c2):
    """Retourne l'addition des deux configs c1 et c2"""
    c_res = [[0 for i in range(N+2)] for j in range(N+2)]
    for i in range(1, N+1):
        for j in range(1, N+1):
            c_res[i][j] = c1[i][j] + c2[i][j]
    return c_res


def movement(direction):
    unbind()
    if direction == "up": movement_up()
    if direction == "down": movement_down()
    if direction == "right": movement_right()
    if direction == "left": movement_left()

def unbind():
    global root
    root.unbind("<Up>"), root.unbind("<Down>"), root.unbind("<Right>"), root.unbind("<Left>")

def bind():
    global root
    root.bind("<Up>", lambda e: movement("up"))
    root.bind("<Down>", lambda e: movement("down"))
    root.bind("<Right>", lambda e: movement("right"))
    root.bind("<Left>", lambda e: movement("left"))
    matrice_game()
# Création des widgets
root = tk.Tk()
canvas = tk.Canvas(root, width=400, height=400, bg="black")
canvas.grid()

# ...
bind()
#print(square)

root.mainloop()