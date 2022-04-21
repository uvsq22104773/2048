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
mix=[False, False, False, False]

color = {2 : "#b0e3f6", 4 : "#b1cae9", 8 : "#c0bbdc", 16 : "#cfb1d5", 32 : "#e1b0d0", 64 : "#f6accd", 128 : "#fac0b5", 256 : "#fdd6ab", 512 : "#fce8b3", 1024 : "#ebefb2", 2048 : "#d7e8b2", 4096 : "#d9e8b1", 8192 : "#cee7c7", 16384 : "#c7e6d7", 32768 : "#a7d8bb", 65536 : "#8dcca6", 131072 : "#52d085"}
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
    canvas.itemconfigure(rectangle_exit, fill="#B5b5b5", outline="#B5b5b5")
    canvas.itemconfigure(button_exit, fill="black")
    status="play"

def exit(event):
    global game_over, matrice, status
    place_square, score=False, 0
    unbind()
    opacity_rectangle(8, 8, 392, 392, fill="black", alpha=0.7)
    game_over.append(canvas.create_text((200, 200), text="Game Over", font=("helvetica", "40"), fill="white"))
    for i in range(4):
        for j in range(4):
            score+=matrice[i][j]
    game_over.append(canvas.create_text((200,230), text=str(score), font=("helvetica", "15"), fill="white"))
    canvas.itemconfigure(rectangle_exit, fill="#E0e0e0", outline="#E0e0e0")
    canvas.itemconfigure(button_exit, fill="#C6c5c5")
    status=""
    
def detect_lose():
    global place_square, game_over, status
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
        opacity_rectangle(8, 8, 392, 392, fill="black", alpha=0.7)
        game_over.append(canvas.create_text((200, 200), text="Game Over", font=("helvetica", "40"), fill="white"))
        for i in range(4):
            for j in range(4):
                score+=matrice[i][j]
        game_over.append(canvas.create_text((200,230), text=str(score), font=("helvetica", "15"), fill="white"))
        canvas.itemconfigure(button_exit, fill="#C6c5c5")
        status=""

def matrice_game():
    global square, numbers, place_square, matrice
    if place_square==True:
        ligne, colonne = random.randint(0,3), random.randint(0,3)
        while matrice[ligne][colonne] != 0:
            ligne, colonne = random.randint(0,3), random.randint(0,3)

        if square[ligne][colonne] ==None :
            random_2_4=random.randint(0,9)
            if random_2_4==0:
                matrice[ligne][colonne]=4
            else: matrice[ligne][colonne]=2

            square[ligne][colonne] = create_square(colonne*98, ligne*98, ligne, colonne)
            numbers[ligne][colonne] = create_number(colonne*98, ligne*98, ligne, colonne)
        place_square=False
    print(matrice[0], "|", square[0], "|", numbers[0]), print(matrice[1], "|", square[1], "|", numbers[1]), print(matrice[2], "|", square[2], "|", numbers[2]), print(matrice[3], "|", square[3], "|", numbers[3]), print("-----------")

def create_square(x, y, i, j):
    global color
    square = canvas.create_rectangle((x+8, y+8), (98+x, 98+y), fill=color[matrice[i][j]], outline=color[matrice[i][j]])
    return square
        
def create_number(x, y, ligne, colonne):
    global matrice
    number = canvas.create_text((x+52, y+52), text=matrice[ligne][colonne], font=("helvetica", "35"), fill="black")
    return number

