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
        
numbers = [ [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None]]

place_square=True
# Fonctions
def matrice_game():
    global square, numbers, place_square
    if place_square==True:
        ligne, colonne = random.randint(0,3), random.randint(0,3)
        while matrice[ligne][colonne] != 0:
            ligne, colonne = random.randint(0,3), random.randint(0,3)
        if square[ligne][colonne] ==None :
            square[ligne][colonne] = create_square(colonne*100, ligne*100)
            numbers[ligne][colonne] = create_number(colonne*100, ligne*100, ligne, colonne)
        place_square=False
    print(matrice[0], "|", square[0], "|", numbers[0]), print(matrice[1], "|", square[1], "|", numbers[1]), print(matrice[2], "|", square[2], "|", numbers[2]), print(matrice[3], "|", square[3], "|", numbers[3]), print("-----------")

def create_square(x, y):
    square = canvas.create_rectangle((x, y), (100+x, 100+y), fill="yellow")
    return square
        
def create_number(x, y, ligne, colonne):
    global matrice
    random_2_4=random.randint(0,9)
    if random_2_4==0:
        chiffre="4"
    else: chiffre="2"
    number = canvas.create_text((x+50, y+50), text=chiffre, font=("helvetica", "40"), fill="black")
    matrice[ligne][colonne]=int(chiffre)
    return number

def movement_up():
    global square, numbers, matrice, place_square
    move=False
    for i in range(4):
        for j in range(4):
            d=0
            if i!=0 and square[i][j]!=None and square[i-1][j]==None:
                place_square=True
            if square[i][j] != None:
                if place_square==True: canvas.itemconfigure(square[i][j],fill="lightblue")
                x0, y0, x1, y1 = canvas.coords(square[i][j])
                if i>0 and square[i-1][j]!=None:
                    a, b, c, d = canvas.coords(square[i-1][j])
                if y0>d:
                    move=True
                    canvas.move(square[i][j], 0, -2)
                    canvas.move(numbers[i][j], 0, -2)
                    y0-=2
                    if y0==0: square[i][j], square[i-1][j], numbers[i][j], numbers[i-1][j], matrice[i][j], matrice[i-1][j]=None, square[i][j], None, numbers[i][j], 0, matrice[i][j]
                    if y0==100: square[i][j], square[i-1][j], numbers[i][j], numbers[i-1][j], matrice[i][j], matrice[i-1][j]=None, square[i][j], None, numbers[i][j], 0, matrice[i][j]
                    if y0==200: square[i][j], square[i-1][j], numbers[i][j], numbers[i-1][j], matrice[i][j], matrice[i-1][j]=None, square[i][j], None, numbers[i][j], 0, matrice[i][j]
                elif i>0 and matrice[i][j]!=0 and matrice[i-1][j]!=0 and matrice[i][j]==matrice[i-1][j] and y0>b:
                    canvas.move(square[i][j], 0, -2)
                    canvas.move(numbers[i][j], 0, -2)
                    move=True
                    if y0-2==b:
                        canvas.delete(square[i][j])
                        canvas.itemconfigure(square[i-1][j],fill="blue")
                        square[i][j]=None
                        canvas.delete(numbers[i][j])
                        canvas.itemconfigure(numbers[i-1][j], text=str(matrice[i-1][j]*2))
                        numbers[i][j]=None
                        matrice[i-1][j]*=2
                        matrice[i][j]=0
                        place_square=True
    canvas.after(1, movement_up) if move==True else bind()

def movement_down():
    global square, numbers, matrice, place_square
    move=False
    for i in range(3, -1, -1):
        for j in range(4):
            b=400
            if i!=3 and square[i][j]!=None and square[i+1][j]==None:
                place_square=True
            if square[i][j] != None:
                if place_square==True: canvas.itemconfigure(square[i][j],fill="lightblue")
                x0, y0, x1, y1 = canvas.coords(square[i][j])
                if i<3 and square[i+1][j]!=None:
                    a, b, c, d = canvas.coords(square[i+1][j])
                if y1<b:
                    move=True
                    canvas.move(square[i][j], 0, 2)
                    canvas.move(numbers[i][j], 0, 2)
                    y1+=2
                    if y1==400: square[i][j], square[i+1][j], numbers[i][j], numbers[i+1][j], matrice[i][j], matrice[i+1][j]=None, square[i][j], None, numbers[i][j], 0, matrice[i][j]
                    if y1==300: square[i][j], square[i+1][j], numbers[i][j], numbers[i+1][j], matrice[i][j], matrice[i+1][j]=None, square[i][j], None, numbers[i][j], 0, matrice[i][j]
                    if y1==200: square[i][j], square[i+1][j], numbers[i][j], numbers[i+1][j], matrice[i][j], matrice[i+1][j]=None, square[i][j], None, numbers[i][j], 0, matrice[i][j]
                elif i<3 and matrice[i][j]!=0 and matrice[i+1][j]!=0 and matrice[i][j]==matrice[i+1][j] and y1<d:
                    canvas.move(square[i][j], 0, 2)
                    canvas.move(numbers[i][j], 0, 2)
                    move=True
                    if y1+2==d:
                        canvas.delete(square[i][j])
                        canvas.itemconfigure(square[i+1][j],fill="blue")
                        square[i][j]=None
                        canvas.delete(numbers[i][j])
                        canvas.itemconfigure(numbers[i+1][j], text=str(matrice[i+1][j]*2))
                        numbers[i][j]=None
                        matrice[i+1][j]*=2
                        matrice[i][j]=0
                        place_square=True
    canvas.after(1, movement_down) if move==True else bind()
                
