import sys
import math


def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def angle(x1, y1, x2, y2):
    return math.atan2(y2 - y1, x2 - x1)


def calc_target_position(x, y, next_checkpoint_x, next_checkpoint_y, radius):
    angle_to_checkpoint = angle(x, y, next_checkpoint_x, next_checkpoint_y)

    target_x = next_checkpoint_x + radius * math.cos(angle_to_checkpoint)
    target_y = next_checkpoint_y + radius * math.sin(angle_to_checkpoint)

    return target_x, target_y


def adjust_target_position(target_x, target_y, speed, speed_direction):
    adjust_factor = 2000 * speed / max_speed
    dx = speed_direction[0]
    dy = speed_direction[1]
    adjusted_x = target_x - dx * adjust_factor
    adjusted_y = target_y - dy * adjust_factor
    return adjusted_x, adjusted_y



def calc_speed(previous_x, previous_y, x, y):
    return distance(previous_x, previous_y, x, y)


def calc_speed_direction(previous_x, previous_y, x, y):
    dx = x - previous_x
    dy = y - previous_y
    
    magnitude = math.sqrt(dx ** 2 + dy ** 2)
    
    if magnitude == 0:
        return 0, 0
    
    return dx / magnitude, dy / magnitude


def is_new_checkpoint(next_checkpoint_x, next_checkpoint_y, map_memory):
    for checkpoint in map_memory:
        if distance(next_checkpoint_x, next_checkpoint_y, checkpoint[0], checkpoint[1]) < 100:
            return False
    return True


def find_next_checkpoint(map_memory, next_x, next_y):
    for i, checkpoint in enumerate(map_memory):
        dist = distance(next_x, next_y, checkpoint[0], checkpoint[1])
        if dist < 1000:
            if i + 1 < len(map_memory):
                return map_memory[i + 1]
            else:
                return map_memory[0]
    return (next_x, next_y)


def calc_first_checkpoint(x, y, opponent_x, opponent_y):
    return (opponent_x + x) // 2, (opponent_y + y) // 2


# game loop
map_memory = []
boost_available = True
first_action = True
first_turn = True
checkpoint_radius = 600
enemy_radius = 400
max_speed = 558

previous_x = 0
previous_y = 0
speed = 0
speed_direction = 0, 0

while True:
    x, y, next_checkpoint_x, next_checkpoint_y, next_checkpoint_dist, next_checkpoint_angle = [int(i) for i in input().split()]
    opponent_x, opponent_y = [int(i) for i in input().split()]
    if first_action:
        first_action = False
        map_memory.append(calc_first_checkpoint(x, y, opponent_x, opponent_y))
    else:
        speed = calc_speed(previous_x, previous_y, x, y)
        speed_direction = calc_speed_direction(previous_x, previous_y, x, y)
    if first_turn and next_checkpoint_x == map_memory[0][0] and next_checkpoint_y == map_memory[0][1]:
        first_turn = False
    previous_x = x
    previous_y = y
    if is_new_checkpoint(next_checkpoint_x, next_checkpoint_y, map_memory):
        map_memory.append((next_checkpoint_x, next_checkpoint_y))
        print(f"NEW CHECKPOINT: {next_checkpoint_x}, {next_checkpoint_y}", file=sys.stderr)
    if not first_turn and next_checkpoint_dist < 1750:
        next_checkpoint_x, next_checkpoint_y = find_next_checkpoint(map_memory, next_checkpoint_x, next_checkpoint_y)

        
        print(f"NEXT CHECKPOINT: {next_checkpoint_x}, {next_checkpoint_y}", file=sys.stderr)

    target_x, target_y = calc_target_position(x, y, next_checkpoint_x, next_checkpoint_y, checkpoint_radius)
    target_x, target_y = adjust_target_position(target_x, target_y, speed, speed_direction)
    target_distance = distance(x, y, target_x, target_y)

    if abs(next_checkpoint_angle) < 2 and target_distance > 6000 and boost_available:
        boost = "BOOST"
        boost_available = False
    elif abs(next_checkpoint_angle) < 45:
        boost = "100"
    elif abs(next_checkpoint_angle) < 90:
        boost = "100"
    elif abs(next_checkpoint_angle) < 135:
        boost = "40"
    else:
        boost = "0"

    # Print all details in a readable way
    print(f"Position: {x}, {y}", file=sys.stderr)
    print(f"Speed: {speed}, Speed direction: {speed_direction}", file=sys.stderr)
    print(f"next_checkpoint_x: {next_checkpoint_x}, next_checkpoint_y: {next_checkpoint_y}", file=sys.stderr)
    print(f"map_memory: {map_memory}", file=sys.stderr)
    print(f"next_checkpoint_distance: {next_checkpoint_dist}, target_distance: {target_distance}", file=sys.stderr)
    print(f"boost: {boost}", file=sys.stderr)
    print(f"Angle: {next_checkpoint_angle}", file=sys.stderr)

    print(f"{int(target_x)} {int(target_y)} {boost} {boost}")