def movement_up():
    global square, numbers, matrice, place_square, color, mix
    move=False
    for i in range(4):
        for j in range(4):
            d=8
            if i!=0 and square[i][j]!=None and square[i-1][j]==None:
                place_square=True
            if square[i][j] != None:
                x0, y0, x1, y1 = canvas.coords(square[i][j])
                if i>0 and square[i-1][j]!=None:
                    a, b, c, d = canvas.coords(square[i-1][j])
                    d+=8
                if y0>d:
                    move=True
                    canvas.move(square[i][j], 0, -2)
                    canvas.move(numbers[i][j], 0, -2)
                    y0-=2
                    if y0==8: square[i][j], square[i-1][j], numbers[i][j], numbers[i-1][j], matrice[i][j], matrice[i-1][j]=None, square[i][j], None, numbers[i][j], 0, matrice[i][j]
                    if y0==106: square[i][j], square[i-1][j], numbers[i][j], numbers[i-1][j], matrice[i][j], matrice[i-1][j]=None, square[i][j], None, numbers[i][j], 0, matrice[i][j]
                    if y0==204: square[i][j], square[i-1][j], numbers[i][j], numbers[i-1][j], matrice[i][j], matrice[i-1][j]=None, square[i][j], None, numbers[i][j], 0, matrice[i][j]
                elif i>0 and matrice[i][j]!=0 and matrice[i-1][j]!=0 and matrice[i][j]==matrice[i-1][j] and y0>b and mix[j]==False:
                    canvas.move(square[i][j], 0, -2)
                    canvas.move(numbers[i][j], 0, -2)
                    move=True
                    if y0-2==b:
                        mix[j]=True
                        if y0-2==8:
                            mix[j]="remix"
                        canvas.delete(square[i][j])
                        matrice[i-1][j]*=2
                        matrice[i][j]=0
                        canvas.itemconfigure(square[i-1][j],fill=color[matrice[i-1][j]], outline=color[matrice[i-1][j]])
                        square[i][j]=None
                        canvas.delete(numbers[i][j])
                        canvas.itemconfigure(numbers[i-1][j], text=str(matrice[i-1][j]))
                        numbers[i][j]=None
                        place_square=True
                elif i>1 and matrice[i][j]!=0 and matrice[i-1][j]!=0 and matrice[i][j]==matrice[i-1][j] and y0>b and mix[j]=="remix":
                    canvas.move(square[i][j], 0, -2)
                    canvas.move(numbers[i][j], 0, -2)
                    move=True
                    if y0-2==b:
                        canvas.delete(square[i][j])
                        matrice[i-1][j]*=2
                        matrice[i][j]=0
                        canvas.itemconfigure(square[i-1][j],fill=color[matrice[i-1][j]], outline=color[matrice[i-1][j]])
                        square[i][j]=None
                        canvas.delete(numbers[i][j])
                        canvas.itemconfigure(numbers[i-1][j], text=str(matrice[i-1][j]))
                        numbers[i][j]=None
                        place_square=True
    if move==True: canvas.after(1, movement_up)
    else: bind(), detect_lose()

def movement_down():
    global square, numbers, matrice, place_square, mix
    move=False
    for i in range(3, -1, -1):
        for j in range(4):
            b=392
            if i!=3 and square[i][j]!=None and square[i+1][j]==None:
                place_square=True
            if square[i][j] != None:
                x0, y0, x1, y1 = canvas.coords(square[i][j])
                if i<3 and square[i+1][j]!=None:
                    a, b, c, d = canvas.coords(square[i+1][j])
                    b-=8
                if y1<b:
                    move=True
                    canvas.move(square[i][j], 0, 2)
                    canvas.move(numbers[i][j], 0, 2)
                    y1+=2
                    if y1==392: square[i][j], square[i+1][j], numbers[i][j], numbers[i+1][j], matrice[i][j], matrice[i+1][j]=None, square[i][j], None, numbers[i][j], 0, matrice[i][j]
                    if y1==294: square[i][j], square[i+1][j], numbers[i][j], numbers[i+1][j], matrice[i][j], matrice[i+1][j]=None, square[i][j], None, numbers[i][j], 0, matrice[i][j]
                    if y1==196: square[i][j], square[i+1][j], numbers[i][j], numbers[i+1][j], matrice[i][j], matrice[i+1][j]=None, square[i][j], None, numbers[i][j], 0, matrice[i][j]
                elif i<3 and matrice[i][j]!=0 and matrice[i+1][j]!=0 and matrice[i][j]==matrice[i+1][j] and y1<d and mix[j]==False:
                    canvas.move(square[i][j], 0, 2)
                    canvas.move(numbers[i][j], 0, 2)
                    move=True
                    if y1+2==d:
                        mix[j]=True
                        if y1+2==392:
                            mix[j]="remix"
                        canvas.delete(square[i][j])
                        matrice[i+1][j]*=2
                        matrice[i][j]=0
                        canvas.itemconfigure(square[i+1][j],fill=color[matrice[i+1][j]], outline=color[matrice[i+1][j]])
                        square[i][j]=None
                        canvas.delete(numbers[i][j])
                        canvas.itemconfigure(numbers[i+1][j], text=str(matrice[i+1][j]))
                        numbers[i][j]=None
                        place_square=True
                elif i<2 and matrice[i][j]!=0 and matrice[i+1][j]!=0 and matrice[i][j]==matrice[i+1][j] and y1<d and mix[j]=="remix":
                    canvas.move(square[i][j], 0, 2)
                    canvas.move(numbers[i][j], 0, 2)
                    move=True
                    if y1+2==d:
                        canvas.delete(square[i][j])
                        matrice[i+1][j]*=2
                        matrice[i][j]=0
                        canvas.itemconfigure(square[i+1][j],fill=color[matrice[i+1][j]], outline=color[matrice[i+1][j]])
                        square[i][j]=None
                        canvas.delete(numbers[i][j])
                        canvas.itemconfigure(numbers[i+1][j], text=str(matrice[i+1][j]))
                        numbers[i][j]=None
                        place_square=True
    if move==True: canvas.after(1, movement_down)
    else: bind(), detect_lose()
                
