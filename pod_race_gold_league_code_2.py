import sys
import math


def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def calculate_angle(x1, y1, x2, y2):
    """Renommé de `angle` à `calculate_angle` pour éviter les conflits."""
    return math.atan2(y2 - y1, x2 - x1)


def calc_target_position(x, y, next_checkpoint_x, next_checkpoint_y, radius):
    angle_to_checkpoint = calculate_angle(x, y, next_checkpoint_x, next_checkpoint_y)

    target_x = next_checkpoint_x + radius * math.cos(angle_to_checkpoint)
    target_y = next_checkpoint_y + radius * math.sin(angle_to_checkpoint)

    return target_x, target_y


def adjust_target_position(target_x, target_y, speed, speed_direction):
    adjust_factor = 3000 * speed / max_speed
    dx = speed_direction[0]
    dy = speed_direction[1]
    adjusted_x = target_x - dx * adjust_factor
    adjusted_y = target_y - dy * adjust_factor
    return adjusted_x, adjusted_y


def calc_speed(speed_x, speed_y):
    return math.sqrt(speed_x ** 2 + speed_y ** 2)


def calc_speed_direction(vx, vy):
    norm = math.sqrt(vx ** 2 + vy ** 2)
    if norm == 0:
        return 0, 0
    return vx / norm, vy / norm


def go_next_checkpoint(map_memory, next_cp_id):
    if next_cp_id == checkpoint_count - 1:
        return map_memory[0]
    else:
        return map_memory[next_cp_id + 1]


def calculate_distance_threshold(speed):
    return speed * 4.75


# Initialisation
laps = int(input())
checkpoint_count = int(input())
map_memory = []
for i in range(checkpoint_count):
    checkpoint_x, checkpoint_y = [int(j) for j in input().split()]
    map_memory.append((checkpoint_x, checkpoint_y))

boost_available = [True, True]  # Pour chaque pod
checkpoint_radius = 600
max_speed = 961

# Boucle principale
while True:
    pod_data = []
    for i in range(2):
        # Lecture des données des pods
        x, y, vx, vy, angle, next_check_point_id = [int(j) for j in input().split()]
        pod_data.append((x, y, vx, vy, angle, next_check_point_id))

    opponent_positions = []
    for i in range(2):
        # Lecture des données des adversaires
        x_2, y_2, vx_2, vy_2, angle_2, next_checkpoint_id_2 = [int(j) for j in input().split()]
        opponent_positions.append((x_2, y_2, vx_2, vy_2, angle_2, next_checkpoint_id_2))

    for i in range(2):
        # Données du pod
        x, y, vx, vy, pod_angle, next_check_point_id = pod_data[i]
        
        # Initialisation des variables
        boost = "0"
        speed = calc_speed(vx, vy)
        speed_direction = calc_speed_direction(vx, vy)

        # Distance au prochain checkpoint
        next_checkpoint_x, next_checkpoint_y = map_memory[next_check_point_id]
        next_checkpoint_dist = distance(x, y, next_checkpoint_x, next_checkpoint_y)

        # Passer au checkpoint suivant si proche
        threshold = calculate_distance_threshold(speed)
        if next_checkpoint_dist < threshold:
            next_checkpoint_x, next_checkpoint_y = go_next_checkpoint(map_memory, next_check_point_id)
            print(f"NEXT CHECKPOINT UPDATE: {next_checkpoint_x}, {next_checkpoint_y}", file=sys.stderr)

        # Calcul de la position cible
        target_x, target_y = calc_target_position(x, y, next_checkpoint_x, next_checkpoint_y, checkpoint_radius)
        target_x, target_y = adjust_target_position(target_x, target_y, speed, speed_direction)
        target_distance = distance(x, y, target_x, target_y)
        
        # Normalize pod_angle to [-180, 180] range
        if pod_angle > 180:
            pod_angle -= 360

        # Calculate angle to checkpoint in radians
        angle_to_checkpoint = calculate_angle(x, y, next_checkpoint_x, next_checkpoint_y)

        # Convert to degrees and adjust relative to pod orientation
        next_checkpoint_angle = math.degrees(angle_to_checkpoint) - pod_angle

        # Gestion du boost ou de la puissance
        if abs(next_checkpoint_angle) < 2 and target_distance > 6000 and boost_available[i]:
            boost = "BOOST"
            boost_available[i] = False
        elif abs(next_checkpoint_angle) < 20:
            boost = "100"
        elif abs(next_checkpoint_angle) < 45:
            boost = "95"
        elif abs(next_checkpoint_angle) < 90:
            boost = "80"
        elif abs(next_checkpoint_angle) < 135:
            boost = "40"
        else:
            boost = "0"

        # Affichage des informations de debug
        print(f"--- POD {i + 1} INFO ---", file=sys.stderr)
        print(f"Position: ({x}, {y}), Speed: {speed} | Speed direction: {speed_direction}", file=sys.stderr)
        print(f"Next checkpoint: ({next_checkpoint_x}, {next_checkpoint_y})", file=sys.stderr)
        print(f"Next checkpoint distance: {next_checkpoint_dist}, Threshold: {threshold}", file=sys.stderr)
        print(f"Target position: ({int(target_x)}, {int(target_y)})", file=sys.stderr)
        print(f"Boost: {boost}", file=sys.stderr)
        print(f"Angles, pod to checkpoint: {pod_angle}, checkpoint to target: {next_checkpoint_angle}", file=sys.stderr)

        # Envoi des commandes
        print(f"{int(target_x)} {int(target_y)} {boost}")
