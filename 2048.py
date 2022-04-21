from sqlite3 import Row
import tkinter as tk
import random
from PIL import Image, ImageTk

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

images=[]

game_over=[None, None, None, None]

place_square=True
status="exit"
# Fonctions
def play(event):
    global place_square, matrice, square, numbers, game_over, status
    for i in range(4):
        for j in range(4):
            if square[i][j]!=None:
                canvas.delete(square[i][j])
            if numbers[i][j]!=None:
                canvas.delete(numbers[i][j])
            square[i][j], numbers[i][j], matrice[i][j]=None, None, 0
    canvas.delete(game_over[0])
    canvas.delete(game_over[1])
    canvas.delete(game_over[2])
    canvas.delete(game_over[3])
    game_over=[None, None, None, None]
    place_square=True
    matrice_game()
    place_square=True
    bind()
    status="play"

import tkinter as tk
import random
from PIL import Image, ImageTk

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

images=[]

game_over=[]

place_square=True
status=""
# Fonctions
def play(event):
    global place_square, matrice, square, numbers, game_over, status
    for i in range(4):
        for j in range(4):
            if square[i][j]!=None:
                canvas.delete(square[i][j])
            if numbers[i][j]!=None:
                canvas.delete(numbers[i][j])
            square[i][j], numbers[i][j], matrice[i][j]=None, None, 0
    for i in range(len(game_over)):
        canvas.delete(game_over[i])
    game_over=[]
    text_over=[None, None]
    place_square=True
    matrice_game()
    place_square=True
    bind()
    canvas.itemconfigure(button_exit, fill="black")
    status="play"

def exit(event):
    global game_over, matrice, status
    place_square, score=False, 0
    unbind()
    opacity_rectangle(0, 0, 400, 400, fill="black", alpha=0.7)
    game_over.append(canvas.create_text((200, 200), text="Game Over", font=("helvetica", "40"), fill="white"))
    for i in range(4):
        for j in range(4):
            score+=matrice[i][j]
    game_over.append(canvas.create_text((200,230), text=str(score), font=("helvetica", "15"), fill="white"))
    canvas.itemconfigure(button_exit, fill="grey")
    
def detect_lose():
    global place_square, game_over
    lose, score=True, 0
    for i in range(4):
        for j in range(4):
            if matrice[i][j]==0:
                lose=False
            if i!=3 and matrice[i][j]==matrice[i+1][j]:
                lose=False
            if  j!=3 and matrice[i][j]==matrice[i][j+1]:
                lose=False
    if lose==True:
        place_square=False
        unbind()
        opacity_rectangle(0, 0, 400, 400, fill="black", alpha=0.7)
        game_over.append(canvas.create_text((200, 200), text="Game Over", font=("helvetica", "40"), fill="white"))
        for i in range(4):
            for j in range(4):
                score+=matrice[i][j]
        game_over.append(canvas.create_text((200,230), text=str(score), font=("helvetica", "15"), fill="white"))

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
    if move==True: canvas.after(1, movement_up)
    else: bind(), detect_lose()

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
    if move==True: canvas.after(1, movement_down)
    else: bind(), detect_lose()
                
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
    if move==True: canvas.after(1, movement_right)
    else: bind(), detect_lose()
                
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
    if move==True: canvas.after(1, movement_left)
    else: bind(), detect_lose()
                
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


def grille_en_4():
    LARGEUR = 600
    HAUTEUR = 400
    mur_G = canvas.create_line(1,0,1,HAUTEUR,fill='white')
    mur_D = canvas.create_line(150,0,150,HAUTEUR,fill='white')
    pass

# Création des widgets
root = tk.Tk()
root.title("2048")
canvas = tk.Canvas(root, width=398, height=435, bg="black")
canvas.create_rectangle(0, 400, 410, 440, fill="white")
canvas.create_line(100, 400, 100, 440, fill="darkgrey")
canvas.create_line(200, 400, 200, 440, fill="darkgrey")
canvas.create_line(300, 400, 300, 440, fill="darkgrey")
button_play=canvas.create_text((250, 418), text="Play", font=("helvetica", "20"), fill="black")
button_exit=canvas.create_text((350, 418), text="Exit", font=("helvetica", "20"), fill="grey")
# création de la grille separée en 4
button_grid_4 =canvas.create_text((50, 418), text = "grille 4", font=("helvetica", "20"), fill = "blue")
canvas.grid()



# Détection de la position de la souris inspiré de la source: https://codertw.com/程式語言/114662/

def motion(event):
    global status
    x, y=event.x, event.y
    if x>200 and x<300 and y>400 and y<436:
        root.bind('<Button-1>', play)
    elif x>300 and x<400 and y>400 and y<436 and status=="play":
        root.bind('<Button-1>', exit)
    else: root.unbind('<Button-1>')
    #print("Mouse position: (%s %s)" % (event.x, event.y))

canvas.bind('<Motion>', motion)

# ...
#bind()

# Sert uniquement pour l'esthétique, source: https://www.tutorialspoint.com/how-to-make-a-tkinter-canvas-rectangle-transparent
def opacity_rectangle(x, y, a, b, **options):
    global game_over
    if 'alpha' in options:
        alpha = int(options.pop('alpha') * 255)
        fill = options.pop('fill')
        fill = root.winfo_rgb(fill) + (alpha,)
        image = Image.new('RGBA', (a-x, b-y), fill)
        images.append(ImageTk.PhotoImage(image))
        game_over.append(canvas.create_image(x, y, image=images[-1], anchor='nw'))
        game_over.append(canvas.create_rectangle(x, y, a, b, **options))

root.mainloop()