# Olivia Snake Game

# Imports
from tkinter import *
from PIL import Image, ImageTk
import random
import os

# Constants
class Config:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    ASSETS_DIR = os.path.join(BASE_DIR, "assets")

    GAME_WIDTH = 700
    GAME_HEIGHT = 700
    GAME_SPEED = 80
    SPACE_SIZE = 50
    BODY_PARTS = 3

    SNAKE_IMAGE_PATH = os.path.join(ASSETS_DIR, "olivia.png")
    FOOD_IMAGE_PATH = os.path.join(ASSETS_DIR, "pear.png")

    BACKGROUND_COLOUR = "#E6E6E6"

# Classes
class Snake:
    def __init__(self) -> None:
        self.body = Config.BODY_PARTS
        self.cords = []
        self.squares = []

        for i in range(Config.BODY_PARTS):
            self.cords.append([0, 0])

        # Load and resize the snake image
        self.image = Image.open(Config.SNAKE_IMAGE_PATH)
        self.image = self.image.resize(
            (Config.SPACE_SIZE, Config.SPACE_SIZE),
            Image.LANCZOS
        )
        self.photo = ImageTk.PhotoImage(self.image)

        # Create image representations of the snake
        for x, y in self.cords:
            square = canvas.create_image(
                x, y, image=self.photo, anchor=NW, tag="Snake"
            )
            self.squares.append(square)

class Food:
    def __init__(self) -> None:
        max_x = (Config.GAME_WIDTH // Config.SPACE_SIZE) - 1
        max_y = (Config.GAME_HEIGHT // Config.SPACE_SIZE) - 1
        
        x = random.randint(0, max_x) * Config.SPACE_SIZE
        y = random.randint(0, max_y) * Config.SPACE_SIZE

        self.cords = [x, y]

        # Load and resize the food image
        self.image = Image.open(Config.FOOD_IMAGE_PATH)
        self.image = self.image.resize(
            (Config.SPACE_SIZE, Config.SPACE_SIZE),
            Image.LANCZOS
        )
        self.photo = ImageTk.PhotoImage(self.image)

        canvas.create_image(
            x, y, image=self.photo, anchor=NW, tag="food"
        )

# Functions
def next_turn(snake, food):
    global score, game_loop_id

    x, y = snake.cords[0]

    if direction == "up":
        y -= Config.SPACE_SIZE
    elif direction == "down":
        y += Config.SPACE_SIZE
    elif direction == "left":
        x -= Config.SPACE_SIZE
    elif direction == "right":
        x += Config.SPACE_SIZE

    snake.cords.insert(0, (x, y))
    square = canvas.create_image(
        x, y, image=snake.photo, anchor=NW, tag="Snake"
    )
    snake.squares.insert(0, square)

    if x == food.cords[0] and y == food.cords[1]:
        score += 1
        label.config(text=f"Score: {score}")
        canvas.delete("food")
        food = Food()
    else:
        del snake.cords[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
        return  # stop scheduling turns after death

    game_loop_id = window.after(
        Config.GAME_SPEED, next_turn, snake, food
    )

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
    x, y = snake.cords[0]

    if x < 0 or x >= Config.GAME_WIDTH:
        return True
    if y < 0 or y >= Config.GAME_HEIGHT:
        return True

    for body_part in snake.cords[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2,
        font=("Arial", 70),
        text="GAME OVER",
        fill="red",
        tag="gameover"
    )

def restart_game():
    global snake, food, score, direction, game_loop_id

    if game_loop_id is not None:
        window.after_cancel(game_loop_id)
        game_loop_id = None

    canvas.delete(ALL)

    score = 0
    direction = "down"
    label.config(text=f"Score: {score}")

    snake = Snake()
    food = Food()

    next_turn(snake, food)

# Window Settings
window = Tk()
window.title("Snake Game!")
window.resizable(False, False)

# Globals
score = 0
direction = "right"
game_loop_id = None

# Restart Button
restart_button = Button(
    window, text="Restart", command=restart_game, font=("Arial", 20)
)
restart_button.place(x=0, y=0)

# Score Label
label = Label(window, text=f"Score: {score}", font=("Arial", 40))
label.pack()

# Canvas
canvas = Canvas(
    window,
    bg=Config.BACKGROUND_COLOUR,
    height=Config.GAME_HEIGHT,
    width=Config.GAME_WIDTH
)
canvas.pack()

# Key Bindings
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# Start Game
snake = Snake()
food = Food()
next_turn(snake, food)

window.mainloop()
