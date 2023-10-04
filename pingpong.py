import tkinter as tk

# Parameters
WIDTH = 1000
HEIGHT = 600
BALL_RADIUS = 15
PADDLE_WIDTH = 200
PADDLE_HEIGHT = 20
SPEED_INCREMENT = 1

class Game:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
        self.canvas.pack()
        self.paddle_speed = 20

        # Key repetition variables
        self.left_key_pressed = False
        self.right_key_pressed = False

        # Create Start and Reset buttons
        self.start_button = tk.Button(root, text="Start", command=self.start_game)
        self.start_button.pack(side=tk.LEFT, padx=20)
        self.reset_button = tk.Button(root, text="Reset", command=self.reset_game, state=tk.DISABLED)
        self.reset_button.pack(side=tk.RIGHT, padx=20)

        self.game_active = False
        self.setup_game()

    def setup_game(self):
        self.ball = self.canvas.create_oval(WIDTH // 2 - BALL_RADIUS, HEIGHT // 4 - BALL_RADIUS,
                                            WIDTH // 2 + BALL_RADIUS, HEIGHT // 4 + BALL_RADIUS, fill='red')
        self.ball_speed = [2, 3]

        self.paddle = self.canvas.create_rectangle((WIDTH - PADDLE_WIDTH) // 2, HEIGHT - PADDLE_HEIGHT,
                                                   (WIDTH + PADDLE_WIDTH) // 2, HEIGHT, fill='blue')
        # Modified bindings
        self.canvas.bind_all("<KeyPress-Left>", self.start_move_left)
        self.canvas.bind_all("<KeyRelease-Left>", self.stop_move_left)
        self.canvas.bind_all("<KeyPress-Right>", self.start_move_right)
        self.canvas.bind_all("<KeyRelease-Right>", self.stop_move_right)

    def move_left(self, _event=None):
        if not self.game_active:
            return
        coords = self.canvas.coords(self.paddle)
        if coords[0] > 0:
            self.canvas.move(self.paddle, -self.paddle_speed, 0)

    def move_right(self, _event=None):
        if not self.game_active:
            return
        coords = self.canvas.coords(self.paddle)
        if coords[2] < WIDTH:
            self.canvas.move(self.paddle, self.paddle_speed, 0)

    # Continuous movement functions
    def start_move_left(self, _event=None):
        self.left_key_pressed = True
        self.continuous_move_left()

    def stop_move_left(self, _event=None):
        self.left_key_pressed = False

    def start_move_right(self, _event=None):
        self.right_key_pressed = True
        self.continuous_move_right()

    def stop_move_right(self, _event=None):
        self.right_key_pressed = False

    def continuous_move_left(self):
        if self.left_key_pressed and self.game_active:
            self.move_left()
            self.root.after(10, self.continuous_move_left)

    def continuous_move_right(self):
        if self.right_key_pressed and self.game_active:
            self.move_right()
            self.root.after(10, self.continuous_move_right)

    # Rest of the methods remain unchanged
    def animate(self):
        if not self.game_active:
            return

        self.move_ball()
        self.root.after(10, self.animate)

    def move_ball(self):
        coords = self.canvas.coords(self.ball)
        paddle_coords = self.canvas.coords(self.paddle)

        if coords[0] <= 0 or coords[2] >= WIDTH:
            self.ball_speed[0] = -self.ball_speed[0]

        if coords[1] <= 0:
            self.ball_speed[1] = -self.ball_speed[1]
        elif coords[2] > paddle_coords[0] and coords[0] < paddle_coords[2] and coords[3] >= paddle_coords[1]:
            self.ball_speed[1] = -self.ball_speed[1]
            self.ball_speed[1] -= SPEED_INCREMENT
        elif coords[3] > HEIGHT:
            self.end_game()
            return

        self.canvas.move(self.ball, self.ball_speed[0], self.ball_speed[1])

    def start_game(self):
        self.start_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.NORMAL)
        self.game_active = True
        self.animate()

    def end_game(self):
        self.game_active = False
        self.canvas.create_text(WIDTH / 2, HEIGHT / 2, text="GAME OVER", font=("Arial", 40), fill="black")

    def reset_game(self):
        self.canvas.delete("all")
        self.setup_game()
        self.start_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Ball Bounce Game")
    game = Game(root)
    root.mainloop()
