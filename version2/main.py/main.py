import tkinter as tk
from PIL import Image, ImageTk
from random import randint

MOVE_INCREMENT = 20
moves_per_sec = 15
GAME_SPEED = 1000 #moves per sec


class Snake(tk.Canvas):
    def __init__(self):
        super().__init__(width = 600,height = 620,background = 'black',highlightthickness = 0)
        self.snake_positions = [(100,100),(80,100),(60,100)]
        self.food_position = self.set_new_food_position()
        self.score = 0
        self.dir = "Right"
        self.bind_all("<Key>",self.on_key_press )


        self.load_assets()
        self.create_objects()
        self.after(GAME_SPEED ,self.perform_actions)


    def load_assets(self):
        try:
            self.snake_body_image = Image.open("snake.png")
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)

            self.food_body_image = Image.open("food.png")
            self.food_body = ImageTk.PhotoImage(self.food_body_image)
        except IOError as error:
            print(error)
            root.destroy()
    def create_objects(self):
        self.create_text(290,12,text = f"Score: {self.score}  Speed: {moves_per_sec}",tag = 'score', fill = "#fff",font = ("TkDefaultFont",14))
        for x_positions, y_positions in self.snake_positions:
            self.create_image(x_positions,y_positions,image = self.snake_body,tag = "snake")
        self.create_image(*self.food_position,image = self.food_body,tag = 'food')
        self.create_rectangle(7,27,593,613,outline = "#525d69")
    def move_snake(self):
        head_x_position,head_y_position = self.snake_positions[0]
        if self.dir == 'Left':
            new_head_position = (head_x_position - MOVE_INCREMENT, head_y_position)
        if self.dir == 'Right':
            new_head_position = (head_x_position + MOVE_INCREMENT, head_y_position)
        if self.dir == 'Up':
            new_head_position = (head_x_position, head_y_position - MOVE_INCREMENT)
        if self.dir == 'Down':
            new_head_position = (head_x_position, head_y_position + MOVE_INCREMENT)
   #increment of head with constant
        self.snake_positions = [new_head_position] + self.snake_positions[:-1]  #list slicing

        for segment , position in zip(self.find_withtag("snake"),self.snake_positions):#dynamic usage of snake moving
            self.coords(segment,position)
    def perform_actions(self):
        if self.collisions():
            self.end_game()
            return
        self.chech_food_collision()
        self.move_snake()
        self.after(75,self.perform_actions)
    def collisions(self):
        head_x_position, head_y_position = self.snake_positions[0]
        return (
            head_x_position in (0,600)
            or head_y_position in (20,620)
            or (head_x_position,head_y_position) in self.snake_positions[1:]
        )

    def on_key_press(self, e):
        new_dir = e.keysym
        all_dir = ('Up','Left','Right','Down')
        opposite_dir =  ({'Up','Down'},{'Right','Left'})#sets dont have order in python
        if (new_dir in all_dir and {new_dir,self.dir} not in opposite_dir):
            self.dir = new_dir

    def chech_food_collision(self):
        if self.snake_positions[0] == self.food_position:
            self.score += 1
            self.snake_positions.append(self.snake_positions[-1])
            if self.score%5 == 0:
                global moves_per_sec
                moves_per_sec += 1
            self.create_image(
                *self.snake_positions[-1],image =self.snake_body,tag = 'snake'
            )
            self.food_position = self.set_new_food_position()
            self.coords(self.find_withtag('food'),self.food_position)
            score = self.find_withtag('score')
            self.itemconfigure(score,text = f"Score: {self.score} Speed: {moves_per_sec }",tag = 'score')

    def set_new_food_position(self):
        while True:
            x_position = randint(1,29)*MOVE_INCREMENT
            y_position = randint(3,30) * MOVE_INCREMENT
            food_position = (x_position,y_position)
            if food_position not in self.snake_positions:
                return food_position
    def end_game(self):


        self.create_text(
            self.winfo_width()/2,
            self.winfo_height()/2,
            text = f'Game Over! You ,scored {self.score} at speed:{moves_per_sec}!',
            fill = '#fff',
            font = ("TkDefaultFont",24)

        )







root = tk.Tk()
root.title('SNAKE GAME')
root.resizable(False,False)

board = Snake()
board.pack()
root.mainloop()