def movement_right():
    global square, numbers, matrice, place_square, mix
    move=False
    for i in range(4):
        for j in range(3, -1, -1):
            a=392
            if j!=3 and square[i][j]!=None and square[i][j+1]==None:
                place_square=True
            if square[i][j] != None:
                x0, y0, x1, y1 = canvas.coords(square[i][j])
                if j<3 and square[i][j+1]!=None:
                    a, b, c, d = canvas.coords(square[i][j+1])
                    a-=8
                if x1<a:
                    move=True
                    canvas.move(square[i][j], 2, 0)
                    canvas.move(numbers[i][j], 2, 0)
                    x1+=2
                    if x1==392: square[i][j], square[i][j+1], numbers[i][j], numbers[i][j+1], matrice[i][j], matrice[i][j+1]=None, square[i][j], None, numbers[i][j], 0, matrice[i][j]
                    if x1==294: square[i][j], square[i][j+1], numbers[i][j], numbers[i][j+1], matrice[i][j], matrice[i][j+1]=None, square[i][j], None, numbers[i][j], 0, matrice[i][j]
                    if x1==196: square[i][j], square[i][j+1], numbers[i][j], numbers[i][j+1], matrice[i][j], matrice[i][j+1]=None, square[i][j], None, numbers[i][j], 0, matrice[i][j]
                elif j<3 and matrice[i][j]!=0 and matrice[i][j+1]!=0 and matrice[i][j]==matrice[i][j+1] and x1<c and mix[i]==False:
                    canvas.move(square[i][j], 2, 0)
                    canvas.move(numbers[i][j], 2, 0)
                    move=True
                    if x1+2==c:
                        mix[i]=True
                        if x1+2==392:
                            mix[i]="remix"
                        canvas.delete(square[i][j])
                        matrice[i][j+1]*=2
                        matrice[i][j]=0
                        canvas.itemconfigure(square[i][j+1],fill=color[matrice[i][j+1]], outline=color[matrice[i][j+1]])
                        square[i][j]=None
                        canvas.delete(numbers[i][j])
                        canvas.itemconfigure(numbers[i][j+1], text=str(matrice[i][j+1]))
                        numbers[i][j]=None
                        place_square=True
                elif j<2 and matrice[i][j]!=0 and matrice[i][j+1]!=0 and matrice[i][j]==matrice[i][j+1] and x1<c and mix[i]=="remix":
                    canvas.move(square[i][j], 2, 0)
                    canvas.move(numbers[i][j], 2, 0)
                    move=True
                    if x1+2==c:
                        canvas.delete(square[i][j])
                        matrice[i][j+1]*=2
                        matrice[i][j]=0
                        canvas.itemconfigure(square[i][j+1],fill=color[matrice[i][j+1]], outline=color[matrice[i][j+1]])
                        square[i][j]=None
                        canvas.delete(numbers[i][j])
                        canvas.itemconfigure(numbers[i][j+1], text=str(matrice[i][j+1]))
                        numbers[i][j]=None
                        place_square=True
    if move==True: canvas.after(1, movement_right)
    else: bind(), detect_lose()
                
