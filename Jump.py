import tkinter
import random
import time

WINDOW_WIDTH = 650
WINDOW_HEIGHT = 650

window = tkinter.Tk()
window.title("Jump")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg="black", width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
canvas.pack()
window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# 화면 위치
window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

# 위치
x = WINDOW_WIDTH/2 - 10
y = WINDOW_HEIGHT - 20
PLAYER_WIDTH = 20
PLAYER_HEIGHT = 20

# 상태
upKey = False
leftKey = False
rightKey = False

vy = 0
gravity = 0.8
jump_power = 13
on_ground = True

# 플랫폼
platforms = []

# 다음 단계
isClear = False

# 점수
INITIAL_SCORE = 0
score = INITIAL_SCORE

# 시간
game_over = False
start_time = None
end_time = None
INITIAL_TIME = 15.9
remaining_time = INITIAL_TIME

def draw():
    global x, y, platforms, isClear, score, start_time, remaining_time, end_time, game_over
    
    player_move()

    canvas.delete("all")

    canvas.create_oval(x, y, x+PLAYER_WIDTH, y+PLAYER_HEIGHT, fill="red")

    for i, (X, Y, W, H) in enumerate(platforms):
        if i == 0:
            canvas.create_rectangle(X, Y, X+W, Y+H, fill="light yellow")
            continue   
        canvas.create_rectangle(X, Y, X+W, Y+H, fill="lime green")

    end_time = time.time()

    if isClear:
        canvas.create_text(WINDOW_WIDTH/2, 60, font="Arial 20", text=f'{score + 10}', fill="white")
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2,
                           font="Arial 20", text=f"Stage Clear", fill="white")
    else:
        canvas.create_text(WINDOW_WIDTH/2, 60, font="Arial 20", text=f'score: {score}', fill="white")
        canvas.create_text(WINDOW_WIDTH/2, 25, font="Arial 20", text=f'time: {remaining_time-(end_time-start_time):.1f}', fill="white")
        
    if score >= 100:
        canvas.delete("all")
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2-15,
                           font="Arial 20", text=f"Finish, score: 100", fill="white")
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2+15,
                           font="Arial 15", text=f"Press the Spacebar to play again", fill="white")
    
    if remaining_time-(end_time-start_time) <= 0 and score < 100 and not isClear:
        game_over = True
        canvas.delete("all")
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2-15,
                           font="Arial 20", text=f"game over, score: {score}", fill="white")
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2+15,
                           font="Arial 15", text=f"Press the Spacebar to play again", fill="white")

    window.after(25, draw)

def reset_stage():
    global x, y, isClear, score, remaining_time
    random_platforms()
    x = WINDOW_WIDTH/2 - 10
    y = WINDOW_HEIGHT - 20
    isClear = False
    score += 10
    remaining_time -= 0.5

def restart():
    global score, remaining_time, game_over, INITIAL_TIME, INITIAL_SCORE
    reset_stage()
    score = INITIAL_SCORE
    remaining_time = INITIAL_TIME
    game_over = False

def random_platforms():
    global platforms, start_time
    platforms = []
    prev_x = random.randint(0, WINDOW_WIDTH-53)
    for i in range(1, 8):
        w = 50+i*3
        h = 15
        y = i*81
        platforms.append([prev_x, y, w, h])
        prev_x += random.randint(-150, 150)
        prev_x = max(0, min(prev_x, WINDOW_WIDTH-w))
    
    start_time = time.time()

def player_move():
    global x, y, leftKey, rightKey, upKey, vy, on_ground, gravity, isClear
    
    if leftKey:
        x -= 6
    if rightKey:
        x += 6
    
    if upKey and on_ground:
        vy = -jump_power
        on_ground = False

    vy += gravity
    y += vy

    on_ground = False
    for i, (X, Y, W, H) in enumerate(platforms):
        if (x+PLAYER_WIDTH > X and x < X+W and
            y+PLAYER_HEIGHT >= Y and y+PLAYER_HEIGHT <= Y+H and vy > 0):
            y = Y - PLAYER_HEIGHT
            vy = 0
            on_ground = True
            if i == 0 and y == Y-PLAYER_HEIGHT and not isClear:
                window.after(3000, reset_stage)
                isClear = True

    if y >= WINDOW_HEIGHT - PLAYER_HEIGHT:
        y = WINDOW_HEIGHT - PLAYER_HEIGHT
        vy = 0
        on_ground = True

    if x < 0:
        x = 0
    if x + PLAYER_WIDTH > WINDOW_WIDTH:
        x = WINDOW_WIDTH - PLAYER_WIDTH

def key_press(event):
    global leftKey, rightKey, upKey, score, game_over
    if event.keysym == "Left":
        leftKey = True
    elif event.keysym == "Right":
        rightKey = True

    if event.keysym == "Up":
        upKey = True

    if event.keysym == "space" and (score >= 100 or game_over):
        restart()

def key_release(event):
    global leftKey, rightKey, upKey
    if event.keysym == "Left":
        leftKey = False
    elif event.keysym == "Right":
        rightKey = False

    if event.keysym == "Up":
        upKey = False

random_platforms()
draw()

window.bind("<KeyPress>", key_press)
window.bind("<KeyRelease>", key_release)

window.mainloop()