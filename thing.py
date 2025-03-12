import tkinter as tk
import math
import time

map_str = (
    "####################"
    "#...........#......#"
    "#..####...........##"
    "#......##..........#"
    "#......##..........#"
    "#..............##..#"
    "#.....#####........#"
    "#...........#......#"
    "#...........#......#"
    "####################"
)
map_width = 20
map_height = 10


player_x = 10.0
player_y = 5.0
player_angle = 0.0  

FOV = math.pi / 4
depth = 20.0  
screen_width = 80
screen_height = 24
move_speed = 4.0  
turn_speed = 2.0  

move_forward = False
move_backward = False
turn_left = False
turn_right = False

def is_wall(x, y):
    ix, iy = int(x), int(y)
    if ix < 0 or ix >= map_width or iy < 0 or iy >= map_height:
        return True
    return map_str[iy * map_width + ix] == '#'

def cast_ray(x, y, angle):
    step_size = 0.05
    distance = 0.0
    while distance < depth:
        distance += step_size
        test_x = x + math.cos(angle) * distance
        test_y = y + math.sin(angle) * distance
        if is_wall(test_x, test_y):
            return distance
    return depth

def render_frame():
    output = [[" " for _ in range(screen_width)] for _ in range(screen_height)]
    
    for x in range(screen_width):
        ray_angle = (player_angle - FOV / 2.0) + (x / screen_width) * FOV
        distance_to_wall = cast_ray(player_x, player_y, ray_angle)
        ceiling = int(screen_height / 2.0 - screen_height / distance_to_wall)
        floor = screen_height - ceiling
        
        for y in range(screen_height):
            if y < ceiling:
                output[y][x] = " "
            elif y <= floor:
                shade = "#" if distance_to_wall < depth / 4 else "%" if distance_to_wall < depth / 2 else "."
                output[y][x] = shade
            else:
                output[y][x] = " "
    
    return output

def frame_to_text(frame):
    return "\n".join("".join(row) for row in frame)

def update_position(dt):
    global player_x, player_y, player_angle
    if move_forward:
        new_x = player_x + math.cos(player_angle) * move_speed * dt
        new_y = player_y + math.sin(player_angle) * move_speed * dt
        if not is_wall(new_x, new_y):
            player_x = new_x
            player_y = new_y
    if move_backward:
        new_x = player_x - math.cos(player_angle) * move_speed * dt
        new_y = player_y - math.sin(player_angle) * move_speed * dt
        if not is_wall(new_x, new_y):
            player_x = new_x
            player_y = new_y
    if turn_left:
        player_angle -= turn_speed * dt
    if turn_right:
        player_angle += turn_speed * dt

def on_key_press(event):
    global move_forward, move_backward, turn_left, turn_right
    key = event.keysym.lower()
    if key == "w":
        move_forward = True
    elif key == "s":
        move_backward = True
    elif key == "a":
        turn_left = True
    elif key == "d":
        turn_right = True

def on_key_release(event):
    global move_forward, move_backward, turn_left, turn_right
    key = event.keysym.lower()
    if key == "w":
        move_forward = False
    elif key == "s":
        move_backward = False
    elif key == "a":
        turn_left = False
    elif key == "d":
        turn_right = False

last_time = time.time()

def update_frame():
    global last_time
    current_time = time.time()
    dt = current_time - last_time
    last_time = current_time

    update_position(dt)
    frame = render_frame()
    label.config(text=frame_to_text(frame))
    root.after(16, update_frame)  

root = tk.Tk()
root.config(bg="black")

label = tk.Label(
    root,
    text="",
    font=("Courier", 8),
    justify="left",
    bg="black",
    fg="white"
)
label.pack()

root.bind("<KeyPress>", on_key_press)
root.bind("<KeyRelease>", on_key_release)

update_frame()
root.mainloop()