def movement_right():
    global square, numbers, matrice, place_square
    move=False
    for i in range(4):
        for j in range(3, -1, -1):
            a=400
            if j!=3 and square[i][j]!=None and square[i][j+1]==None:
                place_square=True
            if square[i][j] != None:
                if place_square==True: canvas.itemconfigure(square[i][j],fill="lightblue")
                x0, y0, x1, y1 = canvas.coords(square[i][j])
                if j<3 and square[i][j+1]!=None:
                    a, b, c, d = canvas.coords(square[i][j+1])
                if x1<a:
                    move=True
                    canvas.move(square[i][j], 2, 0)
                    canvas.move(numbers[i][j], 2, 0)
                    x1+=2
                    if x1==400: square[i][j], square[i][j+1], numbers[i][j], numbers[i][j+1], matrice[i][j], matrice[i][j+1]=None, square[i][j], None, numbers[i][j], 0, matrice[i][j]
                    if x1==300: square[i][j], square[i][j+1], numbers[i][j], numbers[i][j+1], matrice[i][j], matrice[i][j+1]=None, square[i][j], None, numbers[i][j], 0, matrice[i][j]
                    if x1==200: square[i][j], square[i][j+1], numbers[i][j], numbers[i][j+1], matrice[i][j], matrice[i][j+1]=None, square[i][j], None, numbers[i][j], 0, matrice[i][j]
                elif j<3 and matrice[i][j]!=0 and matrice[i][j+1]!=0 and matrice[i][j]==matrice[i][j+1] and x1<c:
                    canvas.move(square[i][j], 2, 0)
                    canvas.move(numbers[i][j], 2, 0)
                    move=True
                    if x1+2==c:
                        canvas.delete(square[i][j])
                        canvas.itemconfigure(square[i][j+1],fill="lightblue")
                        square[i][j]=None
                        canvas.delete(numbers[i][j])
                        canvas.itemconfigure(numbers[i][j+1], text=str(matrice[i][j+1]*2))
                        numbers[i][j]=None
                        matrice[i][j+1]*=2
                        matrice[i][j]=0
                        place_square=True
    canvas.after(1, movement_right) if move==True else bind()
                
def movement_left():
    global square, numbers, matrice, place_square
    move=False
    for i in range(4):
        for j in range(4):
            c=0
            if  j!=0 and square[i][j]!=None and square[i][j-1]==None:
                place_square=True
            if square[i][j] != None:
                if place_square==True: canvas.itemconfigure(square[i][j],fill="lightblue")
                x0, y0, x1, y1 = canvas.coords(square[i][j])
                if j>0 and square[i][j-1]!=None:
                    a, b, c, d = canvas.coords(square[i][j-1])
                if x0>c:
                    move=True
                    canvas.move(square[i][j], -2, 0)
                    canvas.move(numbers[i][j], -2, 0)
                    x0-=2
                    if x0==0: square[i][j], square[i][j-1], numbers[i][j], numbers[i][j-1], matrice[i][j], matrice[i][j-1]=None, square[i][j], None, numbers[i][j], 0, matrice[i][j]
                    if x0==100: square[i][j], square[i][j-1], numbers[i][j], numbers[i][j-1], matrice[i][j], matrice[i][j-1]=None, square[i][j], None, numbers[i][j], 0, matrice[i][j]
                    if x0==200: square[i][j], square[i][j-1], numbers[i][j], numbers[i][j-1], matrice[i][j], matrice[i][j-1]=None, square[i][j], None, numbers[i][j], 0, matrice[i][j]
                elif j>0 and matrice[i][j]!=0 and matrice[i][j-1]!=0 and matrice[i][j]==matrice[i][j-1] and x1>a:
                    canvas.move(square[i][j], -2, 0)
                    canvas.move(numbers[i][j], -2, 0)
                    move=True
                    if x0-2==a:
                        canvas.delete(square[i][j])
                        canvas.itemconfigure(square[i][j-1],fill="blue")
                        square[i][j]=None
                        canvas.delete(numbers[i][j])
                        canvas.itemconfigure(numbers[i][j-1], text=str(matrice[i][j-1]*2))
                        numbers[i][j]=None
                        matrice[i][j-1]*=2
                        matrice[i][j]=0
                        place_square=True
    canvas.after(1, movement_left) if move==True else bind()
                
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

root.mainloop()