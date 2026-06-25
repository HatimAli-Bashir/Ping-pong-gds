import turtle
import time

# إعدادات الشاشة
wind = turtle.Screen()
wind.title("Ping Pong - Shadow GDS Pro Speed")
wind.bgcolor("black")
wind.setup(width=800, height=650)
wind.tracer(0)

# المتغيرات الأساسية
game_state = "menu"
play_mode = "multi"
difficulty = "MEDIUM"
match_duration = 60
current_theme = 0
score1, score2 = 0, 0
start_time = 0
paused = False
pressed_keys = {}

themes = [
    {"name": "Classic", "bg": "black", "p1": "blue", "p2": "red", "ball": "white"},
    {"name": "Shadow", "bg": "#2c3e50", "p1": "#ecf0f1", "p2": "#95a5a6", "ball": "#e74c3c"}
]

# دالات رصد المفاتيح
def k_press(k): pressed_keys[k] = True
def k_release(k): pressed_keys[k] = False

wind.listen()
for key in ["w", "s", "W", "S", "Up", "Down", "space", "1", "2", "3", "4", "5", "6"]:
    wind.onkeypress(lambda k=key: k_press(k), key)
    wind.onkeyrelease(lambda k=key: k_release(k), key)

# كائنات اللعبة
madrab1 = turtle.Turtle()
madrab1.speed(0); madrab1.shape("square"); madrab1.shapesize(5, 1); madrab1.penup(); madrab1.goto(-350, 0); madrab1.hideturtle()

madrab2 = turtle.Turtle()
madrab2.speed(0); madrab2.shape("square"); madrab2.shapesize(5, 1); madrab2.penup(); madrab2.goto(350, 0); madrab2.hideturtle()

ball = turtle.Turtle()
ball.speed(0); ball.shape("square"); ball.penup(); ball.goto(0, 0); ball.hideturtle()

pen = turtle.Turtle()
pen.speed(0); pen.penup(); pen.hideturtle()

def draw_menu():
    global game_state
    game_state = "menu"
    wind.bgcolor("black")
    madrab1.hideturtle(); madrab2.hideturtle(); ball.hideturtle()
    pen.clear()
    pen.goto(0, 200); pen.color("cyan")
    pen.write("SHADOW GDS - PRO SPEED", align="center", font=("Courier", 24, "bold"))
    
    pen.color("white")
    options = [
        f"1. Difficulty: {difficulty}",
        f"2. Mode: {play_mode.upper()}",
        f"3. Time: {match_duration//60} Min",
        f"4. Theme: {themes[current_theme]['name']}",
        f"5. EXIT [5] | 6. Pause [6]"
    ]
    
    y = 100
    for opt in options:
        pen.goto(0, y); pen.write(opt, align="center", font=("Courier", 14, "bold"))
        y -= 35

    pen.goto(0, -110); pen.color("orange")
    pen.write("Left: [W/S] | Right: [Arrows]", align="center", font=("Courier", 13, "bold"))
    pen.goto(0, -140); pen.write("KEYBOARD MUST BE IN ENGLISH", align="center", font=("Courier", 13, "bold"))
    pen.goto(0, -210); pen.color("yellow")
    pen.write("Press [SPACE] to Start", align="center", font=("Courier", 18, "bold"))
    wind.update()

def start_game():
    global game_state, start_time, score1, score2, paused
    score1, score2 = 0, 0; paused = False; game_state = "playing"
    start_time = time.time()
    theme = themes[current_theme]
    wind.bgcolor(theme["bg"])
    madrab1.color(theme["p1"]); madrab2.color(theme["p2"]); ball.color(theme["ball"])
    madrab1.showturtle(); madrab2.showturtle(); ball.showturtle()
    ball.goto(0, 0)
    
    # --- تعديل سرعة الكرة الابتدائية ---
    # رفعت القيم لتكون أسرع قليلاً (Easy: 0.4, Medium: 0.6, Hard: 0.8)
    s = 0.6 if difficulty == "MEDIUM" else 0.8 if difficulty == "HARD" else 0.4
    ball.dx, ball.dy = s, s
    pen.clear()

last_press_time = 0
draw_menu()

while True:
    wind.update()
    
    if game_state == "menu":
        if pressed_keys.get("space"): start_game()
        if time.time() - last_press_time > 0.2:
            if pressed_keys.get("1"): 
                difficulty = "HARD" if difficulty == "MEDIUM" else "MEDIUM" if difficulty == "EASY" else "EASY"
                last_press_time = time.time(); draw_menu()
            if pressed_keys.get("2"):
                play_mode = "single" if play_mode == "multi" else "multi"
                last_press_time = time.time(); draw_menu()
            if pressed_keys.get("3"):
                match_duration = 60 if match_duration == 300 else 300 if match_duration == 120 else 120
                last_press_time = time.time(); draw_menu()
            if pressed_keys.get("4"):
                current_theme = (current_theme + 1) % len(themes)
                last_press_time = time.time(); draw_menu()
            if pressed_keys.get("5"): wind.bye(); break

    elif game_state == "playing":
        if time.time() - last_press_time > 0.3 and pressed_keys.get("6"):
            paused = not paused
            last_press_time = time.time()
            if paused:
                pen.goto(0, 0); pen.color("white"); pen.write("PAUSED", align="center", font=("Courier", 30, "bold"))
            else: pen.clear()

        if not paused:
            # سرعة المضارب (متناسقة مع سرعة الكرة الجديدة)
            paddle_speed = 3.0
            
            if (pressed_keys.get("w") or pressed_keys.get("W")) and madrab1.ycor() < 260:
                madrab1.sety(madrab1.ycor() + paddle_speed)
            if (pressed_keys.get("s") or pressed_keys.get("S")) and madrab1.ycor() > -260:
                madrab1.sety(madrab1.ycor() - paddle_speed)

            if play_mode == "multi":
                if pressed_keys.get("Up") and madrab2.ycor() < 260:
                    madrab2.sety(madrab2.ycor() + paddle_speed)
                if pressed_keys.get("Down") and madrab2.ycor() > -260:
                    madrab2.sety(madrab2.ycor() - paddle_speed)
            else:
                # ذكاء اصطناعي أسرع ليلحق بالكرة
                if madrab2.ycor() < ball.ycor() - 10: madrab2.sety(madrab2.ycor() + 0.6)
                elif madrab2.ycor() > ball.ycor() + 10: madrab2.sety(madrab2.ycor() - 0.6)

            ball.setx(ball.xcor() + ball.dx)
            ball.sety(ball.ycor() + ball.dy)

            if ball.ycor() > 290 or ball.ycor() < -290: ball.dy *= -1
            
            # تصادم المضارب مع زيادة سرعة الكرة عند كل ضربة بنسبة 3%
            if (340 < ball.xcor() < 350) and (madrab2.ycor() - 50 < ball.ycor() < madrab2.ycor() + 50):
                ball.setx(340); ball.dx *= -1.03
            if (-350 < ball.xcor() < -340) and (madrab1.ycor() - 50 < ball.ycor() < madrab1.ycor() + 50):
                ball.setx(-340); ball.dx *= -1.03

            if ball.xcor() > 390: score1 += 1; ball.goto(0, 0); ball.dx = -0.6
            if ball.xcor() < -390: score2 += 1; ball.goto(0, 0); ball.dx = 0.6
            
            rem = int(match_duration - (time.time() - start_time))
            pen.clear(); pen.goto(0, 260); pen.color("white")
            pen.write(f"P1: {score1}  P2: {score2}  Time: {rem}s", align="center", font=("Courier", 18, "bold"))
            if rem <= 0: draw_menu()