def movement_left():
    global square, numbers, matrice, place_square, mix
    move=False
    for i in range(4):
        for j in range(4):
            c=8
            if  j!=0 and square[i][j]!=None and square[i][j-1]==None:
                place_square=True
            if square[i][j] != None:
                x0, y0, x1, y1 = canvas.coords(square[i][j])
                if j>0 and square[i][j-1]!=None:
                    a, b, c, d = canvas.coords(square[i][j-1])
                    c+=8
                if x0>c:
                    move=True
                    canvas.move(square[i][j], -2, 0)
                    canvas.move(numbers[i][j], -2, 0)
                    x0-=2
                    if x0==8: square[i][j], square[i][j-1], numbers[i][j], numbers[i][j-1], matrice[i][j], matrice[i][j-1]=None, square[i][j], None, numbers[i][j], 0, matrice[i][j]
                    if x0==106: square[i][j], square[i][j-1], numbers[i][j], numbers[i][j-1], matrice[i][j], matrice[i][j-1]=None, square[i][j], None, numbers[i][j], 0, matrice[i][j]
                    if x0==204: square[i][j], square[i][j-1], numbers[i][j], numbers[i][j-1], matrice[i][j], matrice[i][j-1]=None, square[i][j], None, numbers[i][j], 0, matrice[i][j]
                elif j>0 and matrice[i][j]!=0 and matrice[i][j-1]!=0 and matrice[i][j]==matrice[i][j-1] and x1>a and mix[i]==False:
                    canvas.move(square[i][j], -2, 0)
                    canvas.move(numbers[i][j], -2, 0)
                    move=True
                    if x0-2==a:
                        mix[i]=True
                        if x0-2==8:
                            mix[i]="remix"
                        canvas.delete(square[i][j])
                        matrice[i][j-1]*=2
                        matrice[i][j]=0
                        canvas.itemconfigure(square[i][j-1],fill=color[matrice[i][j-1]], outline=color[matrice[i][j-1]])
                        square[i][j]=None
                        canvas.delete(numbers[i][j])
                        canvas.itemconfigure(numbers[i][j-1], text=str(matrice[i][j-1]))
                        numbers[i][j]=None
                        place_square=True
                elif j>1 and matrice[i][j]!=0 and matrice[i][j-1]!=0 and matrice[i][j]==matrice[i][j-1] and x1>a and mix[i]=="remix":
                    canvas.move(square[i][j], -2, 0)
                    canvas.move(numbers[i][j], -2, 0)
                    move=True
                    if x0-2==a:
                        canvas.delete(square[i][j])
                        matrice[i][j-1]*=2
                        matrice[i][j]=0
                        canvas.itemconfigure(square[i][j-1],fill=color[matrice[i][j-1]], outline=color[matrice[i][j-1]])
                        square[i][j]=None
                        canvas.delete(numbers[i][j])
                        canvas.itemconfigure(numbers[i][j-1], text=str(matrice[i][j-1]))
                        numbers[i][j]=None
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
    global root, mix
    mix=[False, False, False, False]
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
canvas = tk.Canvas(root, width=398, height=435, bg="#ececec")

canvas.create_rectangle(8, 8, 98, 98, fill="#E0e0e0", outline="#E0e0e0")
canvas.create_rectangle(106, 8, 196, 98, fill="#E0e0e0", outline="#E0e0e0")
canvas.create_rectangle(204, 8, 294, 98, fill="#E0e0e0", outline="#E0e0e0")
canvas.create_rectangle(302, 8, 392, 98, fill="#E0e0e0", outline="#E0e0e0")
canvas.create_rectangle(8, 106, 98, 196, fill="#E0e0e0", outline="#E0e0e0")
canvas.create_rectangle(106, 106, 196, 196, fill="#E0e0e0", outline="#E0e0e0")
canvas.create_rectangle(204, 106, 294, 196, fill="#E0e0e0", outline="#E0e0e0")
canvas.create_rectangle(302, 106, 392, 196, fill="#E0e0e0", outline="#E0e0e0")
canvas.create_rectangle(8, 204, 98, 294, fill="#E0e0e0", outline="#E0e0e0")
canvas.create_rectangle(106, 204, 196, 294, fill="#E0e0e0", outline="#E0e0e0")
canvas.create_rectangle(204, 204, 294, 294, fill="#E0e0e0", outline="#E0e0e0")
canvas.create_rectangle(302, 204, 392, 294, fill="#E0e0e0", outline="#E0e0e0")
canvas.create_rectangle(8, 302, 98, 392, fill="#E0e0e0", outline="#E0e0e0")
canvas.create_rectangle(106, 302, 196, 392, fill="#E0e0e0", outline="#E0e0e0")
canvas.create_rectangle(204, 302, 294, 392, fill="#E0e0e0", outline="#E0e0e0")
canvas.create_rectangle(302, 302, 392, 392, fill="#E0e0e0", outline="#E0e0e0")

canvas.create_rectangle(8, 400, 98, 436, fill="#B5b5b5", outline="#B5b5b5")
canvas.create_rectangle(106, 400, 196, 436, fill="#B5b5b5", outline="#B5b5b5")
canvas.create_rectangle(204, 400, 294, 436, fill="#B5b5b5", outline="#B5b5b5")
rectangle_exit=canvas.create_rectangle(302, 400, 392, 436, fill="#E0e0e0", outline="#E0e0e0")
button_load=canvas.create_text((53, 418), text="Load", font=("helvetica", "18"), fill="black")
button_save=canvas.create_text((151, 418), text="Save", font=("helvetica", "18"), fill="black")
button_play=canvas.create_text((249, 418), text="Play", font=("helvetica", "18"), fill="black")
button_exit=canvas.create_text((347, 418), text="Exit", font=("helvetica", "18"), fill="#C6c5c5")
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