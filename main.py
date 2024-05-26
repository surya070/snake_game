from tkinter import *
import random
import sqlite3
from tkinter import messagebox

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 80
SPACE_SIZE = 25
BODY_PARTS = 3
SNAKE_COLOR = "blue"
FOOD_COLOR = "red"
BACKGROUND_COLOR = "black"

class Snake:   #creating the coordinates where snake moves
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, int((GAME_WIDTH / SPACE_SIZE)) - 1) * SPACE_SIZE
        y = random.randint(0, int((GAME_HEIGHT / SPACE_SIZE)) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    x, y = snake.coordinates[0]
    global direction,SNAKE_COLOR,FOOD_COLOR
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:  #FOOD is getting eaten
        global score, SPEED, highscore,highscore_name
        score += 1
        if score>highscore:
            highscore=score
            label2.config(text="High Score:{} (You!)".format(highscore))
        else:
            label2.config(text="High Score:{} ({})".format(highscore,highscore_name))
        label.config(text="Score:{}".format(score))
        
        canvas.delete("food")
        SPEED -= 2
        if SNAKE_COLOR=='blue':
            SNAKE_COLOR='yellow'
            FOOD_COLOR='green'
        else:
            SNAKE_COLOR='blue'
            FOOD_COLOR='red'
        food = Food()    

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False

def game_over():
    global name
    canvas.delete(ALL)
    canvas.create_text(GAME_WIDTH/2, GAME_HEIGHT/2, font=("calibri", 60), text="GAME OVER", fill='red')
    retry_button.pack()
    window.bind("<space>", lambda event: restart_game()) 
    if score>prev_high:
        label3.pack() 
        name_entry.pack() 
        submit_button.pack()

def restart_game():
    global snake, food, score, SPEED, direction, highscore,highscore_name
    canvas.delete(ALL)
    retry_button.pack_forget()
    label3.pack_forget() 
    name_entry.pack_forget() 
    submit_button.pack_forget()
    window.unbind("<space>")
    score = 0
    tup=get_highscore()
    highscore=tup[0][1]
    highscore_name=tup[0][0]
    prev_high=highscore
    label2.config(text="High Score:{} ({})".format(highscore,highscore_name))
    SPEED = 80
    direction = 'down'
    label.config(text="Score:0")
    snake = Snake()
    food = Food()
    next_turn(snake, food)

def submit_name():
    global highscore,prev_high
    name = name_entry.get()
    messagebox.showinfo("","Your name has been recorded!")
    con = sqlite3.connect('highscore.db')
    cur = con.cursor()
    cur.execute("UPDATE scores SET name = ?, highscore = ?", (name, highscore))
    con.commit()
    con.close()
    

def create_database():
    con = sqlite3.connect('highscore.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS scores(name TEXT, highscore INTEGER)")
    cur.execute("INSERT INTO scores (name, highscore) SELECT ?,? WHERE NOT EXISTS (SELECT 1 FROM scores);",('Surya',3))
    con.commit()
    con.close()

def get_highscore():
    con = sqlite3.connect('highscore.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM scores")
    scores = cur.fetchall()
    con.close()
    return scores


window = Tk()
window.title("Snake Game")
window.resizable(False, False)
score = 0
direction = "down"

label = Label(window, text="Score:{}".format(score), font=("calibri", 20))
label.pack()

create_database()
tup=get_highscore()
highscore=tup[0][1]
highscore_name=tup[0][0]
prev_high=highscore
label2=Label(window,text="High Score:{} ({})".format(highscore,highscore_name),font=("calibri",15))
label2.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

retry_button = Button(window, text="Retry", command=restart_game ,font=("calibri",15))

label3 = Label(window, text="You scored a new highscore enter your name to record it!!",font=("calibri",15)) 
name_entry = Entry(window, font=('Arial', 15))
submit_button = Button(window, text="Submit", command=submit_name)

window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))
window.bind("<a>", lambda event: change_direction("left"))
window.bind("<d>", lambda event: change_direction("right"))
window.bind("<w>", lambda event: change_direction("up"))
window.bind("<s>", lambda event: change_direction("down"))


snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()
